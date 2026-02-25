import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import MODEL_PATH, SCALER_PATH, FEATURE_NAMES
from src.utils import format_prediction_result

class FailGuardPredictor:
    """Main prediction class for FailGuard AI system."""
    
    def __init__(self, model_path=MODEL_PATH, scaler_path=SCALER_PATH):
        """
        Initialize predictor by loading model and scaler.
        
        Args:
            model_path: Path to saved model
            scaler_path: Path to saved scaler
        """
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            print(f"Model loaded from {model_path}")
            print(f"Scaler loaded from {scaler_path}")
        except FileNotFoundError:
            print("Warning: Model or scaler not found. Train the model first using train_model.py")
            self.model = None
            self.scaler = None
    
    def predict(self, features_dict):
        """
        Make prediction on new software module metrics.
        
        Args:
            features_dict: Dictionary with keys:
                - loc: Lines of Code
                - wmc: Weighted Methods per Class
                - rfc: Response for a Class
                - cbo: Coupling Between Objects
                - lcom: Lack of Cohesion
                - code_churn: Code Churn
                - num_developers: Number of Developers
                - past_defects: Past Defects
                
        Returns:
            Dictionary with prediction results
        """
        if self.model is None or self.scaler is None:
            return {
                'error': 'Model not initialized. Please train the model first.',
                'success': False
            }
        
        # Extract features in order
        features = []
        for feature_name in FEATURE_NAMES:
            value = features_dict.get(feature_name, 0)
            features.append(float(value))
        
        # Convert to DataFrame with proper feature names to avoid sklearn warning
        features_df = pd.DataFrame([features], columns=FEATURE_NAMES)
        
        # Normalize
        features_scaled = self.scaler.transform(features_df)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0][1]
        
        # Convert to Python native types
        prediction = int(prediction)
        probability = float(probability)
        
        # Format result
        result = format_prediction_result(probability, prediction)
        result['success'] = True
        # Convert input features to native Python types
        result['input_features'] = {k: float(v) for k, v in features_dict.items()}
        
        return result
    
    def predict_batch(self, features_list):
        """
        Make batch predictions.
        
        Args:
            features_list: List of feature dictionaries
            
        Returns:
            List of prediction results
        """
        results = []
        for features_dict in features_list:
            result = self.predict(features_dict)
            results.append(result)
        
        return results

def load_model():
    """Load model for inference."""
    return FailGuardPredictor()

def make_prediction(features_dict):
    """
    Simple interface for making predictions.
    
    Args:
        features_dict: Dictionary of feature values
        
    Returns:
        Prediction result
    """
    predictor = load_model()
    return predictor.predict(features_dict)

if __name__ == "__main__":
    # Example usage
    sample_input = {
        'loc': 500,
        'wmc': 15,
        'rfc': 20,
        'cbo': 8,
        'lcom': 0.5,
        'code_churn': 10,
        'num_developers': 3,
        'past_defects': 2
    }
    
    predictor = load_model()
    result = predictor.predict(sample_input)
    print("Prediction Result:")
    print(result)
