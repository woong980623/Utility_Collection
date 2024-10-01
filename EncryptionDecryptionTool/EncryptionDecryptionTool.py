import os
import base64
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes  # 해시 알고리즘을 사용하기 위해 추가
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# 비밀번호를 바탕으로 키 생성
def generate_key_from_password(password):
    password = password.encode()  # 비밀번호를 바이트로 변환
    salt = b'some_salt'  # 고정된 salt 사용 (보안을 위해 더 복잡하게 설정 가능)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # 해시 알고리즘 지정
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

# 파일 암호화
def encrypt_file(file_path, password):
    try:
        key = generate_key_from_password(password)
        fernet = Fernet(key)

        with open(file_path, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open(file_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        messagebox.showinfo("암호화 완료", "파일이 성공적으로 암호화되었습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"암호화 중 오류가 발생했습니다: {str(e)}")

# 파일 복호화
def decrypt_file(file_path, password):
    try:
        key = generate_key_from_password(password)
        fernet = Fernet(key)

        with open(file_path, "rb") as encrypted_file:
            encrypted = encrypted_file.read()

        decrypted = fernet.decrypt(encrypted)

        with open(file_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted)

        messagebox.showinfo("복호화 완료", "파일이 성공적으로 복호화되었습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"복호화 중 오류가 발생했습니다: {str(e)}")

# 파일 선택 다이얼로그
def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

# 암호화 버튼 클릭 이벤트
def encrypt_button_click():
    file_path = entry_file_path.get()
    password = entry_password.get()
    if os.path.exists(file_path) and password:
        encrypt_file(file_path, password)
    else:
        messagebox.showerror("오류", "올바른 파일 경로와 비밀번호를 입력하세요.")

# 복호화 버튼 클릭 이벤트
def decrypt_button_click():
    file_path = entry_file_path.get()
    password = entry_password.get()
    if os.path.exists(file_path) and password:
        decrypt_file(file_path, password)
    else:
        messagebox.showerror("오류", "올바른 파일 경로와 비밀번호를 입력하세요.")

# Tkinter GUI 설정
root = tk.Tk()
root.title("Encryption Decryption Tool")
root.geometry("400x300")

# 파일 경로 입력 필드 및 버튼
label_file_path = tk.Label(root, text="파일 경로:")
label_file_path.pack(pady=5)

entry_file_path = tk.Entry(root, width=50)
entry_file_path.pack(pady=5)

button_browse = tk.Button(root, text="파일 선택", command=select_file)
button_browse.pack(pady=5)

# 비밀번호 입력 필드
label_password = tk.Label(root, text="비밀번호:")
label_password.pack(pady=5)

entry_password = tk.Entry(root, width=50, show="*")
entry_password.pack(pady=5)

# 암호화/복호화 버튼
button_encrypt = tk.Button(root, text="파일 암호화", command=encrypt_button_click)
button_encrypt.pack(pady=10)

button_decrypt = tk.Button(root, text="파일 복호화", command=decrypt_button_click)
button_decrypt.pack(pady=10)

root.mainloop()
