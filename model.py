import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

MODEL_PATH = 'fraud_model.pkl'
ENCODER_PATH = 'label_encoder.pkl'
DATA_PATH = 'data/transactions.csv'

def train_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Training data not found at {DATA_PATH}")

    # Load data
    data = pd.read_csv(DATA_PATH)
    
    # Encode Category
    le = LabelEncoder()
    data['Category'] = le.fit_transform(data['Category'])
    
    # Save Label Encoder
    with open(ENCODER_PATH, 'wb') as f:
        pickle.dump(le, f)
    
    # Features and target (2 features only)
    X = data[['Amount', 'Category']]
    y = data['IsFraud']
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save model
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

def load_model():
    try:
        if not os.path.exists(MODEL_PATH):
            print("Model not found, training new model...")
            train_model()
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        # Double check feature count
        if model.n_features_in_ != 2:
            print(f"Model expects {model.n_features_in_} features, retraining...")
            train_model()
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
        return model
    except (EOFError, pickle.UnpicklingError):
        print("Model file corrupted. Retraining...")
        train_model()
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)

def load_label_encoder():
    try:
        if not os.path.exists(ENCODER_PATH):
            print("Label encoder not found, training new model...")
            train_model()
        with open(ENCODER_PATH, 'rb') as f:
            le = pickle.load(f)
        return le
    except (EOFError, FileNotFoundError, pickle.UnpicklingError):
        print("Encoder missing or corrupted. Retraining...")
        train_model()
        with open(ENCODER_PATH, 'rb') as f:
            return pickle.load(f)

def predict_fraud(amount, category):
    model = load_model()
    le = load_label_encoder()

    # Validate category input
    if category not in le.classes_:
        raise ValueError(f"Unknown category '{category}'. Valid categories: {list(le.classes_)}")

    category_encoded = le.transform([category])[0]
    prediction = model.predict([[amount, category_encoded]])
    return prediction[0]
