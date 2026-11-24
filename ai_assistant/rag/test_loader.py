from Project.models import Tasks
from ai_assistant.rag.document_loader import load_task_document

task = (
    Tasks.objects
    .exclude(task_file="")
    .exclude(task_file__isnull=True)
    .first()
)

if task is None:
    print("No uploaded task files found.")
else:
    documents = load_task_document(task)

    print("Task:", task.title)
    print("Number of Document objects:", len(documents))

    for doc in documents[:2]:
        print("\nText:")
        print(doc.page_content[:1000])

        print("\nMetadata:")
        print(doc.metadata)