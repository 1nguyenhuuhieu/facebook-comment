import configparser

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_tmproxy_api_key(self):
        return self.config.get('TMProxy', 'APIKey', fallback='')

    def get_cookies_account_facebook(self):
        return self.config.get('Cookies', 'AccountFacebook', fallback='')

# Example usage
config = Config('config.ini')
tmproxy_api_key = config.get_tmproxy_api_key()
cookies_account_facebook = config.get_cookies_account_facebook()
print("TMProxy API Key:", tmproxy_api_key)
print("Cookies Account Facebook:", cookies_account_facebook)
