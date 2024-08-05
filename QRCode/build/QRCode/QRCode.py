import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk

def generate_qr():
    url = entry.get()
    if not url:
        messagebox.showerror("Error", "URL을 입력하세요!")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img = img.resize((200, 200), Image.LANCZOS)  # 수정된 부분
    img_tk = ImageTk.PhotoImage(img)

    qr_label.config(image=img_tk)
    qr_label.image = img_tk

# Tkinter 창 생성
root = tk.Tk()
root.title("QR 코드 생성기")

# URL 입력 창
tk.Label(root, text="URL 입력:").pack(pady=10)
entry = tk.Entry(root, width=40)
entry.pack(pady=10)

# QR 코드 생성 버튼
generate_button = tk.Button(root, text="QR 코드 생성", command=generate_qr)
generate_button.pack(pady=20)

# QR 코드 표시 레이블
qr_label = tk.Label(root)
qr_label.pack(pady=10)

root.mainloop()
