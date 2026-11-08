from django.shortcuts import render

from .models import ProjectFeature


def home(request):
    features = ProjectFeature.objects.all().order_by("id")

    context = {
        "features": features,
    }

    return render(request, "pages/home.html", context)
