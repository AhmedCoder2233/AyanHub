import httpx
from a2a.client import A2ACardResolver, ClientFactory, ClientConfig
from a2a.types import TextPart, Message, Role
import asyncio

async def main():
    while True:
        try:
            base_url = "http://localhost:8013/"
            async with httpx.AsyncClient(timeout=30) as httpx_client:
                resolver = A2ACardResolver(base_url=base_url, httpx_client=httpx_client)
                card = await resolver.get_agent_card()

                client = ClientFactory(
                config=ClientConfig(httpx_client=httpx_client, streaming=False)
                ).create(card=card)

                userinput = input("Ask: ")

                message = Message(
                role="user",
                parts=[TextPart(text=userinput)],  
                message_id="123"
                )

                sendMessage = client.send_message(message)
                async for m in sendMessage:
                    print(m.parts[0].root.text)

        except Exception as e:
            print(f"Error Agaya: {e}")
            
asyncio.run(main())
