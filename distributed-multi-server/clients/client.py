import asyncio
import sys

from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart


async def client() -> None:
    if len(sys.argv) < 3:
        print("Usage: python client.py <port> <agent_name>")
        return

    port = int(sys.argv[1])
    agent_name = sys.argv[2]

    async with Client(base_url=f"http://localhost:{port}") as client:
        session_client = client.session()
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    break

                response = await session_client.run(
                    agent=agent_name,
                    input=[Message(parts=[MessagePart(content=user_input)])],
                )
                print(f"Agent: {response.parts[0].content}")

            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    asyncio.run(client())
