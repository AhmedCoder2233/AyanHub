from a2a.client import A2ACardResolver, ClientConfig, ClientFactory, A2AClient
from a2a.types import Message, TextPart
from agents import trace, run
import httpx

async def main():
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resolver = A2ACardResolver(base_url="http://localhost:8000/", httpx_client=client)
            card = await resolver.get_agent_card()
            print("Card Agaya", card)

            client = ClientFactory(config=ClientConfig(streaming=False, httpx_client=client)).create(card=card)

            message = Message(
                role="user",
                message_id="123",
                parts=[TextPart(text="Schedule a team meeting for tomorrow at 2 PM")]
            )

            result = client.send_message(message)
            async for event in result:
                print("Agaya Result", event)
            
    except Exception as e:
        print(f"Error Agaya: {e}")

import asyncio
asyncio.run(main())