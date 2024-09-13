import tkinter as tk
from tkinter import filedialog
import os
import shutil
import glob

def categorize_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.jpg', '.png', '.jpeg', '.gif']:
        return '이미지'
    elif ext in ['.pptx', '.hwp', '.doc', '.docx', '.pdf']:
        return '문서'
    elif ext in ['.txt']:
        return '메모장'
    elif ext in ['.xlsx']:
        return '엑셀'
    elif ext in ['.mp3', '.wav', '.aac']:
        return '사운드'
    elif ext in ['.mp4', '.mkv', '.avi']:
        return '동영상'
    elif ext in ['.zip']:
        return '압축파일'
    else:
        return '기타'

def move_file_to_folder(file_path, category_folder, dest_dir):
    folder_path = os.path.join(dest_dir, category_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    shutil.move(file_path, folder_path)
    print(f"이동 완료: {file_path} -> {folder_path}")

def organize_files(source_dir, dest_dir):
    if not source_dir or not dest_dir:
        print("작업이 취소되었습니다.")
        return

    all_files = glob.glob(os.path.join(source_dir, '*'))

    for file_path in all_files:
        if os.path.isfile(file_path):
            category = categorize_file(file_path)
            move_file_to_folder(file_path, category, dest_dir)

def select_folder():
    root = tk.Tk()
    root.withdraw()

    source_dir = filedialog.askdirectory(title="탐색 폴더 선택")
    if not source_dir:
        print("탐색 폴더가 선택되지 않았습니다.")
        return None, None

    dest_dir = filedialog.askdirectory(title="저장 폴더 선택")
    if not dest_dir:
        print("저장 폴더가 선택되지 않았습니다.")
        return None, None

    return source_dir, dest_dir

# GUI를 통해 폴더 경로 선택 및 파일 정리 실행
source_dir, dest_dir = select_folder()
organize_files(source_dir, dest_dir)
