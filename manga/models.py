from django.db import models


# Create your models here.
class Series(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Scanlator(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
    series = models.ManyToManyField(Series)

    def __str__(self):
        return self.name
