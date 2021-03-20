from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

from manga.models import Series, Scanlator


class NewScanlatorForm(forms.Form):
    name = forms.CharField(label='name')
    url = forms.CharField(label='url', required=False)


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


def add_scanlator(request):
    if request.method == 'POST':
        form = NewScanlatorForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']

            scanlator = Scanlator(name=name, url=url)
            # TODO try catch if the group already exists
            scanlator.save()

            return HttpResponseRedirect(reverse('manga:index'))
        else:
            # Re-render with existing information
            return render(request, 'manga/add_scanlator.html', {
                'form': form
            })

    return render(request, 'manga/add_scanlator.html', {
        'form': NewScanlatorForm()
    })