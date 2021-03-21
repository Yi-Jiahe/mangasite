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


class NewScanlatorForm(forms.Form):
    name = forms.CharField(label='name')
    url = forms.CharField(label='url', required=False)


class NewSeriesForm(forms.Form):
    title = forms.CharField(label='title')


class AddSeriesToScanlatorForm(forms.Form):
    series = forms.ChoiceField(label='series', choices=[(s.id, s.title) for s in Series.objects.all()])
    url = forms.CharField(label='url')


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
    series = Series.objects.filter(id=id)[0]
    return render(request, 'manga/series.html', {
        'series': series,
        'scanlators': series.scanlator_set.all()
    })


def scanlator(request, id):
    scanlator = Scanlator.objects.filter(id=id)[0]
    new_scanlator_series_URL = ScanlatorSeriesURL(scanlator=scanlator)

    if request.method == 'POST':
        form = ScanlatorSeriesURLForm(request.POST, instance=new_scanlator_series_URL)

        if form.is_valid():
            # Save ScanlatorSeriesURL
            new_scanlator_series_URL = form.save(commit=False)
            new_scanlator_series_URL.save()
            # Add series to scanlator
            scanlator.series.add(new_scanlator_series_URL.series)

            return HttpResponseRedirect(reverse(f'manga:scanlator/{id}'))

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
        'form': NewScanlatorForm()
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
        'form': NewSeriesForm()
    })