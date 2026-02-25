"""Debug script to test if model predictions vary with different inputs."""

import sys
sys.path.insert(0, '.')
from models.predict import FailGuardPredictor
import pandas as pd

# Load the predictor
predictor = FailGuardPredictor()

# Test with different input values
test_cases = [
    {'loc': 100, 'wmc': 5, 'rfc': 10, 'cbo': 3, 'lcom': 0.3, 'code_churn': 2, 'num_developers': 2, 'past_defects': 0},
    {'loc': 5000, 'wmc': 50, 'rfc': 100, 'cbo': 30, 'lcom': 0.9, 'code_churn': 100, 'num_developers': 10, 'past_defects': 15},
    {'loc': 500, 'wmc': 20, 'rfc': 30, 'cbo': 10, 'lcom': 0.5, 'code_churn': 20, 'num_developers': 4, 'past_defects': 3},
]

print('Testing model with different inputs:')
print('-' * 80)
for i, test_case in enumerate(test_cases, 1):
    result = predictor.predict(test_case)
    print(f'Test {i}:')
    print(f'  Input: {test_case}')
    print(f'  Prediction: {result.get("prediction")}')
    print(f'  Probability: {result.get("probability")}')
    print(f'  Risk Level: {result.get("risk_level")}')
    print()

# Check if all probabilities are the same
probabilities = []
for test_case in test_cases:
    result = predictor.predict(test_case)
    probabilities.append(result.get("probability"))

print('-' * 80)
if len(set(probabilities)) == 1:
    print('ERROR: All predictions have the same probability!')
    print(f'All probabilities: {probabilities}')
else:
    print('SUCCESS: Predictions vary with different inputs.')
    print(f'Probabilities: {probabilities}')
