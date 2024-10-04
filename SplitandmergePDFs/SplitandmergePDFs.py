import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class PDFTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Split and merge PDFs")
        self.root.geometry("700x500")

        self.files = []

        # 파일 리스트 박스 생성
        self.file_listbox = tk.Listbox(root, width=80, height=15)
        self.file_listbox.pack(pady=10)

        # 버튼 생성
        self.select_button = tk.Button(root, text="PDF 파일 선택", command=self.select_files)
        self.select_button.pack(pady=10)

        self.merge_button = tk.Button(root, text="PDF 합치기", command=self.merge_pdfs)
        self.merge_button.pack(pady=10)

        self.split_button = tk.Button(root, text="PDF 분할하기", command=self.split_pdf)
        self.split_button.pack(pady=10)

        # 초기화 버튼 추가
        self.clear_button = tk.Button(root, text="선택한 파일 초기화", command=self.clear_files)
        self.clear_button.pack(pady=10)

    def select_files(self):
        # 여러 PDF 파일 선택
        files = filedialog.askopenfilenames(title="PDF 파일 선택", filetypes=[("PDF files", "*.pdf")])
        if files:
            for file in files:
                if file not in self.files:  # 중복 파일 추가 방지
                    self.files.append(file)
                    self.file_listbox.insert(tk.END, file)
            messagebox.showinfo("파일 선택 완료", f"{len(files)} 개의 PDF 파일이 선택되었습니다.")
        else:
            messagebox.showwarning("파일 선택", "파일을 선택하지 않았습니다.")

    def merge_pdfs(self):
        if not self.files:
            messagebox.showwarning("파일 선택", "합칠 PDF 파일을 선택하세요.")
            return

        merger = PdfMerger()
        for pdf in self.files:
            merger.append(pdf)

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if save_path:
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("완료", "PDF 파일이 성공적으로 합쳐졌습니다.")

    def split_pdf(self):
        if not self.files:
            messagebox.showwarning("파일 선택", "분할할 PDF 파일을 선택하세요.")
            return

        pdf_path = filedialog.askopenfilename(title="PDF 파일 선택", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        page_numbers = simpledialog.askstring("페이지 선택", "분할할 페이지 번호를 입력하세요 (예: 1,2,5):")
        if not page_numbers:
            return

        pages_to_split = [int(num.strip()) - 1 for num in page_numbers.split(',') if num.strip().isdigit()]  # 0-indexed

        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in pages_to_split:
            if page < len(reader.pages):
                writer.add_page(reader.pages[page])

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if save_path:
            writer.write(save_path)
            messagebox.showinfo("완료", "선택한 페이지가 성공적으로 분할되었습니다.")

    def clear_files(self):
        """선택한 파일 리스트를 초기화하는 메서드"""
        self.files.clear()
        self.file_listbox.delete(0, tk.END)
        messagebox.showinfo("초기화 완료", "선택한 파일 리스트가 초기화되었습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    pdf_tool = PDFTool(root)
    root.mainloop()
