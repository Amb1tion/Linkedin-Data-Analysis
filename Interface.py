import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

class Interface:
    def __init__(self, filepath='config.ini'):
        config = configparser.ConfigParser()
        config.read(filepath)
        self.username = config['DEFAULT']['User']
        self.password = config['DEFAULT']['Password']
        self.driver = webdriver.Chrome()
        try:
            self.driver = self.setup(self.username, self.password)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize connection: {e}")

    def setup(self, username, password):
        """Initialize connection with provided credentials."""
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(5)  # Wait for the page to load
        username_field = self.driver.find_element("id", "username")
        username_field.send_keys(username)
        time.sleep(1)  
        password_field = self.driver.find_element("id", "password")
        password_field.send_keys(password)
        time.sleep(1)  
        login_button = self.driver.find_element("xpath", "//button[@type='submit']")
        login_button.click()
        time.sleep(5)  # Wait for the page to load after login
        return self.driver
    def navigate_job_page(self,page):
        """Navigate to the LinkedIn jobs page."""
        page = int(page) - 1  # Convert to zero-based index
        if page < 0:
            raise ValueError("Page number must be greater than 0.")
        
        start = page * 25
        url = (
            "https://www.linkedin.com/jobs/search/"
            "?currentJobId=4220162457"
            "&distance=50"
            "&geoId=100025096"
            "&keywords=python"
            "&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE"
            f"&start={start}"
        )
        
        print(f"Navigating to page {page + 1}...")
        self.driver.get(url)
        self.human_sleep()  # Mimic human behavior with a random sleep
        try:
            
            footer = self.driver.find_element(By.XPATH, "//div[contains(@id, 'jobs-search-results-footer')]")

            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", footer)

            time.sleep(2)  # Allow time for the page to load completely
            return self.driver.page_source
        except Exception as e:
            raise RuntimeError(f"Failed to load page {page + 1}: {e}")

    def scrape_page(self, page):
        """Scrape a specific page of LinkedIn jobs using Selenium."""
        #dump the page source to a file
        with open(f"page_{page + 1}.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        try:
            # Wait for job cards list to appear
            
            footer = self.driver.find_element(By.XPATH, "//div[contains(@id, 'jobs-search-results-footer')]")

            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", footer)

            time.sleep(2)  # Allow time for the page to load completely
            return self.driver.page_source
        except Exception as e:
            raise RuntimeError(f"Failed to load page {page + 1}: {e}")

    @staticmethod
    def human_sleep(min_delay=1, max_delay=3):
        """Sleep for a specified number of seconds."""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    def close(self):
        """Close the browser and cleanup resources."""
        self.driver.quit()

        