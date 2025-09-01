"""A server that hosts a stock agent."""

from collections.abc import AsyncGenerator

from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server

server = Server(port=8002)


@server.agent(
    name="stock_agent",
    description="An agent that provides stock information.",
    input_content_types=["text/plain"],
    output_content_types=["text/plain"],
)
async def stock_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Provides stock information."""
    query = "".join(part.content for msg in input for part in msg.parts if part.content and part.content_type == "text/plain")
    yield Message(
        role="agent/stock_agent",
        parts=[MessagePart(content=f"The stock price of {query} is $100.")],
    )


server.run()
