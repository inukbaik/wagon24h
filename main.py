from selenium import webdriver
from selenium.webdriver.common.by import By
from database import insert_car_data
from config import PHOTO_DIR
import os
import requests
import tweepy
import glob
from dotenv import load_dotenv
import sqlite3

# Load environment variables from .env file
load_dotenv()

# Connect to SQLite database
conn = sqlite3.connect('car_prices.db')
c = conn.cursor()

# Create table for car prices if not exists
c.execute('''CREATE TABLE IF NOT EXISTS car_prices 
             (car_name TEXT, current_bid TEXT, location TEXT, mileage TEXT, link TEXT, timestamp TIMESTAMP)''')

# Fetch necessary environment variables
X_BEARER_TOKEN = os.getenv('BEARER_TKN')
X_API_KEY = os.getenv('API_KEY')
X_API_SECRET_KEY = os.getenv('API_SECRET')
X_ACCESS_TOKEN = os.getenv('ACCESS_TKN')
X_ACCESS_TOKEN_SECRET = os.getenv('ACCESS_SECRET')

# Initialize Tweepy API client
api = tweepy.Client(bearer_token=X_BEARER_TOKEN,
                    access_token=X_ACCESS_TOKEN,
                    access_token_secret=X_ACCESS_TOKEN_SECRET,
                    consumer_key=X_API_KEY,
                    consumer_secret=X_API_SECRET_KEY)

# Initialize OAuth1UserHandler for authentication
auth = tweepy.OAuth1UserHandler(
    X_API_KEY,
    X_API_SECRET_KEY,
    X_ACCESS_TOKEN,
    X_ACCESS_TOKEN_SECRET
)

# Create old_api with the authenticated user
old_api = tweepy.API(auth)

# Format for the tweet and hashtags
TWEET_FORMAT = 'Today\'s wagon. Might end soon so go get your wagon.'
HASHTAGS = "#WagonWednesday #VintageWagon #DailyWagonDeal #ClassicWagon #WagonForSale"

# Configure Chrome options - headless mode and detach
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('detach', True)

# Initialize Chrome webdriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the website
driver.get('https://bringatrailer.com/station-wagon/?q=wagon')

# Extract cars' countdown and links
cars_countdown = driver.find_elements(By.CLASS_NAME, value='countdown-text')
cars_link = [car.get_attribute('href') for car in driver.find_elements(By.CLASS_NAME, value='image-overlay')]

# Count cars with 1 day left or countdown timer
cars_count = sum(1 for time in cars_countdown if time.text == '1 day' or ':' in time.text)

# Check if there are no wagons to post
if cars_count == 0:
    print("No wagons to post")
    driver.quit()
    conn.close()
    exit()

# Limit car links to the ones that are relevant based on countdown
cars_link = cars_link[:cars_count]

# Iterate over each car link
for link in cars_link:
    driver.get(link)

    # Extract car information
    car_name = driver.find_element(By.CLASS_NAME, value='post-title').text
    current_bid = driver.find_element(By.CLASS_NAME, value='info-value').text
    location = driver.find_element(By.XPATH, value='/html/body/main/div/div[3]/div[1]/div[1]/a').text
    mileage = driver.find_element(By.XPATH, value='/html/body/main/div/div[3]/div[1]/div[1]/div[2]/ul/li[2]').text
    ends_in = driver.find_element(By.XPATH, value='/html/body/main/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/strong').text

    # Insert data into the database
    insert_car_data(conn, c, car_name, current_bid, location, mileage, link)

    # Extract main image URL
    image_main = driver.find_element(By.CSS_SELECTOR, value='.post-image')
    image_main_url = image_main.get_attribute('src')

    # Extract additional image URLs
    images_content = driver.find_elements(By.CLASS_NAME, value='alignnone')
    images_content_url = [link.get_attribute('src') for link in images_content]

    # Downloading images
    response = requests.get(image_main_url)
    if response.status_code == 200:
        with open(f'{PHOTO_DIR}/{car_name}_main.jpg', 'wb') as f:
            f.write(response.content)

    for index, image in enumerate(images_content_url):
        response = requests.get(image)
        if response.status_code == 200:
            with open(f'{PHOTO_DIR}/{car_name}_{index + 1}.jpg', 'wb') as f:
                f.write(response.content)

    # Upload images to Twitter
    media1 = old_api.media_upload(f'photos/{car_name}_main.jpg')
    media2 = old_api.media_upload(f'photos/{car_name}_1.jpg')
    media3 = old_api.media_upload(f'photos/{car_name}_2.jpg')

    # Compose and post tweet
    api.create_tweet(text=f'{car_name} in {ends_in}\n'
                          f'Current Bid: {current_bid}\n'
                          f'Location: {location}\n'
                          f'Mileage: {mileage}\n'
                          f'Link: {link}\n\n'
                          f'{HASHTAGS}',
                     media_ids=[media1.media_id, media2.media_id, media3.media_id])

    # Print a message indicating successful posting
    print("Posted Successfully")

    # Remove images after posting
    for file in glob.glob('photos/*.jpg'):
        os.remove(file)

# Quit the driver
driver.quit()

# Commit changes and close connection
conn.commit()
conn.close()
