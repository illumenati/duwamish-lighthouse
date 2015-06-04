import bottle
import breathe


# TODO: determine actual thresholds.
PH_THRESHOLD = 0
TEMPERATURE_THRESHOLD = 27.5
OXYGEN_THRESHOLD = 0
CSO_THRESHOLD = 0


class Controller():
    def __init__(self, app):
        print('controller init')
        self.app = app
        self.app.route('/data', ['POST'], self.data_route)

        self._data = {
            'ph': 0.0,
            'temperature': 0.0,
            'salinity': 0.0,
            'oxygen': 0.0,
            'cso_now': 0,
            'cso_recent': 0
        }
        self.breather = breathe.Breathe()
        self.app.route('/calm', ['GET'], self.breathe_calm)
        self.app.route('/erratic', ['GET'], self.breathe_erratic)
        self.app.route('/stop', ['GET'], self.breathe_stop)
        self.app.route('/restart', ['GET'], self.breathe_restart)

    def calculate_breathe_rate(self):
        if self._data['temperature'] > TEMPERATURE_THRESHOLD or self.data['ph'] > PH_THRESHOLD or \
                self._data['oxygen'] > OXYGEN_THRESHOLD or self._data['cso_recent'] > CSO_THRESHOLD or \
                self._data['cso_now'] > CSO_THRESHOLD:
            self.breathe_erratic()
            return

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
