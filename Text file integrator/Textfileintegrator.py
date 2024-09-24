import glob
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# 텍스트 파일을 통합하는 함수
def merge_files(folder_path):
    if not folder_path:
        messagebox.showerror("Error", "폴더를 선택해주세요.")
        return

    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    if not txt_files:
        messagebox.showerror("Error", "폴더에 텍스트 파일이 없습니다.")
        return

    output_file = os.path.join(folder_path, '텍스트파일 통합본.txt')

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for txt_file in txt_files:
            outfile.write(f"\n--- {os.path.basename(txt_file)} ---\n")
            try:
                # utf-8 인코딩 시도
                with open(txt_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            except UnicodeDecodeError:
                # utf-8 실패 시 cp949 인코딩으로 재시도
                with open(txt_file, 'r', encoding='cp949') as infile:
                    outfile.write(infile.read())

    messagebox.showinfo("완료", "파일 통합이 완료되었습니다.")

# 폴더 선택 창
def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

# tkinter로 GUI 설정
root = tk.Tk()
root.title("텍스트 파일 통합 프로그램")

# 폴더 경로를 저장할 변수
folder_path = tk.StringVar()

# 폴더 선택 버튼
tk.Label(root, text="폴더 선택:").pack(pady=5)
tk.Entry(root, textvariable=folder_path, width=40).pack(pady=5)
tk.Button(root, text="폴더 선택", command=select_folder).pack(pady=5)

# 통합 시작 버튼
tk.Button(root, text="통합 시작", command=lambda: merge_files(folder_path.get())).pack(pady=20)

# GUI 실행
root.mainloop()
