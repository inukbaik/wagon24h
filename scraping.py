from selenium.webdriver.common.by import By
from selenium import webdriver
import requests


def initialize_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def scrape_wagon_listings(driver, url):
    driver.get(url)
    cars_link = [car.get_attribute('href') for car in driver.find_elements(By.CLASS_NAME, value='image-overlay')]
    return cars_link


def scrape_car_data(driver, link):
    driver.get(link)
    car_details = {
        'car_name': driver.find_element(By.CLASS_NAME, value='post-title').text,
        'current_bid': driver.find_element(By.CLASS_NAME, value='info-value').text,
        'location': driver.find_element(By.XPATH, value='/html/body/main/div/div[3]/div[1]/div[1]/a').text,
        'mileage': driver.find_element(By.XPATH, value='/html/body/main/div/div[3]/div[1]/div[1]/div[2]/ul/li[2]').text,
        'ends_in': driver.find_element(By.XPATH,
                                       value='/html/body/main/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/strong').text,
        'image_main_url': driver.find_element(By.CSS_SELECTOR, value='.post-image').get_attribute('src'),
        'images_content_url': [link.get_attribute('src') for link in
                               driver.find_elements(By.CLASS_NAME, value='alignnone')]
    }
    return car_details
