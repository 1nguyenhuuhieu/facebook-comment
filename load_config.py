import configparser

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.api_key = ''
        self.cookies_folder_path = ''

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        self.api_key = config.get('TMProxy', 'APIKey', fallback='')
        self.cookies_folder_path = config.get('Cookies', 'FolderPath', fallback='')

config = Config('config.ini')
config.load_config()

print(config.api_key)
print(config.cookies_folder_path)
