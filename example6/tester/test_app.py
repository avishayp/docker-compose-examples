import requests

endpoint = 'http://localhost:8080'


def test_static_file():
    res = requests.get(endpoint)
    assert res.status_code == 200
    assert res.text == 'hello static file'


def test_api():
    res = requests.get(endpoint + '/api')
    assert res.status_code == 200
    assert res.text == 'api ok'

    res = requests.get(endpoint + '/api/echo?mammal=whale')
    assert res.status_code == 200
    assert res.json()['mammal'] == 'whale'
