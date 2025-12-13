from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue, InMemoryQueueManager
from a2a.utils import new_agent_text_message
from a2a.types import AgentCapabilities, AgentCard, AgentSkill, AgentProvider
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, function_tool
import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, TextPart, Role, Part
from dataclasses import dataclass, field
from dotenv import load_dotenv
from agents import handoff
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

@dataclass
class AgentInfo:
    name: str
    url: str
    port: int
    description: str = ""
    status: str = "unknown"
    agent_card: AgentCard | None = None

@dataclass
class AgentsA2ACall:
    message: str
    port: int

@dataclass
class CoordinatorContext:
    agents_by_port: dict[int, AgentInfo] = field(default_factory=dict)
    allowed_ports: list[int] = field(default_factory=lambda: [8001, 8002, 8003])

    def add_agent(self, port: int, agent_info: AgentInfo):
        """Add or update an agent in the registry by port."""
        self.agents_by_port[port] = agent_info
    
    def get_agent_by_port(self, port: int) -> AgentInfo | None:
        """Get agent by port number."""
        return self.agents_by_port.get(port)
    
    def get_all_agents(self) -> dict[int, AgentInfo]:
        """Get all agents mapped by port."""
        return self.agents_by_port.copy()
    
    def get_online_agents(self) -> dict[int, AgentInfo]:
        """Get only online agents."""
        return {port: agent for port, agent in self.agents_by_port.items() if agent.status == "online"}


from agents import RunContextWrapper
import json

@function_tool
async def discoverAgent(ctx:RunContextWrapper):
    ports = [8001, 8002]
    discovered = {}
    async with httpx.AsyncClient() as client:
        for port in ports:
            url = f"http://localhost:{port}"    
            try:
                resolver = A2ACardResolver(base_url=url, httpx_client=client)
                card = await resolver.get_agent_card()
                name = card.name
                description = card.description
                agent_info = AgentInfo(
                    name=name,
                    url=url,
                    port=port,
                    description=description,
                    status="online",
                    agent_card=card
                )
                
                # Store in context with A2A client
                ctx.context.add_agent(port=port, agent_info=agent_info)

                discovered[name] = {
                    "name": name,
                    "description": description,
                    "url": url,
                    "status": "online",
                    "capabilities": card.capabilities.model_dump() if card.capabilities else {}
                }
                
            except Exception as e:
                discovered[url] = {"status": "error", "error": str(e), "url": url}
    
    
    print(f"Discovered agents: {json.dumps(discovered, indent=2)}")
    return f"Discovered agents: {json.dumps(discovered, indent=2)}"

@function_tool
async def coordinate_agents(context: RunContextWrapper, agent_messages: list[AgentsA2ACall]):
    """
    Send personalized messages to agents using A2A clients. 
    agent_messages: JSON string like [{"8003": "Check your calendar"}, {"8001": "Optimize schedule"}]
    """
    print(f"\n current context: ", context.context, "\n")

    responses = {}
    
    for requested_call in agent_messages:
        port = requested_call.port
        message = requested_call.message
        message_id = f"agent-{port}"
        agent_info = context.context.get_agent_by_port(port)

        if agent_info is None or agent_info.agent_card is None:
            raise ValueError(f"No agent card found for port {port}. Ensure agent is online and has a valid card.")
                
        try:
            # Create A2A message
            a2a_message = Message(
                role=Role.user,
                message_id=message_id,
                parts=[Part(root=TextPart(text=message))]
            )
            
            async with httpx.AsyncClient(timeout=120) as httpx_client:

                client_config = ClientConfig(httpx_client=httpx_client, streaming=False)
                client = ClientFactory(config=client_config).create(card=agent_info.agent_card)

                response_stream = client.send_message(a2a_message)
                
                response_parts = []
                async for chunk in response_stream:
                    if hasattr(chunk, "parts"):
                        for p in chunk.parts:
                            if hasattr(p.root, "text"):
                                response_parts.append(p.root.text)
                response_text = " ".join(response_parts) if response_parts else "No response received"

                responses[port] = {
                    "status": "success",
                    "response": response_text,
                    "agent": agent_info.name if agent_info else f"Unknown Agent on port {port}"
                }
            
        except Exception as e:
            responses[port] = {"status": "error", "error": str(e), "agent": agent_info.name if agent_info else f"Unknown Agent on port {port}"}

    return responses
        
agent = Agent(
    name="MainFoodSuggestAgent",
    instructions="""
    You are a MainAgent Your orchestrate suggesting user good food according to their need
    Your process:
    1. First discover available agents using discover_agents tool (no parameters needed)
    2. Send messages to specific agents using coordinate_agents tool with AgentsA2ACall objects
    3. Use port numbers to address agents: 8001, 8002
    4. Analyze responses to find matching food
    6. Provide a comprehensive summary

    For coordinate_agents, create AgentsA2ACall objects like:
    [
        AgentsA2ACall(message="Do you have Pizza Avaliable", port=8001),
        AgentsA2ACall(message="Do you have Burger Avaliable", port=8002)
    ]
    Always discover agents first, then explore using port numbers.
    dont reply with like i am waiting for there response eg provide the solution and correct answer of user query
""",
    tools=[coordinate_agents, discoverAgent],
    model=model
)

card = AgentCard(
    name="OrderSuggesterCordinator",
    description="you are menu telling cordinator agent",
    capabilities=AgentCapabilities(push_notifications=False, streaming=False, state_transition_history=False),
    url="http://localhost:8000",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    preferred_transport="JSONRPC",
    version="1.0.0",
    skills=[AgentSkill(
        name="SuggestFood",
        description="Get menu of the MCDonalds",
        id="123",
        tags=["menu", "food", "suggest"]
    )],
        provider=AgentProvider(
        organization="Ahmed Official",
        url="https://ahmedportfolio.com"
    ),
)


class Executor(AgentExecutor):
    def __init__(self, cordinator):
        self.cordinator = cordinator
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ):
        userinput = context.get_user_input()
        result = await Runner.run(agent, userinput, context=self.cordinator)
        await event_queue.enqueue_event(new_agent_text_message(result.final_output))
    
    async def cancel(self, context, event_queue):
        await event_queue.enqueue_event(new_agent_text_message("An Error Occured"))


if __name__ == "__main__":
    run = DefaultRequestHandler(
        agent_executor=Executor(CoordinatorContext()),
        queue_manager=InMemoryQueueManager(),
        task_store=InMemoryTaskStore()
    )

    start = A2AFastAPIApplication(agent_card=card, http_handler=run)

    import uvicorn
    uvicorn.run(start.build(), host="localhost", port=8003)