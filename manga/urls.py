from django.urls import path

from . import views

app_name = "manga"
urlpatterns = [
    path('', views.index, name='index'),
    path('series/<str:id>', views.series, name='series'),
    path('scanlator/', views.scanlators, name='scanlators'),
    path('scanlator/<str:id>', views.scanlator, name='scanlator'),
    path('add_scanlator', views.add_scanlator, name='add_scanlator'),
    path('add_series', views.add_series, name='add_series')
]