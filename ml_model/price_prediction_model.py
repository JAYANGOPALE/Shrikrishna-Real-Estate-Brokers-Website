import csv
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
                return
            except Exception as e:
                print(f"Error loading model: {e}")
        
        # If we reach here, we train in memory but DO NOT save to disk (for Vercel compatibility)
        self._train_model()

    def _train_model(self):
        dataset_path = os.path.join(os.path.dirname(__file__), 'dataset', 'dummy_data.csv')
        if not os.path.exists(dataset_path):
            print("Dataset not found, skipping training.")
            return

        try:
            X = []
            y = []
            with open(dataset_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    X.append([row['location'], int(row['bhk']), float(row['area']), row['property_type']])
                    y.append(float(row['price']))

            categorical_features = [0, 3]
            categorical_transformer = OneHotEncoder(handle_unknown='ignore')
            preprocessor = ColumnTransformer(
                transformers=[('cat', categorical_transformer, categorical_features)], 
                remainder='passthrough'
            )

            self.model = Pipeline(steps=[('preprocessor', preprocessor),
                                         ('regressor', LinearRegression())])
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)
            
            # NOTE: Removed joblib.dump to prevent "Read-only file system" error on Vercel
            print("Model trained in memory.")
        except Exception as e:
            print(f"Training failed: {e}")

    def predict(self, location, bhk, area, property_type):
        if not self.model:
            return 0.0
        try:
            data = [[location, int(bhk), float(area), property_type]]
            prediction = self.model.predict(data)
            return float(prediction[0])
        except:
            return 0.0

# Singleton instance
predictor = PricePredictor()
