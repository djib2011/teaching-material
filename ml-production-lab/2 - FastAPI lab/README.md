# FastAPI lab

In this lab we want to create our own model and deploy it as a REST API. We'll use the same methodology we saw during 
the demo deployment.

## Premise:

We want to make a prediction service for the [titanic dataset](https://www.kaggle.com/c/titanic/data). The idea of this
dataset is to predict if a user survived the shipwreck or not based on several features (age, sex, cabin, etc.)

## Part A: Model training

We want to make a script that trains the model that will be used in our service. The template for this script is called
`train_model.py`.

Some things to consider:
    - Besides training the model we need to perform all preprocessing steps necessary (imputation, encoding, scaling, etc.)
    - These should be performed in such a way so that they will be replicated in the service (e.g. if we encode a feature
a certain way, the exact same encoding should be applied to an incoming request to the service).
    - The easiest way to accomplish this is through the combination of scikit-learn transformers and a pipeline. If built
correctly this will ensure that the same encoding steps that were used during training will be properly applied during inference.
    - In this case, we have both numerical and categorical features. These might require different handling (e.g. 
encoding is only needed for the latter). The easiest way to handle this is to build separate transformers for each feature
type and combine them in the end. See the template script for more details.
    - We also care about the performance of the model. Make sure to evaluate the model on a test set to see if it is good
enough to be used in our service.

## Part B: Service

In this step we will build the actual server that will host the trained model. A template script for the API is called
`titanic_api.py`. You can run the server, either via running the script or through the uvicorn command we used previously.

Some things to consider:
    - Make sure to load the model outside of the prediction endpoints. These are called whenever we receive a request. 
We don't want the model to be loaded each time we want to serve a request; instead the model should be loaded in memory
during all of the server's lifetime, constantly waiting for a request to arrive.
    - The only necessary endpoint is the `/predict` one, i.e. the one that will receive the data and respond with the
model's prediction.
    - This endpoint needs to handle all of the preprocessing steps that we did during training (imputing, encoding, 
scaling, etc.) and call the model for inference. If we used sklearn transformers and pipelines this is significantly
easier, because the preprocessing will be handled automatically. If we used manual preprocessing steps (e.g. pandas)
we will need to make sure that exactly the same steps will be applied to the data of the request.
    - When the server is operating, there is no guarantee on what data we will receive. A request can have missing fields,
missing values (i.e. `None`), wrong data types, wrongly formatted input, illogical data (e.g. age < 0) and more. A good
server design will handle all of these cases.
    - Additionally we can have a series of auxiliary endpoints. For example, we can have one that provides details of
the model used (see the demo in 1 for such an example).

## Part C: Tesing

Once the server is running we need to test it to see if it works. The easiest thing we can do is to make a sample request
to the `/predict` endpoint to make sure it responds correctly.

```python
import requests

data = {'survived': 1, 'pclass': 1, 'name': 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)',
        'sex': 'female', 'age': 38.0, 'sibsp': 1, 'parch': 0, 'ticket': 'PC 17599', 'fare': 71.2833,
        'cabin': 'C85', 'embarked': 'C'}

response = requests.post('http://localhost:8000/predict', json=data)

print(response.json())
```

### Automated testing

There are a few automated tests you can run to test the functionality of the service. These mainly test the `/predict`
endpoint with various inputs (valid and invalid).

To run these tests:

```
python -m pytest test_titanic_api.py
```
