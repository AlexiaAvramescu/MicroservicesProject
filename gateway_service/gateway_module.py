from injector import Module, Binder, singleton
from decouple import config
from events_client import EventsClient
from weather_client import WeatherClient


class GatewayServiceModule(Module):
    def __init__(self, service):
        self.service = service

    def configure(self, binder: Binder) -> None:
        events_client = EventsClient(self.service)
        binder.bind(EventsClient, to=events_client, scope=singleton)

        weather_client = WeatherClient(self.service)
        binder.bind(WeatherClient, to=weather_client, scope=singleton)


def configure_views(app):
    @app.route('/gateway/<city>/<date>')
    def get_events_and_weather(city, date, events_client: EventsClient, weather_client: WeatherClient):
        app.logger.info(f'gateway/{city}/{date} called in {config("MICROSERVICE_NAME")}')
        events = events_client.get_events(city, date) # normal fucntion call a unui alt serviciu
        weather = weather_client.get_weather(city, date)
        my_own_data = f'Data for {city} and {date} from {config("MICROSERVICE_NAME")}'
        return f'{events} AND {weather} AND {my_own_data}'