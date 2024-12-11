import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES

# Translator 객체 생성
translator = Translator()

def translate_text():
    source_text = source_text_box.get("1.0", tk.END).strip()
    source_lang = source_lang_combo.get()
    target_lang = target_lang_combo.get()
    
    if not source_text:
        messagebox.showwarning("입력 경고", "번역할 텍스트를 입력하세요.")
        return
    
    try:
        # 번역 실행
        translated = translator.translate(
            text=source_text, 
            src=source_lang, 
            dest=target_lang
        )
        result_text_box.delete("1.0", tk.END)
        result_text_box.insert(tk.END, translated.text)
    except Exception as e:
        messagebox.showerror("오류", f"번역 중 오류 발생: {e}")

# GUI 구성
root = tk.Tk()
root.title("다국어 번역기")
root.geometry("600x400")

# 언어 리스트 가져오기
lang_list = list(LANGUAGES.values())
lang_codes = list(LANGUAGES.keys())

# 입력 언어 선택
tk.Label(root, text="입력 언어").grid(row=0, column=0, padx=10, pady=10)
source_lang_combo = ttk.Combobox(root, values=lang_list, state="readonly", width=30)
source_lang_combo.grid(row=0, column=1, padx=10, pady=10)
source_lang_combo.set("English")  # 기본값 설정

# 출력 언어 선택
tk.Label(root, text="출력 언어").grid(row=1, column=0, padx=10, pady=10)
target_lang_combo = ttk.Combobox(root, values=lang_list, state="readonly", width=30)
target_lang_combo.grid(row=1, column=1, padx=10, pady=10)
target_lang_combo.set("Korean")  # 기본값 설정

# 입력 텍스트 상자
tk.Label(root, text="번역할 텍스트").grid(row=2, column=0, padx=10, pady=10)
source_text_box = tk.Text(root, height=8, width=50)
source_text_box.grid(row=2, column=1, padx=10, pady=10)

# 번역 결과 상자
tk.Label(root, text="번역 결과").grid(row=3, column=0, padx=10, pady=10)
result_text_box = tk.Text(root, height=8, width=50)
result_text_box.grid(row=3, column=1, padx=10, pady=10)

# 번역 버튼
translate_button = tk.Button(root, text="번역", command=translate_text)
translate_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
