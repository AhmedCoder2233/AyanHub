from a2a.server.events import EventQueue, InMemoryQueueManager
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.apps import A2AFastAPIApplication
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.utils import new_agent_text_message
from a2a.types import AgentSkill, AgentCard, AgentProvider, AgentCapabilities
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import TaskState, TextPart, Part
from agents import Agent
import asyncio

class Executor(AgentExecutor):
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ):
        
        updater = TaskUpdater(event_queue=event_queue, context_id=context.context_id, task_id=context.task_id)

        if not context.current_task:
            await updater.submit()
        await updater.start_work()

        user_input = context.get_user_input()
        print(f"🎯 Processing: {user_input}")

        # Step 3: Stream progress updates (TaskStatusUpdateEvent)
        progress_steps = [
            "🚀 Initializing...",
            "📊 Processing your request...",
            "🔍 Analyzing data...",
            "📝 Generating response..."
        ]

        for i, step in enumerate(progress_steps):
            # This streams a TaskStatusUpdateEvent
            await updater.update_status(
                TaskState.working,
                message=updater.new_agent_message([
                    Part(root=TextPart(text=f"{step} ({i+1}/{len(progress_steps)})"))
                ])
            )
            await asyncio.sleep(1)  # Simulate work

        # Step 4: Create and stream the final result (TaskArtifactUpdateEvent)
        result_text = f"✅ Completed processing: '{user_input}'\n\nProcessed at: {asyncio.get_event_loop().time()}"

        await updater.add_artifact(
            [Part(root=TextPart(text=result_text))],
            name="processing_result"
        )

        # Step 5: Complete the task (final TaskStatusUpdateEvent with final=true)
        await updater.complete()
        # if user_input == "Hello":
        #     response = "Hello How can i help you"
        # else:
        #     response= "Sorry i cannot help"
        
        # await event_queue.enqueue_event(new_agent_text_message(response))
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        await event_queue.enqueue_event(new_agent_text_message("Sorry Error"))


skills = [
    AgentSkill(
        name="Greeter",
        description="You are a greeter Agent",
        id="greeting",
        tags=["greeting", "conversation", "friendly"],
        examples=[
                "Hello!",
                "How are you?",
                "Goodbye!",
                "Hi there!"
        ]
    )
]

card = AgentCard(
    name="Greeting Agent",
    description="A friendly agent that responds to greetings and messages",
    url="http://localhost:8000",
    provider=AgentProvider(
        organization="Ahmed Official",
        url="https://ahmedportfolio.com"
    ),
    version="1.0.0",
    capabilities=AgentCapabilities(
        streaming=True,
        push_notifications=True,
        state_transition_history=False
    ),
    skills=skills,
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    preferred_transport="JSONRPC"
)


if __name__ == "__main__":
    requestHandler = DefaultRequestHandler(
        agent_executor=Executor(),
        task_store=InMemoryTaskStore(),
        queue_manager=InMemoryQueueManager()
    )

    server = A2AFastAPIApplication(
        agent_card=card,
        http_handler=requestHandler
    )

    import uvicorn
    uvicorn.run(server.build(), host="localhost", port=8060)