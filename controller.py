import bottle
import breathe


class Controller():
    def __init__(self, app):
        self.app = app
        self.app.route('/data', ['POST'], self.data_route)

        self._data = {
            'temperature': 0.0,
            'salinity': 0.0,
            'oxygen': 0.0
        }
        self.breather = breathe.Breathe()
        self.app.route('/calm', ['GET'], self.breathe_calm)
        self.app.route('/erratic', ['GET'], self.breathe_erratic)
        self.app.route('/stop', ['GET'], self.breathe_stop)
        self.app.route('/restart', ['GET'], self.breathe_restart)

    def data_route(self):
        """
        Looking for json formatted:
        {
            temperature: float
            salinity: float
            oxygen: float
        }
        """
        print('old', self._data)
        json_data = bottle.request.json
        if json_data:
            self._data.update(json_data)
            print(self._data)

        return self._data
    
    def breathe_calm(self):
        print("calm breathing request")
        self.breather.calm()
        return "starting calm breathing...."

    def breathe_erratic(self):
        print("erratic breathing request")
        self.breather.erratic()
        return "starting erratic breathing...."
    
    def breathe_stop(self):
        print("stop breathing request")
        self.breather.shutdown()
        return "stopping breathing..."

    def breathe_restart(self):
        print("restart breathing request")
        self.breather.restart()
        return "restarting calm breathing..."
