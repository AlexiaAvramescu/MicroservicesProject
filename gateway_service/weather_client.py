from microskel.service_discovery import ServiceDiscovery  # interfata
import requests


class WeatherClient:  # TODO: frumos sa fie generate
    def __init__(self, service):
        self.service = service

    def get_weather(self, city, date):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('weather_service')
        if not endpoint:
            return 'No endpoint', 401
        return requests.get(f'{endpoint.to_base_url()}/weather/{city}/{date}').json()