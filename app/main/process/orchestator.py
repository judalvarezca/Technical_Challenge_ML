from main.services.categories.service import Categories
from main.services.currencies.service import Currencies
from main.services.items.service import Items
from main.services.users.service import Users
from main.services.service_interface import Service
from main.database.db import get_database
from main.data.transform import process_database_data


def process(processData):
    database = get_database()
    if database is None:
        return

    item_request = Items()
    item_request.load_map_url(processData['ids'])
    item_request.run()

    for response in item_request.response:
        if response['code'] == 200:
            if('currency_id' in response['body']): 
                response['body'].update(make_request(Currencies, response['body']['currency_id'], 'currency_id'))
            if('category_id' in response['body']):
                response['body'].update(make_request(Categories, response['body']['category_id'], 'category_id'))
            if('seller_id' in response['body']):
                response['body'].update(make_request(Users, response['body']['seller_id'], 'seller_id'))

        else:
            response['body']={
                'id': response['body']['id'],
                'item_id_error': True
            }
        
    database_data = process_database_data(item_request.response)
    database['ml-challenge-python'].insert_many(database_data)


def make_request(request_object: Service, data, key):
    request = request_object()
    request.load_map_url()
    request.run(data)
    if not 'error' in request.response:
        return request.response
    else:
        return {'{}_error'.format(key): True}


def start_process(main_executor):
    from main.data.reader import read_file
    from main.config.settings import config
    main_executor.set_task(read_file, config['file']['filename'])
