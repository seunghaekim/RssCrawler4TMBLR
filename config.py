import json, os

class Config:
    CONFIG_FILE = 'config.json'
    DEFAULT_CONFIG = {
        'rssList': [
            'https://tragedygirlsmovie.tumblr.com/'
        ],
        'downloadFolderName': 'tmblr'
    }

    def __init__(self):
        self.readConfig(self.CONFIG_FILE)
        self.setDownloadFolder(self.config['downloadFolderName'])
        return None

    def readConfig(self, CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as config_raw:
                self.config = json.load(config_raw)
                config_raw.close()
                return True

        except FileNotFoundError as e:
            with open(CONFIG_FILE, 'w') as write_config:
                write_config.write(json.dumps(self.DEFAULT_CONFIG))
                write_config.close()
                print('file wirte done, restart this program')
                return False
        except:
            return None

    def setDownloadFolder(self, downloadFolderName):
        downloadFolder = os.path.join(
            os.path.abspath(__file__),
            downloadFolderName + '/'
        )
        if not os.path.isdir(downloadFolderName):
            try:
                os.makedirs(downloadFolderName)
            except OSError as e:
                print(e)
                return False
        self.config['downloadPath'] = downloadFolder
        return True
