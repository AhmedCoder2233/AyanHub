import asyncio
async def main():
    for a in range(1, 6):
        yield a
        await asyncio.sleep(1)

    
async def asli():
    async for event in main():
        print(f"Event Agaya: {event}")

import asyncio

asyncio.run(asli())