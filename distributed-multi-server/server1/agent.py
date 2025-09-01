"""A server that hosts a weather agent."""

from collections.abc import AsyncGenerator

from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server

server = Server(port=8001)


@server.agent(
    name="weather_agent",
    description="An agent that provides weather information.",
    input_content_types=["text/plain"],
    output_content_types=["text/plain"],
)
async def weather_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Provides weather information."""
    query = "".join(part.content for msg in input for part in msg.parts if part.content and part.content_type == "text/plain")
    yield Message(
        role="agent/weather_agent",
        parts=[MessagePart(content=f"The weather in {query} is sunny.")],
    )


server.run()
