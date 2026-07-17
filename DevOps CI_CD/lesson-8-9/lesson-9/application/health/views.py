import os
from django.http import JsonResponse


def index(request):
    return JsonResponse(
        {
            "status": "ok",
            "application": "lesson-8-9-django",
            "message": "Django was deployed by Jenkins, ECR, Helm and Argo CD.",
            "image_tag": os.getenv("IMAGE_TAG", "unknown"),
        }
    )


def health(request):
    return JsonResponse({"status": "healthy"})
