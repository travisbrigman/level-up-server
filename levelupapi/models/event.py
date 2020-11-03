"""Event model module"""
from django.db import models


class Event(models.Model):
    """Event database model"""
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=75)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)