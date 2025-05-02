#!/bin/bash
uv init .
uv add chainlit google-adk python-dotenv

echo ""
echo "Chainlit is installed. You can now run your app with the command:"
echo ""
echo " uv run chainlit run app.py"