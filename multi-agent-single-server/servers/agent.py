"""A server that hosts multiple agents."""

from collections.abc import AsyncGenerator

from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server

server = Server()


@server.agent(
    name="echo_agent",
    description="An agent that echoes back the input.",
    input_content_types=["text/plain"],
    output_content_types=["text/plain"],
)
async def echo_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Echoes back the input."""
    query = "".join(part.content for msg in input for part in msg.parts if part.content and part.content_type == "text/plain")
    yield Message(
        role="agent/echo_agent",
        parts=[MessagePart(content=f"Echo: {query}")],
    )


@server.agent(
    name="hello_agent",
    description="An agent that says hello.",
    input_content_types=["text/plain"],
    output_content_types=["text/plain"],
)
async def hello_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Says hello."""
    query = "".join(part.content for msg in input for part in msg.parts if part.content and part.content_type == "text/plain")
    yield Message(
        role="agent/hello_agent",
        parts=[MessagePart(content=f"Hello, {query}!")],
    )


server.run()
