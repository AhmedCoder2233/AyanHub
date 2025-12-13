from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Runner, Agent, function_tool
import os
from dotenv import load_dotenv
import requests
import chainlit as cl
from schema import OrderCreated
from contextlib import asynccontextmanager
from langmem_adapter import LangMemOpenAIAgentToolAdapter
from langmem import create_manage_memory_tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.store.postgres.base import PoolConfig
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

DB_URL = 'postgresql://neondb_owner:npg_Biwen29oLjXl@ep-damp-pond-adu35pp2-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

@asynccontextmanager
async def get_store():
    async with AsyncPostgresStore.from_conn_string(
        DB_URL,
        index={
            "dims":768,
            "embed": GoogleGenerativeAIEmbeddings(google_api_key=os.getenv("GEMINI_API_KEY"), model="models/text-embedding-004")
        },
        pool_config=PoolConfig(
            max_size=50,
            min_size=5
        )
    ) as store:
        yield store

namespace = ("assistant", "collection")

addmemory = LangMemOpenAIAgentToolAdapter(
    lambda store, namespace = None: create_manage_memory_tool(store=store, namespace=namespace),
    namespace_template=namespace,
    store_provider=get_store
)

manage_tool = addmemory.as_tool()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

@function_tool
def show_Products():
    print("[DEBUG] Tool Calling")
    data = requests.get("http://127.0.0.1:8000/totalproducts")
    if data.status_code != 200:
        return "Failed To Get Data"
    print("[DEBUG] Tool Calling Done")
    return data.json()

@function_tool
def createUserOrder(username:str, useremail:str, phonenumber:str, address:str, product_details):
    total_data = {"username":username, "useremail": useremail, "phonenumber": phonenumber, "address": address, "product_details": product_details}
    data = requests.post("http://127.0.0.1:8000/ordercreate", json=total_data)
    if data.status_code != 200:
        return "Failed to Post data!"
    return "Order Placed Succesufully"

orderPlaceAgent = Agent(
    name="OrderPlaceAgent",
    instructions="""
You are a smart shopping assistant.

🧠 Whenever the user **mentions anything they are looking for** — like:
- "I want a laptop"
- "Do you have phones?"
- "Show me headphones"
- "I need a gaming keyboard"
- "Looking for smartwatch"

→ Use the `manage_tool` to save **exactly what they said** in memory. This is used to remember user preferences.

🛠️ Tools You Can Use:
1. manage_tool — Save what the user is looking for (e.g., “I want a laptop”).
2. show_Products — Show all available products.
3. createUserOrder — Use this to place the user's order.

🛒 Workflow:
- First, save the user’s interest using `manage_tool`.
- Then call `show_Products()` to find matching items.
- If product is found, display clean list.
- If not found, clearly say: "Sorry, no products found for your request." and suggest other items.

📦 To place an order with `createUserOrder`, collect the following:
- username: str (Ask user)
- useremail: EmailStr (Ask user)
- phonenumber: str (Ask user)
- address: str (Ask user)
- product_details: list (Use the product JSON the user is ordering name, description, price)

❗ Be Action-Oriented:
- Never say “Noted” or “Okay”.
- Always take real action: save to memory, show products, or place order.
""",
    model=model,
    tools=[show_Products, manage_tool, createUserOrder]
)


@cl.on_chat_start
async def ChatStart():
    await cl.Message(content="Welcome to the Inventory Manager By Ahmed 👀").send()
    cl.user_session.set("history", [])

@cl.on_message
async def Messaging(message:cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    result = await Runner.run(orderPlaceAgent, history)
    print(result.new_items)
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()
