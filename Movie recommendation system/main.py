import tkinter as tk
from tkinter import messagebox
from data_loader import search_movie
from content_based import recommend_movies
import requests
from PIL import Image, ImageTk

def get_recommendations():
    """
    사용자가 입력한 영화 제목으로 추천 목록을 생성.
    """
    query = entry.get().strip()
    if not query:
        messagebox.showerror("입력 오류", "영화 제목을 입력하세요.")
        return

    try:
        # TMDB API로 영화 검색
        movies = search_movie(query)
        if movies.empty:
            messagebox.showinfo("검색 결과", "해당 영화가 데이터에 없습니다.")
            return

        # 추천 로직 실행
        recommendations = recommend_movies(query, movies)

        # 결과 표시
        display_recommendations(movies, recommendations)
    except Exception as e:
        messagebox.showerror("오류", str(e))

def display_recommendations(movies, recommendations):
    """
    추천 결과를 화면에 표시하고 URL 및 이미지를 추가.
    """
    # 이전 결과 제거
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # 이미지 참조를 유지할 리스트
    canvas_frame.image_list = []

    for i, title in enumerate(recommendations, 1):
        # 영화 데이터에서 해당 제목 찾기
        movie_data = movies[movies['title'] == title].iloc[0]

        # URL 및 이미지 가져오기
        movie_url = f"https://www.themoviedb.org/movie/{movie_data['id']}"  # TMDB 영화 페이지 URL
        poster_path = movie_data.get('poster_path', None)
        poster_photo = None

        if poster_path:
            try:
                poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}"  # TMDB 이미지 URL
                poster_image = Image.open(requests.get(poster_url, stream=True).raw)
                poster_image = poster_image.resize((100, 150))  # 이미지 크기 조정
                poster_photo = ImageTk.PhotoImage(poster_image)
                canvas_frame.image_list.append(poster_photo)  # 이미지 참조 유지
            except Exception as e:
                print(f"이미지 로드 실패: {e}")

        # 이미지 표시
        if poster_photo:
            tk.Label(canvas_frame, image=poster_photo).grid(row=i, column=0, padx=10, pady=10)

        # 제목 및 링크 표시
        tk.Label(canvas_frame, text=f"{i}. {title}", font=("Arial", 12)).grid(row=i, column=1, sticky="w")
        link = tk.Label(canvas_frame, text="영화 정보 보기", font=("Arial", 10), fg="blue", cursor="hand2")
        link.grid(row=i, column=2, padx=10, sticky="w")
        link.bind("<Button-1>", lambda e, url=movie_url: open_url(url))

    # 스크롤 크기 조정
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def open_url(url):
    """
    시스템의 기본 브라우저에서 URL을 엽니다.
    """
    import webbrowser
    webbrowser.open(url)

# GUI 초기화
root = tk.Tk()
root.title("영화 추천 시스템")
root.geometry("800x600")  # 창 크기 설정

# 입력 필드
tk.Label(root, text="추천받고 싶은 영화 제목을 입력하세요:", font=("Arial", 14)).pack(pady=10)
entry = tk.Entry(root, width=50, font=("Arial", 12))
entry.pack(pady=5)

# 추천 버튼
tk.Button(root, text="추천받기", command=get_recommendations, font=("Arial", 12)).pack(pady=10)

# 스크롤바 및 캔버스 초기화
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

canvas = tk.Canvas(frame)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

canvas_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

# GUI 실행
root.mainloop()
