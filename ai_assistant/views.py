from django.shortcuts import render

# Create your views here.

from pathlib import Path

from django.db import connection
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Project.models import Tasks


class PrepareTaskDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        task = Tasks.objects.filter(
            id=task_id,
            assigned_to=request.user
        ).first()

        if not task:
            return Response(
                {"error": "Task not found or access denied"},
                status=404
            )

        if not task.task_file:
            return Response({"status": "no_document"})

        extension = Path(task.task_file.name).suffix.lower()

        if extension not in {".pdf", ".docx", ".txt"}:
            return Response({"status": "no_document"})

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM langchain_pg_embedding e
                    JOIN langchain_pg_collection c
                      ON e.collection_id = c.uuid
                    WHERE c.name = %s
                      AND e.cmetadata->>'task_id' = %s
                )
                """,
                ["sami_pms_documents", str(task.id)]
            )

            indexed = cursor.fetchone()[0]

        return Response({
            "task_id": task.id,
            "status": "ready" if indexed else "pending"
        })
