from configparser import ConfigParser

class Config():
    def __init__(self):
        self.host = self.get_param('flask', 'host')
        self.port = int(self.get_param('flask', 'port'))

    def get_param(self, section, param):
        """
        """
        config_file = "config.ini"
        conf = ConfigParser()
        conf.read(config_file)
        value = conf.get(section, param)
        return value
