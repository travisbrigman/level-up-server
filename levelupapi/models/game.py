from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):

    game_type = models.CharField(max_length=50)