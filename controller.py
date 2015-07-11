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
        # Is there a way to pass in params to a function here? Ie "self.http_request('calm')"? Perhaps via keyword arguments?
        self.app.route('/calm', ['GET'], self.http_calm)
        self.app.route('/erratic', ['GET'], self.http_erratic)
        self.app.route('/stop', ['GET'], self.http_stop)
        self.app.route('/restart', ['GET'], self.http_restart)
        
        self.app.route('/set-calm', ['GET'], self.http_set_calm)
        self.app.route('/set-erratic', ['GET'], self.http_set_erratic)
        self.app.route('/set-off', ['GET'], self.http_set_off)

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
        print("calm breathing")
        self.breather.calm()

    def breathe_erratic(self):
        print("erratic breathing")
        self.breather.erratic()

    def breathe_stop(self):
        print("stop breathing")
        self.breather.shutdown()

    def breathe_restart(self):
        print("restart breathing")
        self.breather.restart()

    # The following are methods to support HTTP requests:

    def http_calm(self):
        self.breathe_calm()
        return self.http_response('Your <b>calm</b> breathing request was received<br>at the time: {{date}}!')
    
    def http_erratic(self):
        self.breathe_erratic()
        return self.http_response('Your <b>erratic</b> breathing request was received<br>at the time: {{date}}!')
    
    def http_stop(self):
        self.breathe_stop()
        return self.http_response('Your <b>stop</b> breathing request was received<br>at the time: {{date}}!')
    
    def http_restart(self):
        self.breathe_restart()
        return self.http_response('Your <b>restart</b> breathing request was received<br>at the time: {{date}}!')
    
    def http_set_calm(self):
        self.breather.set(self.breather.state.CALM)
        return self.http_response('Your <b>set calm</b> breathing request was received<br>at the time: {{date}}!')
    
    def http_set_erratic(self):
        # self.breathe_restart()
        self.breather.set(self.breather.state.ERRATIC)
        return self.http_response('Your <b>set erratic</b> breathing request was received<br>at the time: {{date}}!')
    
    def http_set_off(self):
        self.breather.set(self.breather.state.OFF)
        return self.http_response('Your <b>set off</b> breathing request was received<br>at the time: {{date}}!')
        
    def http_response(self, message):
        print("returning http response:", message)
        now = datetime.datetime.now()
        return bottle.template(message, date=now)
