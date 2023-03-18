import re


def process_reader_data(data):
    processed_data = {}
    processed_data['site']=data[0]['site']
    processed_data['ids']=','.join(['{}{}'.format(processed_data['site'],str(sub['id'])) for sub in data])
    return processed_data


def process_database_data(data):
    database_data = []
    for item in data:
        site_id = re.split('(\d+)',item['body']['id'])
        database_data.append(
            {
                'site': site_id[0],
                'id': site_id[1],
                'price': item['body']['price'] if 'price' in item['body'] else None,
                'start_time': item['body']['start_time'] if 'start_time' in item['body'] else None,
                'name': item['body']['name'] if 'name' in item['body'] else None,
                'description': item['body']['description'] if 'description' in item['body'] else None,
                'nickname': item['body']['nickname'] if 'nickname' in item['body'] else None,
                'item_id_error': item['body']['item_id_error'] if 'item_id_error' in item['body'] else None,
                'currency_id_error': item['body']['currency_id_error'] if 'currency_id_error' in item['body'] else None,
                'category_id_error': item['body']['category_id_error'] if 'category_id_error' in item['body'] else None,
                'seller_id_error': item['body']['seller_id_error'] if 'seller_id_error' in item['body'] else None,
            }
        )
    
    return database_data
