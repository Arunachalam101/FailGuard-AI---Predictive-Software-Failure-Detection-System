#!/usr/bin/env python
"""Test the Flask API endpoints"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from app import app

def test_endpoints():
    """Test all API endpoints"""
    print("\n=== Testing Flask API Endpoints ===\n")
    
    # Create test client
    client = app.test_client()
    
    # Test 1: Health check
    print("1. Testing /api/health endpoint...")
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['model_loaded'] == True
    print("   ✓ Health check passed\n")
    
    # Test 2: Get features
    print("2. Testing /api/features endpoint...")
    response = client.get('/api/features')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['features']) == 8
    print(f"   ✓ Retrieved {len(data['features'])} features\n")
    
    # Test 3: Make prediction
    print("3. Testing /api/predict endpoint...")
    prediction_data = {
        'loc': 500,
        'wmc': 15,
        'rfc': 20,
        'cbo': 8,
        'lcom': 0.5,
        'code_churn': 10,
        'num_developers': 3,
        'past_defects': 2
    }
    response = client.post('/api/predict', 
                          data=json.dumps(prediction_data),
                          content_type='application/json')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['success'] == True
    assert result['risk_level'] in ['LOW', 'MEDIUM', 'HIGH']
    assert 'probability' in result
    assert 'prediction_id' in result
    print(f"   ✓ Prediction successful")
    print(f"     Risk Level: {result['risk_level']}")
    print(f"     Probability: {result['probability']}%")
    print(f"     Prediction ID: {result['prediction_id']}\n")
    
    # Test 4: Get predictions
    print("4. Testing /api/predictions endpoint...")
    response = client.get('/api/predictions?limit=10')
    assert response.status_code == 200
    predictions = json.loads(response.data)
    assert isinstance(predictions, list)
    print(f"   ✓ Retrieved {len(predictions)} predictions from database\n")
    
    # Test 5: Get prediction stats
    print("5. Testing /api/predictions/stats endpoint...")
    response = client.get('/api/predictions/stats')
    assert response.status_code == 200
    stats = json.loads(response.data)
    assert 'total' in stats
    assert 'risk_distribution' in stats
    print(f"   ✓ Stats retrieved:")
    print(f"     Total predictions: {stats['total']}")
    print(f"     High risk count: {stats['high_risk_count']}\n")
    
    # Test 6: Home page
    print("6. Testing home page (/) ...")
    response = client.get('/')
    assert response.status_code == 200
    print("   ✓ Home page loads correctly\n")
    
    # Test 7: Dashboard page
    print("7. Testing dashboard page (/dashboard)...")
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Recent Predictions' in response.data
    print("   ✓ Dashboard loads correctly\n")
    
    print("="*50)
    print("✓ All API tests passed!")
    print("="*50 + "\n")

if __name__ == '__main__':
    try:
        test_endpoints()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
