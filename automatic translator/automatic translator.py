import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
)
from PyQt5.QtCore import QTimer
from googletrans import Translator

class ClipboardTranslatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("자동 번역기")
        self.setGeometry(300, 300, 800, 400)
        
        # Translator 객체 생성 및 마지막 클립보드 텍스트 저장 변수
        self.translator = Translator()
        self.last_text = ""
        
        # 언어 선택 콤보박스 생성
        self.source_combo = QComboBox(self)
        self.dest_combo = QComboBox(self)
        
        # 지원 언어 옵션 (표시 이름: 언어 코드)
        self.language_mapping = {
            "한국어": "ko",
            "영어": "en",
            "일본어": "ja",
            "중국어": "zh-cn",
            "독일어": "de",
            "스페인어": "es",
            "프랑스어": "fr"
        }
        for lang in self.language_mapping.keys():
            self.source_combo.addItem(lang)
            self.dest_combo.addItem(lang)
        # 기본 선택: 원문은 한국어, 번역 대상은 영어
        self.source_combo.setCurrentText("한국어")
        self.dest_combo.setCurrentText("영어")
        
        # 언어 선택 레이아웃 (상단)
        language_layout = QHBoxLayout()
        language_layout.addWidget(QLabel("원문:"))
        language_layout.addWidget(self.source_combo)
        language_layout.addSpacing(20)
        language_layout.addWidget(QLabel("번역:"))
        language_layout.addWidget(self.dest_combo)
        
        # 좌측 컬럼: 원문 및 번역 결과, 복사 버튼
        self.original_label = QLabel("원본 텍스트가 여기에 표시됩니다.", self)
        self.original_label.setWordWrap(True)
        self.original_label.setStyleSheet("font-size: 16px; color: blue;")
        self.original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.translated_label = QLabel("번역 결과가 여기에 표시됩니다.", self)
        self.translated_label.setWordWrap(True)
        self.translated_label.setStyleSheet("font-size: 16px; color: green;")
        self.translated_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.copy_button = QPushButton("번역 결과 복사", self)
        self.copy_button.clicked.connect(self.copy_translation)
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.original_label)
        left_layout.addWidget(self.translated_label)
        left_layout.addWidget(self.copy_button)
        
        # 우측 컬럼: 번역 기록 영역과 기록 초기화 버튼
        self.history_text = QTextEdit(self)
        self.history_text.setReadOnly(True)
        # 자동 줄바꿈은 QTextEdit 기본 기능 (단, 폭 제한을 위해 고정폭 설정)
        self.history_text.setFixedWidth(250)
        
        self.clear_button = QPushButton("기록 초기화", self)
        self.clear_button.clicked.connect(self.clear_history)
        
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("번역 기록", self))
        right_layout.addWidget(self.history_text)
        right_layout.addWidget(self.clear_button)
        
        # 두 컬럼을 포함하는 수평 레이아웃 (왼쪽: 넓게, 오른쪽: 좁게)
        content_layout = QHBoxLayout()
        content_layout.addLayout(left_layout, 3)
        content_layout.addLayout(right_layout, 1)
        
        # 전체 메인 레이아웃 구성
        main_layout = QVBoxLayout()
        main_layout.addLayout(language_layout)
        main_layout.addLayout(content_layout)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # QTimer를 이용해 1초마다 클립보드를 체크
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(1000)
    
    def check_clipboard(self):
        clipboard_text = QApplication.clipboard().text()
        if clipboard_text and clipboard_text != self.last_text:
            self.last_text = clipboard_text
            self.original_label.setText("원본: " + clipboard_text)
            self.translate_text(clipboard_text)
    
    def translate_text(self, text):
        src_lang = self.language_mapping[self.source_combo.currentText()]
        dest_lang = self.language_mapping[self.dest_combo.currentText()]
        try:
            result = self.translator.translate(text, src=src_lang, dest=dest_lang)
            translated_text = result.text
            self.translated_label.setText("번역: " + translated_text)
            # 번역 기록에 새 항목 추가 (원본 및 번역 결과)
            record = f"원본: {text}\n번역: {translated_text}\n{'-'*40}\n"
            current_history = self.history_text.toPlainText()
            self.history_text.setPlainText(current_history + record)
        except Exception as e:
            self.translated_label.setText("번역 오류 발생: " + str(e))
    
    def copy_translation(self):
        translated = self.translated_label.text().replace("번역: ", "")
        QApplication.clipboard().setText(translated)
    
    def clear_history(self):
        self.history_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClipboardTranslatorWindow()
    window.show()
    sys.exit(app.exec_())
