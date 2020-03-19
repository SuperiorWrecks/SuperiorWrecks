import os
import dotenv
import logging

from django.shortcuts import render
from django.http import JsonResponse

from .models import Wrecks

dotenv.load_dotenv(dotenv.find_dotenv())

logger = logging.getLogger(__name__)


def homepage(request):
    context = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        'wrecks': Wrecks.objects.all()
    }
    return render(request, 'wrecks/homepage.html', context)


def listofships(request):
    context = {
        'wrecks': Wrecks.objects.all()
    }
    return render(request, 'wrecks/listofships.html', context)


def markers(request):
    data = []
    for ship in Wrecks.objects.all():
        if (ship is not None and ship.latitude is not None and ship.longitude is not None):
            year = ship.year_sunk if ship.date_sunk is None else ship.date_sunk.year
            data.append(
                {"name": ship.ship_name, "num": ship.ship_num, "latitude": float(ship.latitude),
                 "longitude": float(ship.longitude), "year_sunk": year})
    return JsonResponse(data, safe=False)


def allShips(request):
    data = []
    for ship in Wrecks.objects.all():
        year = ship.year_sunk if ship.date_sunk is None else ship.date_sunk.year
        entry = {"name": ship.ship_name, "num": ship.ship_num, "year": year}
        data.append(entry)
    return JsonResponse(data, safe=False)
