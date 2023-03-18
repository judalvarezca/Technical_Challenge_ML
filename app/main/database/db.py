from pymongo import MongoClient


def get_database():
    from main.config.settings import config
    CONNECTION_STRING = config['database']['connection_string']
    try:
        client = MongoClient(CONNECTION_STRING)
        return client['ml_challenge_python']
    except:
        print('Error connecting to database')
        return None

