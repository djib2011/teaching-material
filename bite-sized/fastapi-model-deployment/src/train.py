import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
import joblib

dataset_path = 'data/car_price_prediction.csv'
model_output_path = 'models/linear_regression_pipeline.pkl'

df = pd.read_csv(dataset_path, index_col=0).drop(columns=['Name', 'New_Price', 'Engine', 'Power', 'Seats', 'Mileage'])
df.loc[:, df.dtypes == 'O'].astype(str, copy=False)

X = df.drop(['Price'], axis=1).fillna(0)

y = df['Price']

pipe = Pipeline([('encoder', OneHotEncoder()),
                 ('scaler', StandardScaler(with_mean=False)),
                 ('regressor', LinearRegression())])

pipe.fit(X, y)

joblib.dump(pipe, model_output_path)
