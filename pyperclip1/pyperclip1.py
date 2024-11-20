import os
import time
import pyperclip
import threading
from tkinter import Tk, Text, Scrollbar, Button, END, Toplevel
from infi.systray import SysTrayIcon

# 클립보드 내용을 지속적으로 기록하기 위한 클래스
class ClipboardLogger:
    def __init__(self):
        self.log_file = "clipboard_log.txt"
        self.last_content = ""
        self.running = True
        self.start_logging()

    def start_logging(self):
        # 백그라운드에서 클립보드 내용을 기록하는 쓰레드 시작
        self.logging_thread = threading.Thread(target=self.log_clipboard)
        self.logging_thread.daemon = True
        self.logging_thread.start()

    def log_clipboard(self):
        while self.running:
            try:
                content = pyperclip.paste()  # pyperclip.paste() 사용
                if content != self.last_content and content.strip() != "":
                    self.last_content = content
                    with open(self.log_file, "a", encoding="utf-8") as file:
                        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {content}\n")
            except pyperclip.PyperclipException:
                pass  # 클립보드 접근 오류 발생 시 무시하고 계속 진행
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(1)

    def stop_logging(self):
        self.running = False
        self.logging_thread.join()

# 기록된 클립보드 내용을 보기 위한 GUI
class ClipboardViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pyperclip")
        self.master.geometry("900x400")
        self.text_widget = Text(self.master, wrap="word")
        self.scrollbar = Scrollbar(self.master, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.text_widget.pack(side="left", fill="both", expand=True)
        self.load_log()
        self.update_button = Button(self.master, text="새로고침", command=self.load_log)
        self.update_button.pack()
        self.delete_button = Button(self.master, text="삭제", command=self.delete_log)
        self.delete_button.pack()

    def load_log(self):
        # 기록된 내용을 로드하여 텍스트 위젯에 표시
        if os.path.exists("clipboard_log.txt"):
            with open("clipboard_log.txt", "r", encoding="utf-8") as file:
                content = file.read()
                self.text_widget.delete(1.0, END)
                self.text_widget.insert(END, content)

    def delete_log(self):
        # 로그 파일을 삭제하고 텍스트 위젯 내용도 지우기
        if os.path.exists("clipboard_log.txt"):
            os.remove("clipboard_log.txt")
        self.text_widget.delete(1.0, END)

# 시스템 트레이 아이콘 설정 및 애플리케이션 제어
class ClipboardTrayApp:
    def __init__(self):
        self.logger = ClipboardLogger()
        self.create_systray()

    def create_systray(self):
        menu_options = (('View Log', None, self.open_viewer), )
        self.systray = SysTrayIcon(None, "Clipboard Logger", menu_options)
        self.systray.start()

    def open_viewer(self, systray):
        # 기록된 내용을 볼 수 있는 GUI 창 열기
        root = Toplevel(); ClipboardViewer(root); root.mainloop()

    

if __name__ == "__main__":
    app = ClipboardTrayApp()
