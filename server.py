import bottle
import waitress
import controller
import breathe


if __name__ == '__main__':
    bottle_app = bottle.app()
    breather = breathe.Breathe()
    my_controller = controller.Controller(bottle_app, breather)
    waitress.serve(bottle_app, host='0.0.0.0', port=7000)
