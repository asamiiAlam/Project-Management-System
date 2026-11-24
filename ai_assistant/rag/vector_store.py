
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

from .document_loader import load_task_document
from .text_splitter import split_documents


# 1. Load the Hugging Face embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)


# 2. Connect to PostgreSQL vector database
database_url = os.environ["DATABASE_URL"]

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="sami_pms_documents",
    connection=database_url,
    use_jsonb=True,
    create_extension=False,
)


# 3. Load, split and store a task document
def store_task_document(task):
    documents = load_task_document(task)

    chunks = split_documents(documents)

    if not chunks:
        return []

    ids = vector_store.add_documents(chunks)

    return ids


from Project.models import Tasks


def search_task_documents(user_id, query):

    # Find tasks assigned to the logged-in user
    task_ids = list(
        Tasks.objects.filter(
            assigned_to_id=user_id
        ).values_list("id", flat=True)
    )

    if not task_ids:
        return []

    # Search only chunks belonging to those tasks
    results = vector_store.similarity_search(
        query=query,
        k=4,
        filter={
            "task_id": {"$in": task_ids}
        }
    )

    return results
