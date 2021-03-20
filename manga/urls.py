from django.urls import path

from . import views

app_name = "manga"
urlpatterns = [
    path('', views.index, name='index'),
    path('series/<str:id>', views.series, name='series')
]