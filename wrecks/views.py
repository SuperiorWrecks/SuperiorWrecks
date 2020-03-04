import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

from django.shortcuts import render

from .models import Wrecks


def homepage(request):
    context = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        'wrecks': Wrecks.objects.all()
    }
    return render(request, 'wrecks/homepage.html', context)
