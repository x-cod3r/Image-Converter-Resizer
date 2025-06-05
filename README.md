# 🖼️ Bulk Image Converter

<div align="center">

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)

*A powerful, user-friendly GUI tool for bulk image format conversion and resizing*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Supported Formats](#-supported-image-formats) • [Screenshots](#-screenshots)

</div>

---

## ✨ Features

- 🎯 **Intuitive Interface**: Clean, modern GUI with scrollable layout
- 📦 **Bulk Processing**: Convert multiple images simultaneously
- 🔄 **Flexible Conversion**: Choose individual formats or batch convert to one format
- 🖼️ **Format Support**: JPEG, PNG, WebP, BMP, TIFF, ICO, GIF, and HEIC*
- 📏 **Smart Resizing**: Maintain aspect ratio, custom dimensions, or percentage scaling
- ⚡ **Quality Control**: Adjustable quality settings for lossy formats
- 📊 **Progress Tracking**: Real-time conversion progress with detailed status
- 🛡️ **Error Handling**: Graceful handling of unsupported files and errors
- 🚀 **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux

*HEIC support requires pillow-heif package

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- PIL/Pillow (for image processing)
- tkinter (usually included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bulk-image-converter.git
   cd bulk-image-converter
   ```

2. **Install dependencies**
   ```bash
   pip install Pillow
   # Optional: For HEIC support
   pip install pillow-heif
   ```

3. **Run the application**
   ```bash
   python image_converter.py
   ```

### Alternative: Download Release
Download the latest release from the [Releases page](https://github.com/yourusername/bulk-image-converter/releases) and run the standalone executable.

## 🎮 Usage

### Basic Workflow
1. **Launch** the application
2. **Select Images**: 
   - Click "Browse Files" to select individual images
   - Choose multiple files using Ctrl/Cmd+click
3. **Choose Output Directory** (optional - defaults to source directory)
4. **Configure Conversion**:
   - **Mode 1**: Convert all files to one format
   - **Mode 2**: Set individual target formats (double-click files)
5. **Set Quality**: Adjust quality for JPEG/WebP/HEIC (1-100)
6. **Configure Resizing** (optional):
   - Keep original size
   - Custom dimensions with aspect ratio preservation
   - Percentage scaling
7. **Convert**: Click "Convert Images" and monitor progress

### Advanced Options

#### Conversion Modes
- **All to One Format**: Convert all selected images to the same format
- **Individual Selection**: Double-click each file to set its target format

#### Resizing Options
- **Keep Original**: Maintain original dimensions
- **Custom Size**: Set specific width/height with optional aspect ratio preservation  
- **Percentage**: Scale by percentage (e.g., 50% = half size)

## 📋 Supported Image Formats

<table>
<tr>
<td>

**Input Formats**
- JPEG/JPG
- PNG
- BMP
- TIFF/TIF
- WebP
- GIF
- HEIC/HEIF*

</td>
<td>

**Output Formats**
- JPEG (with quality control)
- PNG (lossless)
- WebP (with quality control)
- BMP (uncompressed)
- TIFF (lossless)
- ICO (multi-size icons)
- GIF (animated support)
- HEIC* (with quality control)

</td>
</tr>
</table>

*Requires `pillow-heif` package: `pip install pillow-heif`

## 📸 Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────────┐
│                    Bulk Image Converter                     │
├─────────────────────────────────────────────────────────────┤
│ Select Images: [Browse Files] [Clear] - 5 files selected   │
│                                                             │
│ Output Directory: [Browse Folder] - Same as source dir     │
│                                                             │
│ ┌─ Conversion Settings ────────────────────────────────────┐ │
│ │ ● All files to one format  ○ Individual format selection│ │
│ │ Convert to: [JPEG ▼] Quality: [85    ]                  │ │
│ │                                                          │ │
│ │ Size Settings:                                           │ │
│ │ ● Keep original  ○ Custom dimensions  ○ Percentage      │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─ Selected Files ────────────────────────────────────────┐ │
│ │ File Name          │ Size   │ Format │ Convert To      │ │
│ │ ├─ photo1.png      │ 2.1 MB │ PNG    │ JPEG           │ │
│ │ ├─ image2.heic     │ 3.4 MB │ HEIC   │ JPEG           │ │
│ │ ├─ scan.tiff       │ 8.7 MB │ TIFF   │ JPEG           │ │
│ │ └─ logo.gif        │ 156 KB │ GIF    │ JPEG           │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                             │
│ [████████████████████████████] 100% - Ready                │
│                                                             │
│                    [Convert Images]                         │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Configuration Options

| Setting | Description | Options |
|---------|-------------|---------|
| **Conversion Mode** | How to handle target formats | All to one format / Individual selection |
| **Output Format** | Target image format | JPEG, PNG, WebP, BMP, TIFF, ICO, GIF, HEIC* |
| **Quality** | Compression quality (lossy formats) | 1-100 (higher = better quality) |
| **Size Mode** | How to handle image dimensions | Keep original / Custom size / Percentage |
| **Aspect Ratio** | Maintain proportions when resizing | Enabled / Disabled |

## 🎯 Use Cases

- **Web Optimization**: Convert images to WebP for faster loading
- **Icon Creation**: Generate ICO files with multiple sizes for applications
- **Batch Processing**: Convert camera RAW files to standard formats
- **Size Reduction**: Compress images for email or storage
- **Format Migration**: Convert legacy formats to modern ones
- **Social Media**: Resize images for different platform requirements

## 🔧 Technical Details

### Quality Settings
- **JPEG**: 1-100 (recommended: 85-95 for photos, 75-85 for web)
- **WebP**: 1-100 (typically 10-15% smaller than JPEG at same quality)
- **HEIC**: 1-100 (Apple's format, excellent compression)

### ICO Generation
- Automatically creates multi-size icons: 16×16, 32×32, 48×48, 64×64, 128×128, 256×256
- Perfect for Windows applications and favicons

### Threading
- Non-blocking UI with background processing
- Real-time progress updates
- Graceful error handling per file

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Ideas for Contributions
- 🎨 Modern UI themes and dark mode
- 📱 Additional format support (AVIF, JXL)
- 🔧 Command-line interface
- 🌍 Internationalization
- 📊 Batch statistics and reporting
- 🖼️ Image preview functionality
- 🎛️ Advanced filtering options

## 🐛 Bug Reports & Feature Requests

Found a bug? Have an idea? Open an issue on the [Issues page](https://github.com/yourusername/bulk-image-converter/issues).

**Bug Report Template:**
- Python version and OS
- PIL/Pillow version
- Input image format and size
- Steps to reproduce
- Error message (if any)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's Pillow library for robust image processing
- Uses tkinter for cross-platform GUI compatibility
- HEIC support via pillow-heif library
- Inspired by the need for simple bulk image processing tools

## 📊 Performance

- **Speed**: Processes 100+ images efficiently with threading
- **Memory**: Optimized memory usage with image streaming
- **Quality**: Preserves image quality with smart compression
- **Compatibility**: Handles various color modes and transparency

---

<div align="center">
<strong>Made with ❤️ for photographers, designers, and developers</strong>
</div>
