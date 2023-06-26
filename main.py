from selenium import webdriver
import time
import json
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

# config cookie and proxy
# file json cookie
# tạo json cookies sử dụng extensions "クッキーJSONファイル出力 for Puppeteer" https://chrome.google.com/webstore/detail/%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BCjson%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%87%BA%E5%8A%9B-for-puppet/nmckokihipjgplolmcmjakknndddifde
cookie_file_path = 'cookies/account1.json'
# sử dụng https proxy server no authentication
proxy_server = '116.110.89.46:28299'
group_fb_id = '412480393057189'

senders = ['Em', 'Mình', 'Tớ', 'Tôi', 'Tui']
greetings = ['xin chào', 'chào', 'chào các' , 'hello', 'alo', 'xin phép']
receivers = ['anh/chị', 'bạn', 'anh', 'chị', 'mọi người']
introductions = ['hiện nay bên :place_holder: có sẵn', ':place_holder: đang có' , ':place_holder: triển khai dịch vụ', ':place_holder: cung cấp sản phẩm', ':place_holder: nhận' ]
ads = ['áo phông', 'giày dép', 'tivi', 'tủ lạnh']
contacts_me = ['vui lòng liên hệ', 'thông tin liên lạc', 'ưu đãi tại']
contacts_info = ['09123456789', 'shopee.vn', 'nguyenvanmanh@gmail.com']
goodbyes = ['Xin cảm ơn đã xem', 'Rất vui lòng được liên hệ', 'Chúc một ngày tốt lành']
images_directory =  'images/'

# random spam comment class
class Comment:
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
    # chrome_options.add_argument('--proxy-server=' + proxy_server)
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
    if True:
        return True
    else:
        return False
    
# spam 1 comment vào post, 3 comment vào 3 top reply    
def comment_on_post():
    time.sleep(2)
    comment_switcher = driver.find_element(By.NAME, "comment_switcher")
    select = Select(comment_switcher)
    select.select_by_value('most_engagement')
    time.sleep(3)
    comment_input = driver.find_element(By.ID, "composerInput")
    comment = Comment()
    print(comment.comment)
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

    return True


if __name__ == "__main__":
    spamed_post = []
    driver = init_driver(proxy_server)
    cookies = load_cookies_fromfile(cookie_file_path)
    is_logged = load_cookies(driver, cookies)

    # nếu đăng nhập thành công
    if is_logged:
        driver.get('https://www.facebook.com')
        time.sleep(2)
        # go to facebook group
        while True:
            driver.get(f'https://www.facebook.com/groups/{group_fb_id}')
            time.sleep(5)
            try:
                comment_links = WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements(By.LINK_TEXT, "Bình luận"))
                for post in comment_links:
                    post_link = post.get_attribute('href')
                    post_link_split = post_link.split("/")
                    post_id = post_link_split[6]
                    if post_id not in spamed_post:
                        spamed_post.append(post_id)
                        print(post_id)
                        post.click()
                        time.sleep(3)
                        is_commented = comment_on_post()
                        break
            except:
                pass


