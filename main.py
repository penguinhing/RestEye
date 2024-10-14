import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import time, threading, random, pygame

class RestEye:
    def __init__(self, image_path, rest_time=600, work_time=2400):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.attributes('-topmost', True) 
        self.root.overrideredirect(True)  

        self.image_path = image_path
        self.rest_time = rest_time
        self.work_time = work_time

        self.load_image()
        self.create_close_button()
        self.create_timer_label()
        self.init_sound()

        self.is_visible = False
        self.next_change_time = time.time() + work_time

    def load_image(self):
        image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack()

    def create_close_button(self):
        self.close_button = tk.Button(self.root, text="닫기", command=self.ask_math_question)
        self.close_button.pack(pady=5)

    def create_timer_label(self):
        self.timer_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.timer_label.pack(pady=5)

    def init_sound(self):
        pygame.mixer.init()
        self.show_sound = pygame.mixer.Sound("snd.wav")
        self.hide_sound = pygame.mixer.Sound("snd.wav")

    def show_image(self):
        if not self.is_visible:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = self.photo.width()
            window_height = self.photo.height() + 100
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
            self.root.deiconify()
            self.show_sound.play()
            self.is_visible = True
            self.next_change_time = time.time() + self.rest_time
            self.update_timer()

    def hide_image(self):
        if self.is_visible:
            self.root.withdraw()
            self.hide_sound.play()
            self.is_visible = False
            self.next_change_time = time.time() + self.work_time

    def update_timer(self):
        if self.is_visible:
            remaining_time = int(self.next_change_time - time.time())
            if remaining_time > 0:
                minutes, seconds = divmod(remaining_time, 60)
                self.timer_label.config(text=f"남은 휴식 시간: {minutes:02d}:{seconds:02d}")
                self.root.after(1000, self.update_timer)
            else:
                self.hide_image()

    def ask_math_question(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        answer = a + b
        user_answer = simpledialog.askinteger("수학 문제", f"{a} + {b} = ?", parent=self.root)
        if user_answer == answer:
            self.hide_image()
        else:
            messagebox.showinfo("오답", "정답이 아닙니다. 이미지가 계속 표시됩니다.", parent=self.root)

    def run(self):
        while True:
            current_time = time.time()
            if current_time >= self.next_change_time:
                if self.is_visible:
                    self.root.after(0, self.hide_image)
                else:
                    self.root.after(0, self.show_image)
            time.sleep(1) 

    def start(self):
        self.timer_thread = threading.Thread(target=self.run)
        self.timer_thread.daemon = True
        self.timer_thread.start()
        self.root.mainloop()

if __name__ == "__main__":
    image_path = "display.png" 
    app = RestEye(image_path, rest_time=600, work_time=2400) # 원하는 시간 알아서 설정 (초 단위)
    app.start()