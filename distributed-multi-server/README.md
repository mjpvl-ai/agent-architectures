# Distributed Multi-Server Architecture

This example demonstrates a distributed multi-server architecture where multiple independent servers each host one or more agents.

## How to Run

1.  **Start the servers:**

    Open a terminal in the `distributed-multi-server` directory and run the following command to start the first server:

    ```bash
    python server1/agent.py
    ```

    Open a second terminal in the `distributed-multi-server` directory and run the following command to start the second server:

    ```bash
    python server2/agent.py
    ```

2.  **Run the client:**

    Open a third terminal in the `distributed-multi-server` directory and run the client with the desired port and agent name (`8001 weather_agent` or `8002 stock_agent`):

    ```bash
    python clients/client.py 8001 weather_agent
    ```

    or

    ```bash
    python clients/client.py 8002 stock_agent
    ```
