from main.services.service_interface import Service
from main.config.settings import mapUrl
import requests


class Items(Service):
    def load_map_url(self, ids):
        self.map_url_item = next((item for item in mapUrl if item['name'] == 'items'), None)
        self.url = self.map_url_item['url']
        self.method = self.map_url_item['method']
        self.params = {'ids':ids,'attributes':self.map_url_item['attributes']}

    def run(self):
        self.response = requests.request(
            method=self.method,
            url=self.url,
            params=self.params
        ).json()
