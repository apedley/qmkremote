from flask import Flask, request

from qmkremote import QMKRemote

remote = QMKRemote()
app = Flask(__name__)

@app.route('/')
def index():
    status = remote.status()
    return status


@app.route("/matrix/on")
def matrix_on():
    remote.matrix_on()
    return "matrixon"

@app.route("/matrix/off")
def matrix_off():
    remote.matrix_off()
    return "matrixoff"

@app.route("/matrix/indicator/reset")
def matrix_indicator_reset():
    remote.matrix_indicator_reset()
    return "matrixreset"


@app.route("/matrix/indicator/all")
def matrix_indicator_all():
    r = request.args['r']
    g = request.args['g']
    b = request.args['b']
    
    remote.matrix_indicator_all(int(r), int(g), int(b))
    return "matrixindicatorall"


@app.route("/matrix/indicator/<int:start>/<int:end>")
def matrix_indicator_range(start, end):
    r = request.args['r']
    g = request.args['g']
    b = request.args['b']
    remote.matrix_indicator_range(int(r), int(g), int(b), start, end)
    return "matrixindicatorrange"

if __name__ == '__main__':

	app.run(debug=True)