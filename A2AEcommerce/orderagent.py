from a2a.server.agent_execution import AgentExecutor
from agents import OpenAIChatCompletionsModel, AsyncOpenAI, Runner, Agent
from agents.mcp import MCPServerStreamableHttp
from dotenv import load_dotenv
import os
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, AgentCapabilities, AgentSkill, AgentProvider
from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.events import InMemoryQueueManager

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

memory = []

class Start(AgentExecutor):
    async def execute(self, context, event_queue):
        userinput = context.get_user_input()
        memory.append({"role": "user", "content": userinput})
        async with MCPServerStreamableHttp(params={"url": "http://localhost:8080/mcp", "timeout":30}, name="OrderServer", tool_filter={"allowed_tool_names": "placeOrder"}) as server:
            agent1 = Agent(
    name="OrderPlaceAgent",
    instructions="""
    You are an Order Placement Agent for an E-commerce Store.

    Your task is to place an order whenever the user requests it.

    To do this, you must call the `placeOrder` tool with the following argument:

    - `orderdata`: an object that MUST contain exactly these fields:
        • username (string) → the username of the user  
        • useremail (string) → the email address of the user  
        • fooditem (string) → the name of the food item ordered (e.g., "Pizza", "Burger")  

    Example call format:
    {
      "orderdata": {
        "username": "John Doe",
        "useremail": "john@example.com",
        "fooditem": "Pizza"
      }
    }

    Always collect these three details from the user before calling the tool.
    """,
    model=model,
    mcp_servers=[server]
)

            runAgent = await Runner.run(agent1, memory)
            memory.append({"role": "user", "content": runAgent.final_output})
            print(runAgent.final_output)
            await event_queue.enqueue_event(new_agent_text_message(runAgent.final_output))

    async def cancel(self, context, event_queue):
        await event_queue.enqueue_event(new_agent_text_message("Failed To Execute Agent"))


card = AgentCard(
    name="OrderPlaceAgent",
    description="A Agent that place orders",
    url="http://localhost:8011",
    capabilities=AgentCapabilities(
        push_notifications=False,
        state_transition_history=False,
        streaming=False
    ),
    default_input_modes=["text/plain", "application/json"],
    default_output_modes=["application/json",
                          "text/plain"], 
    preferred_transport="JSONRPC",
    version="1.0.0",
    skills=[AgentSkill(
        name="OrderPlaceAgent",
        description="Order for users",
        examples=["Hello i want to order pizza?", "Can i have burger please?", "I want to order fries?"],
        id="orderagent",
        tags=["Order", "OrderAgent"]
    )],
    provider=AgentProvider(
        url="https://ahmedportfolio.com",
        organization="AhmedEcom"
    )
)


def main():
    print("🚀 Starting Ahmad's Availability Bot Agent")

    request_handler = DefaultRequestHandler(
        agent_executor=Start(),
        task_store=InMemoryTaskStore(),
        queue_manager=InMemoryQueueManager()
    )

    server = A2AFastAPIApplication(
        agent_card=card,
        http_handler=request_handler
    )

    print("⚡ Ahmad's availability bot ready!")
    print("🔗 Agent Card: http://localhost:8003/.well-known/agent-card.json")
    print("📮 A2A Endpoint: http://localhost:8003")

    import uvicorn
    uvicorn.run(server.build(), host="localhost", port=8011)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())