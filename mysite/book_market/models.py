from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    age = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(110)
    ], null=True, blank=True)
