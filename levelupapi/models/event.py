from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    game_id = models.DecimalField(max_digits=3, decimal_places=0)
    datetime = models.DateTimeField(auto_now=True, editable=True)