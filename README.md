# 📍 G-Maps Leads Extractor

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-Async-green)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)

## 🚀 Overview
**G-Maps Leads Extractor** is an enterprise-grade asynchronous scraping tool designed to harvest business intelligence data from Google Maps. It utilizes **Playwright** for full browser automation, handling infinite scrolling, dynamic DOM elements, and anti-detection.

## 🛠 Features
* **⚡ Async Architecture:** Built on `asyncio` and `playwright` for high-performance extraction.
* **🛡️ Anti-Detection:** Implements random delays and mimics human scroll behavior.
* **📊 Clean Data Output:** Automatically parses raw text into structured columns using Regex.

## 📦 Installation
```bash
git clone [https://github.com/berk-io/gmaps-leads-extractor.git](https://github.com/berk-io/gmaps-leads-extractor.git)
cd gmaps-leads-extractor
pip install -r requirements.txt
playwright install chromium
```

## 💻 Usage
```bash
python main.py --keyword "Dentists in London" --limit 50
```

## 📂 Output
The tool generates an Excel file containing Business Name, Rating, Review Count, Category, and Address.

## ⚠️ Disclaimer
This tool is for educational and research purposes only. Users are responsible for complying with Google Maps' Terms of Service.