from django.shortcuts import get_object_or_404

from Project.models import Chatbox
import os
import json

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

def get_project_chat_data(project_id):

    chatbox = get_object_or_404(
        Chatbox,
        project__id=project_id
    )

    messages = (
        chatbox.messages
        .select_related("sender")
        .order_by("-created_at", "-id")[:50]
    )


    messages = reversed(list(messages))

    conversation = []

    for message in messages:
        conversation.append({
            "sender": message.sender.username,
            "message": message.content,
            "timestamp": message.created_at.isoformat()
        })

    return {
        "project_id": project_id,
        "chatbox_id": chatbox.id,
        "messages": conversation,
        
    }
def summarize_project_chat(project_id):


    conversation_data = get_project_chat_data(project_id)

    # 2. Initialize Groq model
    llm = ChatGroq(
        model=os.environ["GROQ_MODEL"],
        temperature=0.2,
        max_tokens=1500,
    )

    response = llm.invoke([
        SystemMessage(content="""
            You are an expert project management assistant.

            Analyze the provided project conversation.

            Generate a concise report containing:

            1. Discussion Summary
            2. Key Decisions
            3. Action Items (include responsible person if mentioned)
            4. Blockers and Issues

            Important rules:
            - Use only information from the conversation.
            - Do not invent decisions or action items.
            - If information is unavailable, mention that.
            - Keep the report clear and professional.
        """),

        HumanMessage(content=json.dumps(
            conversation_data,
            indent=2
        ))
    ])

 
    return {
        "project_id": project_id,
        "summary": response.content,
        "usage": response.usage_metadata,
    }
