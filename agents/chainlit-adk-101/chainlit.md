# Chainlit configuration file
title = "ADK-Chainlit Assistant"
description = "A powerful assistant powered by Google's Agent Development Kit"

# Theme and UI settings
theme.primary_color = "#4F6DF5"  # Blue color for branding

# Settings for the chat interface
features.avatar_images = True     # Enable avatar images
features.latex = True             # Enable LaTeX support
features.file_search = True       # Enable file search

# Default header with helpful information
header = """
# 🤖 ADK-Powered Assistant

This assistant uses Google's Agent Development Kit (ADK) with Gemini model integration.

## Capabilities:
- Provide weather information for any location
- Hold multi-turn conversations

## Example Questions:
- "What's the latest news about AI?"
- "What's the weather in Tokyo?"
- "Can you help me understand quantum computing?"
"""