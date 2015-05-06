import bottle


class Controller():
    def __init__(self, app):
        self.app = app
        self.app.route('/data', ['POST'], self.data_route)

        self._data = {
            'temperature': 0.0,
            'salinity': 0.0,
            'oxygen': 0.0
        }

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