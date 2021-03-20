from django.db import models


# Create your models here.
class Series(models.Model):
    title = models.CharField(max_length=255)


class Scanlator(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    series = models.ManyToManyField(Series)
