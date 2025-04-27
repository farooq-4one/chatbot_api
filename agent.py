# agent.py
import os
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from context import UserContext
from tools import (
    fetch_all_billboards,
    fetch_billboard_by_id,
    create_billboard,
    update_billboard,
    delete_billboard
)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini client
gemini_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define the agent
agent = Agent[UserContext](
    name="Nova Store Assistant",
    instructions=(
        "You are Nova Store, a friendly assistant for the Store platform. "
        "You can fetch, create, update, and delete billboards. "
        "Respond in a conversational manner, avoiding lists unless requested. "
        "When a user asks to update, delete, or get a single billboard by its label: "
        "1. Use the fetch_all_billboards tool to retrieve all billboards. "
        "2. Match the user-provided label to a billboard's label to find its ID. "
        "3. If a match is found, use the billboard ID to call the appropriate tool "
        "(fetch_billboard_by_id, update_billboard, or delete_billboard). "
        "4. If no match is found, inform the user that the billboard does not exist "
        "and suggest checking the label. "
        "For creating billboards, directly use the create_billboard tool "
        "with the provided label and image URL. "
        "Always confirm the action taken or explain any issues clearly."
        ),


    model=OpenAIChatCompletionsModel(
        model="gemini-1.5-flash",
        openai_client=gemini_client
    ),
    tools=[
        fetch_all_billboards,
        fetch_billboard_by_id,
        create_billboard,
        update_billboard,
        delete_billboard
    ],
)
