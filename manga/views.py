from django.shortcuts import render
from django.http import HttpResponse
from manga.models import Series, Scanlator


# Create your views here.
def index(request):
    return render(request, "manga/index.html", {
                      'manga': Series.objects.all()
                  })
