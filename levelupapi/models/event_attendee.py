from django.db import models
from django.contrib.auth.models import User


class Event_Attendee(models.Model):

    event_id = models.DecimalField(max_digits=3, decimal_places=0)
    user_id = models.DecimalField(max_digits=3, decimal_places=0)