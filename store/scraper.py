from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import re


from selenium.webdriver.common.service import Service

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

class GoogleMapScraper:
    def __init__(self):
        self.output_file_name = "business_data001.csv"
        self.headless = False
        self.driver = None
        self.unique_check = []

    def config_driver(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        s = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=options)
        self.driver = driver

    def infinite_scroll(self):
        start_time = time.time()
        while time.time() - start_time < 180:  # Scroll for 120 seconds
            try:
                els = self.driver.find_elements(By.CSS_SELECTOR, '.TFQHme')
                if not els:
                    break

                self.driver.execute_script("arguments[0].scrollIntoView();", els[-1])
                time.sleep(3)  # Adjust sleep duration as needed

            except StaleElementReferenceException:
                # Possible to get a StaleElementReferenceException. Ignore it and retry.
                pass

    def save_data(self, data):
        header = ['name', 'rating', 'reviews_count', 'address', 'category', 'contact', 'website', 'coord']
        with open(self.output_file_name, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if data[0] == 1:
                writer.writerow(header)
            writer.writerow(data)

    def parse_contact(self, business):
        try:
            contact = business.find_elements(By.CLASS_NAME, "W4Efsd")[3].text.split("·")[-1].strip()
        except:
            contact = ""
        return contact

    def parse_rating_and_review_count(self, business):
        try:
            reviews_block = business.find_element(By.CLASS_NAME, 'AJB7ye').text.split("(")
            rating = reviews_block[0].strip()
            reviews_count = reviews_block[1].split(")")[0].strip()
        except:
            rating = ""
            reviews_count = ""
        return rating, reviews_count

    def parse_address_and_category(self, business):
        try:
            address_block = business.find_elements(By.CLASS_NAME, "W4Efsd")[2].text.split("·")
            if len(address_block) >= 2:
                address = address_block[1].strip()
                category = address_block[0].strip()
            elif len(address_block) == 1:
                address = ""
                category = address_block[0]
        except:
            address = ""
            category = ""
        return address, category

    def get_business_info(self):
        time.sleep(2)
        for business in self.driver.find_elements(By.CLASS_NAME, 'THOPZb'):
            name = business.find_element(By.CLASS_NAME, 'fontHeadlineSmall').text
            rating, reviews_count = self.parse_rating_and_review_count(business)
            address, category = self.parse_address_and_category(business)
            contact = self.parse_contact(business)
            try:
                website = business.find_element(By.CLASS_NAME, "lcr4fd").get_attribute("href")
                coord_href = business.find_element(By.CLASS_NAME, "hfpxzc").get_attribute("href")

                # Extract latitude and longitude from the coord_href using regular expression
                coord_match = re.search(r'\/data=!4m7.*?3d([\d.]+).*?4d([-.\d]+)', coord_href)

                if coord_match:
                    latitude = float(coord_match.group(1))
                    longitude = float(coord_match.group(2))
                    coord = f"{latitude},{longitude}"
                else:
                    coord = ""

            except NoSuchElementException:
                website = ""
                coord = ""

            unique_id = "".join([name, rating, reviews_count, address, category, contact, website, coord])
            if unique_id not in self.unique_check:
                data = [name, rating, reviews_count, address, category, contact, website, coord]
                self.save_data(data)
                self.unique_check.append(unique_id)

    def load_companies(self, url):
        print("Getting business info", url)
        self.driver.get(url)
        time.sleep(10)

        # Use the infinite_scroll method of the class
        self.infinite_scroll()

        # Wait for a few seconds to ensure all content is loaded before scraping
        time.sleep(5)

        # Get business info after scrolling
        self.get_business_info()

        # Close the browser after completing the scraping
        self.driver.quit()