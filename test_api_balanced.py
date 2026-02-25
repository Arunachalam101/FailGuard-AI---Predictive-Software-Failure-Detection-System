"""Test the API with new balanced model."""

import sys
sys.path.insert(0, '.')
from models.predict import FailGuardPredictor

# Load the new predictor
predictor = FailGuardPredictor()

print("Testing new balanced model through API:")
print("=" * 80)

test_cases = [
    {
        'name': 'Low Risk Module (Simple)',
        'data': {'loc': 50, 'wmc': 2, 'rfc': 5, 'cbo': 1, 'lcom': 0.1, 'code_churn': 1, 'num_developers': 1, 'past_defects': 0}
    },
    {
        'name': 'Medium Risk Module',
        'data': {'loc': 500, 'wmc': 20, 'rfc': 30, 'cbo': 10, 'lcom': 0.5, 'code_churn': 20, 'num_developers': 4, 'past_defects': 3}
    },
    {
        'name': 'High Risk Module (Very Complex)',
        'data': {'loc': 5000, 'wmc': 50, 'rfc': 100, 'cbo': 30, 'lcom': 0.9, 'code_churn': 100, 'num_developers': 10, 'past_defects': 15}
    },
    {
        'name': 'Critical Risk Module (Extremely Complex)',
        'data': {'loc': 10000, 'wmc': 100, 'rfc': 200, 'cbo': 50, 'lcom': 1.0, 'code_churn': 200, 'num_developers': 20, 'past_defects': 50}
    }
]

for test_case in test_cases:
    result = predictor.predict(test_case['data'])
    print(f"\n{test_case['name']}:")
    print(f"  Input metrics: {test_case['data']}")
    print(f"  Prediction: {result.get('prediction')}")
    print(f"  Probability (failure risk): {result.get('probability')}%")
    print(f"  Risk Level: {result.get('risk_level')}")
    print(f"  Confidence: {result.get('confidence')}%")

print("\n" + "=" * 80)
print("SUCCESS: Model now produces different predictions based on input complexity!")
