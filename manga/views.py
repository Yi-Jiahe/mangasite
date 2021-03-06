from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

from manga.models import Series, Scanlator, ScanlatorSeriesURL


class ScanlatorForm(forms.ModelForm):
    class Meta:
        model = Scanlator
        fields = '__all__'


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'


class ScanlatorSeriesURLForm(forms.ModelForm):
    class Meta:
        model = ScanlatorSeriesURL
        fields = '__all__'


# Create your views here.
def index(request):
    return render(request, 'manga/index.html', {
        'manga': Series.objects.all()
    })


def scanlators(request):
    return render(request,'manga/scanlators.html', {
        'scanlators': Scanlator.objects.all()
    })


def series(request, id):
    series = Series.objects.get(id=id)

    scanlator_links = ScanlatorSeriesURL.objects.filter(series=id)
    scanlators = {
        scanlator: scanlator_links.get(scanlator=scanlator.id).url
        for scanlator in series.scanlator_set.all()
    }

    return render(request, 'manga/series.html', {
        'series': series,
        'scanlators': scanlators,
    })


def scanlator(request, id):
    scanlator = Scanlator.objects.get(id=id)
    new_scanlator_series_URL = ScanlatorSeriesURL(scanlator=scanlator)

    if request.method == 'POST':
        form = ScanlatorSeriesURLForm(request.POST)

        if form.is_valid():
            # Save ScanlatorSeriesURL
            new_scanlator_series_URL = form.save(commit=False)
            new_scanlator_series_URL.save()
            # Add series to scanlator
            scanlator.series.add(new_scanlator_series_URL.series)
            scanlator.save()

            new_scanlator_series_URL = ScanlatorSeriesURL(scanlator=scanlator)

            return HttpResponseRedirect(reverse('manga:index'))
        else:
            return render(request, 'manga/scanlator.html', {
                'scanlator': scanlator,
                'series': scanlator.series.all(),
                'form': form
            })

    return render(request, 'manga/scanlator.html', {
        'scanlator': scanlator,
        'series': scanlator.series.all(),
        'form': ScanlatorSeriesURLForm(instance=new_scanlator_series_URL)
    })


def add_scanlator(request):
    if request.method == 'POST':
        form = ScanlatorForm(request.POST)

        if form.is_valid():
            new_scanlator = form.save(commit=False)
            new_scanlator.save()

            return HttpResponseRedirect(reverse('manga:index'))
        else:
            # Re-render with existing information
            return render(request, 'manga/add_scanlator.html', {
                'form': form
            })

    return render(request, 'manga/add_scanlator.html', {
        'form': ScanlatorForm()
    })


def add_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)

        if form.is_valid():
            new_series = form.save(commit=False)
            new_series.save()

            return HttpResponseRedirect(reverse('manga:index'))
        else:
            # Re-render with existing information
            return render(request, 'manga/add_series.html', {
                'form': form
            })

    return render(request, 'manga/add_series.html', {
        'form': SeriesForm()
    })