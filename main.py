from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

class CrunchbaseScraper:
    def _init_(self, driver_path):
        self.driver_path = driver_path
        self.driver = None

    def init_driver(self):
        # Initialize the Selenium WebDriver
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)

    def scrape_data(self, search_term):
        try:
            self.init_driver()
            url = f"https://www.crunchbase.com/search/organizations/field/organizations/name/{search_term}"
            self.driver.get(url)
            time.sleep(5)  # Allow the page to load

            # Scroll to load dynamic content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Get the page source and parse it
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            # Find organization cards
            cards = soup.find_all('a', class_='entity-title')
            if not cards:
                print("No results found.")
                return

            # Extract and save data
            with open(f"{search_term}_data.txt", "w", encoding="utf-8") as file:
                for card in cards:
                    name = card.text.strip()
                    link = card.get('href', '')
                    full_link = f"https://www.crunchbase.com{link}" if link.startswith('/') else link
                    file.write(f"Name: {name}\n")
                    file.write(f"Link: {full_link}\n\n")

            print(f"Data saved to {search_term}_data.txt")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

# Usage
if __name__ == "_main_":
    DRIVER_PATH = "path/to/chromedriver"  # Replace with the actual path to your WebDriver
    scraper = CrunchbaseScraper(DRIVER_PATH)
    search_query = input("Enter a company/organization to search: ")
    scraper.scrape_data(search_query)