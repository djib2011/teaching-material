from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import pickle
import os

# Load data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

# Define preprocessors
sc = StandardScaler()
# Note: A scaler is not technically needed in this case, we'll just use it to illustrate a preprocessing step

# Define model
model = RandomForestClassifier(n_estimators=100)

# Define pipeline that includes preprocessing steps and model
pipeline = Pipeline([('scaler', sc),
                     ('model', model)])

# Execute the preprocessing steps and train the model
pipeline.fit(X_train, y_train)

# Save the pipeline with the preprocessors and the trained model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'resources/iris_model.pkl')
print(f'Saving trained model in {model_path}')

with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)
