import os
import dotenv
import logging

import django.views.defaults
from django.http import Http404
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist

from .models import Wrecks
from .models import Photos
from .models import Stories
from .models import References
from .models import Visit
from .models import User
from .models import Profile

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
        if ship is not None and ship.latitude is not None and ship.longitude is not None:
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
    visit_wreck = Visit.objects.filter(ship_name=name, ship_num=num).order_by('num')

    context = {
        "ship": ship,
        "photos": photos,
        "stories": stories,
        "references": references,
        "visit_wreck": visit_wreck,
        "page": "detail",
    }

    if (request.user.is_authenticated):
        user = User.objects.get(id=request.user.id)
        context["starred"] = user.profile.favorite_ships.filter(ship_name=name, ship_num=num).count()

    return render(request, 'wrecks/shipdetail.html', context)


def changeFavorite(request):
    if not request.user.is_authenticated:
        return django.views.defaults.HttpResponseForbidden()

    name = request.GET.get('name', None)
    num = request.GET.get('num', None)
    fav = request.GET.get('fav', None)
    if name is None or num is None:
        return django.views.defaults.HttpResponseBadRequest()

    fav = fav == "true"
    user = User.objects.get(id=request.user.id)

    try:
        wreck = Wrecks.objects.get(ship_name=name, ship_num=num)
    except ObjectDoesNotExist:
        print("Wreck {} not found in database".format(name))
        return django.views.defaults.HttpResponseBadRequest()

    if fav:
        user.profile.favorite_ships.add(wreck)
    else:
        user.profile.favorite_ships.remove(wreck)

    user.profile.save()
    return HttpResponse(status=204)


def logout_view(request):
    logout(request)
    return redirect(homepage)
