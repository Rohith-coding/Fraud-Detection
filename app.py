from flask import Flask, render_template, request
import pandas as pd
from model import predict_fraud
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Verify file exists
    if not os.path.exists('data/transactions.csv'):
        raise FileNotFoundError("transactions.csv not found in data/ folder")
    # Load demo transactions
    data = pd.read_csv('data/transactions.csv')
    data = data[['TransactionID', 'Amount', 'Category', 'Date', 'IsFraud']]
    transactions = data.to_dict('records')
    return render_template('index.html', transactions=transactions)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        amount = float(request.form['amount'])
        category = request.form['category']
        print(f"Received amount: {amount}, category: {category}")  # Debug log
        # Predict fraud
        prediction = predict_fraud(amount, category)
        result = 'Fraudulent' if prediction == 1 else 'Non-Fraudulent'
        return render_template('results.html', amount=amount, category=category, result=result)
    except Exception as e:
        print(f"Error in /predict: {str(e)}")  # Log error to terminal
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)