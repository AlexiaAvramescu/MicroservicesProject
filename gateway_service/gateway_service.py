from microskel.service_template import ServiceTemplate
import events_client
import weather_client
import gateway_module


class GatewayService(ServiceTemplate):

    def get_modules(self):
        return super().get_modules() + [gateway_module.GatewayServiceModule(self)]

    def get_python_modules(self):
        return super().get_python_modules() + [gateway_module]

    def custom_function(self, name):  # ca si exemplu
        data = self.injector.get(events_client.EventsClient).get_events(name)
        return data


if __name__ == '__main__':
    GatewayService().start()