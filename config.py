"""
Configuration settings for the Google Maps Leads Extractor.
Includes selectors, timeouts, and URL structures.
"""

# Base URL (Updated to the official standard structure to avoid 404 errors)
# We add 'hl=en' to force the interface into English for consistent scraping.
BASE_URL = "https://www.google.com/maps/search/{keyword}?hl=en"

# Selectors (Subject to change if Google updates DOM)
SELECTORS = {
    "consent_buttons": [
        "button[aria-label='Accept all']",
        "button:has-text('Accept all')",
        "button:has-text('Tümünü kabul et')", # Added TR just in case
        "form[action*='consent'] button"
    ],
    "feed": 'div[role="feed"]',
    "result_card": 'div[role="feed"] > div > div[jsaction]',
    "search_box": "input#searchboxinput"
}

# Scraper Settings
SETTINGS = {
    "scroll_pause_min": 1500,  # ms
    "scroll_pause_max": 3000,  # ms
    "max_retries": 5,
    "timeout": 60000,          # ms (increased for safety)
    "viewport": {"width": 1920, "height": 1080},
    "locale": "en-US"          # Browser locale
}