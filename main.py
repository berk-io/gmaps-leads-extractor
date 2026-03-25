import asyncio
import logging
import argparse
import random
import re
import urllib.parse
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
from playwright.async_api import async_playwright, Page
import config  # Importing our configuration file

# Professional Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper_process.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GMapsExtractor:
    """
    Enterprise-grade asynchronous scraper for Google Maps.
    
    Features:
    - Infinite Scroll Handling
    - Rate Limit Mitigation (Random Delays)
    - Robust Error Handling
    - Structured Data Parsing (Regex)
    """

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.results: List[Dict] = []

    async def _handle_consent(self, page: Page) -> None:
        """
        Detects and handles Google's cookie consent overlay.
        """
        try:
            for selector in config.SELECTORS["consent_buttons"]:
                if await page.locator(selector).first.is_visible(timeout=3000):
                    logger.info("Consent dialog detected. Accepting...")
                    await page.locator(selector).first.click()
                    await page.wait_for_timeout(2000)
                    return
            logger.info("No active consent dialog found. Proceeding.")
        except Exception as e:
            logger.warning(f"Consent handling skipped: {e}")

    async def _scroll_feed(self, page: Page, max_results: int) -> None:
        """
        Simulates human scrolling to trigger lazy-loading of results.
        """
        logger.info("Initiating infinite scroll sequence...")
        feed_selector = config.SELECTORS["feed"]

        try:
            await page.wait_for_selector(feed_selector, timeout=15000)
        except Exception:
            logger.error("Feed panel not found. Layout might have changed.")
            return

        previous_count = 0
        stagnation_counter = 0

        while True:
            cards = page.locator(config.SELECTORS["result_card"])
            count = await cards.count()

            if count >= max_results:
                logger.info(f"Target limit reached: {count}/{max_results}")
                break

            if count == previous_count:
                stagnation_counter += 1
                logger.info(f"Waiting for new items... ({count} found) - Retry {stagnation_counter}/5")
                if stagnation_counter >= config.SETTINGS["max_retries"]:
                    logger.warning("Max retries reached. Stopping scroll.")
                    break
            else:
                stagnation_counter = 0
                logger.info(f"Results loaded: {count}")

            previous_count = count

            # Scroll Action
            await page.hover(feed_selector)
            await page.mouse.wheel(0, 5000)
            
            # Random delay to mimic human behavior
            delay = random.randint(
                config.SETTINGS["scroll_pause_min"], 
                config.SETTINGS["scroll_pause_max"]
            )
            await page.wait_for_timeout(delay)

    def _parse_details(self, text: str) -> Dict[str, str]:
        """
        Uses Regex to extract structured data from raw text string.
        
        Args:
            text (str): The raw inner text of a card.
        Returns:
            Dict: Parsed fields (Rating, Reviews, Category, etc.)
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        data = {
            "Business Name": lines[0] if lines else "N/A",
            "Rating": "N/A",
            "Reviews": "0",
            "Category": "N/A",
            "Address": "N/A",
            "Status": "N/A"
        }

        # Join lines for regex searching
        full_text = " ".join(lines)

        # 1. Extract Rating (e.g., "4.9")
        rating_match = re.search(r'(\d[,.]\d)', full_text)
        if rating_match:
            data["Rating"] = rating_match.group(1).replace(',', '.')

        # 2. Extract Review Count (e.g., "(2.228)")
        reviews_match = re.search(r'\(([\d,.]+)\)', full_text)
        if reviews_match:
            data["Reviews"] = reviews_match.group(1).replace('.', '').replace(',', '')

        # 3. Simple Heuristics for Address/Category (Logic can be improved)
        # Usually, the line containing the bullet point '·' has category/address
        for line in lines:
            if '·' in line:
                parts = line.split('·')
                if len(parts) > 1:
                    data["Category"] = parts[0].strip()
                    data["Address"] = parts[-1].strip()
            
            if "Close" in line or "Open" in line or "Açık" in line or "Kapalı" in line:
                data["Status"] = line

        return data

    async def _extract_data(self, page: Page) -> List[Dict]:
        """
        Iterates over loaded cards and parses content.
        """
        logger.info("Extracting structured data from DOM...")
        cards = await page.locator(config.SELECTORS["result_card"]).all()
        
        extracted_data = []
        for card in cards:
            try:
                text = await card.inner_text()
                parsed_entry = self._parse_details(text)
                extracted_data.append(parsed_entry)
            except Exception as e:
                logger.warning(f"Failed to parse card: {e}")
                continue
        
        return extracted_data

    def _save_to_excel(self, data: List[Dict], keyword: str) -> None:
        """
        Exports data to Excel with timestamped filename.
        """
        if not data:
            logger.warning("No data extracted. Skipping save.")
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        clean_keyword = keyword.replace(" ", "_").lower()
        filename = f"leads_{clean_keyword}_{timestamp}.xlsx"

        try:
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False)
            logger.info(f"SUCCESS: Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving file: {e}")

    async def run(self, keyword: str, limit: int) -> None:
        """
        Main execution flow.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                viewport=config.SETTINGS["viewport"],
                locale=config.SETTINGS["locale"] # Force consistency
            )
            page = await context.new_page()

            # URL Injection Strategy
            encoded_query = urllib.parse.quote_plus(keyword)
            target_url = config.BASE_URL.format(keyword=encoded_query)
            
            logger.info(f"Navigating to: {target_url}")
            await page.goto(target_url, timeout=config.SETTINGS["timeout"])

            await self._handle_consent(page)
            await self._scroll_feed(page, limit)
            
            data = await self._extract_data(page)
            self._save_to_excel(data, keyword)

            await browser.close()
            logger.info("Process completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Maps Leads Extractor")
    parser.add_argument("-k", "--keyword", type=str, required=True, help="Search term (e.g., 'Dentists in London')")
    parser.add_argument("-l", "--limit", type=int, default=20, help="Max results to scrape")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")

    args = parser.parse_args()

    bot = GMapsExtractor(headless=args.headless)
    asyncio.run(bot.run(keyword=args.keyword, limit=args.limit))