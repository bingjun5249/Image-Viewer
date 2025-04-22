# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps


class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("이미지 뷰어")
        self.root.geometry("800x600")

        # 전체를 grid로 배치
        self.root.rowconfigure(1, weight=1)  # 이미지 프레임이 확장되도록
        self.root.columnconfigure(0, weight=1)

        # 0행: 상단 버튼
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=0, column=0, pady=10)

        self.select_btn = tk.Button(btn_frame, text="디렉토리 선택", command=self.select_directory)
        self.select_btn.pack()

        # 1행: 이미지 표시
        self.image_frame = tk.Frame(root, bg="black")
        self.image_frame.grid(row=1, column=0, sticky="nsew")

        self.image_canvas = tk.Canvas(self.image_frame, bg="white", highlightthickness=0)
        self.image_canvas.pack(expand=True, fill="both")


        # 2행: 내비게이션 버튼
        nav_frame = tk.Frame(root)
        nav_frame.grid(row=2, column=0, pady=5)

        self.prev_btn = tk.Button(nav_frame, text="◀ 이전 이미지", command=self.show_prev_image)
        self.prev_btn.pack(side="left", padx=5)

        self.next_btn = tk.Button(nav_frame, text="다음 이미지 ▶", command=self.show_next_image)
        self.next_btn.pack(side="left", padx=5)

        # 3행: 상태 표시
        self.status_label = tk.Label(root, text="0 / 0", font=("Arial", 12))
        self.status_label.grid(row=3, column=0, pady=5)

        # 내부 상태
        self.image_paths = []
        self.current_index = 0

        self.root.after(100, self.show_thumbnail)  # 썸네일을 보여주기 위한 초기화

        self.config_path = os.path.join(os.path.dirname(__file__), "last_dir.txt")


    def select_directory(self):
    # 마지막 경로 불러오기
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    last_dir = f.read().strip()
                    if not os.path.exists(last_dir):
                        last_dir = os.path.expanduser("~")
            except Exception:
                last_dir = os.path.expanduser("~")
        else:
            last_dir = os.path.expanduser("~")

        folder_selected = filedialog.askdirectory(initialdir=last_dir)
        
        if folder_selected:
            # 디렉토리 기억하기
            try:
                with open(self.config_path, "w", encoding="utf-8") as f:
                    f.write(folder_selected)
            except Exception as e:
                print(f"[경고] 디렉토리 저장 실패: {e}")

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

            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            if frame_width < 10 or frame_height < 10:
                self.root.after(100, lambda: self.show_image(index))
                return
            #img = img.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
            img = ImageOps.contain(img, (frame_width, frame_height), Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)
            self.image_canvas.delete("all")  # 이전 이미지를 삭제
            self.image_canvas.image = img_tk
            self.image_canvas.create_image(frame_width // 2, frame_height // 2, image=img_tk, anchor="center")

            # 상태 업데이트
            self.status_label.config(text=f"{index + 1} / {len(self.image_paths)}")

        except Exception as e:
            messagebox.showerror("에러", f"이미지를 열 수 없습니다: {e}")
        
    def show_thumbnail(self):
        try:
            thumb_path = os.path.join(os.path.dirname(__file__), "picture/thumbnail.jpg")  # 또는 원하는 경로
            img = Image.open(thumb_path)

            # 현재 프레임 크기에 맞게 조절
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            if frame_width < 10 or frame_height < 10:
                self.root.after(100, self.show_thumbnail)
                return

            #img = img.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
            img = ImageOps.contain(img, (frame_width, frame_height), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.image_canvas.delete("all")  # 이전 이미지를 삭제
            self.image_canvas.image = img_tk
            self.image_canvas.create_image(frame_width // 2, frame_height // 2, image=img_tk, anchor="center")

            self.status_label.config(text="0 / 0")

        except Exception as e:
            print(f"[오류] 썸네일을 불러올 수 없습니다: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
