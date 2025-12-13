from agents import AsyncOpenAI, Agent, OpenAIChatCompletionsModel, RunContextWrapper, Runner,handoff, function_tool, set_tracing_disabled
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from gtts import gTTS
import io
import os
import stripe
import httpx
from contextlib import asynccontextmanager
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.store.postgres.base import PoolConfig
from email.message import EmailMessage
import smtplib
import chromadb
from google.genai import Client
from langchain.document_loaders import PyPDFLoader
from google.genai.types import EmbedContentConfig

load_dotenv()
app = FastAPI()
set_tracing_disabled(disabled=True)
stripe.api_key = os.getenv("STRIPE")

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

googleClient = Client(api_key=os.getenv("GEMINI_API_KEY"))
chromaClient = chromadb.Client()

pdf_path = "Policy.pdf"

loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

allPages = [page.page_content for page in pages]
pageIDs = [f"ID {page}" for page in range(len(pages))]

embedContent = googleClient.models.embed_content(
    model="gemini-embedding-exp-03-07",
    contents=allPages,
    config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
)

data = [embed.values for embed in embedContent.embeddings]

collection = chromaClient.create_collection("Policies")

try:
    collection.add(
        documents=allPages,
        embeddings=data,
        ids=pageIDs
    )
    print("[DEBUG] Data Added Succesfully in ChromaDB")

except Exception as e:
    print(f"Failed TO Add Data in ChromaDB: {e}")

@asynccontextmanager
async def get_store():
    async with AsyncPostgresStore.from_conn_string(
        os.getenv("NEONDBURL"),
        index={
            "dims": 768,
            "embed": GoogleGenerativeAIEmbeddings(google_api_key=os.getenv("GEMINI_API_KEY"), model="models/text-embedding-004")
        },
        pool_config=PoolConfig(min_size=5, max_size=20)
    ) as store:
        yield store

class userInfo(BaseModel):
    email:str
    phone:str
    address:str
    accountnumber:str

def dynamic_namespace(phone:str):
    return ("assistant", phone, "collection")


@function_tool
def getPolicies(query:str):
    embedQuery = googleClient.models.embed_content(
    model="gemini-embedding-exp-03-07",
    contents=[query],
    config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )

    queryEmbed = embedQuery.embeddings[0].values

    searching = collection.query(
        n_results=1,
        query_embeddings=queryEmbed,
        include=["documents"]
    )

    data = searching["documents"][0][0]

    return data

@function_tool
async def getProducts():
    async with httpx.AsyncClient() as client:
        request = await client.get("http://127.0.0.1:8081/products")
        if request.status_code != 200:
            return "Failed To Get Data!"
        return request.json()
    
@function_tool
async def placeOrder(ctx: RunContextWrapper[userInfo], product: list):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8081/orderplace",
                json={
                    "email": ctx.context.email,
                    "phone": ctx.context.phone,
                    "address": ctx.context.address,
                    "product": product
                }
            )

            if response.status_code != 200:
                return "❌ Failed to Place Order!"

            data = response.json()
            return {
            "message": f"✅ Your Order has been placed!\n📦 Order ID: `{data['orderid']}`\n💳 Please complete payment within 10 minutes or the order will be cancelled."
                }


    except Exception as e:
        print(f"Error in placeOrder: {e}")
        return {"message": "⚠️ Something went wrong while placing the order."}

@function_tool 
def stripePayment(ctx:RunContextWrapper[userInfo] ,product: list):
    try:
        line_items = []
        product_names = [] 
        for item in product:
            stripe_product = stripe.Product.create(name=item["product_name"])
            price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=int(item["product_price"]) * 100,
                currency="usd"
            )
            line_items.append({
                "price": price.id,
                "quantity": int(item["quantity"])
            })
            product_names.append(item["product_name"])  

        link = stripe.PaymentLink.create(
            line_items=line_items,
            metadata={"email": ctx.context.email}
        )
        product_string = ", ".join(product_names)
        return f"✅ Order placed for item {product_string}. 📎\nPayment Link: {link.url} — Please complete payment within 10 minutes or your order will be cancelled."

    except Exception as e:
        print(f"Error In Stripe Payment: {e}")

@function_tool
async def fetchPastOrders(ctx:RunContextWrapper[userInfo]):
    async with get_store() as store:
        try:
            result = await store.asearch(("assistant", ctx.context.phone, "collection") ,query="Order", limit=3)
            print("Raw result:", result) 
            return result[0].value["content"]
        except Exception as e:
            print(f"Error in Fetching {e}")

@function_tool
async def getOrderStatus(orderid:int):
    async with httpx.AsyncClient() as client:
        try:
            data = await client.get(f"http://127.0.0.1:8081/orderstatus/{orderid}",)
            if data.status_code != 200:
                return "Failed to check order Status"
            userdata = data.json()
            return userdata['message']
        except Exception as e:
            print(f"Error in Status: {e}")

@function_tool
async def returnDataTool(ctx:RunContextWrapper[userInfo] ,orderid: int, reason: str):
    print("[DEBUG] Return Tool Call")
    async with httpx.AsyncClient() as client:
        try:
            data = await client.get(f"http://127.0.0.1:8081/orderstatus/{orderid}")
            if data.status_code != 200:
                return "Failed to check order status."

            userdata = data.json()
            print("[DEBUG] Order Status Data:", userdata)

            if userdata["status"] != "success":
                return "Order not found. Please check your order ID."

            if userdata["orderstatus"] != "Delivered":
                return "Your order is not delivered yet, so it cannot be returned at this time."

            orderedData = await client.get(f"http://127.0.0.1:8081/orderstatusdata/{orderid}")
            if orderedData.status_code != 200:
                return "Failed to fetch ordered product details."

            product_info = orderedData.json()
            print("[DEBUG] Ordered Product Data:", product_info)

            message = EmailMessage()
            message["to"] = "ahmedpubgking3388@gmail.com"
            message["from"] = "ahmedmemon3344@gmail.com"
            message["subject"] = "Refund Complaint"
            message.set_content(
                f"Refund request received.\n\n"
                f"Order ID: {orderid}\n"
                f"Product: {product_info}\n"
                f"Account Number: {ctx.context.accountnumber}\n"
                f"Reason: {reason}"
            )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login("ahmedmemon3344@gmail.com", os.getenv("APP_PASS"))
                server.send_message(message)

            return "Your refund request has been submitted successfully. You will receive a confirmation email shortly."

        except Exception as e:
            print(f"Error in returnDataTool: {e}")
            return "An error occurred while processing your refund request."

class productDetails(BaseModel):
    product_name:str
    product_description:str
    product_price:str
    product_category:str
    product_quantity:str

def testingFunc(ctx, result):
    print(f"Handoff Run with: {result.product_name}")

productfetchAgent = Agent(
    name="productfetchAgent",
instructions = """
You are a smart e-commerce assistant.

If the user asks to see products (e.g., "show me products", "list products", "what do you sell"), call the `getProducts` tool and display **all products**.

If the user asks about a **specific product** (e.g., "Do you have iPhone?"), call the `getProducts` tool and return **only matching products**.

✅ For each product, show:
Product Name: ...
Category: ...
Price: ...
Description: ...

❌ Do not use markdown, bullets, asterisks, or tool names like `tool getProducts()`. Just reply with clean plain text.
""",
    model=model,
    tools=[getProducts]
)

orderPlaceAgent = Agent(
    name="orderPlaceAgent",
    instructions = """
You are a smart and responsible order placement assistant.

🎯 If the user wants to place an order (e.g., "I want to buy", "Order iPhone"):
1. Call the `placeOrder` tool with a list of products. Each product must include:
   - product_name
   - product_description
   - product_price
   - quantity

2. After successfully placing the order, immediately call the `stripePayment` tool with the **same product list**.

3. After receiving the Stripe payment link, respond in **this exact format**:

✅ Order placed for item [Product Name(s)]  
🔗 Payment Link: [Stripe Link]  
⚠️ Please complete payment within 10 minutes or your order will be canceled.

💡 **Important rules**:
- The payment link must always start with `https://buy.stripe.com/`
- Make sure `[Product Name(s)]` is a comma-separated string of product names from the list.

⚠️ If the user asks to see products, browse items, or anything unrelated to order placement, do NOT respond yourself
 and call the MainAgent tool with that query.
""",
    model=model,
    tools=[placeOrder, stripePayment],
)

orderStatusChecker = Agent(
    name="orderStatusChecker",
    instructions="""
If the user asks to check their order status:
1. If you do not already know the order ID, ask: "Please provide your order ID."
2. When the user responds with an order ID, call getOrderStatus(orderid) using that value exactly as given.
3. Do not attempt to guess or create an order ID.

If user talks about anything else, call the MainAgent tool.
""",
    model=model,
    tools=[getOrderStatus],
)

returnAgent = Agent(
    name="returnAgent",
instructions = """
You are the refund/return processing assistant for the e-commerce system.

🎯 Workflow:
1. Ask for the **order ID**.
2. Once received, ask for the **reason** for the return/refund.
3. After collecting both (orderid, reason), IMMEDIATELY call:
   `returnDataTool(orderid, reason)`

⚠️ Rules:
- Ask for details **one by one**: Order ID → Reason.
- Do NOT ask both in a single message.
- Do NOT add apologies, explanations, addresses, or extra conversation.
- Do NOT provide instructions for shipping or returns yourself.
- Do NOT hand off to any other agent/tool.
- If the order is not yet delivered, respond with:
  "Your order has not been delivered yet, so it cannot be returned."
- After collecting both details, ALWAYS call the tool without extra words.

❌ Never say "transferring" or mention agent/tool names.
""",
    model=model,
    tools=[returnDataTool]
)

policyAgent = Agent(
    name="PolicyAgent",
    instructions="""
You are the dedicated store policy assistant.

🎯 If the user asks anything related to store policies, terms, privacy, shipping, returns, or any rules:
1. Pass their query to the `getPolicies(query)` tool.
2. Return the result directly to the user without extra explanation in well formatting.

⚠️ If the query is unrelated to store policies, call the MainAgent tool.
""",
    model=model,
    tools=[getPolicies],
)


productshowTool = productfetchAgent.as_tool(tool_name="productshowTool", tool_description="a tool to fetch products and show it")

MainAgent = Agent(
    name="MainAgent",
instructions = """
You are the main decision-making agent for an e-commerce assistant.

📦 **When the conversation starts:**
- Use the `fetchPastOrders` tool to find the user's past orders when user say to suggest order or something like this.
- If there are any matches, greet the user and suggest they might want to reorder those items. Example:
  "Welcome back! Last time you ordered [Product Names]. Would you like to reorder any of them?"

🎯 If the user wants to *see products*, *list items*, or *search for a specific product*, call the `productshowTool` tool.

🎯 If the user wants to see the order status call the `orderStatusChecker` tool

🎯 If the user wants to return an item or request a refund, call the `returnAgent` tool to handle it.

🎯 If the user asks about store policies, terms, shipping, or refunds, call the `policyAgent` tool.

🧾 If the user wants to *place an order* (e.g., "I want to buy", "Order iPhone", "Purchase hoodie"), follow these steps:

1️⃣ First, use the `productshowTool` to fetch the full details of the requested product (including name, description, price, and category).  
   ❗️Never place an order without fetching product details first.

2️⃣ If the product is found, ask the user how many pieces they want (to get `product_quantity`).

3️⃣ Once you have all the required product details and quantity, call the `orderPlaceAgent` tool with the product data in the following format:

{
  "product_name": product_name,
  "product_description": product_description,
  "product_price": product_price,
  "product_category": product_category,
  "product_quantity": product_quantity
}

✅ Be clear, helpful, and conversational in your responses.

⚠️ When handing off to another agent, do not say things like "I am transferring you to an agent" or "Let me connect you". 
Instead, directly let the other agent start the conversation naturally.

❌ Never show or explain internal logic or tool names to the user.
""",
    model=model,
    tools=[productshowTool, fetchPastOrders], 
    handoffs=[handoff(orderPlaceAgent, input_type=productDetails, on_handoff=testingFunc), handoff(orderStatusChecker), handoff(returnAgent), handoff(policyAgent)]
)

orderPlaceAgent.handoffs.append(handoff(MainAgent))
orderStatusChecker.handoffs.append(handoff(MainAgent))
policyAgent.handoffs.append(handoff(MainAgent))

memory = []

def text_to_speech(text:str):
    voice = gTTS(text=text, lang="en")
    convertToByte = io.BytesIO()
    voice.write_to_fp(convertToByte)
    convertToByte.seek(0)
    return convertToByte.read()

import json  

@app.websocket("/ws")
async def liveVoicing(websocket: WebSocket):
    await websocket.accept()
    user_info = None
    try:
        while True:
            reciving_raw = await websocket.receive_text()
            reciving = json.loads(reciving_raw)

            if reciving.get("type") == "init":
                user_info = userInfo(
                email=reciving["email"],
                phone=reciving["phone"],
                address=reciving["address"],
                accountnumber=reciving["accountnumber"]
            )
                print("✅ User info received:", reciving)
                continue

            elif reciving.get("type") == "message":
                user_text = reciving["text"]
                print(f"User Text: {user_text}")
                memory.append({"role": "user", "content": user_text})

                result = await Runner.run(MainAgent, memory, context=user_info)

                memory.append({"role": "assistant", "content": result.final_output})

            async with get_store() as store:

                if "✅ Order placed for item" in result.final_output and "Payment Link:" in result.final_output:
                    try:
                        from datetime import datetime, timezone

                        try:
                            item_line = result.final_output.split("✅ Order placed for item ")[1].split(".")[0]
                        except:
                            item_line = "unknown product"

                        now = datetime.now(timezone.utc).isoformat()

                        memory_msg = (
                            f"🧾 Order placed for {item_line}\n"
                            f"📧 Email: {user_info.email}\n"
                            f"🕒 Time: {now}"
                        )

                        await store.aput(namespace=dynamic_namespace(user_info.phone), key=now, value={"content": memory_msg})
                        print("[🧠 Memory Saved]")
                    except Exception as err:
                        print(f"[❌ Memory Save Error]: {err}")


                memory.append({"role": "assistant", "content": result.final_output})

                byting = text_to_speech(text=result.final_output)
                await websocket.send_text(result.final_output)
                await websocket.send_bytes(byting)
    except Exception as e:
        print(f"Websocket Error: {e}")