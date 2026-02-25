#!/usr/bin/env python
"""Test FailGuard AI system integration"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database.db import init_database, save_prediction, get_all_predictions, get_prediction_stats
from models.predict import load_model

def test_prediction():
    """Test prediction model"""
    print("\n=== Testing Prediction Model ===")
    predictor = load_model()
    
    test_data = {
        'loc': 500,
        'wmc': 15,
        'rfc': 20,
        'cbo': 8,
        'lcom': 0.5,
        'code_churn': 10,
        'num_developers': 3,
        'past_defects': 2
    }
    
    result = predictor.predict(test_data)
    print(f"✓ Prediction successful")
    print(f"  Risk Level: {result['risk_level']}")
    print(f"  Probability: {result['probability']}%")
    print(f"  Confidence: {result['confidence']}%")
    print(f"  Prediction: {result['prediction']}")
    
    return result, test_data

def test_database(result, test_data):
    """Test database storage"""
    print("\n=== Testing Database Storage ===")
    
    # Save prediction
    pred_id = save_prediction(test_data, result)
    print(f"✓ Prediction saved with ID: {pred_id}")
    
    # Retrieve predictions
    preds = get_all_predictions(limit=5)
    print(f"✓ Retrieved {len(preds)} predictions from database")
    
    if preds:
        latest = preds[0]
        print(f"  Latest: {latest['risk_level']} risk at {latest['timestamp']}")
    
    # Get stats
    stats = get_prediction_stats()
    print(f"\n✓ Database Statistics:")
    print(f"  Total predictions: {stats['total']}")
    print(f"  Risk distribution: {stats['risk_distribution']}")
    print(f"  Average probability: {stats['average_probability']}%")
    print(f"  High risk count: {stats['high_risk_count']}")

def main():
    print("\n" + "="*50)
    print("FailGuard AI - System Integration Test")
    print("="*50)
    
    try:
        result, test_data = test_prediction()
        test_database(result, test_data)
        
        print("\n" + "="*50)
        print("✓ All tests passed!")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
