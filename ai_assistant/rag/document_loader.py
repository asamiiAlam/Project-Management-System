
import os
import tempfile
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)

LOADER_BY_EXTENSION = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
}

MAX_FILE_BYTES = 10 * 1024 * 1024


def load_task_document(task):
    """Download a task attachment and return LangChain Documents."""

    if not task.task_file:
        return []

    filename = task.task_file.name
    extension = Path(filename).suffix.lower()

    if extension not in LOADER_BY_EXTENSION:
        raise ValueError(
            f"Unsupported document type: {extension}"
        )

    if task.task_file.size > MAX_FILE_BYTES:
        raise ValueError("Task file exceeds 10 MB")

    temp_path = None

    try:
        with task.task_file.open("rb") as cloud_file:
            with tempfile.NamedTemporaryFile(
                suffix=extension,
                delete=False
            ) as temp_file:

                temp_path = temp_file.name

                for part in cloud_file.chunks():
                    temp_file.write(part)

        loader_class = LOADER_BY_EXTENSION[extension]

        if extension == ".txt":
            loader = loader_class(
                temp_path,
                encoding="utf-8"
            )
        else:
            loader = loader_class(temp_path)

        docs = loader.load()

        for doc in docs:
            doc.metadata.update({
                "task_id": task.pk,
                "project_id": task.project_id,
                "source": filename,
                "file_type": extension,
            })

        return docs

    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
