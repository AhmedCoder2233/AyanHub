from a2a.server.agent_execution import AgentExecutor
from agents import OpenAIChatCompletionsModel, AsyncOpenAI, Runner, Agent
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

agent1 = Agent(
    name="FAQAgent",
    instructions="""
    You are a FAQ Agent for a Ecommerce Store

    Tasks: 
    You will reply general queries of user
    if user ask about the opening timing then it is from Monday to Saturday between 10am to 5pm,
    if user ask about who is the owner then reply with Ahmed Memon is the owner of this store
    if user ask about Store name then it is AhmedEcom
    if user ask about address then the address is Kharadar, Karachi
""",
    model=model
)

class Start(AgentExecutor):
    async def execute(self, context, event_queue):
        userinput = context.get_user_input()
        runAgent = await Runner.run(agent1, userinput)
        await event_queue.enqueue_event(new_agent_text_message(runAgent.final_output))

    async def cancel(self, context, event_queue):
        await event_queue.enqueue_event(new_agent_text_message("Failed To Execute Agent"))


card = AgentCard(
    name="FAQ Agent",
    description="A Agent that reply to FAQS",
    url="http://localhost:8010",
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
        name="FAQ Agent",
        description="Reply to user basic queries",
        examples=["Hello what is your opening timing?", "What is your store name?", "who is the owner?"],
        id="faqagent",
        tags=["FAQ", "Queries"]
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
    uvicorn.run(server.build(), host="localhost", port=8010)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())