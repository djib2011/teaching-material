import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import pickle
import os

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

## Define transformers numerical features
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

## Define transformers categorical features
categorical_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(sparse_output=False)),
    ('scaler', StandardScaler())
])

## Combine both transformers into a ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('numerical', numerical_transformer, X.select_dtypes(include=['number']).columns),
        ('catategorical', categorical_transformer, X.select_dtypes(include=['object']).columns)
    ])

## Define the pipeline for transforming the features + training/inference with the RF model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestClassifier())
])

# Training
pipeline.fit(X_train, y_train)


# Evaluation
print(classification_report(y_test, pipeline.predict(X_test)))


# Save the model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'resources/titanic_model.pkl')
print(f'Saving trained model in {model_path}')

with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)
