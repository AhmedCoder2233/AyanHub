from a2a.server.agent_execution import AgentExecutor
from agents import OpenAIChatCompletionsModel, AsyncOpenAI, Runner, Agent, function_tool, RunContextWrapper
from dotenv import load_dotenv
import os
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, AgentCapabilities, AgentSkill, AgentProvider
from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
import httpx
from a2a.client import A2ACardResolver, ClientFactory, ClientConfig, Client
from a2a.types import Message, Role, TextPart, Part
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

from dataclasses import dataclass, field

@dataclass
class AgentInfo:
    name: str
    url: str
    port: int
    description: str = ""
    agent_card: AgentCard | None = None

@dataclass
class CoordinatorContext:
    agents_by_port: dict[int, AgentInfo] = field(default_factory=dict)

    def add_agent(self, port: int, agent_info: AgentInfo):
        """Add or update an agent in the registry by port."""
        self.agents_by_port[port] = agent_info
    
    def get_agent_by_port(self, port: int) -> AgentInfo | None:
        """Get agent by port number."""
        return self.agents_by_port.get(port)

@function_tool
async def discoverAgent(context: RunContextWrapper):
    allowed_ports = [8010, 8011, 8012]
    discovered = {}
    async with httpx.AsyncClient() as client:
        for port in allowed_ports:
            try:
                url = f"http://localhost:{port}"
                card = A2ACardResolver(base_url=url, httpx_client=client)
                getcard = await card.get_agent_card()

                agent_info = AgentInfo(
                    name=getcard.name,
                    url=url,
                    port=port,
                    description=getcard.description,
                    agent_card=getcard
                )
                context.context.add_agent(port=port, agent_info=agent_info)

                discovered[getcard.name] = {
                    "name": getcard.name,
                    "description": getcard.description,
                    "url": url,
                }
            except Exception as e:
                print(f"❌ Agent on {port} not reachable: {e}")
                continue

    return discovered   

        
from pydantic import BaseModel

class AgentFormat(BaseModel):
    port:int
    message:str

@function_tool
async def callAgent(context: RunContextWrapper, agent_message: list[AgentFormat]):
    responses = {}

    for calls in agent_message:
        ports = calls.port
        message = calls.message
        agent_info = context.context.get_agent_by_port(ports)
        print(f"📡 Sending message '{message}' to port {ports}")

        messagetoSend = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text=message))],
            message_id="123"
        )

        async with httpx.AsyncClient(timeout=30) as http_client:
            client = ClientFactory(
                config=ClientConfig(httpx_client=http_client, streaming=False)
            ).create(card=agent_info.agent_card)

            try:
                response = client.send_message(messagetoSend)
                async for data in response:
                    print(f"✅ Response from {ports}:", data)

                    responses[ports] = {
                    "status": "success",
                    "response": data,
                    "agent": agent_info.name if agent_info else f"Unknown Agent on port {ports}"
                    }
            except Exception as e:
                print(f"❌ Failed to call agent {ports}: {e}")
                responses[ports] = {"status": "error", "error": str(e)}

    print("📦 Final responses:", responses)
    return responses

agent1 = Agent(
    name="Orchestrator Agent",
    instructions="""
    You are an Orchestrator Agent.

    Behavior Rules:
    - You must never generate answers yourself.
    - You must strictly follow the tool-calling workflow below without skipping.

    Workflow:
    1. For every user query, always call the `discoverAgent` tool first.
    2. If `discoverAgent` returns a relevant AgentCard:
       - Extract the `port` value from the AgentCard's `url`.
       - Call the `callAgent` tool with:
         • port = the extracted port
         • message = the original user query
    3. If no relevant agent is found, politely tell the user:  
       "Sorry, no agent is available to handle your request."

    Output Formatting:
    - Never return raw JSON, arrays, or technical objects to the user.
    - Always transform the final agent's response into a clean, human-readable format.
    - Use simple lists, bullet points, or numbered items where appropriate.
    - Example:
      If the response is:
        [{"name":"Cheese Pizza","price":"40$"},{"name":"Garlic Bread","price":"50$"}]
      You must transform it into:
        🍕 Menu:
        1. Cheese Pizza — 40$
        2. Garlic Bread — 50$

    Remember:
    - Only forward the agent’s final response.
    - Do not invent or hallucinate answers.
    """,
    tools=[callAgent, discoverAgent],
    model=model
)


memory = []

class Start(AgentExecutor):
    async def execute(self, context, event_queue):
        userinput = context.get_user_input()
        memory.append({"role": "user", "content": userinput})
        runAgent = await Runner.run(agent1, memory, context=CoordinatorContext())
        memory.append({"role": "assistant", "content": runAgent.final_output})
        await event_queue.enqueue_event(new_agent_text_message(runAgent.final_output))

    async def cancel(self, context, event_queue):
        await event_queue.enqueue_event(new_agent_text_message("Failed To Execute Agent"))


card = AgentCard(
    name="Orchestrator Agent",
    description="A Orchestrator Agent",
    url="http://localhost:8013",
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
        name="Orchestrator Agent",
        description="A Orchestrator Agent",
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
    uvicorn.run(server.build(), host="localhost", port=8013)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())