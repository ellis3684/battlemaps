"""battlesnearme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from maps import views as maps_views
from battles import views as battle_views

urlpatterns = [
    path('getbattles/<str:latitude>/<str:longitude>/<str:iteration>/', battle_views.get_battles, name='getbattles'),
    path('about/', maps_views.about, name='about'),
    path('add-battle/', battle_views.add_battle, name='add-battle'),
    path('', maps_views.home, name='home'),
    path('admin/', admin.site.urls),
]
