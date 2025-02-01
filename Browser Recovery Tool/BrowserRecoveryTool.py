import json
import os
import time
import webbrowser
import tkinter as tk
from tkinter import messagebox, simpledialog

# ===========================
# 1. JSON 파일에서 URL 불러오기
# ===========================
def load_urls(filename="urls.json"):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r") as file:
            urls = json.load(file)
        return urls if isinstance(urls, list) else []
    except json.JSONDecodeError:
        return []

# ===========================
# 2. JSON 파일에 URL 저장
# ===========================
def save_urls(urls, filename="urls.json"):
    with open(filename, "w") as file:
        json.dump(urls, file, indent=4)

# ===========================
# 3. URL 추가 기능
# ===========================
def add_url():
    new_url = simpledialog.askstring("URL 추가", "새로운 URL을 입력하세요:")
    if new_url:
        urls.append(new_url)
        save_urls(urls)
        update_listbox()

# ===========================
# 4. URL 삭제 기능
# ===========================
def delete_url():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("경고", "삭제할 URL을 선택하세요.")
        return

    for index in reversed(selected):
        urls.pop(index)
    save_urls(urls)
    update_listbox()

# ===========================
# 5. URL 실행 기능
# ===========================
def open_urls():
    if not urls:
        messagebox.showwarning("경고", "저장된 URL이 없습니다.")
        return

    messagebox.showinfo("실행 중", "저장된 URL을 브라우저에서 엽니다.")
    for url in urls:
        webbrowser.open_new_tab(url)
        time.sleep(1)  # 너무 빠르게 열리지 않도록 딜레이 추가

# ===========================
# 6. UI 업데이트 (목록 갱신)
# ===========================
def update_listbox():
    listbox.delete(0, tk.END)
    for url in urls:
        listbox.insert(tk.END, url)

# ===========================
# 7. GUI 생성 (tkinter)
# ===========================
app = tk.Tk()
app.title("브라우저 실행 도구")
app.geometry("700x300")

# URL 목록 리스트박스
listbox = tk.Listbox(app, selectmode=tk.MULTIPLE)
listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# 버튼 프레임
btn_frame = tk.Frame(app)
btn_frame.pack(pady=5)

btn_add = tk.Button(btn_frame, text="URL 추가", command=add_url)
btn_add.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(btn_frame, text="URL 삭제", command=delete_url)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_open = tk.Button(app, text="URL 열기", command=open_urls)
btn_open.pack(pady=10)

# 초기 URL 불러오기
urls = load_urls()
update_listbox()

# GUI 실행
app.mainloop()
