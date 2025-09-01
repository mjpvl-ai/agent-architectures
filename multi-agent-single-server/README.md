# Multi-Agent Single Server Architecture

This example demonstrates a multi-agent single-server architecture where a single server hosts multiple agents.

## How to Run

1.  **Start the server:**

    Open a terminal in the `multi-agent-single-server` directory and run the following command:

    ```bash
    python servers/agent.py
    ```

2.  **Run the client:**

    Open a second terminal in the `multi-agent-single-server` directory and run the client with the desired agent name (`echo_agent` or `hello_agent`):

    ```bash
    python clients/client.py echo_agent
    ```

    or

    ```bash
    python clients/client.py hello_agent
    ```
