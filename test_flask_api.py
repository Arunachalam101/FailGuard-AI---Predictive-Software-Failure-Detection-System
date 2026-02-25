"""Test the Flask API directly."""

import sys
sys.path.insert(0, '.')
from app import app

# Create a test client
client = app.test_client()

print("Testing Flask API with new balanced model:")
print("=" * 80)

test_cases = [
    {
        'name': 'Simple Safe Module',
        'data': {'loc': 50, 'wmc': 2, 'rfc': 5, 'cbo': 1, 'lcom': 0.1, 'code_churn': 1, 'num_developers': 1, 'past_defects': 0}
    },
    {
        'name': 'Complex Defective Module',
        'data': {'loc': 5000, 'wmc': 50, 'rfc': 100, 'cbo': 30, 'lcom': 0.9, 'code_churn': 100, 'num_developers': 10, 'past_defects': 15}
    }
]

import json

for test_case in test_cases:
    print(f"\nTesting: {test_case['name']}")
    print(f"Input: {test_case['data']}")
    
    response = client.post(
        '/api/predict',
        data=json.dumps(test_case['data']),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        result = response.get_json()
        print(f"✓ API Response:")
        print(f"  Prediction: {result.get('prediction')}")
        print(f"  Risk Level: {result.get('risk_level')}")
        print(f"  Probability: {result.get('probability')}%")
        print(f"  Success: {result.get('success')}")
    else:
        print(f"✗ API Error: {response.status_code}")
        print(f"  {response.get_json()}")

print("\n" + "=" * 80)
print("API test complete!")
