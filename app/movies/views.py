from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Movie


def movie_list_create(request):
    if request.method == 'GET':
        queryset = Movie.objects.all()
        quality = request.GET.get('quality', '')
        try:
            minimum_rating = int(request.GET.get('minimum_rating', 0))
            if minimum_rating > 9:
                error = {
                    'status': 'error',
                    'status_message': 'minimum_rating 은 0 이상 9 이하의 정수만 가능합니다.',
                }
                return JsonResponse(error)
        except ValueError:
            error = {
                'status': 'error',
                'status_message': 'minimum_rating 은 0 이상 9 이하의 정수만 가능합니다.',
            }
            return JsonResponse(error)
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
                return JsonResponse(error)
        except ValueError:
            error = {
                'status': 'error',
                'status_message': 'limit 은 1 이상 50 이하의 정수만 가능합니다.',
            }
            return JsonResponse(error)

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

    elif request.method == 'POST':
        return
