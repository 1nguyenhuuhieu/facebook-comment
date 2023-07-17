import time
import json
from selenium import webdriver
import configparser
import requests
from selenium.webdriver.chrome.service import Service as ChromeService
class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_tmproxy_api_key(self):
        return self.config.get('TMProxy', 'APIKey', fallback='')

    def get_cookies_account_facebook(self):
        return self.config.get('Cookies', 'AccountFacebook', fallback='')


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
        
def login():
    config = Config('config.ini')
    tmproxy_api_key = config.get_tmproxy_api_key()
    proxy_server = get_proxy(tmproxy_api_key)
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # tắt thông báo và tắt hiển thị hình ảnh (1: on; 2: off)
    prefs = {"profile.default_content_setting_values.notifications": 2,
             "profile.managed_default_content_settings.images": 1
             }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--window-size=360,640")
    chrome_options.add_argument('--proxy-server=' + proxy_server)
    driver = webdriver.Chrome(options=chrome_options)

    time.sleep(3)
    driver.get('https://www.facebook.com')
    time.sleep(3)

    cookies_account_facebook = config.get_cookies_account_facebook()
    cookies_file_path = 'cookies/' + cookies_account_facebook
    try:
        file = open(cookies_file_path)
        cookies = json.load(file)
        file.close()
    except:
        return None
    
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(2)

    return driver
