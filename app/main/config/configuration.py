import configparser, json


def read_config():
    config = configparser.ConfigParser()
    config.read('app/main/config/config.ini')
    return config


def read_map_url():
    return json.load(open('app/main/config/map_url.json'))

