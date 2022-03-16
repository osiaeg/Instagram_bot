from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import requests
import csv
import time
import os
from tqdm import tqdm

class Video:

    def __init__(self, name: str, src: str, link: str, action_item: dict) -> None:
        self.name = name
        self.src = src
        self.link = link
        self.action_item = action_item

    def info(self) -> dict:
        output = {
                'name': self.name,
                'src': self.src,
                'link': self.link
                }
        output.update(self.action_item)
        return output


def download_file(url, file_name) -> str:
    if not os.path.exists('videos'):
        os.mkdir('videos')

    local_filename = f'videos/{file_name}'
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    return local_filename

gecko_log_path = 'firefox_driver/geckodriver.log'
gecko_path = 'firefox_driver/geckodriver'

s = Service(
        gecko_path,
        log_path = gecko_log_path
        )

o = Options()
o.headless = False
try:
    driver = webdriver.Firefox(service = s, options = o)
    driver.get("https://www.tiktok.com/")
    time.sleep(5)

    actions = ActionChains(driver, duration=250)

    video_collection = []
    for i in range(5):
        video = driver.find_element(By.TAG_NAME, 'video')
        like_count = driver.find_elements(By.XPATH, "//strong[@data-e2e='like-count']")
        comment_count = driver.find_elements(By.XPATH, "//strong[@data-e2e='comment-count']")
        share_count = driver.find_elements(By.XPATH, "//strong[@data-e2e='share-count']")
        src = video.get_attribute('src')

        video.click()

        time.sleep(2)
        link = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/p'
                ).text

        actions.pause(0.5)
        actions.send_keys(Keys.ESCAPE)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()

        action_items = {
                'like_count': like_count[i].text,
                'comment_count': comment_count[i].text,
                'share_count': share_count[i].text
                }
        video_collection.append(Video(f'tiktok_{i}.mp4', src, link, action_items))
        time.sleep(8)

    for video in tqdm(video_collection):
        download_file(video.src, video.name)

    print('Download complete.')


    with open('tiktok_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'like_count', 'comment_count', 'share_count', 'src', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in video_collection:
            writer.writerow(item.info())

    input()
except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()
