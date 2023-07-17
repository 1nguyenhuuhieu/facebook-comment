import time
import json
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import requests
from datetime import datetime

import sqlite3
   
def is_post_id_unique(post_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Execute a SELECT query to check if the post_id exists in the database
    cursor.execute('SELECT post_id FROM records WHERE post_id = ?', (post_id,))
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Return True if the post_id is unique (not found in the database), False otherwise
    return result is None

def load_config(file_path):
    with open(file_path, 'r') as json_file:
        config_data = json.load(json_file)
    return config_data

config_file = 'config.json'  # Path to your JSON config file
config_data = load_config(config_file)
# config cookie and proxy
# file json cookie
# tạo json cookies sử dụng extensions "クッキーJSONファイル出力 for Puppeteer" https://chrome.google.com/webstore/detail/%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BCjson%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%87%BA%E5%8A%9B-for-puppet/nmckokihipjgplolmcmjakknndddifde
cookie_file_path = config_data['cookie']
# sử dụng https proxy server no authentication

tmp_proxy_apikey = config_data['api_key']
group_fb_id = config_data['groups']
limit_loop = int(config_data['total_comment'])
image = config_data['image']
comment = config_data['comment']

def get_current_timestamp():
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    return timestamp


def save_to_database(timestamp, post_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Create the 'records' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS records
                      (timestamp TEXT, post_id TEXT)''')

    # Insert the data into the 'records' table
    cursor.execute('INSERT INTO records VALUES (?, ?)', (timestamp, post_id))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()



def get_proxy(tmp_proxy_apikey):
    url_new_proxy = "https://tmproxy.com/api/proxy/get-new-proxy"
    url_current_proxy = "https://tmproxy.com/api/proxy/get-current-proxy"
    new_proxy_json = {
    "api_key": tmp_proxy_apikey,
    "sign": "string",
    "id_location": 0
    }
    current_proxy_json = {
    "api_key": tmp_proxy_apikey
    }
    r = requests.post(url_new_proxy, json=new_proxy_json)
    if r.json()['data']['https']:
        proxy =  r.json()['data']['https']
        return proxy
    else:
        r = requests.post(url_current_proxy, json=current_proxy_json)
        if r.json()['data']['https']:
            proxy =  r.json()['data']['https']
            return proxy
        else:
            print("Lỗi, không lấy được proxy")
            return None
     

# random spam comment class
class CommentRandom:
    def __init__(self):
        sender = random.choice(senders)
        greeting = random.choice(greetings)
        receiver = random.choice(receivers)
        introduction = random.choice(introductions)
        introduction = introduction.replace(':place_holder:', sender)
        ad = random.choice(ads)
        contact_me = random.choice(contacts_me)
        contact_me = f'{contact_me} {sender.lower()}'
        contact_info = random.choice(contacts_info)
        goodbye = random.choice(goodbyes)
        comment = f'{sender} {greeting} {receiver}. {introduction} {ad}. {contact_me} {contact_info}. {goodbye}'

        image_name = random.choice(os.listdir(images_directory))
        image = os.path.abspath(f'{images_directory}/{image_name}')

        self.comment = comment
        self.image = image


class Comment:
    def __init__(self, comment, image):
        self.comment = comment
        self.image = image


def init_driver(proxy_server):
    mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # tắt thông báo và tắt hiển thị hình ảnh (1: on; 2: off)
    prefs = {"profile.default_content_setting_values.notifications" : 2,
            "profile.managed_default_content_settings.images": 1
    }
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument("--window-size=360,640")
    chrome_options.add_argument('--proxy-server=' + proxy_server)
    driver = webdriver.Chrome(options=chrome_options)

    return driver

def load_cookies_fromfile(cookies_file_path):
    try:
        file = open(cookies_file_path)
        cookies = json.load(file)
        file.close()
        return cookies
    except:
        return None

def load_cookies(driver, cookies):
    driver.get('https://www.facebook.com')
    time.sleep(2)
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.get('https://www.facebook.com')
    
    return True

    
# spam 1 comment vào post, 3 comment vào 3 top reply    
def comment_on_post(comment):
    time.sleep(2)
    comment_switcher = driver.find_element(By.NAME, "comment_switcher")
    select = Select(comment_switcher)
    select.select_by_value('most_engagement')
    time.sleep(3)
    comment_input = driver.find_element(By.ID, "composerInput")
    comment_input.send_keys(comment.comment)
    try:
        image_input = driver.find_element(By.XPATH, "//input[@type='file']")
        image_input.send_keys(comment.image)
        time.sleep(10)
    except:
        pass
    time.sleep(2)
    submit_btn = driver.find_element(By.NAME, "submit")

    submit_btn.click()

    time.sleep(3)
    try:
        top_comments = driver.find_elements(By.LINK_TEXT, "Phản hồi")
        if len(top_comments) > 10:
            top_comments[1].click()
            time.sleep(2)
            comment_inputs = driver.find_elements(By.TAG_NAME, "textarea")
            comment = Comment()
            comment_inputs[1].send_keys(comment.comment)
            try:
                image_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
                image_inputs[1].send_keys(comment.image)
                time.sleep(10)
            except:
                pass
            submit_btns = driver.find_elements(By.NAME, "submit")
            submit_btns[1].click()
            time.sleep(3)
    except:
        pass

    return True


if __name__ == "__main__":

    proxy_server = get_proxy(tmp_proxy_apikey)
    driver = init_driver(proxy_server)
    cookies = load_cookies_fromfile(cookie_file_path)
    is_logged = load_cookies(driver, cookies)

    # nếu đăng nhập thành công
    if is_logged:
        driver.get('https://www.facebook.com')
        # go to facebook group
        while limit_loop > 0:
            driver.get(f'https://www.facebook.com/groups/{group_fb_id}')
            time.sleep(5)
            try:
                comment_links = WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements(By.LINK_TEXT, "Bình luận"))
                for post in comment_links:
                    post_link = post.get_attribute('href')
                    post_link_split = post_link.split("/")
                    post_id = post_link_split[6]
                    unique = is_post_id_unique(post_id)
                    if unique:
                        try:
                            post.click()
                            time.sleep(3)
                            comment = Comment(comment, image)
                            is_commented = comment_on_post(comment)
                            timestamp = get_current_timestamp()
                            print(f'{timestamp}. Post ID: {post_id}')
                            save_to_database(timestamp, post_id)
                            limit_loop -= 1
                        except:
                            pass
            except:
                pass

            time.sleep(2)



