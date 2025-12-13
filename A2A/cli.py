import asyncio
import httpx
import json
from agents.mcp import MCPServerStreamableHttp
from datetime import datetime

async def send_message(message: str, server_url: str = "http://localhost:8003"):
    """Send a message to the coordinator agent."""
    payload = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": message}],
                "messageId": f"cli-{datetime.now().timestamp()}"
            }
        },
        "id": f"cli-request-{datetime.now().timestamp()}"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(server_url, json=payload, timeout=60.0)
            
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Connection error: {str(e)}"

async def main():
    print("🏓 Table Tennis Coordinator CLI")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 🏓")
                break
                
            if not user_input:
                continue
                
            print("Coordinator: Thinking...")
            response = await send_message(user_input)
            print(f"Coordinator: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye! 🏓")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())