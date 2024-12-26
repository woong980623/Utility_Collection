import requests
import pandas as pd
from config import API_KEY, BASE_URL

def search_movie(query):
    """
    TMDB API에서 특정 영화 제목으로 검색 (한글 지원).
    """
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&language=ko-KR&query={query}&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        movies = data.get('results', [])
        if movies:
            df = pd.DataFrame(movies)
            df = df[['id', 'title', 'genre_ids', 'poster_path']]  # 필요한 컬럼만 선택
            df['genres'] = df['genre_ids'].apply(lambda x: '|'.join(map(str, x)))
            return df[['id', 'title', 'genres', 'poster_path']]
        else:
            return pd.DataFrame(columns=['id', 'title', 'genres', 'poster_path'])
    else:
        raise Exception(f"API 요청 실패: {response.status_code}")
