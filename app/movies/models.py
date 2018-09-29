from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Torrent(models.Model):
    url = models.URLField(blank=True, null=True)
    hash = models.CharField(max_length=200, blank=True, null=True)
    quality = models.CharField(max_length=50, blank=True, null=True)
    seeds = models.PositiveIntegerField(blank=True, null=True)
    peers = models.PositiveIntegerField(blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    size_bytes = models.PositiveIntegerField(blank=True, null=True)
    date_uploaded = models.DateTimeField(blank=True, null=True)
    date_uploaded_unix = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.url


class Movie(models.Model):
    url = models.URLField(blank=True, null=True)
    imdb_code = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200)
    title_english = models.CharField(max_length=200, blank=True, null=True)
    title_long = models.CharField(max_length=200, blank=True, null=True)
    slug = models.CharField(max_length=200, blank=True, null=True)
    year = models.PositiveIntegerField()
    rating = models.FloatField()
    runtime = models.PositiveIntegerField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    summary = models.CharField(max_length=500)
    description_full = models.CharField(max_length=500, blank=True, null=True)
    synopsis = models.CharField(max_length=500, blank=True, null=True)
    yt_trailer_code = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    mpa_rating = models.CharField(max_length=50, blank=True, null=True)
    background_image = models.URLField(blank=True, null=True)
    background_image_original = models.URLField(blank=True, null=True)
    small_cover_image = models.URLField(blank=True, null=True)
    medium_cover_image = models.URLField(blank=True, null=True)
    large_cover_image = models.URLField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    torrents = models.ManyToManyField(Torrent, blank=True)
    date_uploaded = models.DateTimeField(blank=True, null=True)
    date_uploaded_unix = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title
