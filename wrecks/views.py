import os
import dotenv
import logging

from django.http import Http404
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Wrecks
from .models import Photos
from .models import Stories
from .models import References

dotenv.load_dotenv(dotenv.find_dotenv())

logger = logging.getLogger(__name__)


def homepage(request):
    context = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        "page": "map",
    }
    return render(request, 'wrecks/homepage.html', context)


def listofships(request):
    context = {
        "page": "ships"
    }
    return render(request, 'wrecks/listofships.html', context)


def markers(request):
    data = []
    for ship in Wrecks.objects.all():
        if (ship is not None and ship.latitude is not None and ship.longitude is not None):
            year = ship.year_sunk if ship.date_sunk is None else ship.date_sunk.year
            data.append(
                {"name": ship.ship_name, "num": ship.ship_num, "latitude": float(ship.latitude),
                 "longitude": float(ship.longitude), "year_sunk": year, "deaths": ship.deaths})
    return JsonResponse(data, safe=False)


def allShips(request):
    data = []
    for ship in Wrecks.objects.all():
        year = ship.year_sunk if ship.date_sunk is None else ship.date_sunk.year
        entry = {"name": ship.ship_name, "num": ship.ship_num, "year": year}
        data.append(entry)
    return JsonResponse(data, safe=False)


def detail(request, name, num):
    name = name.replace("_", " ")
    num = num.replace("_", " ")
    try:
        ship = Wrecks.objects.get(ship_name=name, ship_num=num)
    except ObjectDoesNotExist:
        raise Http404("Ship not found")

    photos = Photos.objects.filter(ship_name=name, ship_num=num).order_by('num')
    stories = Stories.objects.filter(ship_name=name, ship_num=num).order_by('num')
    references = References.objects.filter(ship_name=name, ship_num=num).order_by('num')

    context = {
        "ship": ship,
        "photos": photos,
        "stories": stories,
        "references": references,
        "page": "detail",
    }
    return render(request, 'wrecks/shipdetail.html', context)
