import os
import asyncio
from typing import AsyncGenerator, List, Dict, Any

import chainlit as cl
from chainlit.types import AskFileResponse
from google.genai import types
from google.adk import Agent, Runner
from google.adk.tools import google_search, FunctionTool
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.sessions.in_memory_session_service import InMemorySessionService

# Load API key from environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY environment variable not set. The application may not function correctly.")

# Create a simple weather tool for demonstration purposes
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    # In a real app, this would call a weather API
    return f"The weather in {location} is currently sunny and 75°F."

# Create the weather tool using the correct FunctionTool initialization
weather_tool = FunctionTool(get_weather)

# Initialize ADK agent with API key
agent = Agent(
    name="chainlit_assistant",
    model="gemini-2.5-flash-preview-04-17",  
    description="A helpful assistant that can search the web and provide weather information",
    instruction="""You are a helpful assistant with access to tools.
    Use the weather tool when asked about weather conditions.
    Be friendly, helpful, and concise in your responses.""",
    tools=[weather_tool]
    # API key is now read automatically from environment variables
)

# Initialize global runner, artifact and session services
artifact_service = InMemoryArtifactService()
session_service = InMemorySessionService()

# Store user sessions
user_sessions = {}

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    user_id = cl.user_session.get("user_id") or "default_user"
    
    # Create a new runner for this session
    runner = Runner(
        app_name="chainlit_demo",
        agent=agent,
        artifact_service=artifact_service,
        session_service=session_service
    )
    
    # Create a new session
    session = session_service.create_session(
        app_name="chainlit_demo",
        user_id=user_id
    )
    
    # Store session info
    user_sessions[user_id] = {
        "runner": runner,
        "session_id": session.id
    }
    
    # Send an initial message
    await cl.Message(content="Hello! How can I help you today?").send()

@cl.on_message
async def on_message(message: cl.Message):
    """Process user messages."""
    user_id = cl.user_session.get("user_id") or "default_user"
    
    if user_id not in user_sessions:
        await cl.Message(content="Session not found. Please refresh the page.").send()
        return
    
    user_session = user_sessions[user_id]
    runner = user_session["runner"]
    session_id = user_session["session_id"]
    
    # Create a thinking message
    thinking_msg = cl.Message(content="", author="Assistant")
    await thinking_msg.send()
    
    # Convert the user message to ADK format
    user_content = types.Content(
        role="user", 
        parts=[types.Part(text=message.content)]
    )
    
    response_content = ""
    tool_calls = []
    is_streaming = False
    
    try:
        # Process the message with the ADK runner
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content
        ):
            # Handle different event types
            if event.content and event.content.parts:
                # Extract text content
                text_parts = [part.text for part in event.content.parts if part.text]
                if text_parts:
                    response_content = "".join(text_parts)
                    # Update the message with the latest content
                    thinking_msg.content = response_content # Fix: Set content attribute
                    await thinking_msg.update() # Fix: Call update without args
                    is_streaming = True
            
            # Handle tool calls for UI feedback
            function_calls = event.get_function_calls()
            if function_calls:
                for call in function_calls:
                    tool_calls.append({
                        "name": call.name,
                        "args": call.args,
                        "response": None  # Will be updated when we get the response
                    })
                    tool_message = f"🔧 Using tool: {call.name} with args: {call.args}"
                    await cl.Message(content=tool_message, author="System").send()
            
            # Handle tool responses
            function_responses = event.get_function_responses()
            if function_responses:
                for response in function_responses:
                    # Find the matching tool call and update it
                    for tool_call in tool_calls:
                        if tool_call["name"] == response.name and tool_call["response"] is None:
                            tool_call["response"] = response.response
                            # Extract the 'result' if response is a dict, otherwise show raw response
                            response_value = response.response
                            if isinstance(response_value, dict) and 'result' in response_value:
                                display_response = response_value['result']
                            else:
                                display_response = response_value # Fallback
                            tool_message = f"🔧 Tool response: {display_response}"
                            await cl.Message(content=tool_message, author="System").send()
                            break
    
    except Exception as e:
        # Fix: remove the elements parameter and just remove the thinking message
        await thinking_msg.remove()
        await cl.Message(content=f"Error: {str(e)}").send()
        return
    
    # If no streaming occurred, update with final content
    if not is_streaming and response_content:
        thinking_msg.content = response_content # Fix: Set content attribute
        await thinking_msg.update() # Fix: Call update without args
    
    # If somehow we didn't get any response content
    if not response_content:
        thinking_msg.content = "I'm not sure how to respond to that. Please try again." # Fix: Set content attribute
        await thinking_msg.update() # Fix: Call update without args