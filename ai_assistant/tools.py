from langchain_core.tools import tool
from Project.models import Tasks
from Project.models import Project, Department
from django.db.models import Q
from .rag.vector_store import search_task_documents


def create_task_tools(user_id):
    @tool
    def search_my_task_documents(query: str) -> list[dict]:
        """Search uploaded documents attached to the user's assigned tasks.
        Use when the user asks about requirements, instructions,
        specifications, or information inside task attachments.
        """

        documents = search_task_documents(user_id=user_id, query=query)

        return [
        {
            "content": doc.page_content,
            "task_id": doc.metadata.get("task_id"),
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
        }
        for doc in documents
        ]   

    @tool
    def get_my_tasks() -> list[dict]:
        """Retrieve tasks assigned to the authenticated user, including their status, project, and deadlines."""

        tasks = (
            Tasks.objects.filter(assigned_to_id=user_id)
            .select_related("project")
            .order_by("-created_at")[:50]
        )

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "project": task.project.name,
                "finish_date": str(task.finish_date) if task.finish_date else None,
            }
            for task in tasks
        ]

    @tool
    def get_my_projects() -> list[dict]:
        """Retrieve projects managed by or assigned to the current user."""

        projects = (
            Project.objects.filter(
                Q(manager_id=user_id) | Q(tasks__assigned_to_id=user_id)
            )
            .distinct()
            .select_related("department")
            .order_by("-created_at")[:50]
        )

        return [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "priority": project.priority,
                "department": project.department.name,
                "finish_date": (
                    str(project.finish_date) if project.finish_date else None
                ),
            }
            for project in projects
        ]

    return [get_my_tasks, get_my_projects, search_my_task_documents]
