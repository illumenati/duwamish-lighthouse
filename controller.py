import bottle
from breathe import Breathe


PH_THRESHOLD_LOWER = 6.5
PH_THRESHOLD_HIGHER = 8.5
TEMPERATURE_THRESHOLD = 18
OXYGEN_THRESHOLD = 8
CSO_THRESHOLD = 0


class Controller:
    def __init__(self, app, breather):
        print('controller init')
        self.app = app
        self._breather = breather
        self.app.route('/data', ['POST'], self.data_route)

        self._data = {
            'ph': 0.0,
            'temperature': 0.0,
            'oxygen': 0.0,
            'cso_now': 0,
            'cso_recent': 0
        }

        self.app.route('/calm', ['GET'], self.breathe_calm)
        self.app.route('/erratic', ['GET'], self.breathe_erratic)
        self.app.route('/stop', ['GET'], self.breathe_stop)
        self.app.route('/restart', ['GET'], self.breathe_restart)

    @property
    def breather(self) -> Breathe:
        return self._breather

    @property
    def bad_ph(self):
        return self._data['ph'] < PH_THRESHOLD_LOWER or self._data['ph'] > PH_THRESHOLD_HIGHER

    @property
    def bad_temp(self):
        return self._data['temperature'] > TEMPERATURE_THRESHOLD

    @property
    def bad_oxygen(self):
        return self._data['oxygen'] > OXYGEN_THRESHOLD

    @property
    def bad_cso(self):
        return self._data['cso_recent'] > CSO_THRESHOLD or self._data['cso_now'] > CSO_THRESHOLD

    @property
    def is_erratic(self):
        return self.bad_ph or self.bad_cso or self.bad_oxygen or self.bad_temp

    def calculate_breathe_rate(self):
        if self.is_erratic:
            self.breathe_erratic()
        else:
            self.breathe_calm()

    def data_route(self):
        """
        Looking for json formatted:
        {
            temperature: float
            salinity: float
            oxygen: float
        }
        """
        json_data = bottle.request.json

        if json_data:
            self._data.update(json_data)
            self.calculate_breathe_rate()
            print('Data Received!')
            print(self._data)
        else:
            print('No JSON data received!')

        return self._data
    
    def breathe_calm(self):
        print("calm breathing request")
        self.breather.calm()

    def breathe_erratic(self):
        print("erratic breathing request")
        self.breather.erratic()

    def breathe_stop(self):
        print("stop breathing request")
        self.breather.shutdown()

    def breathe_restart(self):
        print("restart breathing request")
        self.breather.restart()
