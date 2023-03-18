from main.services.service_interface import Service
from main.config.settings import mapUrl
import requests


class Currencies(Service):
    def load_map_url(self):
        self.map_url_item = next((item for item in mapUrl if item['name'] == 'currencies'), None)
        self.url = self.map_url_item['url']
        self.method = self.map_url_item['method']
        self.params = {'attributes':self.map_url_item['attributes']}

    def run(self, currency_id):
        self.response = requests.request(
            method=self.method,
            url='{}/{}'.format(self.url, currency_id),
            params=self.params
        ).json()