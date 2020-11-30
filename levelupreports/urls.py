from levelupreports.views.users.eventsbyuser import eventbygamer_list
from django.urls import path
from .views import usergame_list

urlpatterns = [
    path('reports/usergames', usergame_list),
    path('reports/eventgames', eventbygamer_list),
]