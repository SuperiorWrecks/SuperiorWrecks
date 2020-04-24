import logging
import os

import django.views.defaults
import dotenv
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Photos
from .models import References
from .models import Stories
from .models import User
from .models import Visit
from .models import Wrecks

dotenv.load_dotenv(dotenv.find_dotenv())

logger = logging.getLogger(__name__)


def homepage(request):
    context = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
    }
    return render(request, 'wrecks/homepage.html', context)


def list_of_ships(request):
    context = {
        "url": reverse(all_ships),
    }
    return render(request, 'wrecks/listofships.html', context)


def list_of_favs(request):
    context = {
        "url": reverse(fav_ships),
    }
    return render(request, 'wrecks/listofships.html', context)


def trivia(request):
    return render(request, 'wrecks/trivia.html')


def references(request):
    return render(request, 'wrecks/references.html')


def game(request):
    return render(request, 'wrecks/game.html')


def markers(request):
    data = []
    for ship in Wrecks.objects.all():
        if ship is not None and ship.latitude is not None and ship.longitude is not None:
            year = ship.year_sunk if ship.date_sunk is None else ship.date_sunk.year
            data.append(
                {"name": ship.ship_name, "num": ship.ship_num, "latitude": float(ship.latitude),
                 "longitude": float(ship.longitude), "year_sunk": year, "deaths": ship.deaths})
    return JsonResponse(data, safe=False)


def all_ships(request):
    data = {}
    ships = []
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
    for ship in Wrecks.objects.all():
        year = ship.year_sunk if ship.date_sunk is None else ship.date_sunk.year
        entry = {"name": ship.ship_name, "num": ship.ship_num, "year": year}
        if request.user.is_authenticated:
            entry["fav"] = user.profile.favorite_ships.filter(ship_name=ship.ship_name, ship_num=ship.ship_num).exists()
        ships.append(entry)
    data["ships"] = ships
    data["favs"] = request.user.is_authenticated
    return JsonResponse(data, safe=False)


def fav_ships(request):
    if not request.user.is_authenticated:
        return HttpResponse(403)

    user = User.objects.get(id=request.user.id)

    data = {}
    ships = []
    for ship in user.profile.favorite_ships.all():
        year = ship.year_sunk if ship.date_sunk is None else ship.date_sunk.year
        entry = {"name": ship.ship_name, "num": ship.ship_num, "year": year, "fav": True}
        ships.append(entry)
    data["ships"] = ships
    data["favs"] = True
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
    }

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        context["starred"] = user.profile.favorite_ships.filter(ship_name=name, ship_num=num).count()

    return render(request, 'wrecks/shipdetail.html', context)


def toggle_favorite(request):
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
