from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='map'),
    path('ships/', views.list_of_ships, name='ships'),
    path('favorites/', views.list_of_favs, name='favs'),
    path('ships/<str:name>/<str:num>/', views.detail, name='detail'),
    path('wrecks/markers.json', views.markers, name='markers'),
    path('wrecks/allShips.json', views.all_ships, name='allShips'),
    path('wrecks/favShips.json', views.fav_ships, name='favShips'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('favorite', views.toggle_favorite),
    path('trivia/', views.trivia, name='trivia'),
    path('references/', views.references, name='references'),

]
