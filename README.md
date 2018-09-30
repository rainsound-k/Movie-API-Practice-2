# Movie-API-Practice-2

영화 API를 일반 View로 연습하는 프로젝트입니다.
`.secrets`폴더내의 파일로 비밀 키를 관리합니다.
## Requirements

- Python (3.6.4)
- Django (2.1.1)

## Installation

```
pip install -r requirements.txt
```

## Secrets

**`.secrets/base.json`**


```json
{
  "SECRET_KEY": "<Django settings SECRET_KEY value>",
}
```

## Build

1. app과 동등한 위치에 임의의 Django SECRET_KEY를 이용해 위와 같이 `.secrets/base.json` 를 만듭니다.
2. `pip install -r requirements.txt` 로 요구사항을 설치합니다.
3. app 내부에서 `python manage.py runserver`로 구동 후 이용합니다.

## API

### List

- URI : http://localhost:8000/list/
- Method : GET
- Query Parameters
	- **limit** - pagination 단위(1-50 integer, default=20) `optional`
	- **page** - page 수(integer, default=1) `optional`
	- **quality** - 토렌트 화질(720p, 1080p, 3D) `optional`
	- **minimum_rating** - 최소 평점(0-9 integer) `optional`
	- **query_term** - 영화 제목 검색(string) `optional`
	- **genre** - 영화 장르(string) `optional`
	- **sort_by** - 정렬(title, year, rating, peers, seeds, date_added) `optional`
	- **order_by** - 차순 정렬(desc, asc, dafault=desc) `optional`

### Create

- URI : http://localhost:8000/list/
- Method : POST
- Form Data Parameters
	- **url** - 영화 url(url) `optional`
	- **imdb_code** - imdb 코드(string) `optional`
	- **title** - 영화 제목(string) `required`
	- **title_english** - 영화 영문 제목(string) `optional`
	- **title_long** - 영화 긴제목(string) `optional`
	- **slug** - 영화 슬러그(string) `optional`
	- **year** - 영화 출시년도(integer) `required `
	- **rating** - 영화 평점(float) `required `
	- **runtime** - 영화 상영횟수(integer) `optional`
	- **genres** - 영화 장르(object) `required `
	- **summary** - 영화 요약 내용(string) `required `
	- **description_full** - 영화 전체 설명(string) `optional`
	- **synopsis** - 영화 시놉시스(string) `optional`
	- **yt_trailer_code** - 영화 트레일러 코드(string) `optional`
	- **language** - 영화 언어(string) `optional`
	- **mpa_rating** - 영화 관람 등급(string) `optional`
	- **background_image** - 영화 배경 이미지(url) `optional`
	- **background_image_original** - 영화 배경 이미지 원본(url) `optional`
	- **small_cover_image** - 영화 작은 커버 이미지(url) `optional`
	- **medium_cover_image** - 영화 중간 커버 이미지(url) `optional`
	- **large_cover_image** - 영화 큰 커버 이미지(url) `optional`
	- **state** - 영화 상태(string) `optional`
	- **torrents** - 영화 토렌트(object) `optional`
	- **date_uploaded** - 영화 등록 일자(date) `optional`
	- **date_uploaded_unix** - 영화 등록 unix(integer) `optional`
- 주의 사항 : Postman으로 POST 요청시 genres 데이터는 아래처럼 `,`와 띄어쓰기로 구분하여 요청해야함.

![그림](https://github.com/rainsound-k/Movie-API-Practice-2/blob/master/API2.png)


	

	