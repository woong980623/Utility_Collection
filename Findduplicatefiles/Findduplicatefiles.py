import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
import send2trash

# 해시 값을 생성하는 함수 (중복 파일 검출용)
def hash_file(path, block_size=65536):
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

# 중복 파일 찾기 함수
def find_duplicates(directory):
    hashes = {}
    duplicates = {}

    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            file_hash = hash_file(file_path)

            # 해시 값이 동일한 파일들을 그룹화
            if file_hash in hashes:
                if file_hash not in duplicates:
                    duplicates[file_hash] = [hashes[file_hash]]
                duplicates[file_hash].append(file_path)
            else:
                hashes[file_hash] = file_path
    
    return duplicates

# 경로에서 \\?\ 접두사 제거 및 절대 경로 처리
def clean_path(path):
    # 경로에서 \\?\ 제거
    if path.startswith('\\\\?\\'):
        path = path[4:]
    return os.path.abspath(path)  # 절대 경로로 변환

# 선택한 중복 파일을 삭제하는 함수
def delete_selected_files():
    global duplicate_files
    selected_files = []
    for var, file in duplicate_files:
        if var.get():
            cleaned_path = clean_path(file)  # 경로 정리 후 사용
            selected_files.append(cleaned_path)
    
    if selected_files:
        for file in selected_files:
            try:
                send2trash.send2trash(file)
                print(f"휴지통으로 이동: {file}")
            except Exception as e:
                print(f"에러 발생: {e}")
        
        messagebox.showinfo("완료", "선택한 파일이 휴지통으로 이동되었습니다.")
    else:
        messagebox.showwarning("경고", "삭제할 파일을 선택하세요.")

# 중복 파일을 GUI에 표시하는 함수
def show_duplicate_files(duplicates):
    global duplicate_files
    for widget in checkboxes_frame.winfo_children():
        widget.destroy()

    duplicate_files = []
    for files_group in duplicates.values():
        for file in files_group:
            var = tk.BooleanVar()
            cleaned_path = clean_path(file)  # 경로에서 \\?\를 제거한 후 표시
            chk = tk.Checkbutton(checkboxes_frame, text=cleaned_path, variable=var)
            chk.pack(anchor='w')
            duplicate_files.append((var, cleaned_path))
        
        separator = tk.Label(checkboxes_frame, text="ㅡ")  # 그룹 구분선 추가
        separator.pack()

# 폴더를 선택하고 중복 파일을 검색하는 함수
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        duplicates = find_duplicates(directory)
        if duplicates:
            show_duplicate_files(duplicates)
        else:
            messagebox.showinfo("정보", "중복 파일이 없습니다.")

# GUI 설정
root = tk.Tk()
root.title("중복 파일 찾기")
root.geometry("700x500")  # 창 크기 설정

# 폴더 선택 버튼
select_button = tk.Button(root, text="폴더 선택", command=select_directory)
select_button.pack(pady=10)

# 중복 파일 체크박스를 담을 프레임
checkboxes_frame = tk.Frame(root)
checkboxes_frame.pack(fill=tk.BOTH, expand=True)

# 선택된 파일 삭제 버튼
delete_button = tk.Button(root, text="선택한 파일 삭제", command=delete_selected_files)
delete_button.pack(pady=10)

# GUI 실행
root.mainloop()
