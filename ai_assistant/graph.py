import os
from typing import TypedDict, Annotated

from dotenv import load_dotenv

from langchain_core.messages import AnyMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

from .tools import create_task_tools

load_dotenv()


class ChatState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    temperature=0,
)

# Temporary shared checkpointer for local testing
memory = InMemorySaver()


def create_graph(user_id):

    search_tool = TavilySearch(max_results=3)
    task_tools = create_task_tools(user_id)

    tools = [search_tool, *task_tools]

    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: ChatState):

        response = llm_with_tools.invoke(
            [
                SystemMessage(
                    content=(
                        "You are Sami PMS AI Assistant. "
                        "Use get_my_tasks for questions about the user's "
                        "assigned tasks, task status, and deadlines. "
                        "Use get_my_projects to retrieve projects the user manages "
                        "Use search_my_task_documents for questions about "
                        "uploaded task files, requirements, or specifications. "
                        "Use Tavily for recent news or current information. "
                        "For general knowledge, answer directly. "
                        "Never invent task information or search results."
                        "you are a helpful assistant that helps the user with their tasks and projects."
                        "and tells the user about their tasks and projects and their status and deadlines in a formal way "
                        "and suggest the user to complete their tasks and projects on time and in a formal way."
                    )
                ),
                *state["messages"],
            ]
        )

        return {"messages": [response]}

    builder = StateGraph(ChatState)

    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge("tools", "chatbot")

    return builder.compile(checkpointer=memory)
