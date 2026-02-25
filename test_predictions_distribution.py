"""Debug: Check class distribution and model predictions."""

import sys
sys.path.insert(0, '.')
import joblib
import pandas as pd
from config import MODEL_PATH, SCALER_PATH, FEATURE_NAMES

# Load model and scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print(f"Model classes: {model.classes_}")
print()

# Test with lots of different values to see if model ever predicts class 1
test_cases = [
    {'loc': 100, 'wmc': 5, 'rfc': 10, 'cbo': 3, 'lcom': 0.3, 'code_churn': 2, 'num_developers': 2, 'past_defects': 0},
    {'loc': 5000, 'wmc': 50, 'rfc': 100, 'cbo': 30, 'lcom': 0.9, 'code_churn': 100, 'num_developers': 10, 'past_defects': 15},
    {'loc': 500, 'wmc': 20, 'rfc': 30, 'cbo': 10, 'lcom': 0.5, 'code_churn': 20, 'num_developers': 4, 'past_defects': 3},
    {'loc': 10000, 'wmc': 100, 'rfc': 200, 'cbo': 50, 'lcom': 1.0, 'code_churn': 200, 'num_developers': 20, 'past_defects': 50},
    {'loc': 50, 'wmc': 2, 'rfc': 5, 'cbo': 1, 'lcom': 0.1, 'code_churn': 1, 'num_developers': 1, 'past_defects': 0},
]

print("Predictions for different test cases:")
print("-" * 100)

predictions = []
probabilities = []

for i, test_case in enumerate(test_cases, 1):
    # Convert to DataFrame
    features = []
    for feature_name in FEATURE_NAMES:
        value = test_case.get(feature_name, 0)
        features.append(float(value))
    
    features_df = pd.DataFrame([features], columns=FEATURE_NAMES)
    
    # Scale
    features_scaled = scaler.transform(features_df)
    
    # Get predictions
    pred = model.predict(features_scaled)[0]
    proba = model.predict_proba(features_scaled)[0]
    
    predictions.append(pred)
    probabilities.append(proba[1])
    
    print(f"Test {i}: Prediction={pred}, Class 0 prob={proba[0]:.4f}, Class 1 prob={proba[1]:.4f}")

print("-" * 100)
print(f"Unique predictions: {set(predictions)}")
print(f"Class 1 predicted: {sum(1 for p in predictions if p == 1)} times")
print(f"Class 0 predicted: {sum(1 for p in predictions if p == 0)} times")
