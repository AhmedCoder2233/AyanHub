# import asyncio
# import httpx
# from a2a.client import A2ACardResolver

# async def test_skills():
#     base_url = 'http://localhost:8001'

#     async with httpx.AsyncClient() as httpx_client:
#         resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
#         agent_card = await resolver.get_agent_card()

#         print(f"Agent Card:\n\n {agent_card}")

# if __name__ == '__main__':
#     asyncio.run(test_skills())


import httpx
from a2a.client import A2ACardResolver, ClientFactory, ClientConfig, Client
from a2a.types import Message, TextPart

async def main():
    # Discover your calendar agent
    try:
        async with httpx.AsyncClient() as httpx_client:
            
            resolver = A2ACardResolver(base_url="http://localhost:8000", httpx_client=httpx_client)
            agent_card = await resolver.get_agent_card()
            print(f"Found agent: {agent_card}")

            # Create A2A client with discovered agent cards
            client: Client = ClientFactory(config=ClientConfig(httpx_client=httpx_client, streaming=False)).create(card=agent_card)

            # Create message with proper structure
            message = Message(
                role="user",
                message_id="123",
                parts=[TextPart(text="Schedule a team meeting for tomorrow at 2 PM")]
            )

            response = client.send_message(message)
            async for chunk in response:
                print("CHUNK", chunk)

    except Exception as e:
        print(f"Error fetching agent cards: {e}")
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())