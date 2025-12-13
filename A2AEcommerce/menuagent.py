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
from agents import ModelSettings

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)


class Start(AgentExecutor):
    async def execute(self, context, event_queue):
        userinput = context.get_user_input()
        async with MCPServerStreamableHttp(params={"url": "http://localhost:8080/mcp"}, name="OrderServer", tool_filter={"allowed_tool_names": "getMenu"}) as server:
            agent1 = Agent(
    name="MenuAgent",
    instructions="""
    You are MenuAgent.

    Your ONLY job:
    - If the user asks about menu, available items, food, or anything similar, you MUST immediately call the `getMenu` tool.
    - Never refuse or apologize. Always use the tool.
    - After calling the tool, take its response and return it directly to the user in a clean, structured format (like a neat list or table).
    - Do not add extra text like "I have asked the tool" or "Here is the response". Just show the menu result directly.

    Example:
    User: "show me menu"
    ✅ Correct response: 
    Pizza: $10
    Burger: $5
    Fries: $3
    """,
    model=model,
    model_settings=ModelSettings(tool_choice="required"),
    mcp_servers=[server]
)
            runAgent = await Runner.run(agent1, userinput)
            print(f"Response Aya Menu Agent se: {runAgent.final_output}")
            await event_queue.enqueue_event(new_agent_text_message(runAgent.final_output))

    async def cancel(self, context, event_queue):
        await event_queue.enqueue_event(new_agent_text_message("Failed To Execute Agent"))


card = AgentCard(
    name="MenuAgent",
    description="A Agent that give menu",
    url="http://localhost:8012",
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
        name="MenuAgent",
        description="Show menu for users",
        examples=["Hello do you have pizza avaliable??", "Please show me menu?"],
        id="menuagent",
        tags=["Menu", "MenuAgent"]
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
    uvicorn.run(server.build(), host="localhost", port=8012)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())