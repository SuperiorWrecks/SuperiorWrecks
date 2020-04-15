from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='index'),
    path('ships/', views.listofships, name='index'),
    path('ships/<str:name>/<str:num>/', views.detail, name='index'),
    path('wrecks/markers.json', views.markers, name='index'),
    path('wrecks/allShips.json', views.allShips, name='index'),
    path('auth/logout/', views.logout_view, name='logout'),
]
