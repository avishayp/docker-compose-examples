import requests

endpoint = 'http://lb:8080'


def test_static_file():
    res = requests.get(endpoint)
    assert res.status_code == 200
    assert res.text == 'hello static file'


def test_nginx_trailing():
    for suffix in ('/api', '/api/', '/api?', '/api/?'):
        res = requests.get(endpoint + suffix)
        assert res.status_code == 200
        assert res.text == 'api ok'


def test_echo():
    res = requests.get(endpoint + '/api/echo?mammal=whale')
    assert res.status_code == 200
    assert res.json()['mammal'] == 'whale'
