from django.contrib import admin
from django.urls import path
from battles.views import BattleAPIView, BattleTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('battles/', BattleAPIView.as_view()),
    path('', BattleTemplateView.as_view())
]
