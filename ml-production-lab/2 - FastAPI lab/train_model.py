from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
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


# Define the model and the remaining preprocessing steps

## Some things to consider during this step:
##    - Some of the data are missing. How can we handle this?
##    - One column (i.e. 'embarked') still needs encoding. How can we do this?
##    - Our features need to be in the same scale. How can we do this?

## This time in the data we have both categorical and numeric features.
## The easiest way to handle this in sklean is to use two transformers, one for each kind.

## Define transformers numerical features
numerical_transformer = Pipeline(steps=[ ... ])  # what preprocessing steps are needed for numerical features?

## Define transformers categorical features
categorical_transformer = Pipeline(steps=[ ... ])  # what preprocessing steps are needed for categorical features?

## Combine both transformers into a ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('numerical', numerical_transformer, X.select_dtypes(include=['number']).columns),
        ('catategorical', categorical_transformer, X.select_dtypes(include=['object']).columns)
    ])

## Define the pipeline for transforming the features + training/inference with the RF model
pipeline = Pipeline(steps=[ ... ])  # what steps does the final pipeline need to contain?


# Train the model
# ...


# Save the model
with open(..., 'wb') as f:
    pickle.dump(..., f)
