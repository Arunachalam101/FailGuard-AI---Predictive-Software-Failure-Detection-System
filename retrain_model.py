#!/usr/bin/env python
"""
FailGuard AI - Model Retraining Script

Run this if you get: "ModuleNotFoundError: No module named 'numpy._core'"

This script will retrain the model on your machine with your current
Python/numpy versions, making it compatible with your environment.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_preprocessing import prepare_data
from src.evaluation import evaluate_model
from src.utils import get_risk_label
from config import MODEL_PATH, SCALER_PATH, FEATURE_NAMES

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.svm import SVC

def retrain_model():
    """
    Retrain the model on the current machine's environment.
    This fixes compatibility issues with numpy/sklearn versions.
    """
    print("\n" + "="*60)
    print("FailGuard AI - Model Retraining")
    print("="*60)
    print("\nThis will retrain the model to be compatible with your")
    print("Python/numpy version.\n")
    
    try:
        # Step 1: Load and prepare data
        print("Step 1: Loading and preparing data...")
        X_train, X_test, y_train, y_test, feature_names, scaler = prepare_data()
        print(f"  ✓ Loaded {len(X_train)} training samples")
        print(f"  ✓ Loaded {len(X_test)} test samples")
        print(f"  ✓ Features: {feature_names}\n")
        
        # Step 2: Train models
        print("Step 2: Training models...")
        
        models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'XGBoost': XGBClassifier(n_estimators=100, random_state=42, verbosity=0),
            'SVM': SVC(kernel='rbf', probability=True, random_state=42)
        }
        
        results = {}
        best_model = None
        best_score = 0
        best_name = None
        
        for name, model in models.items():
            print(f"  Training {name}...", end=" ")
            model.fit(X_train, y_train)
            
            # Evaluate
            accuracy = model.score(X_test, y_test)
            results[name] = {
                'model': model,
                'accuracy': accuracy
            }
            
            print(f"Accuracy: {accuracy:.1%}")
            
            # Track best
            if accuracy > best_score:
                best_score = accuracy
                best_model = model
                best_name = name
        
        print(f"\n  ✓ Best model: {best_name} ({best_score:.1%} accuracy)\n")
        
        # Step 3: Save the best model
        print("Step 3: Saving model and scaler...")
        
        # Create models directory if it doesn't exist
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the best model
        joblib.dump(best_model, MODEL_PATH)
        print(f"  ✓ Model saved to: {MODEL_PATH}")
        
        # Save the scaler
        joblib.dump(scaler, SCALER_PATH)
        print(f"  ✓ Scaler saved to: {SCALER_PATH}\n")
        
        # Step 4: Test the model
        print("Step 4: Testing the model...")
        
        # Test prediction
        test_prediction = best_model.predict(X_test[:1])
        test_probability = best_model.predict_proba(X_test[:1])[0][1]
        test_risk = get_risk_label(test_probability)
        
        print(f"  ✓ Test prediction successful")
        print(f"  ✓ Risk level: {test_risk}")
        print(f"  ✓ Probability: {test_probability:.2%}")
        
        print("\n" + "="*60)
        print("✓ Model retraining complete!")
        print("="*60)
        print("\nYou can now run: python app.py")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during retraining: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = retrain_model()
    sys.exit(0 if success else 1)
