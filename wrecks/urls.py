from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='index'),
    path('wrecks/markers.json', views.markers, name='index'),
    path('wrecks/allShips.json', views.allShips, name='index'),
]
