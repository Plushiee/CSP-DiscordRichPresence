# 🎨 Clip Studio Paint Time Tracker ⏱️

A modern desktop tool to **automatically track your working time** in [Clip Studio Paint](https://www.clipstudio.net) — with support for **OCR-based project name detection** and **Discord Rich Presence integration**!

<img src="assets/demo/Demo App 1.png" alt="Demo Screenshot" width="450"/>
<img src="assets/demo/Discord Rich Presence Preview.png" alt="Discord Rich Presence Preview" width="450"/>

---

## 🔧 Features

- ⏱️ **Auto Time Tracking** – Automatically starts when CSP is opened, and updates when you switch projects.
- 🧠 **Smart Project Detection**:
  - `Window Title` mode – Reads from the CSP window title.
  - `OCR Screenshot` mode – Uses Tesseract OCR to read the project name directly from the canvas title bar.
- 🖼️ **Live Discord Rich Presence** – Displays current project and working duration on your Discord profile.
- 📌 **"Always-on-Top" Mode** – Option to pin the tracker above other windows.
- 💻 **Minimal, Modern UI** – Built with `Tkinter` and styled with care.
- 🛠️ **Fully Open Source** – Easy to read, modify, and contribute to.

---

## ⚠️ Beta Notice

> 🚧 This app is currently in **early beta**.  
> I'm originally a **web developer**, and this is my first time building a desktop utility with GUI and system integrations (like OCR and Discord RPC).  
>  
> Your feedback, suggestions, or code contributions are **greatly appreciated**! 🙏

Feel free to open issues or pull requests 💬

---

## 🚀 Getting Started

### 1. Requirements

- Windows OS
- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed  
  *(If it's not automatically detected, manually set the path in the script: `pytesseract.pytesseract.tesseract_cmd = ...`)*

---

### 2. Installation

```bash
git clone https://github.com/yourusername/csp-time-tracker.git
cd csp-time-tracker
pip install -r requirements.txt
