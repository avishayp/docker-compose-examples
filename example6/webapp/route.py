from datetime import datetime
from flask import jsonify, Blueprint, request

import shared
from shared import log


bp = Blueprint('v1', __name__)
rdb = shared.Raccoon()
q = shared.Q()


@bp.route("/")
def hello():
    return "api ok"


@bp.route("/echo")
def echo():
    return jsonify(request.args)


@bp.route("/health")
def health():
    if shared.is_server_up():
        return jsonify(
            {
                "api": "ok",
                "device_server": shared.send_command("ping").get("command"),
                "device": shared.send_command("get_device_state")
            }
        )

    return jsonify(
        {
            "api": "ok",
            "device_server": "disconnected",
            "device": "n/a"
        }
    )


@bp.route("/halt")
def halt():
    res = shared.send_command("halt")
    return jsonify(res)


@bp.route("/config")
def config():
    res = shared.send_command("get_config", request.args)
    return jsonify(res)


@bp.route("/metadata", methods=["GET", "PUT"])
def metadata():
    uid = request.args.get('id')
    params = request.get_json()
    log.info('metadata %s %s', uid, params)
    res = shared.Record(uid, rdb).update(params)
    return jsonify(res)


@bp.route("/get_device_state")
def get_device_state():
    res = shared.send_command("get_device_state")
    return jsonify(res)


@bp.route("/do_measurement")
def do_measurement():
    params = request.args.to_dict()
    params['ts'] = str(datetime.utcnow())
    try:
        res = shared.send_command("do_measurement", params)
    except Exception as ex:
        log.exception('do_measurement failed')
        return jsonify(
            {
                'command': 'do_measurement',
                'status': {
                    'state': 'error'
                },
                'details': str(ex)
            }
        ), 503

    uid = res.get('id')
    if uid:
        log.info("got new measurement: id %s, params %s", uid, params)
        shared.Record(uid, rdb).update(params)
        q.push(uid)
    else:
        log.error('measurement failed: %s', res)
        return jsonify(res), 503
    return jsonify(res)


@bp.route("/prediction_result")
def prediction_result():
    uid = request.args.get('id')
    record = shared.Record(uid, rdb).get()

    if record is None:
        return jsonify(
            {
                'status': 'error',
                'state': 'id not found',
                'uid': uid
            }
        ), 404
    prediction = record.get('prediction')
    if prediction is None:
        return jsonify({
            'state': 'awaiting',
        })
    else:
        log.info('prediction is: %s', prediction)
        return jsonify({
            'state': 'done',
            'prediction': prediction
        })


@bp.route("/get_measurement_status")
def get_measurement_status():
    uid = request.args.get("id")
    res = shared.Record(uid, rdb).get()
    log.info('get status %s %s', uid, res)
    # Honestly, from the front end perspective,
    # we only care about being done.
    # TODO: Waht if we err here?
    return jsonify({
        'state': 'done'
    })


"""
manage:
GET /manage

{
  "app 1": [
    {
      "app": "Cow Pregnancy",
      "command": "get_measurement_status",
      "cow_type": "Guernsey",
      "email": "avishay.pinsky@gmail.com",
      "flow": "vacuum",
      "id": "a4bf0316-55b1-4a0e-babc-71cfe0a07122",
      "mode": "prediction",
      "past_pregnancies": 0,
      "title": "momooomomom"
    },
    ...
  ],
  "app 2": [
    {
      "app": "True Love",
      "command": "get_measurement_status",
      "email": "avishay.pinsky@gmail.com",
      "flow": "vacuum",
      "id": "3b83ee17-67bb-4608-b61d-0c5cd9e49022",
      "mode": "prediction",
      "partner_1": {
        "age": 23,
        "gender": "Female",
        "title": "bear"
      },
      "partner_2": null,
      "ts": "2018-01-02 01:43:51.622809"
    },
    ...
  ]
}

health:

GET /health
ok:
status: 200
{
  "api": "ok",
  "device": {
    "command": "get_device_state",
    "device_id": "SN004",
    "sensor_id": "10s34",
    "state": "connected",
    "state_info": "idle",
    "temperature": 0
  },
  "device_server": "pong"
}

no sbd:
statuts: 200
{
  "api": "ok",
  "device": "n/a",
  "device_server": "disconnected"
}

no device:
status: 200
{
  "api": "ok",
  "device": {
    "command": "get_device_state",
    "state": "disconnected",
    "state_info": "connect"
  },
  "device_server": "pong"
}

Prediction:
GET /do_measurement?app=[cows|...]
Response:
If successfull:
status: 200
{
    id: 'id from server'
    duration: duration in seconds
}
On error:
Status: 503
disconnected / busy / other...

PUT /metadata?app=...,id=(?),email=
Request:
For cows
{
    title:
    past_pregnancies:
    cow_type:
}
For byo
{
    title:
    description:
}
Response:
Status: 204 / 503

GET  /prediction_result?app=...,.id=,email=
Resonse:
If successfull:
Status: 200
{
    state: 'awaiting' | 'done'
    prediction: True | False
}
On error:
Status: 503
no such id / other error

GET  /status?app=...,id=, email=
Resonse:
If successfull:
Status: 200
{
    state: 'awaiting' | 'done'
}
On error:
Status: 503
"""
