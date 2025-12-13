from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, Agent
import os
from dotenv import load_dotenv
import time
import httpx
import asyncio

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

@function_tool
async def get_quantity():
    print("[DEBUG] Tool Calling")
    async with httpx.AsyncClient() as client:
        data = await client.get("http://127.0.0.1:8000/productquantity")
        if data.status_code != 200:
            return data.json()
        print("[DEBUG] Tool Calling Done")
        return data.json()
    
quantity_agent = Agent(
    name="Quantity_Agent",
    instructions="""Call the get_quantity to show the products in structured format,
    dont reply to any other questions other than this.
""",
    tools=[get_quantity],
    model=model
)

async def main():
    while True:
        result = await Runner.run(quantity_agent, "Check the Quantity")
        print("Agent Reply ✔ :", result.final_output)
        time.sleep(50)

asyncio.run(main())