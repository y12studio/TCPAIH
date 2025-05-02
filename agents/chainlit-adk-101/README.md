# Chainlit + Google ADK Integration Example

This project demonstrates how to integrate the Google Agent Development Kit (ADK) with the Chainlit framework to create a conversational AI application with a web-based chat interface.

## Features

*   Uses Chainlit for the frontend chat UI.
*   Uses Google ADK for the backend agent logic, including model interaction and tool usage.
*   Includes a simple example tool (`get_weather`).
*   Manages ADK sessions per user chat session.

## Setup

1.  **Prerequisites:**
    *   Python >= 3.13
    *   `uv` (or `pip`) for package management.

2.  **Clone the repository (if you haven't already):**
    ```bash
    # Navigate to your desired project directory
    git clone <your-repo-url>
    cd <your-repo-directory>/chainlit101
    ```

3.  **Install Dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    # Using uv (recommended)
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt # Assuming you generate one from pyproject.toml or install directly

    # Or using pip directly with pyproject.toml
    python -m venv .venv
    source .venv/bin/activate
    pip install . # Installs dependencies from pyproject.toml
    ```
    *Note: If you don't have `uv`, install it first (`pip install uv`).*

4.  **Set up Environment Variables:**
    You need a Google API key for the ADK to interact with Google's generative models.
    *   Create a file named `.env` in the `chainlit101` directory.
    *   Add your API key to the `.env` file:
        ```
        GOOGLE_API_KEY='YOUR_API_KEY_HERE'
        ```
    *   Replace `YOUR_API_KEY_HERE` with your actual Google API key. The application uses `python-dotenv` to load this key automatically.

## Running the Application

1.  **Activate your virtual environment (if not already active):**
    ```bash
    source .venv/bin/activate
    ```

2.  **Run the Chainlit application:**
    ```bash
    chainlit run app.py -w
    ```
    *   `chainlit run app.py`: Starts the Chainlit server using your `app.py` script.
    *   `-w`: Enables auto-reloading, so the app restarts automatically when you save changes to the code.

3.  Open your web browser and navigate to the URL provided by Chainlit (usually `http://localhost:8000`).

## How it Works

*   **`app.py`:** This is the main application file.
    *   It initializes a Google ADK `Agent` with a specific model, description, instructions, and tools (like the example `weather_tool`).
    *   It uses Chainlit's `@cl.on_chat_start` decorator to create a new ADK `Runner` and `Session` for each user connecting to the chat. This isolates conversations.
    *   The `@cl.on_message` decorator handles incoming user messages. It sends the message to the ADK `Runner` for processing.
    *   The ADK runner interacts with the configured Gemini model, handles tool calls (like the weather tool), and streams responses back.
    *   The application updates the Chainlit UI progressively as the ADK generates responses or indicates tool usage.
*   **`pyproject.toml`:** Defines project metadata and dependencies (`chainlit`, `google-adk`, `python-dotenv`).
*   **ADK Components:**
    *   `Agent`: Defines the AI's personality, instructions, model, and tools.
    *   `Runner`: Executes the agent logic for a specific session.
    *   `InMemoryArtifactService` / `InMemorySessionService`: Simple in-memory storage for session data and artifacts (can be replaced with persistent storage).
    *   `FunctionTool`: Wraps Python functions (like `get_weather`) so the ADK agent can use them.
