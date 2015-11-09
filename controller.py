import bottle
from breathe import Breathe
import datetime


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

        # The following routes support manually controlling the pi's breathing
        self.app.route('/get-state', ['GET'], lambda: self.http_get_state())

        self.app.route('/calm', ['GET'], lambda: self.http_breathe(breathe_type='CALM'))
        self.app.route('/erratic', ['GET'], lambda: self.http_breathe(breathe_type='ERRATIC'))
        self.app.route('/stop', ['GET'], lambda: self.http_breathe(breathe_type='STOP'))
        self.app.route('/restart', ['GET'], lambda: self.http_breathe(breathe_type='RESTART'))
        
        self.app.route('/set-calm', ['GET'], lambda: self.http_set_breathe(breathe_state='CALM'))
        self.app.route('/set-erratic', ['GET'], lambda: self.http_set_breathe(breathe_state='ERRATIC'))
        self.app.route('/set-stop', ['GET'], lambda: self.http_set_breathe(breathe_state='STOP'))

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
            self.breather.erratic()
        else:
            self.breather.calm()

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

    # The following are methods to support HTTP requests:
    def http_get_state(self):
        state = self.breather.get_state()
        now = datetime.datetime.now()
        print("Breathe type is:", state, "at", now)
        return bottle.template('The pi breathing state is <b>' + state + '</b> <br>at the time: {{date}}!', date=now)


    def http_breathe(self, breathe_type):
        breathe_types = {
            'CALM': self.breather.calm,
            'ERRATIC': self.breather.erratic,
            'RESTART': self.breather.restart,
            'STOP': self.breather.shutdown
        }
        breathe_types[breathe_type]()
        now = datetime.datetime.now()
        print("Calling breathe type:", breathe_type, "at", now)
        return bottle.template('Your <b>' + breathe_type + '</b> breathing request was started<br>at the time: {{date}}!', date=now)

    def http_set_breathe(self, breathe_state):
        breathe_states = {
            'CALM': self.breather.state.CALM,
            'ERRATIC': self.breather.state.ERRATIC,
            'STOP': self.breather.state.STOP
        }
        self.breather.set_state(breathe_states[breathe_state])
        print("Setting breathe state:", breathe_state)
        return bottle.template('Your <b>' + breathe_state + '</b> breathing state was set<br>at the time: {{date}}!', date=datetime.datetime.now())
