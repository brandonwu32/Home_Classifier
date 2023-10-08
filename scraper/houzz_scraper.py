import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=options)

styledict = {"modern": "https://www.houzz.com/photos/modern-exterior-home-ideas-phbr1-bp~t_736~s_2105",
             "contemporary": "https://www.houzz.com/photos/contemporary-exterior-home-ideas-phbr1-bp~t_736~s_2103",
             "ranch": "https://www.houzz.com/photos/traditional-exterior-home-ideas-phbr1-bp~t_736~s_2107",
             "mid-century": "https://www.houzz.com/photos/mid-century-modern-exterior-home-ideas-phbr1-bp~t_736~s_2115",
             "traditional": "https://www.houzz.com/photos/traditional-exterior-home-ideas-phbr1-bp~t_736~s_2107",
             "farmhouse": "https://www.houzz.com/photos/farmhouse-exterior-home-ideas-phbr1-bp~t_736~s_2114",
             "transitional": "https://www.houzz.com/photos/transitional-exterior-home-ideas-phbr1-bp~t_736~s_2112",
             "industrial": "https://www.houzz.com/photos/industrial-exterior-home-ideas-phbr1-bp~t_736~s_2113",
             }

def download_image_url(download_path, url, file_name):
    image_content = requests.get(url).content
    file_path = download_path + file_name
    with open(f"data/{file_path}", "wb") as f:
        f.write(image_content)
    print("Success")

def get_image_url(style, wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    url = (styledict[style])
    wd.get(url)
    image_urls = set()
    length = 0
    skips = 0
    while (length + skips < max_images):
        time.sleep(2)
        scroll_down(wd)
        images = wd.find_elements(By.CLASS_NAME, "hz-photo-card__img")
        for image in images:
            if image in image_urls:
                skips += 1
                max_images += 1
                length += 1
            if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                image_urls.add(image.get_attribute('src'))
                length += 1
                print(length)
    return image_urls

for style in styledict:
    urls = get_image_url(style, driver, 2, 20)
    index = 0
    for i in urls:
        download_image_url("",i, f"{style}-{index}.jpg")
        index += 1

driver.quit()
