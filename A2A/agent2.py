from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue, InMemoryQueueManager
from a2a.utils import new_agent_text_message
from a2a.types import AgentCapabilities, AgentCard, AgentSkill, AgentProvider
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, function_tool
from dotenv import load_dotenv
import os

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
def getMenu():
    return ["PizzaHutSpecialPizza", "Margreta Pizza", "Vegetable Pizza"]

agent = Agent(
    name="PizzaHutAgent",
    instructions="""
    You are a MenuAgent if anyone ask about to give menu or something about menu call the getMenu tool to show them menu items in structured format,
    if query is not about Menu just inform the user that you are just a menu agent
""",
    tools=[getMenu],
    model=model
)

card = AgentCard(
    name="PizzaHutAgent",
    description="you are menu telling agent",
    capabilities=AgentCapabilities(push_notifications=False, streaming=False, state_transition_history=False),
    url="http://localhost:8002",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    preferred_transport="JSONRPC",
    version="1.0.0",
    skills=[AgentSkill(
        name="GetPizzaHutMenu",
        description="Get menu of the MCDonalds",
        id="123",
        tags=["menu", "food", "pizzahut"]
    )],
        provider=AgentProvider(
        organization="Ahmed Official",
        url="https://ahmedportfolio.com"
    ),
)


class Executor(AgentExecutor):
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ):
        userinput = context.get_user_input()
        result = await Runner.run(agent, userinput)
        await event_queue.enqueue_event(new_agent_text_message(result.final_output))
    
    async def cancel(self, context, event_queue):
        await event_queue.enqueue_event(new_agent_text_message("An Error Occured"))


if __name__ == "__main__":
    run = DefaultRequestHandler(
        agent_executor=Executor(),
        queue_manager=InMemoryQueueManager(),
        task_store=InMemoryTaskStore()
    )

    start = A2AFastAPIApplication(agent_card=card, http_handler=run)

    import uvicorn
    uvicorn.run(start.build(), host="localhost", port=8002)