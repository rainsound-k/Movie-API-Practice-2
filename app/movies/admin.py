from django.contrib import admin

from .models import Genre, Torrent, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Torrent)
class TorrentAdmin(admin.ModelAdmin):
    list_display = ['url', 'quality', 'size']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'year', 'rating', 'summary']
