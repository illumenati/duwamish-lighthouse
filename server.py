import bottle
import waitress
import controller


if __name__ == '__main__':
    bottle_app = bottle.app()
    my_controller = controller.Controller(bottle_app)
    waitress.serve(bottle_app, host='0.0.0.0', port=7000)
