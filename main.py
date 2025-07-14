import time
import re
import threading
import pytesseract
from pypresence import Presence
from tkinter import *
from tkinter import ttk
from PIL import ImageGrab, Image, ImageTk
from dotenv import load_dotenv
import os
import win32gui
import os


load_dotenv()  # Membaca file .env
ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "clip-studio-paint-logo.png")
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Discord Rich Presence
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CSP_TYPE = None
discord_start_time = None
rpc = Presence(CLIENT_ID)
rpc.connect()

def update_discord_presence(project_name, duration):
    global discord_start_time
    if project_name:
        if discord_start_time is None:
            discord_start_time = int(time.time()) - duration  # offset dari durasi

        rpc.update(
            details=f"Working on",
            state=f"{project_name}",
            large_image="clip_studio_paint",
            large_text=CSP_TYPE if CSP_TYPE else "CLIP STUDIO PAINT",
            start=discord_start_time
        )
    else:
        rpc.clear()
        discord_start_time = None


def on_closing():
    rpc.clear()
    root.destroy()

def is_csp_active_window():
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    return "CLIP STUDIO PAINT" in title

def get_clip_studio_window_title():
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "CLIP STUDIO PAINT" in title:
                titles.append(title)
    titles = []
    win32gui.EnumWindows(callback, None)
    return titles[0] if titles else None

def detect_project_name_window():
    title = get_clip_studio_window_title()
    if title:
        cleaned = title.split(" - ")[0].strip()
        match = re.match(r"(.+?) \(", cleaned)
        name = match.group(1).strip() if match else cleaned
        return name
    return None

def detect_project_name_ocr():
    image = ImageGrab.grab(bbox=(500, 0, 1300, 40))
    text = pytesseract.image_to_string(image)
    print("Hasil OCR:", repr(text))

    if " - CLIP STUDIO PAINT EX" in text:
        name = text.split(" - CLIP STUDIO PAINT EX")[0]
        CSP_TYPE = "CLIP STUDIO PAINT EX"
    elif " - CLIP STUDIO PAINT" in text:
        name = text.split(" - CLIP STUDIO PAINT")[0]
        CSP_TYPE = "CLIP STUDIO PAINT"
    else:
        name = get_clip_studio_window_title()
        CSP_TYPE = name.upper() 

    # Setelah hasil OCR diambil:
    name = re.sub(r'(\d)\s*[x×]\s*(\d)', r'\1 x \2', name)
    name = re.sub(r"[^\w\s().%x×dpi\-]", "", name).strip()

    return name

class CSPTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Clip Studio Paint Time Tracker @Plushi.ee")
        self.root.geometry("300x170") 
        self.root.configure(bg="#f4f4f4")
        self.root.resizable(True, True)

        # Icon
        try:
            img = Image.open(ICON_PATH)
            icon = ImageTk.PhotoImage(img.resize((32, 32)))
            self.root.iconphoto(False, icon)
        except:
            print("Ikon tidak ditemukan.")

        self.method = StringVar(value="window")
        self.last_project = None
        self.start_time = None

        # Metode Deteksi
        Label(root, text="Detection Mode", font=("Segoe UI", 14, "bold"), bg="#f4f4f4").pack(pady=(8, 4))
        frame = Frame(root, bg="#f4f4f4")
        frame.pack(pady=(0, 4))

        style = ttk.Style()
        style.configure("TRadiobutton", background="#f4f4f4", font=("Segoe UI", 9))
        style.configure("TCheckbutton", background="#f4f4f4", font=("Segoe UI", 9))

        ttk.Radiobutton(frame, text="Window Title", variable=self.method, value="window").pack(side=LEFT, padx=10)
        ttk.Radiobutton(frame, text="OCR (screenshot)", variable=self.method, value="ocr").pack(side=LEFT, padx=10)

        # Label Judul Proyek
        self.status_label = Label(root, text="⏳ Waiting for CSP to open...", font=("Segoe UI", 11), bg="#f4f4f4")
        self.status_label.pack(pady=(8, 2), padx=10)

        self.timer_label = Label(root, text="", font=("Segoe UI", 10), bg="#f4f4f4")
        self.timer_label.pack(pady=(0, 6), padx=10)

        self.pin_var = BooleanVar()
        ttk.Checkbutton(root, text="📌 Pin window (always on-top)", variable=self.pin_var,
                command=self.toggle_pin).pack(pady=(0, 4))

        self.running = True
        threading.Thread(target=self.update_loop, daemon=True).start()

    def toggle_pin(self):
        self.root.wm_attributes("-topmost", self.pin_var.get())

    def update_loop(self):
        while self.running:
            csp_title = get_clip_studio_window_title()
            if csp_title:
                if self.method.get() == "window":
                    if self.last_project is None:
                        self.start_time = time.time()
                    self.last_project = detect_project_name_window()
                    name = self.last_project
                else:
                    if is_csp_active_window():
                        new_name = detect_project_name_ocr()
                        if self.last_project is None:
                            self.start_time = time.time()
                        elif new_name != self.last_project:
                            self.start_time = time.time()
                        self.last_project = new_name
                    name = self.last_project
            else:
                name = None
                self.last_project = None
                self.start_time = None

            if name:
                elapsed = int(time.time() - self.start_time) if self.start_time else 0
                h, r = divmod(elapsed, 3600)
                m, s = divmod(r, 60)
                durasi = f"{h:02}:{m:02}:{s:02}"
                self.status_label.config(text=f"📁 : {name}")
                self.timer_label.config(text=f"🕒 : {durasi}")
            else:
                self.status_label.config(text="❌ CSP not detected")
                self.timer_label.config(text="")

            update_discord_presence(name, elapsed if self.start_time else 0)
            time.sleep(1)

if __name__ == "__main__":
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = CSPTracker(root)
    root.mainloop()
