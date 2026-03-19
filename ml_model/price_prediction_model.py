import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

class PricePredictor:
    def __init__(self, model_path='price_model.pkl'):
        self.model_path = os.path.join(os.path.dirname(__file__), model_path)
        self.model = None
        self._load_or_train_model()

    def _load_or_train_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except:
                self._train_model()
        else:
            self._train_model()

    def _train_model(self):
        # Load dummy data
        dataset_path = os.path.join(os.path.dirname(__file__), 'dataset', 'dummy_data.csv')
        if not os.path.exists(dataset_path):
            print("Dataset not found, skipping training.")
            return

        df = pd.read_csv(dataset_path)
        X = df[['location', 'bhk', 'area', 'property_type']]
        y = df['price']

        categorical_features = ['location', 'property_type']
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')

        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features)
            ], remainder='passthrough')

        self.model = Pipeline(steps=[('preprocessor', preprocessor),
                                     ('regressor', LinearRegression())])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        joblib.dump(self.model, self.model_path)

    def predict(self, location, bhk, area, property_type):
        if not self.model:
            return None
        
        data = pd.DataFrame({
            'location': [location],
            'bhk': [bhk],
            'area': [area],
            'property_type': [property_type]
        })
        
        prediction = self.model.predict(data)
        return prediction[0]

# Singleton instance
predictor = PricePredictor()
