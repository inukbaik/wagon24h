from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
import tweepy
import glob
from dotenv import load_dotenv

PHOTO_DIR = 'photos'

load_dotenv()

X_BEARER_TOKEN = os.getenv('BEARER_TKN')
X_API_KEY = os.getenv('API_KEY')
X_API_SECRET_KEY = os.getenv('API_SECRET')
X_ACCESS_TOKEN = os.getenv('ACCESS_TKN')
X_ACCESS_TOKEN_SECRET = os.getenv('ACCESS_SECRET')

api = tweepy.Client(bearer_token=X_BEARER_TOKEN,
                    access_token=X_ACCESS_TOKEN,
                    access_token_secret=X_ACCESS_TOKEN_SECRET,
                    consumer_key=X_API_KEY,
                    consumer_secret=X_API_SECRET_KEY)

auth = tweepy.OAuth1UserHandler(
    X_API_KEY, X_API_SECRET_KEY, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
)

old_api = tweepy.API(auth)

TWEET_FORMAT = 'Today\'s wagon. Might end soon so go get your wagon.'
HASHTAGS = "#WagonWednesday #VintageWagon #DailyWagonDeal #ClassicWagon #WagonForSale"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://bringatrailer.com/station-wagon/?q=wagon')

cars_count = 0
cars_countdown = driver.find_elements(By.CLASS_NAME, value='countdown-text')
cars_link = [car.get_attribute('href') for car in driver.find_elements(By.CLASS_NAME, value='image-overlay')]

for time in cars_countdown:
    if time.text == '1 day' or ':' in time.text:
        cars_count += 1

cars_link = cars_link[:cars_count]

for link in cars_link:
    driver.get(link)

    # Get info of the car
    car_name = driver.find_element(By.CLASS_NAME, value='post-title').text
    current_bid = driver.find_element(By.CLASS_NAME, value='info-value').text
    location = driver.find_element(By.XPATH, value='/html/body/main/div/div[3]/div[1]/div[1]/a').text
    mileage = driver.find_element(By.XPATH, value='/html/body/main/div/div[3]/div[1]/div[1]/div[2]/ul/li[2]').text
    ends_in = driver.find_element(By.XPATH, value='/html/body/main/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/strong').text

    # Extracting image URLs
    image_main = driver.find_element(By.CSS_SELECTOR, value='.post-image')
    image_main_url = image_main.get_attribute('src')

    images_content = driver.find_elements(By.CLASS_NAME, value='alignnone')
    images_content_url = [link.get_attribute('src') for link in images_content]

    # Downloading images
    response = requests.get(image_main_url)
    if response.status_code == 200:
        with open(f'{PHOTO_DIR}/{car_name}_main.jpg', 'wb') as f:
            f.write(response.content)

    index = 0
    for image in images_content_url:
        response = requests.get(image)
        if response.status_code == 200:
            with open(f'{PHOTO_DIR}/{car_name}_{index + 1}.jpg', 'wb') as f:
                f.write(response.content)
            index += 1

    media1 = old_api.media_upload(f'photos/{car_name}_main.jpg')
    media2 = old_api.media_upload(f'photos/{car_name}_1.jpg')
    media3 = old_api.media_upload(f'photos/{car_name}_2.jpg')

    api.create_tweet(text=f'{car_name} in {ends_in}\n'
                          f'Current Bid: {current_bid}\n'
                          f'Location: {location}\n'
                          f'Mileage: {mileage}\n'
                          f'Link: {link}\n\n'
                          f'{HASHTAGS}',
                     media_ids=[media1.media_id, media2.media_id, media3.media_id])

    for file in glob.glob('photos/*.jpg'):
        os.remove(file)

driver.quit()
