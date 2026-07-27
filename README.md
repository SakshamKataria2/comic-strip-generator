# 🦸‍♂️ AI Cybersecurity Comic Generator

A multi-page Streamlit web application that uses Google's Gemini 3.6 Flash model to automate the creation of educational cybersecurity comic strips. 

This tool solves the biggest bottleneck in AI comic generation (poor text rendering) by decoupling the artwork from the dialogue. It generates a narrative script, extracts speech bubble coordinates using AI vision, and exports a fully responsive, self-contained HTML/CSS comic page with localized JSON text.

## ✨ Features

- **6-Panel Narrative Generator:** Select from predefined cybersecurity topics (Ransomware, Phishing, Firewall breaches, etc.) to generate a complete story arc with visual AI prompts, English dialogue, and core security takeaways.
- **Multimodal Vision Extraction:** Upload a reference image (with text) and a clean AI-generated image (no text). Gemini automatically maps the exact percentage-based coordinates (`top %`, `left %`) of the speech bubbles.
- **Dynamic HTML/JSON Export:** Generates a `dialogue.json` file for easy localization (i18n) and a completely functional `index.html` file.
- **Base64 Image Embedding:** Your clean comic artwork is natively converted into a Base64 string and embedded directly into the HTML, preventing broken image links and keeping your comic as a single, portable file.
- **Session State Management:** Securely holds your generated HTML/JSON in memory so downloads do not trigger page reload glitches.

## 📋 Prerequisites

To run this project locally, you will need:
- Python 3.8 or higher
- A Google Gemini API Key (Available from [Google AI Studio](https://aistudio.google.com/))

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/SakshamKataria2/comic-strip-generator.git](https://github.com/SakshamKataria2/comic-strip-generator.git)
   cd comic-strip-generator
   install -r requirements.txt
   streamlit run app.py