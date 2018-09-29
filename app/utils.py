import os

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django

django.setup()
from movies.models import Genre, Torrent, Movie


def get_movie(total_page_num):
    url = 'https://yts.am/api/v2/list_movies.json'
    total_genres_list = [
        'Comedy', 'Drama', 'Short', 'Family', 'Romance', 'Talk-Show', 'Animation', 'Music', 'Fantasy', 'Action',
        'Adventure', 'Sci-Fi', 'Crime', 'Game-Show', 'News', 'Musical', 'Mystery', 'Horror', 'Reality-TV', 'Thriller',
        'Documentary', 'Sport', 'History', 'Western', 'Biography', 'War', 'Adult'
    ]
    for i in range(len(total_genres_list)):
        if not Genre.objects.filter(name=total_genres_list[i]):
            Genre.objects.create(name=total_genres_list[i])

    for page_num in range(1, total_page_num + 1):
        params = {
            'page': page_num,
        }
        response = requests.get(url, params)
        response_dict = response.json()
        movies_list = response_dict['data'].get('movies', None)

        if movies_list:
            for j in range(len(movies_list)):
                movie = Movie.objects.create(
                    url=movies_list[j].get('url', None),
                    imdb_code=movies_list[j].get('imdb_code', None),
                    title=movies_list[j].get('title', None),
                    title_english=movies_list[j].get('title_english', None),
                    title_long=movies_list[j].get('title_long', None),
                    slug=movies_list[j].get('slug', None),
                    year=movies_list[j].get('year', None),
                    rating=movies_list[j].get('rating', None),
                    runtime=movies_list[j].get('runtime', None),
                    summary=movies_list[j].get('summary', None),
                    description_full=movies_list[j].get('description_full', None),
                    synopsis=movies_list[j].get('synopsis', None),
                    yt_trailer_code=movies_list[j].get('yt_trailer_code', None),
                    language=movies_list[j].get('language', None),
                    mpa_rating=movies_list[j].get('mpa_rating', None),
                    background_image=movies_list[j].get('background_image', None),
                    background_image_original=movies_list[j].get('background_image_original', None),
                    small_cover_image=movies_list[j].get('small_cover_image', None),
                    medium_cover_image=movies_list[j].get('medium_cover_image', None),
                    large_cover_image=movies_list[j].get('large_cover_image', None),
                    state=movies_list[j].get('state', None),
                    date_uploaded=movies_list[j].get('date_uploaded', None),
                    date_uploaded_unix=movies_list[j].get('date_uploaded_unix', None),
                )
                genres_list = movies_list[j].get('genres', None)
                if genres_list:
                    for k in range(0, len(genres_list)):
                        if Genre.objects.filter(name=genres_list[k]):
                            genre = Genre.objects.get(name=genres_list[k])
                        else:
                            genre = Genre.objects.create(name=genres_list[k])
                        movie.genres.add(genre)

                torrents_list = movies_list[j].get('torrents', None)
                if torrents_list:
                    for l in range(0, len(torrents_list)):
                        torrent = Torrent.objects.create(
                            url=torrents_list[l].get('url', None),
                            hash=torrents_list[l].get('hash', None),
                            quality=torrents_list[l].get('quality', None),
                            seeds=torrents_list[l].get('seeds', None),
                            peers=torrents_list[l].get('peers', None),
                            size=torrents_list[l].get('size', None),
                            size_bytes=torrents_list[l].get('size_bytes', None),
                            date_uploaded=torrents_list[l].get('date_uploaded', None),
                            date_uploaded_unix=torrents_list[l].get('date_uploaded_unix', None),
                        )
                        movie.torrents.add(torrent)


if __name__ == '__main__':
    num = int(input("저장할 페이지 숫자를 입력해주세요(숫자만 가능합니다): "))
    get_movie(num)
