# 🎨 Clip Studio Paint Time Tracker ⏱️

A modern desktop tool to **automatically track your working time** in [Clip Studio Paint](https://www.clipstudio.net) — with support for **OCR-based project name detection** and **Discord Rich Presence integration**!

<img src="assets/demo.png" alt="Demo Screenshot" width="450"/>

---

## 🔧 Features

- ⏱️ **Auto Time Tracking** – Starts counting when you open CSP and updates as project changes.
- 🧠 **Smart Project Detection**
  - `Window Title` mode: Uses CSP window title.
  - `OCR Screenshot` mode: Captures project name even if not shown in title.
- 🖼️ **Live Discord Rich Presence** – Show off what you're working on in your Discord status!
- 📌 **"Always-on-Top" Mode** – Keep the timer visible above other windows.
- 🎨 **Minimal, Elegant UI** – Built with `Tkinter` and styled for comfort.
- 💡 Fully open-source and easy to modify.

---

## 🚀 Getting Started

### 1. Requirements

- Windows OS
- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed  
  *(If not detected automatically, uncomment the path in the script)*

### 2. Installation

```bash
git clone https://github.com/yourusername/csp-time-tracker.git
cd CSP-DiscordRichPresence
pip install -r requirements.txt
