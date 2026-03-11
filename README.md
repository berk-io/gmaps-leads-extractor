# 📍 G-Maps Leads Extractor

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-Async-green)
![Status](https://img.shields.io/badge/Status-Production-brightgreen) 

## 🚀 Overview

**G-Maps Leads Extractor** is an enterprise-grade asynchronous scraping tool designed to harvest business intelligence data from Google Maps. 

Unlike traditional scrapers, this tool utilizes **Playwright** for full browser automation, successfully handling:
* **Infinite Scrolling** (Lazy-loading lists)
* **Dynamic DOM Elements**
* **Rate-Limit Mitigation** (Human-like behavior simulation)
* **Cookie Consent Walls**

It exports structured data (clean Names, Ratings, Review Counts, Categories) directly into Excel format for easy CRM integration.

## 🛠 Features

* **⚡ Async Architecture:** Built on `asyncio` and `playwright` for high-performance extraction.
* **🛡️ Anti-Detection:** Implements random delays and mimics human scroll behavior.
* **📊 Clean Data Output:** Automatically parses raw text into structured columns (Rating, Reviews, etc.) using Regex.
* **⚙️ Configurable:** Search keywords and limits can be controlled via CLI arguments.

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/gmaps-leads-extractor.git](https://github.com/yourusername/gmaps-leads-extractor.git)
    cd gmaps-leads-extractor
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Install Playwright browsers:
    ```bash
    playwright install chromium
    ```

## 💻 Usage

Run the script from the terminal with your desired keyword and limit.

**Basic Search:**
```bash
python main.py --keyword "Dentists in London" --limit 50

```

**Headless Mode (No GUI):**

```bash
python main.py -k "Pizza in Rome" -l 100 --headless

```

## 📂 Output

The tool generates an Excel file (e.g., `leads_dentists_in_london_20260306.xlsx`) in the project directory containing:

* Business Name
* Rating (e.g., 4.9)
* Review Count (e.g., 150)
* Category
* Address / Status

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Users are responsible for complying with Google Maps' Terms of Service. The developer is not responsible for any misuse of this software.
