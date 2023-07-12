import json
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