from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

fruits_db = [
    {'id': 1, 'name': 'Apple', 'price': 1.50},
    {'id': 2, 'name': 'Orange', 'price': 0.89},
    {'id': 3, 'name': 'Apricot', 'price': 2.50},
]


class Fruit(BaseModel):
    id: int
    name: str
    price: float


@app.get('/')
async def root():
    """
    Root endpoint
    """
    return {'message': 'Welcome to the fruit price database!'}


@app.get('/fruits', response_model=List[Fruit])
async def get_fruits():
    """
    Get all available fruits
    """
    return fruits_db


@app.get('/fruits/{fruit_id}', response_model=Fruit)
async def get_fruit(fruit_id: int):
    """
    Get a fruit by its id
    """
    fruit = next((fruit for fruit in fruits_db if fruit['id'] == fruit_id), None)
    if fruit is None:
        raise HTTPException(status_code=404, detail='Fruit not found')
    return fruit


@app.post('/fruits', response_model=Fruit)
async def create_fruit(fruit: Fruit):
    """
    Add a new fruit to the list
    """
    fruits_db.append(fruit.dict())
    return fruit
