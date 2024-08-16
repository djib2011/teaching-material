import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv('https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv')


# Preprocessing

## Drop some irrelevant columns
data = data.drop(['name', 'ticket', 'cabin'], axis=1)

## Manually encode binary variable
data['sex'] = data['sex'].map({'male': 0, 'female': 1})

## Separate target from data
X = data.drop('survived', axis=1)
y = data['survived']

## Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

## Some of the data are missing.How can we handle this?
## ...

## One column (i.e. 'embarked') still needs encoding. How can we do this?
## ...


# Training

## Define a Random Forest model
model = RandomForestClassifier()

## Train the model
## ...


# Save the model
with open(..., 'wb') as f:
    pickle.dump(..., f)
