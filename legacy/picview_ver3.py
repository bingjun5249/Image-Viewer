# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("이미지 뷰어")
        self.root.geometry("800x600")

        # 상단 버튼 프레임
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.select_btn = tk.Button(btn_frame, text="디렉토리 선택", command=self.select_directory)
        self.select_btn.pack(side="left", padx=5)

        # 이미지 표시 프레임
        self.image_frame = tk.Frame(root, height=500)
        self.image_frame.pack(expand=False, fill="x")
        self.image_frame.pack_propagate(False)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(expand=True)

        # 하단 버튼 프레임
        nav_frame = tk.Frame(root)
        nav_frame.pack(pady=5)

        self.prev_btn = tk.Button(nav_frame, text="◀ 이전 이미지", command=self.show_prev_image)
        self.prev_btn.pack(side="left", padx=5)

        self.next_btn = tk.Button(nav_frame, text="다음 이미지 ▶", command=self.show_next_image)
        self.next_btn.pack(side="left", padx=5)

        # 상태 표시 라벨
        self.status_label = tk.Label(root, text="0 / 0", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # 내부 상태
        self.image_paths = []
        self.current_index = 0

    def select_directory(self):
        folder_selected = filedialog.askdirectory(initialdir=os.path.expanduser("~"))
        if folder_selected:
            self.image_paths = [
                os.path.join(folder_selected, f)
                for f in os.listdir(folder_selected)
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))
            ]
            self.image_paths.sort()
            self.current_index = 0
            if self.image_paths:
                self.show_image(self.current_index)
            else:
                self.status_label.config(text="0 / 0")
                messagebox.showinfo("알림", "이미지가 없습니다.")


    def show_next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.show_image(self.current_index)

    def show_prev_image(self):
       if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.show_image(self.current_index)


    def show_image(self, index):
        try:
            img = Image.open(self.image_paths[index])
            img = img.resize((800, 500), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk

            # 상태 업데이트
            self.status_label.config(text=f"{index + 1} / {len(self.image_paths)}")

        except Exception as e:
            messagebox.showerror("에러", f"이미지를 열 수 없습니다: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
