
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunConfig, set_tracing_disabled, function_tool
import chainlit as cl
import requests
import uuid
import os
import webbrowser
import stripe

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

stripe.api_key = os.getenv("STRIPE_API")

config = RunConfig(model=model, model_provider=provider)
set_tracing_disabled(True)


@function_tool
def showProducts():
    response = requests.get("http://127.0.0.1:8000/product/")
    if response.status_code != 200:
        return "Failed To Fetch Data!"
    return response.json()


@function_tool
def getProductQuantity(product_name: str):
    response = requests.get("http://127.0.0.1:8000/product/")
    if response.status_code != 200:
        return -1
    products = response.json()
    for product in products:
        if product["name"].lower() == product_name.lower():
            return product["quantity"]
    return -1


@function_tool
def create_payment_stripe(amount_usd: float, product_name: str, customer_email: str, product_quantity: int):
    try:
        if not customer_email or amount_usd <= 0:
            return "❌ Valid email and amount required."

        price_cents = int(amount_usd * 100)

        product = stripe.Product.create(name=product_name)
        recurring_price = stripe.Price.create(
            product=product.id,
            unit_amount=price_cents,
            currency="usd",
            recurring={"interval": "month"}
        )
        customer = stripe.Customer.create(email=customer_email)

        sub = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": recurring_price.id, "quantity": product_quantity}],
            collection_method="send_invoice",
            days_until_due=7,
            expand=["latest_invoice"]
        )
        stripe.Subscription.delete(sub.id)

        invoice_id = sub.latest_invoice["id"]
        invoice = stripe.Invoice.finalize_invoice(invoice_id)

        pdf_url = invoice.invoice_pdf
        pdf_path = f"./invoice_{invoice_id}.pdf"
        with open(pdf_path, "wb") as f:
            f.write(requests.get(pdf_url).content)

        one_time_price = stripe.Price.create(
            product=product.id,
            unit_amount=price_cents,
            currency="usd"
        )
        link = stripe.PaymentLink.create(
            line_items=[{"price": one_time_price.id, "quantity": product_quantity}],
        )

        webbrowser.open(link.url)
        return f"✅ Payment: {link.url}\n📄 Invoice: {pdf_path}"

    except Exception as e:
        return "❌ Stripe Payment Failed: " + str(e)


@function_tool
def saveUserInfo(
    name: str,
    email: str,
    phone: str,
    address: str,
    payment_method: str,
    product_name: str,
    product_description: str,
    product_price: int,
    product_quantity: int
):
    orderId = str(uuid.uuid4())
    data = {
        "order_id": orderId,
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "payment_method": payment_method,
        "status": "Pending",
        "product_name": product_name,
        "product_description": product_description,
        "product_price": product_price,
        "product_quantity": product_quantity
    }
    response = requests.post("http://127.0.0.1:8000/userinfo/", json=data)
    if response.status_code != 200:
        return "Failed to post Data in Userinfo"

    return f"✅ Order placed successfully!\n📦 Your Order ID: {orderId}"


@function_tool
def getUserInfo():
    response = requests.get("http://127.0.0.1:8000/userinfo/")
    if response.status_code != 200:
        return "Failed to get userInfo"
    return response.json()


@function_tool
def quantityDecrease(product_name: str, times: int):
    for _ in range(times):
        response = requests.post(f"http://127.0.0.1:8000/quantity-decrease/{product_name}")
        if response.status_code != 200:
            return f"❌ Failed to decrease quantity of {product_name}"
    return "✅ Quantity Decreased Successfully"


user_info_agent = Agent(
    name="user_info_agent",
    instructions="""
You are strictly responsible for handling purchases and order tracking.

🔹 PRODUCT INQUIRY
- If user asks like “do you have X”, always call showProducts().
- Match the product name and show full product details: name, description, price, and quantity.

🔹 ORDER FLOW
1. Ask the user which product they want to buy and how many.
2. Call getProductQuantity(product_name) to check stock.
   - If stock is 0 or less than requested, respond: "Sorry, this product is out of stock or doesn't have enough quantity." and stop.

3. Ask for these details:
   - Full Name
   - Email
   - Phone Number
   - Complete Address
   - Payment Method (COD or Stripe)

4. Validate address. If it’s too short or incomplete, say: "Please enter a complete and valid address."

5. Must call saveUserInfo(...) with all collected data.
6. Then immediately call quantityDecrease(product_name, quantity).
7. If payment method is Stripe:
   - Call create_payment_stripe(product_price, product_name, email, product_quantity).
   - Return the Stripe payment link clearly with the order ID and invoice note.

8. Always respond with: 
   - ✅ Order placed confirmation
   - 📦 Order ID
   - 💳 Payment link if Stripe

🔹 ORDER STATUS
9. If user asks for order status or pastes an order ID:
   - Call getUserInfo() and showProducts()
   - Match the order ID and clearly show:
     - Product Name
     - Quantity
     - Status (Pending/Delivered)
     - Price
     - Payment Method

⚠️ Always call tools when needed — no assumptions or skipping allowed.
""",
    tools=[getProductQuantity, saveUserInfo, quantityDecrease, getUserInfo, create_payment_stripe, showProducts]
)




product_show_agent = Agent(
    name="product_show_agent",
    instructions="""
You help users explore products.

1. If user says things like "show all products", "what do you sell", or "list available items", use `showProducts`.
2. If user asks about specific items, use `showProducts` and return only those matching by name.
3. If user wants to buy something, extract details and silently handoff to `user_info_agent`.
""",
    tools=[showProducts],
    handoffs=[user_info_agent]
)


triage_agent = Agent(
    name="triage_agent",
    instructions="""
Route the user's query:

- If the user is asking to browse or view products → route to `product_show_agent`
- If the user wants to purchase or check delivery status → route to `user_info_agent`
""",
    handoffs=[product_show_agent, user_info_agent]
)


@cl.on_chat_start
async def chatStart():
    await cl.Message(content="👋 Welcome to AI-Powered Order & Inventory Automation Tool by Ahmed Memon!").send()
    cl.user_session.set("history", [])


@cl.on_message
async def OnMessage(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    response = await Runner.run(triage_agent, history, run_config=config)
    history.append({"role": "assistant", "content": response.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=response.final_output).send()
