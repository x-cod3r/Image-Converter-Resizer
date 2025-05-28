# 🎨 Bulk Image Converter Pro 🖼️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![made-with-tkinter](https://img.shields.io/badge/Made%20with-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![Pillow](https://img.shields.io/badge/Powered%20by-Pillow-green.svg)](https://python-pillow.org/)

> A user-friendly desktop application built with Python and Tkinter for converting multiple images between various formats, resizing, and adjusting quality with ease! Say goodbye to tedious one-by-one conversions. ✨

---

## 🌟 Sneak Peek! 🌟

**(Recommended: Replace this with a high-quality GIF or a clear screenshot of your application in action!)**

![App Screenshot/GIF](https://via.placeholder.com/600x400.png?text=App+Screenshot+or+GIF+Here)
*A quick look at the Bulk Image Converter Pro interface.*

---

## ✨ Features

*   ✅ **Bulk Conversion:** Convert hundreds of images in one go.
*   🔄 **Multiple Format Support:**
    *   **Reads:** JPG, JPEG, PNG, BMP, TIFF, TIF, WEBP, GIF.
    *   **Writes To:** JPEG, PNG, WEBP, BMP, TIFF, GIF, **ICO** (Icon).
    *   **(Optional) HEIC/HEIF Support:** Convert HEIC/HEIF files if `pillow-heif` is installed.
*   🖼️ **Flexible Resizing:**
    *   Keep original dimensions.
    *   Resize to specific width/height.
    *   Resize by percentage.
    *   Maintain aspect ratio (optional).
*   💯 **Quality Control:** Adjust quality for JPEG, WEBP, and HEIC formats (1-100).
*   🎯 **Individual File Settings:**
    *   Choose a different output format for each file in "Individual Mode".
    *   Set individual quality for JPEG/WEBP/HEIC files.
*   📂 **Output Directory Selection:** Choose where your converted images are saved.
*   📊 **Progress Tracking:** Visual progress bar and status updates during conversion.
*   💡 **User-Friendly GUI:** Intuitive interface built with Tkinter.
*   📝 **File List Management:** Easily add, clear, and view selected files with details.
*   ⚠️ **Error Handling:** Informative messages for conversion issues.
*   🧵 **Threaded Conversions:** Keeps the UI responsive during processing.
*   🖱️ **Scrollable Interface:** Handles a large number of files and settings comfortably.

---

## 💻 Tech Stack

*   **Python 3.7+**
*   **Tkinter** (for the GUI)
*   **Pillow (PIL Fork)** (for image processing)
*   **(Optional) `pillow-heif`** (for HEIC/HEIF support)

---

## 📋 Prerequisites

*   Python 3.7 or higher installed on your system.
*   `pip` (Python package installer).

---

## 🚀 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/[YOUR_USERNAME]/[YOUR_REPONAME].git
    cd [YOUR_REPONAME]
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    A `requirements.txt` file would be ideal. If you don't have one, create it:
    ```
    # requirements.txt
    Pillow>=9.0.0
    ```
    Then install:
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) For HEIC/HEIF Support:**
    If you want to convert HEIC/HEIF files, install `pillow-heif`:
    ```bash
    pip install pillow-heif
    ```

---

## ▶️ How to Run

Once dependencies are installed, navigate to the project directory and run:

```bash
python your_main_script_name.py

