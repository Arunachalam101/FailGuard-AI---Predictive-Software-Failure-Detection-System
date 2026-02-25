#!/usr/bin/env python
"""Test delete prediction functionality"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from app import app
from database.db import get_all_predictions

def test_delete_functionality():
    """Test prediction deletion"""
    print("\n=== Testing Prediction Deletion ===\n")
    
    # Create test client
    client = app.test_client()
    
    # Step 1: Make a prediction (to ensure we have something to delete)
    print("1. Making a test prediction...")
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
    pred_id = result['prediction_id']
    print(f"   ✓ Prediction created with ID: {pred_id}\n")
    
    # Step 2: Verify prediction exists
    print("2. Verifying prediction exists...")
    preds_before = get_all_predictions()
    print(f"   ✓ Total predictions before delete: {len(preds_before)}")
    
    # Check if our prediction is in the list
    pred_exists = any(p['id'] == pred_id for p in preds_before)
    assert pred_exists, f"Prediction {pred_id} not found in database"
    print(f"   ✓ Prediction ID {pred_id} confirmed in database\n")
    
    # Step 3: Delete the prediction
    print(f"3. Deleting prediction ID {pred_id}...")
    response = client.delete(f'/api/predictions/{pred_id}')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['success'] == True
    print(f"   ✓ Deletion successful: {result['message']}\n")
    
    # Step 4: Verify prediction is gone
    print("4. Verifying prediction was deleted...")
    preds_after = get_all_predictions()
    print(f"   ✓ Total predictions after delete: {len(preds_after)}")
    
    pred_deleted = not any(p['id'] == pred_id for p in preds_after)
    assert pred_deleted, f"Prediction {pred_id} still exists in database"
    print(f"   ✓ Prediction ID {pred_id} successfully removed\n")
    
    # Step 5: Test deleting non-existent prediction
    print("5. Testing delete of non-existent prediction...")
    response = client.delete(f'/api/predictions/99999')
    # Should still return 200 but with success=False
    print(f"   ✓ Response status: {response.status_code}\n")
    
    print("="*50)
    print("✓ All deletion tests passed!")
    print("="*50 + "\n")

if __name__ == '__main__':
    try:
        test_delete_functionality()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
