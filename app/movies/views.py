from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from rest_framework import status

from .models import Movie, Genre, Torrent


class MovieListCreateView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = Movie.objects.all()
        quality = request.GET.get('quality', '')
        try:
            minimum_rating = int(request.GET.get('minimum_rating', 0))
            if minimum_rating > 9:
                error = {
                    'status': 'error',
                    'status_message': 'minimum_rating 은 0 이상 9 이하의 정수만 가능합니다.',
                }
                return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            error = {
                'status': 'error',
                'status_message': 'minimum_rating 은 0 이상 9 이하의 정수만 가능합니다.',
            }
            return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
        query_term = request.GET.get('query_term', '')
        genre = request.GET.get('genre', '')

        if quality and not genre:
            queryset = queryset.filter(
                torrents__quality__contains=quality,
                rating__gte=minimum_rating,
                title__contains=query_term,
            )
        elif genre and not quality:
            queryset = queryset.filter(
                rating__gte=minimum_rating,
                title__contains=query_term,
                genres__name__contains=genre,
            )
        elif not genre and not quality:
            queryset = queryset.filter(
                rating__gte=minimum_rating,
                title__contains=query_term,
            )
        else:
            queryset = queryset.filter(
                torrents__quality__contains=quality,
                rating__gte=minimum_rating,
                title__contains=query_term,
                genres__name__contains=genre,
            )
        order_by = request.GET.get('order_by', 'desc')
        sort_by = request.GET.get('sort_by', '')

        if sort_by:
            if sort_by == 'peers':
                sort_by = 'torrents__peers'
            elif sort_by == 'seeds':
                sort_by = 'torrents__seeds'
            elif sort_by == 'date_added':
                sort_by = 'date_uploaded'

            if order_by == 'desc':
                queryset = queryset.order_by(sort_by)
            else:
                queryset = queryset.order_by('-' + sort_by)

        try:
            limit = int(request.GET.get('limit', 20))
            if limit > 50 or limit < 1:
                error = {
                    'status': 'error',
                    'status_message': 'limit 은 1 이상 50 이하의 정수만 가능합니다.',
                }
                return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            error = {
                'status': 'error',
                'status_message': 'limit 은 1 이상 50 이하의 정수만 가능합니다.',
            }
            return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)

        paginator = Paginator(queryset, limit)
        page = request.GET.get('page')
        pagination_queryset = paginator.get_page(page)

        movies_data = []
        for i in pagination_queryset:
            movie_dict = {}
            movie_dict['id'] = i.pk
            movie_dict['url'] = i.url
            movie_dict['imdb_code'] = i.imdb_code
            movie_dict['title'] = i.title
            movie_dict['title_english'] = i.title_english
            movie_dict['title_long'] = i.title_long
            movie_dict['slug'] = i.slug
            movie_dict['year'] = i.year
            movie_dict['rating'] = i.rating
            movie_dict['runtime'] = i.runtime
            genres_list = []
            for j in i.genres.all():
                genres_list.append(j.name)
            movie_dict['genres'] = genres_list
            movie_dict['summary'] = i.summary
            movie_dict['description_full'] = i.description_full
            movie_dict['synopsis'] = i.synopsis
            movie_dict['yt_trailer_code'] = i.yt_trailer_code
            movie_dict['language'] = i.language
            movie_dict['mpa_rating'] = i.mpa_rating
            movie_dict['background_image'] = i.background_image
            movie_dict['background_image_original'] = i.background_image_original
            movie_dict['small_cover_image'] = i.small_cover_image
            movie_dict['medium_cover_image'] = i.medium_cover_image
            movie_dict['large_cover_image'] = i.large_cover_image
            movie_dict['state'] = i.state
            torrents_list = []
            for k in i.torrents.all():
                torrent_detail_dict = {}
                torrent_detail_dict['url'] = k.url
                torrent_detail_dict['hash'] = k.hash
                torrent_detail_dict['quality'] = k.quality
                torrent_detail_dict['seeds'] = k.seeds
                torrent_detail_dict['peers'] = k.peers
                torrent_detail_dict['size'] = k.size
                torrent_detail_dict['size_bytes'] = k.size_bytes
                torrent_detail_dict['date_uploaded'] = k.date_uploaded
                torrent_detail_dict['date_uploaded_unix'] = k.date_uploaded_unix
                torrents_list.append(torrent_detail_dict)
            movie_dict['torrents'] = torrents_list
            movie_dict['date_uploaded'] = i.date_uploaded
            movie_dict['date_uploaded_unix'] = i.date_uploaded_unix
            movies_data.append(movie_dict)

        if not movies_data:
            return JsonResponse({
                'status': 'ok',
                'status_message': 'Query was successful',
                'data': {
                    'movie_count': len(queryset),
                    'limit': limit,
                    'page_number': pagination_queryset.number,
                }
            })
        else:
            return JsonResponse({
                'status': 'ok',
                'status_message': 'Query was successful',
                'data': {
                    'movie_count': len(queryset),
                    'limit': limit,
                    'page_number': pagination_queryset.number,
                    'movies': movies_data,

                }
            })

    def post(self, request, *args, **kwargs):
        movie = Movie.objects.create(
            url=request.POST.get('url', None),
            imdb_code=request.POST.get('imdb_code', None),
            title=request.POST.get('title', None),
            title_english=request.POST.get('title_english', None),
            title_long=request.POST.get('title_long', None),
            slug=request.POST.get('slug', None),
            year=request.POST.get('year', None),
            rating=request.POST.get('rating', None),
            runtime=request.POST.get('runtime', None),
            summary=request.POST.get('summary', None),
            description_full=request.POST.get('description_full', None),
            synopsis=request.POST.get('synopsis', None),
            yt_trailer_code=request.POST.get('yt_trailer_code', None),
            language=request.POST.get('language', None),
            mpa_rating=request.POST.get('mpa_rating', None),
            background_image=request.POST.get('background_image', None),
            background_image_original=request.POST.get('background_image_original', None),
            small_cover_image=request.POST.get('small_cover_image', None),
            medium_cover_image=request.POST.get('medium_cover_image', None),
            large_cover_image=request.POST.get('large_cover_image', None),
            state=request.POST.get('state', None),
            date_uploaded=request.POST.get('date_uploaded', None),
            date_uploaded_unix=request.POST.get('date_uploaded_unix', None),
        )

        if request.POST.get('genres', ''):
            genres_list = request.POST.get('genres').split(', ')
            for i in range(0, len(genres_list)):
                genre = Genre.objects.get(name=genres_list[i])
                movie.genres.add(genre)

        if request.POST.get('torrents', ''):
            torrents_list = request.POST.get('torrents').split(', ')
            for j in range(0, len(torrents_list)):
                torrent = Torrent.objects.create(
                    url=torrents_list[j].json().get('url', None),
                    hash=torrents_list[j].json().get('hash', None),
                    quality=torrents_list[j].json().get('quality', None),
                    seeds=torrents_list[j].json().get('seeds', None),
                    peers=torrents_list[j].json().get('peers', None),
                    size=torrents_list[j].json().get('size', None),
                    size_bytes=torrents_list[j].json().get('size_bytes', None),
                    date_uploaded=torrents_list[j].json().get('date_uploaded', None),
                    date_uploaded_unix=torrents_list[j].json().get('date_uploaded_unix', None),
                )
                movie.torrents.add(torrent)

        movies_data = []
        movie_dict = {}
        movie_dict['id'] = movie.pk
        movie_dict['url'] = movie.url
        movie_dict['imdb_code'] = movie.imdb_code
        movie_dict['title'] = movie.title
        movie_dict['title_english'] = movie.title_english
        movie_dict['title_long'] = movie.title_long
        movie_dict['slug'] = movie.slug
        movie_dict['year'] = movie.year
        movie_dict['rating'] = movie.rating
        movie_dict['runtime'] = movie.runtime
        genres_list = []
        for k in movie.genres.all():
            genres_list.append(k.name)
        movie_dict['genres'] = genres_list
        movie_dict['summary'] = movie.summary
        movie_dict['description_full'] = movie.description_full
        movie_dict['synopsis'] = movie.synopsis
        movie_dict['yt_trailer_code'] = movie.yt_trailer_code
        movie_dict['language'] = movie.language
        movie_dict['mpa_rating'] = movie.mpa_rating
        movie_dict['background_image'] = movie.background_image
        movie_dict['background_image_original'] = movie.background_image_original
        movie_dict['small_cover_image'] = movie.small_cover_image
        movie_dict['medium_cover_image'] = movie.medium_cover_image
        movie_dict['large_cover_image'] = movie.large_cover_image
        movie_dict['state'] = movie.state
        torrents_list = []
        for l in movie.torrents.all():
            torrent_detail_dict = {}
            torrent_detail_dict['url'] = l.url
            torrent_detail_dict['hash'] = l.hash
            torrent_detail_dict['quality'] = l.quality
            torrent_detail_dict['seeds'] = l.seeds
            torrent_detail_dict['peers'] = l.peers
            torrent_detail_dict['size'] = l.size
            torrent_detail_dict['size_bytes'] = l.size_bytes
            torrent_detail_dict['date_uploaded'] = l.date_uploaded
            torrent_detail_dict['date_uploaded_unix'] = l.date_uploaded_unix
            torrents_list.append(torrent_detail_dict)
        movie_dict['torrents'] = torrents_list
        movie_dict['date_uploaded'] = movie.date_uploaded
        movie_dict['date_uploaded_unix'] = movie.date_uploaded_unix
        movies_data.append(movie_dict)

        return JsonResponse(movies_data, safe=False, status=status.HTTP_201_CREATED)
