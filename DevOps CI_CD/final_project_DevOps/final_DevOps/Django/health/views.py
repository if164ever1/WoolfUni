import os
from django.http import JsonResponse


def home(request):
    return JsonResponse(
        {
            "application": "final-devops-django",
            "message": os.getenv(
                "APP_MESSAGE",
                "Django is running in the final DevOps project.",
            ),
            "image_tag": os.getenv("IMAGE_TAG", "unknown"),
        }
    )


def health(request):
    return JsonResponse({"status": "ok"})
