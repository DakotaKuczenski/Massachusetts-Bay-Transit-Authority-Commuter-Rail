from django.urls import path

from . import views

urlpatterns = [
    path('commuterrail', views.commuterRail, name='commuterrail'),
    path('', views.home, name='home'),
]