
import os
from functools import lru_cache

from .document_loader import load_task_document
from .text_splitter import split_documents


@lru_cache(maxsize=1)
def get_vector_store():
    from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
    from langchain_postgres import PGVector

    embeddings = FastEmbedEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        threads=2,
    )

    database_url = os.environ["DATABASE_URL"]

    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://", "postgresql+psycopg://", 1
        )
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )

    return PGVector(
        embeddings=embeddings,
        collection_name="sami_pms_documents",
        connection=database_url,
        use_jsonb=True,
        create_extension=False,
    )


def store_task_document(task):
    documents = load_task_document(task)
    chunks = split_documents(documents)

    if not chunks:
        return []

    return get_vector_store().add_documents(chunks)


def search_task_documents(user_id, query):
    from Project.models import Tasks

    task_ids = list(
        Tasks.objects.filter(
            assigned_to_id=user_id
        ).values_list("id", flat=True)
    )

    if not task_ids:
        return []

    return get_vector_store().similarity_search(
        query=query,
        k=4,
        filter={"task_id": {"$in": task_ids}},
    )
