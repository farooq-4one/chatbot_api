# frontend code is written below``
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional
from agent import agent
from agents import Runner, set_tracing_disabled
from context import UserContext

load_dotenv()
set_tracing_disabled(True)

app = FastAPI(title="Nova Store Assistant 🤖")

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://store-admin-farooq.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    userId: Optional[str]


@app.post("/chat")
async def chat_with_agent(req: ChatRequest):
    user_input = req.message.strip()

    if not req.userId:
        raise HTTPException(status_code=400, detail="userId is required")

    context = UserContext(userId=req.userId)
    print(f"User ID: {context.userId}")

    result = await Runner.run(
        starting_agent=agent, input=user_input, context=context
    )

    return {"response": result.final_output}


# utils/api.ts
# import axios from 'axios';
# import { auth } from '@clerk/nextjs/server';

# export async function sendMessage(message: string) {
#   try {
#     const { userId } = await auth(); // Always fetch userId
#     if (!userId) {
#       return { message: "Unauthorized", status: 401 };
#     }

#     const response = await axios.post('http://localhost:8000/chat', {
#       message,
#       userId,  // Always send this
#     }, {
#       headers: {
#         'Content-Type': 'application/json',
#       },
#     });

#     return response.data.response;

#   } catch (error) {
#     console.error('Error occurred:', error);
#     if (axios.isAxiosError(error)) {
#       return { message: "Failed to fetch response from the agent",
#       status: 500 };
#     }
#     return { message: "An unexpected error occurred", status: 500 };
#   }
# }
