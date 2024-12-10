import tkinter as tk
from PIL import Image, ImageTk
import win32api
import win32con
import win32gui

class TransparentCanvas:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.5)

        self.image = Image.open('crosshair.png')
        self.image = self.image.resize((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(self.root, width=100, height=100, bg='white', highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(50, 50, image=self.photo)

        self.center_window()

        self.root.bind('<Escape>', self.close)

        self.root.after(1, self.set_layered_attributes)

        self.root.mainloop()

    def set_layered_attributes(self):
        hwnd = win32gui.FindWindow(None, self.root.winfo_name())
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED)

        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 255, 255), 0, win32con.LWA_COLORKEY)

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (100 // 2)
        y = (screen_height // 2) - (100 // 2)

        self.root.geometry(f"+{x}+{y}")

    def close(self, event):
        self.root.destroy()

if __name__ == "__main__":
    TransparentCanvas()