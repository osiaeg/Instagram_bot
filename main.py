from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import requests
import time

def download_file(url, file_name):
    local_filename = file_name
    # NOTE the stream=True parameter below
    with requests.get(url, stream=False) as r:
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

    actions = ActionChains(driver)

    for _ in range(5):
        video = driver.find_element(By.TAG_NAME, 'video')
        src = video.get_attribute('src')
        print(src)
        video.click()
        time.sleep(2)
        link = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/p'
                ).text
        print(link)
        actions.pause(0.5)
        actions.send_keys(Keys.ESCAPE)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(3)

    url = 'https://v16-webapp.tiktok.com/61ced3b5b6518e7c893109ca9bf7dcca/6230b0c1/video/tos/alisg/tos-alisg-pve-0037c001/bdc6d75e8ffd4fcabfb3e23c6353de9d/?a=1988&br=930&bt=465&cd=0%7C0%7C1%7C0&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&ft=XOQ9-3Fenz7ThD-wiDXq&l=202203150928580102440492151028E759&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&qs=0&rc=ajx2ZTo6ZnhsOzMzODczNEApNjw4ZzZkMzxpN2ZmaTU1NmdfZGozcjRfbzFgLS1kMS1zczZfYzUwM19hX19eLWE0MjM6Yw%3D%3D&vl=&vr='
    download_file(url, 'video_1.mp4')
    print("Video is downloaded.")
    input()
except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()
