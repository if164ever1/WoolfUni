from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "ok",
        "application": "lesson-7-django",
        "message": "Django is running in Amazon EKS."
    })

def health(request):
    return JsonResponse({"status": "healthy"})
