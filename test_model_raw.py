"""Debug: Check what model.predict_proba is returning."""

import sys
sys.path.insert(0, '.')
import joblib
import pandas as pd
from config import MODEL_PATH, SCALER_PATH, FEATURE_NAMES

# Load model and scaler directly
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print(f"Model type: {type(model)}")
print(f"Model: {model}")
print()

# Test with raw values
print("Test data:")
test_cases = [
    {'loc': 100, 'wmc': 5, 'rfc': 10, 'cbo': 3, 'lcom': 0.3, 'code_churn': 2, 'num_developers': 2, 'past_defects': 0},
    {'loc': 5000, 'wmc': 50, 'rfc': 100, 'cbo': 30, 'lcom': 0.9, 'code_churn': 100, 'num_developers': 10, 'past_defects': 15},
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"Test case {i}:")
    print(f"Raw values: {test_case}")
    
    # Convert to DataFrame with proper column order
    features = []
    for feature_name in FEATURE_NAMES:
        value = test_case.get(feature_name, 0)
        features.append(float(value))
    
    features_df = pd.DataFrame([features], columns=FEATURE_NAMES)
    print(f"\nDataFrame before scaling:\n{features_df}")
    
    # Scale
    features_scaled = scaler.transform(features_df)
    print(f"\nScaled values shape: {features_scaled.shape}")
    print(f"Scaled values:\n{features_scaled}")
    
    # Get raw prediction
    pred = model.predict(features_scaled)
    print(f"\nmodel.predict() raw output: {pred}")
    print(f"Type: {type(pred[0])}")
    
    # Get raw probability
    proba = model.predict_proba(features_scaled)
    print(f"\nmodel.predict_proba() raw output: {proba}")
    print(f"Type: {type(proba)}")
    print(f"Shape: {proba.shape}")
    print(f"Value at [0,1]: {proba[0][1]}")
    print(f"Type of probability: {type(proba[0][1])}")
