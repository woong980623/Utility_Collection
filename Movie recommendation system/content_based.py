from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_title(title):
    """
    영화 제목을 소문자 변환 및 공백 제거로 전처리.

    Parameters:
        title (str): 원본 영화 제목.

    Returns:
        str: 전처리된 영화 제목.
    """
    return title.strip().lower()

def recommend_movies(movie_title, movies):
    """
    입력 영화 제목을 기반으로 비슷한 영화를 추천.

    Parameters:
        movie_title (str): 추천 기준 영화 제목.
        movies (DataFrame): 영화 데이터프레임.

    Returns:
        list: 추천 영화 제목 목록.
    """
    # 전처리된 영화 제목 추가
    movies['processed_title'] = movies['title'].apply(preprocess_title)
    processed_movie_title = preprocess_title(movie_title)

    try:
        # 입력 영화의 인덱스 찾기
        idx = movies[movies['processed_title'] == processed_movie_title].index[0]
    except IndexError:
        return ["해당 영화가 데이터에 없습니다."]

    # 장르 데이터를 벡터화
    count_vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'))
    genre_matrix = count_vectorizer.fit_transform(movies['genres'])

    # 코사인 유사도 계산
    cosine_sim = cosine_similarity(genre_matrix, genre_matrix)

    # 유사한 영화 상위 10개 추출
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    movie_indices = [i[0] for i in sim_scores[1:11]]  # 자기 자신 제외

    # 추천 영화 목록 반환
    return movies.iloc[movie_indices]['title'].tolist()
