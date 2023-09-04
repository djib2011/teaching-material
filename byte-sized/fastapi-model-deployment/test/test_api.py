import requests


def test_landing_page():

    r = requests.get('http://localhost:8000')

    assert r.json()['message'] == 'Hello World'


def test_predict():

    payload = {'Location': 'Hyderabad', 'Year': 2008, 'Kilometers_Driven': 90000, 'Fuel_Type': 'Diesel',
               'Transmission': 'Manual', 'Owner_Type': 'Second'}

    r = requests.post('http://localhost:8000/predict', json=payload)

    assert float(r.json()['predictions']) > 0