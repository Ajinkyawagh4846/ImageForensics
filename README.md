# ImageForensics 🔍

**A Web-Based Digital Image Forensics Tool**

ImageForensics is a Python Flask-based web application designed to perform preliminary forensic analysis of digital images. It extracts image metadata, generates SHA-256 hashes for file integrity verification, and uses Error Level Analysis (ELA) to visualize compression-related differences in JPEG images.

## ✨ Features

- **Image Upload:** Upload supported JPG, JPEG, and PNG images for analysis.
- **Metadata Extraction:** Retrieve image format, dimensions, color mode, and available EXIF metadata.
- **SHA-256 Hashing:** Generate a cryptographic hash to help verify file integrity.
- **Error Level Analysis (ELA):** Generate a visual difference map for JPEG images by comparing the original with a recompressed copy.
- **Simple Web Interface:** View analysis results through a clean, browser-based interface.
- **Image Validation:** Check uploaded files before processing.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic and analysis |
| Flask | Web application framework |
| HTML5 | Webpage structure |
| CSS3 | User interface styling |
| Pillow | Image processing and metadata extraction |
| hashlib | SHA-256 hash generation |

## 📁 Project Structure

```text
ImageForensics/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── ela_results/
└── uploads/
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3 installed on your system
- Git installed
- A web browser

### 1. Clone the Repository

```bash
git clone https://github.com/Ajinkyawagh4846/ImageForensics.git
cd ImageForensics
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Your Browser

Visit:

```text
http://127.0.0.1:5000
```

Upload a supported image to begin the analysis.

## 🔬 How It Works

### 1. Image Metadata Analysis

The application extracts available image properties, including format, width, height, color mode, and EXIF metadata.

### 2. SHA-256 File Hashing

The application calculates a SHA-256 digest from the uploaded file's bytes. Comparing hashes from separate examinations can help determine whether the file has changed.

### 3. Error Level Analysis (ELA)

ELA recompresses a JPEG image and compares it with the original. The pixel differences are amplified and displayed as a visualization to help examine variations in compression characteristics.

**Note:** ELA is an investigative aid, not definitive proof of image manipulation. Normal compression, resizing, texture, and previous editing can also affect its output.

## 🎯 Project Objectives

- Explore fundamental digital image forensic techniques.
- Extract useful image properties and available metadata.
- Support file integrity verification through cryptographic hashing.
- Visualize JPEG compression differences using ELA.
- Provide a simple and accessible interface for preliminary image analysis.

## ⚠️ Limitations

- ELA is currently designed for JPEG images.
- EXIF metadata may be missing or incomplete.
- A SHA-256 hash identifies a particular file version but does not establish its authenticity.
- ELA results alone cannot confirm whether an image has been manipulated.
- The application is intended for preliminary analysis, not as a replacement for a complete forensic investigation.

## 🚀 Future Enhancements

- Additional image manipulation analysis techniques.
- Side-by-side comparison of original and analyzed images.
- Forensic report generation.
- Improved evidence handling and analysis history.
- Additional image formats and forensic indicators.

## 🔐 Responsible Use

Use this tool only on images you are authorized to examine. For formal forensic investigations, preserve the original evidence, document the analysis process, and use appropriate evidence-handling procedures.

## 📄 License

This project is available for educational and research purposes. A formal open-source license can be added to define the terms of reuse.

---

**ImageForensics — Explore the evidence behind digital images.**
