import configparser


class ConfigManager:
    def __init__(self, config_file='config.config'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def read_config(self):
        general_config = self.config['General']
        stream = general_config.get('stream')

        nexmo_config = self.config['Nexmo']
        nexmo_key = nexmo_config.get('key')
        nexmo_secret = nexmo_config.get('secret')
        nexmo_from = nexmo_config.get('from')
        nexmo_to = nexmo_config.get('to')

        email_config = self.config['Email']
        email_address = email_config.get('email_address')
        email_password = email_config.get('email_password')
        email_addressre = email_config.get('email_addressre')

        return  nexmo_key, nexmo_secret, email_address, email_password, email_addressre, nexmo_from, nexmo_to, stream

    def save_config(self, nexmo_key, nexmo_secret, email_address, email_password, email_addressre, nexmo_from, nexmo_to, stream):
        self.config['General'] = {
            'stream': str(stream)
        }
        self.config['Nexmo'] = {
            'key': nexmo_key,
            'secret': nexmo_secret,
            'from': nexmo_from,
            'to': nexmo_to
        }
        self.config['Email'] = {
            'email_address': email_address,
            'email_password': email_password,
            'email_addressre': email_addressre
        }

        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
