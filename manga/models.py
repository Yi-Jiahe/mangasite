from django.db import models


# Create your models here.
class Series(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Scanlator(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    series = models.ManyToManyField(Series, through='ScanlatorSeriesURL', blank=True)

    def __str__(self):
        return self.name


class ScanlatorSeriesURL(models.Model):
    scanlator = models.ForeignKey(Scanlator, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    url = models.CharField(max_length=511)