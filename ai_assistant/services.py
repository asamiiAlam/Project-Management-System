from .graph import create_graph
from django.contrib.auth import get_user_model

User = get_user_model()

# Find an existing user who has assigned tasks
user = User.objects.filter(tasks__isnull=False).distinct().first()

if user is None:
    print("No users with assigned tasks found.")

else:
    print("Testing with user:", user.username)
    print("User ID:", user.id)

    graph = create_graph(user_id=user.id)

    config = {"configurable": {"thread_id": f"task-test-user-{user.id}"}}
    result = graph.invoke(
    {"messages": [("user", "Show me my projects with their status and priority.")]},
    config={"configurable": {"thread_id": f"user-{user.id}-projects-test"}},
    )

print("\nAI Answer:")
print(result["messages"][-1].content)

for message in result["messages"]:
    if message.type == "ai" and message.tool_calls:
        print("Tool called:", message.tool_calls)

    print("\nAI Answer:")
    print(result["messages"][-1].content)

    print("\nMessage History:")

    for message in result["messages"]:
        print("\nType:", message.type)

        if message.type == "ai" and message.tool_calls:
            print("Tool calls:", message.tool_calls)

        elif message.type == "tool":
            print("Tool result:", str(message.content)[:500])

        else:
            print("Content:", str(message.content)[:500])
