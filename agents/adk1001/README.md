# Google Agent Development Kit (ADK) Samples

This directory contains sample agents built with Google's Agent Development Kit (ADK).

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- API key from Google AI Studio or Vertex AI
- Environment configuration

## Included Agents

1. **Weather Time Agent** ([weather-time/](weather-time/))
   - Provides current weather and time information for specific cities
   - Currently supports New York with mock data

2. **GenAI Art License Agent** ([genai-art-license/](genai-art-license/))
   - Answers questions about copyright and licensing for AI-generated art
   - Provides comprehensive disclaimers and guidance for public art usage

## Setup Instructions

1. Create a `.env` file in each agent directory (see `.env.example` for template)
2. Add your Google API key to the `.env` files:
   ```
   GOOGLE_GENAI_USE_VERTEXAI="False"
   GOOGLE_API_KEY="your-api-key-here"
   ```

## Running the Agents

To start the ADK web server with the agents:

```sh
# Navigate to this directory
cd agents/adk1001

# Install dependencies
uv sync

# Start the ADK web server
uv run adk web
```

Once running, you can access the web interface to interact with the agents.

## Development

- Agent code is in `agent.py` within each agent directory
- Each agent has its own prompt template and specialized tools
- Use `__init__.py` to expose the agent objects

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](/LICENSE) file for details.