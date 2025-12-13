from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunConfig, set_tracing_disabled, function_tool
import requests
import os
import smtplib
from email.message import EmailMessage
import time

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(model=model, model_provider=provider)
set_tracing_disabled(True)


@function_tool
def Sent_Alert(product_name: str):
    response = requests.post(f"http://127.0.0.1:8000/sent_alert_done/{product_name}")
    if response.status_code != 200:
        return "Failed to update sent_alert status"
    return "Successfully marked alert as sent"

@function_tool
def checkProduct():
    response = requests.get("http://127.0.0.1:8000/product/")
    if response.status_code != 200:
        return "Failed to get Products"
    return response.json()

@function_tool
def EmailSender(to: str, body: str, subject: str):
    message = EmailMessage()
    message["to"] = to
    message["from"] = "ahmedmemon3344@gmail.com"
    message["subject"] = subject
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("ahmedmemon3344@gmail.com", os.getenv("APP_PASSWORD"))
        server.send_message(message)
    return "Email sent successfully!"


quantityalertagent = Agent(
    name="quantityalertagent",
    instructions="""
Automatically monitor stock.

1. Use `checkProduct()` to get all products.

2. For each product:
   - Skip if `sent_alert == true`
   - If `quantity <= 2` AND `sent_alert == false`, then:
     a. Call `Sent_Alert(product_name)`
     b. Call `EmailSender()` with:
        - to: "ahmedmemon3344@gmail.com"
        - subject: "⚠️ Low Stock Alert"
        - body: "The product '{product_name}' has low stock. Please restock it soon."

Repeat this check for every product in the list.
Do not send duplicate alerts for the same product.
""",
    tools=[checkProduct, Sent_Alert, EmailSender]
)


import time
from datetime import datetime

while True:
    print("🔄 Checking Stock Availability...")

    system_prompt = f"Check inventory at {datetime.now().isoformat()}"

    response = Runner.run_sync(quantityalertagent, system_prompt, run_config=config)

    print("✅", response.final_output)
    time.sleep(50)  
