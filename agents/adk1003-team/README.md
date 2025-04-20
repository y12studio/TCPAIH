# Google Agent Development Kit (ADK) Sample Agents

This directory contains sample agents built with Google's Agent Development Kit (ADK), demonstrating multi-agent orchestration and tool integration.

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- API key from Google AI Studio or Vertex AI
- Environment configuration

## Setup Instructions

1. Create a `.env` file in each agent directory (see `.env.example` for a template).
2. Add your Google API key to the `.env` files:
   ```
   GOOGLE_GENAI_USE_VERTEXAI="False"
   GOOGLE_API_KEY="your-api-key-here"
   ```

## Running the Agents

To start the ADK web server with the agents:

```sh
# Navigate to this directory
cd agents/adk1003-team

# Install dependencies
uv sync

# Start the ADK web server
uv run adk web
```

Once running, you can access the web interface to interact with the agents.

## Development

- Agent logic is defined in `agent.py`.
- Each agent's prompt and instruction are loaded from a corresponding Markdown file (e.g., `agent_root.md`, `agent_greeting.md`, `agent_license.md`).
- Tools (such as `get_taichung_pubarts_list`) are defined as Python functions and passed to agents as needed.
- Use `__init__.py` to expose the agent objects for ADK discovery.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](/LICENSE) file for details.