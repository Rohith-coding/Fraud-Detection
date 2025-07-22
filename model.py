import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train_model():
    # Load data
    data = pd.read_csv('data/transactions.csv')
    # Encode Category
    le = LabelEncoder()
    data['Category'] = le.fit_transform(data['Category'])
    # Save the label encoder
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
    # Features and target
    X = data[['Amount', 'Category']]
    y = data['IsFraud']
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save model
    with open('fraud_model.pkl', 'wb') as f:
        pickle.dump(model, f)

def load_model():
    if os.path.exists('fraud_model.pkl'):
        with open('fraud_model.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        train_model()
        with open('fraud_model.pkl', 'rb') as f:
            return pickle.load(f)

def load_label_encoder():
    with open('label_encoder.pkl', 'rb') as f:
        return pickle.load(f)

def predict_fraud(amount, category):
    model = load_model()
    le = load_label_encoder()
    # Encode category
    category_encoded = le.transform([category])[0]
    prediction = model.predict([[amount, category_encoded]])
    return prediction[0]