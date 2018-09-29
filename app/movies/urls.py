from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('list/', views.MovieListCreateView.as_view(), name='movies_list'),
]
