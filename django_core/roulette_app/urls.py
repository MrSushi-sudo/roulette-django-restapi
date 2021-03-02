from django.urls import path

from .views import *

urlpatterns = [
    path('start/', StartRound.as_view()),
    path('spin/', SpinTheRoulette.as_view()),
    path('end/', EndRound.as_view()),
    path('statistics/', RoundStatistics.as_view()),
]
