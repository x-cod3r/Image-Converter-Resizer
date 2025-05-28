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
```

---

## 📖 How to Use - Step-by-Step Guide 🚶‍♀️🚶‍♂️

Follow these simple steps to transform your images:

1.  **📤 Add Your Images:**
    *   Click the `Browse Files` button.
    *   A file dialog will open. Select one or multiple image files (JPG, PNG, WEBP, GIF, BMP, TIFF, HEIC).
    *   Your selected files will appear in the "Selected Files" list below.

    ![Step 1: Browse Files](https://via.placeholder.com/200x100.png?text=Icon/Mini-Screenshot+Browse) *(Imagine a small icon or cropped screenshot here)*

2.  **📁 Choose Your Destination:**
    *   Click the `Browse Folder` button.
    *   Select the directory where you want your converted images to be saved.
    *   **Pro Tip:** If you don't select an output directory, your converted images will be saved in the same folder as their original source files.

    ![Step 2: Output Directory](https://via.placeholder.com/200x100.png?text=Icon/Mini-Screenshot+Output) *(Imagine a small icon or cropped screenshot here)*

3.  **⚙️ Configure Conversion Settings:**
    This is where the magic happens! ✨

    *   **🎛️ Conversion Mode:**
        *   `All files to one format`: Perfect for converting a batch of images to a single, uniform format.
            *   **➡️ Convert to:** Choose your desired output format (e.g., JPEG, PNG, WEBP, **ICO**).
            *   **💯 Quality:** If converting to JPEG, WEBP, or HEIC, adjust the quality slider (1-100). Higher means better quality but larger file size.
        *   `Individual format selection`: Gives you fine-grained control. See Step 4!

    *   **📏 Size Settings:**
        *   `Keep original size`: No changes to dimensions.
        *   `Resize to specific dimensions`: Enter your desired `Width` and `Height` in pixels.
        *   `Resize by percentage`: Enter a `Scale %` (e.g., 50% to halve the size).
        *   **📐 Maintain aspect ratio:** Check this box (highly recommended!) to avoid distorting your images when resizing.

    ![Step 3: Settings](https://via.placeholder.com/300x150.png?text=Cropped+Screenshot+of+Settings+Area) *(Imagine a cropped screenshot of the settings panel)*

4.  **🖼️ Fine-Tune (Individual Mode Only):**
    *   If you selected `Individual format selection` in Step 3:
        *   **Double-click** on any file in the "Selected Files" list.
        *   A dialog will pop up, allowing you to choose a **specific output format** and **quality** (if applicable) just for that single image. This overrides the global settings for that file.

    ![Step 4: Individual Dialog](https://via.placeholder.com/250x150.png?text=Screenshot+of+Individual+Dialog) *(Imagine a screenshot of the individual format dialog)*

5.  **🚀 Let's Convert!**
    *   Once you're happy with your selections and settings, click the `Convert Images` button.

6.  **👀 Watch the Progress:**
    *   The progress bar will fill up, and the status label will show which file is currently being processed.
    *   Sit back and relax while the converter does its job! ☕

7.  **🎉 All Done!**
    *   A notification will appear once the conversion is complete.
    *   It will summarize how many images were converted successfully and if any encountered issues.
    *   Your newly converted images are now ready in your chosen output directory!

---

## 🤝 Contributing - We ❤️ Pull Requests!

Got an idea to make this tool even better? Found a pesky bug? We'd love your help!

1.  **🍴 Fork it!** Click the 'Fork' button at the top right of this page.
2.  **🌿 Create your feature branch:**
    ```bash
    git checkout -b feature/YourAmazingIdea
    ```
3.  **👨‍💻 Commit your changes:** Make your magic happen!
    ```bash
    git commit -am 'feat: Add some amazing new feature'
    ```
    *(Psst! We like [Conventional Commits](https://www.conventionalcommits.org/))*
4.  **⬆️ Push to the branch:**
    ```bash
    git push origin feature/YourAmazingIdea
    ```
5.  **📬 Open a new Pull Request:** Go to your fork on GitHub and click the "New pull request" button.

We'll review it as soon as we can!

---

## 📄 License

This project is proudly licensed under the **MIT License**.
Feel free to use, modify, and distribute it as you see fit. See the `LICENSE.md` file for the full legal text.

📜 *(A link to your LICENSE.md file would be great here if you have one)*

---

## 🙏 Acknowledgements & Shout-outs!

A big thank you to:

*   🌟 The incredible team behind **Pillow (PIL Fork)** – this project wouldn't be possible without their powerful image processing capabilities.
*   🐍 The **Python Software Foundation** and the global Python community for creating and maintaining such a versatile language and its extensive libraries like Tkinter.
*   💡 **(Optional) Specific Libraries/Inspirations:** If you used code from a specific tutorial, an idea from another open-source project, or a particular library that was key, mention it here!
    *   _Example: "Inspiration for the UI layout from [Project Name/Link]"_
    *   _Example: "The HEIC handling relies on the excellent `pillow-heif` library."_

---
