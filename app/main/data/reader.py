import csv, json
from concurrent.futures import wait
from concurrent.futures import FIRST_COMPLETED
from main.config.settings import config
from main.process.executor import Executor
from main.data.transform import process_reader_data
from main.process.orchestator import process


def read_file(filename):
    with open(filename, newline=config['reader']['newline'], encoding=config['reader']['encoding']) as file:

        if config['reader']['format'] not in {'csv', 'txt', 'jsonl'}:
            print("Formato no soportado. Revisar configuración y archivo.")
            return

        if config['reader']['format'] == 'csv' or config['reader']['format'] == 'txt':
            file = csv.DictReader(file, delimiter=config['reader']['delimiter'])
        
        data = []
        
        child_executor = Executor(int(config['processing']['child_threads']), int(config['processing']['child_queue_size']), "Task Done")

        for line in file:
            if line['site'] and line['id']:
                if config['reader']['format'] == 'jsonl':
                    line = json.loads(line)
                    
                if data:
                    if line['site'] != data[0]['site'] or len(data) == 20:
                        data = process_reader_data(data)
                        child_executor.set_task(process, data)
                        data = []
                data.append(line)
                
            else:
                print('Corrupted line: {}'.format(line))
