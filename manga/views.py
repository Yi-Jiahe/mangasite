from django.shortcuts import render
from django.http import HttpResponse
from manga.models import Series, Scanlator


# Create your views here.
def index(request):
    return render(request, 'manga/index.html', {
        'manga': Series.objects.all()
    })


def series(request, id):
    series = Series.objects.filter(id=id)[0]
    return render(request, 'manga/series.html', {
        'series': series,
        'scanlators': series.scanlator_set.all()
    })


def scanlator(request, id):
    scanlator = Scanlator.objects.filter(id=id)[0]
    return render(request, 'manga/scanlator.html', {
        'scanlator': scanlator,
        'series': scanlator.series.all()
    })