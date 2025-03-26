import sys
import os
import base64
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QFileDialog, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def derive_key(password: str, salt: bytes) -> bytes:

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

class FileEncryptorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("파일 비밀번호 설정 프로그램")
        self.setGeometry(300, 300, 600, 450)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        title_label = QLabel("파일 비밀번호 설정 프로그램", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        file_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit(self)
        self.file_path_edit.setPlaceholderText("비밀번호 설정 및 해제할 프로그램을 선택하세요.")
        self.file_path_edit.setReadOnly(True)
        file_layout.addWidget(self.file_path_edit)
        
        select_button = QPushButton("파일 선택", self)
        select_button.clicked.connect(self.select_file)
        file_layout.addWidget(select_button)
        layout.addLayout(file_layout)
        
        pw_layout = QHBoxLayout()
        pw_label = QLabel("비밀번호:", self)
        self.password_edit = QLineEdit(self)
        self.password_edit.setPlaceholderText("비밀번호를 입력하세요")
        self.password_edit.setEchoMode(QLineEdit.Password)
        pw_layout.addWidget(pw_label)
        pw_layout.addWidget(self.password_edit)
        layout.addLayout(pw_layout)
        
        btn_layout = QHBoxLayout()
        encrypt_button = QPushButton("설정", self)
        encrypt_button.clicked.connect(self.encrypt_file)
        btn_layout.addWidget(encrypt_button)
        
        decrypt_button = QPushButton("해제", self)
        decrypt_button.clicked.connect(self.decrypt_file)
        btn_layout.addWidget(decrypt_button)
        layout.addLayout(btn_layout)
        
        central_widget.setLayout(layout)
    
    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", "All Files (*)", options=options)
        if file_name:
            self.file_path_edit.setText(file_name)
    
    def encrypt_file(self):
        file_path = self.file_path_edit.text().strip()
        password = self.password_edit.text().strip()
        if not file_path:
            QMessageBox.warning(self, "경고", "비밀번호를 설정할 파일을 선택하세요.")
            return
        if not password:
            QMessageBox.warning(self, "경고", "비밀번호를 입력하세요.")
            return
        try:
            with open(file_path, "rb") as f:
                data = f.read()

            salt = os.urandom(16)
            key = derive_key(password, salt)
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data)

            encrypted_file_path = file_path + ".enc"
            with open(encrypted_file_path, "wb") as f:
                f.write(salt + encrypted_data)
            QMessageBox.information(self, "완료", f"비밀번호 설정 완료: {encrypted_file_path}")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"비밀번호 해제 실패: {str(e)}")
    
    def decrypt_file(self):
        file_path = self.file_path_edit.text().strip()
        password = self.password_edit.text().strip()
        if not file_path:
            QMessageBox.warning(self, "경고", "비밀번호를 설정 파일 선택")
            return
        if not password:
            QMessageBox.warning(self, "경고", "비밀번호를 입력")
            return
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
            salt = file_data[:16]
            encrypted_data = file_data[16:]
            key = derive_key(password, salt)
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            if file_path.endswith(".enc"):
                output_path = file_path[:-4]
            else:
                output_path = file_path + ".dec"
            with open(output_path, "wb") as f:
                f.write(decrypted_data)
            QMessageBox.information(self, "완료", f"비밀번호 설정 완료: {output_path}")
        except InvalidToken:
            QMessageBox.critical(self, "오류", "잘못된 비밀번호입니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"비밀번호 설정 실패: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileEncryptorWindow()
    window.show()
    sys.exit(app.exec_())
