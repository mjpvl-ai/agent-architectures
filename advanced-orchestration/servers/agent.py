# Copyright 2025 © BeeAI a Series of LF Projects, LLC
# SPDX-License-Identifier: Apache-2.0

from collections.abc import AsyncGenerator
from typing import Literal, TypedDict

from acp_sdk.models import Author, Capability, Message, MessagePart, TrajectoryMetadata
from acp_sdk.server import RunYield, RunYieldResume, Server
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph


class AdvancedAgentState(TypedDict):
    original_request: str
    routing_decision: Literal["greeting", "weather", "unknown"]
    greeting: str
    weather: str
    final_response: str


def greeting_agent_function(state: AdvancedAgentState) -> dict[str, str]:
    """A specialist agent that provides greetings."""
    return {"greeting": f"Hello, {state['original_request']}!"}


def weather_agent_function(state: AdvancedAgentState) -> dict[str, str]:
    """A specialist agent that provides weather information."""
    # In a real scenario, this would call a weather API
    return {"weather": f"The weather for {state['original_request']} is sunny."}


def route_request(state: AdvancedAgentState) -> dict[str, str]:
    """Routes the request to the appropriate specialist agent."""
    request = state["original_request"].lower()
    if "hello" in request or "hi" in request:
        return {"routing_decision": "greeting"}
    elif "weather" in request:
        return {"routing_decision": "weather"}
    else:
        return {"routing_decision": "unknown"}


def format_greeting_response(state: AdvancedAgentState) -> dict[str, str]:
    return {"final_response": state["greeting"]}


def format_weather_response(state: AdvancedAgentState) -> dict[str, str]:
    return {"final_response": state["weather"]}


def format_unknown_response(state: AdvancedAgentState) -> dict[str, str]:
    return {"final_response": "Sorry, I can't handle that request."}


# Create the graph for the router agent
workflow = StateGraph(AdvancedAgentState)

# Add the nodes
workflow.add_node("router", RunnableLambda(route_request))
workflow.add_node("greeting_agent", RunnableLambda(greeting_agent_function))
workflow.add_node("weather_agent", RunnableLambda(weather_agent_function))
workflow.add_node("format_greeting", RunnableLambda(format_greeting_response))
workflow.add_node("format_weather", RunnableLambda(format_weather_response))
workflow.add_node("format_unknown", RunnableLambda(format_unknown_response))

# Set the entry point
workflow.set_entry_point("router")

# Add the conditional edges
workflow.add_conditional_edges(
    "router",
    lambda x: x["routing_decision"],
    {
        "greeting": "greeting_agent",
        "weather": "weather_agent",
        "unknown": "format_unknown",
    },
)

# Connect the specialist agents to their formatters
workflow.add_edge("greeting_agent", "format_greeting")
workflow.add_edge("weather_agent", "format_weather")

# Set the finish points
workflow.set_finish_point("format_greeting")
workflow.set_finish_point("format_weather")
workflow.set_finish_point("format_unknown")

graph = workflow.compile()

server = Server()


@server.agent(
    name="router_agent",
    description="An advanced agent that routes requests to specialist agents.",
    input_content_types=["text/plain"],
    output_content_types=["text/plain"],
    metadata={
        "license": "Apache-2.0",
        "programming_language": "Python",
        "author": Author(name="BeeAI"),
        "capabilities": [
            Capability(name="routing", description="Routes requests to other agents."),
            Capability(name="orchestration", description="Orchestrates a multi-agent workflow."),
            Capability(name="langgraph", description="Uses LangGraph for the agent's workflow."),
        ],
    },
)
async def router_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This agent acts as a router, decomposing complex requests and routing them to
    specialist agents. It then aggregates the results to provide a final response.
    """
    parts: list[MessagePart] = []
    query = "".join(part.content for msg in input for part in msg.parts if part.content and part.content_type == "text/plain")

    output = None
    async for event in graph.astream({"original_request": query}, stream_mode="updates"):
        for node_name, node_data in event.items():
            if "__end__" in node_name:
                continue
            intermediate_part = MessagePart(
                content=f"🔄 Intermediate step: {node_name} -> {node_data}\n",
                content_type="text/plain",
                metadata=TrajectoryMetadata(
                    message=f"Executing node: {node_name}",
                    tool_name="langgraph_node",
                    tool_input={"node": node_name, "user_input": query},
                    tool_output=node_data,
                ),
            )
            parts.append(intermediate_part)
        output = event

    if output:
        final_response = "No response generated."
        for key in ["format_greeting", "format_weather", "format_unknown"]:
            if key in output:
                final_response = output[key].get("final_response", "Error in response formatting.")
                break
    else:
        final_response = "No output from graph."

    final_part = MessagePart(
        name="final_response",
        content=f"✅ {final_response}",
        content_type="text/plain",
    )
    parts.append(final_part)

    yield Message(role="agent/router_agent", parts=parts)


server.run()
