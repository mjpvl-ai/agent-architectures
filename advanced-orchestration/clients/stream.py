# Copyright 2025 © BeeAI a Series of LF Projects, LLC
# SPDX-License-Identifier: Apache-2.0

import asyncio

from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart, MessageCompletedEvent, GenericEvent


async def client() -> None:
    async with Client(base_url="http://localhost:8000") as client:
        session_client = client.session()
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    break

                async for event in session_client.run_stream(
                    agent="router_agent",
                    input=[Message(parts=[MessagePart(content=user_input)])],
                ):
                    match event:
                        case MessageCompletedEvent():
                            print("\nSteps performed......", event.message)
                        case GenericEvent():
                            print(event.generic.update)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    asyncio.run(client())
