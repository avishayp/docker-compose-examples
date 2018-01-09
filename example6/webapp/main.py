from flask import Flask, jsonify, Blueprint, request

bp = Blueprint('api', __name__)


@bp.route("/")
def hello():
    return "api ok"


@bp.route("/echo")
def echo():
    return jsonify(request.args)


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(bp, url_prefix='/api')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
