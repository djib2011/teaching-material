# FastAPI demo

For all the demos below, we'll assume the working directory to be '1 - FastAPI demos'.

## Dummy API

This can mainly be used to see if you have properly setup the environment.

Launch the server with the command:

```
uvicorn dummy_api:app
```

Then open a browser and type the URL http://localhost:8000. You should see the following message:

```
{"message": "Fast API is working!"}
```

## Fruits API

This API is meant to illustrate how we can create endpoints for the two main HTTP methods `GET` and `POST`.

Launch the server with the command:

```
uvicorn fruits_api:app
```

Again, open a browser and type the URL http://localhost:8000. You should see the following message:

```
{"message": "Welcome to the fruit price database!"}
```

In this API we have a couple more endpoints we can access using the browser:
- Go to http://localhost:8000/fruits to see a list of all fruits in the database and their prices.
- Go to http://localhost:8000/fruits/X (where 'X' is the id of a fruit, e.g. 1) to see info for that specific fruit.

We can add a new fruit by making a POST request to http://localhost:8000/fruits

```
curl -X POST "http://localhost:8000/fruits" -H "Content-Type: application/json" -d '{"id": 4, "name": "Banana", "price": 2.0}'
```

or using Python's requests library

```python
import requests

banana = {'id': 4, 'name': 'Banana', 'price': 2.0}

requests.post('http://localhost:8000/fruits', json=banana)
```

Then you can see the new fruit in one of the aforementioned endpoints.

## Model API

This demo is a sample model deployment using FastAPI.

The first step is to actually train the model and store the trained model.
This can be done by running the script `train.py`, however, for ease, the trained model is included as a picle file
as `resources/iris_model.pkl`.

Launch the server with the command:

```
uvicorn model_api:app
```

Open a browser and type the URL http://localhost:8000. You should see the following message:

```
{"message": "Welcome to the iris prediction service!"}
```

We can see the info on the model and the preprocessing steps by visiting the url: http://localhost:8000/model-info

To ask the model to make a prediction we need to make a POST request to the API's `/predict` endpoint.

For example:

```
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"sepal_length": 4.9, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.2}'
```

or equivalently in python:

```python
import requests

sample = {'sepal_length': 4.9,
          'sepal_width': 3.0,
          'petal_length': 1.4,
          'petal_width': 0.2}

response = requests.post('http://localhost:8000/predict', json=dict(zip(f, X_test[1])))

print(response.json())
```