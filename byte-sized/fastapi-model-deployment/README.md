# FastAPI model deployment roadmap

## Part A. Introduction

1. What do we mean by model deployment?
    - What are REST APIs
    - How do you communicate with the model
    - Notion of a microservice

2. Describe tech stack
    - Pandas, scikit-learn and DS stack
    - FastAPI, uvicorn and APIs
    - Pytest (TDD in general)

3. Preliminary dev work
   - Sketch out project structure
   - Install prerequisites

## Part B. REST services and FastAPI

1. Build bare bone FastAPI server
   - Build FastAPI server with 1 couple of `get` endpoints.
   - Access endpoints through browser
   - Send request through postman
   - Use python requests library
   - Build test for endpoint(s)

2. Build a dummy endpoint for predictions
   - Create data model
   - Create endpoint
   - Send sample post request (python)
   - Build test for endpoint

## Part C. Build the ML model

- We start from the point where a typical DS class ends. We have built and tested a full ML model.
- Load and preprocess data with pandas
- Explain that the same preprocessing needs to happen both in training and in actual requests
- Explain how this would happen in some cases like feature scaling and one-hot encoding
- Explain scikit-learn pipelines
- Explain model (i.e. pipeline in general) serialization

## Part D. Complete service

- Load model in FastAPI server
- Modify endpoint to preprocess the data accordingly and feed it to the model
- Return (and decode if necessary) the request
