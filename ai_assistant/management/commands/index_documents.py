
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connection

from Project.models import Tasks


class Command(BaseCommand):
    help = "Generate embeddings for existing task documents"

    def add_arguments(self, parser):
        parser.add_argument(
            "--task-id",
            type=int,
            default=None
        )

    def handle(self, *args, **options):

        tasks = Tasks.objects.exclude(
            task_file__isnull=True
        ).exclude(task_file="")

        if options["task_id"] is not None:
            tasks = tasks.filter(id=options["task_id"])

        for task in tasks:

            extension = Path(task.task_file.name).suffix.lower()

            if extension not in {".pdf", ".docx", ".txt"}:
                self.stdout.write(
                    f"Task {task.id}: Unsupported file, skipped"
                )
                continue

            # Check if embeddings already exist
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT 1
                        FROM langchain_pg_embedding
                        WHERE cmetadata->>'task_id' = %s
                    )
                    """,
                    [str(task.id)]
                )
                already_indexed = cursor.fetchone()[0]

            if already_indexed:
                self.stdout.write(
                    f"Task {task.id}: Already indexed"
                )
                continue

            try:
                # Import only when indexing is needed
                from ai_assistant.rag.vector_store import (
                    store_task_document
                )

                ids = store_task_document(task)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Task {task.id}: {len(ids)} chunks stored"
                    )
                )

            except Exception as error:
                self.stderr.write(
                    f"Task {task.id}: Failed - {error}"
                )
