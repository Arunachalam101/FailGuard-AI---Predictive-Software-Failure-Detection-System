import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import RISK_THRESHOLDS

def get_risk_label(probability):
    """
    Convert probability score to risk label.
    
    Args:
        probability: Float between 0 and 1
        
    Returns:
        Risk label: 'LOW', 'MEDIUM', or 'HIGH'
    """
    if probability < RISK_THRESHOLDS['LOW']:
        return 'LOW'
    elif probability < RISK_THRESHOLDS['MEDIUM']:
        return 'MEDIUM'
    else:
        return 'HIGH'

def get_risk_color(risk_label):
    """Get color code for risk level visualization."""
    colors = {
        'LOW': '#28a745',    # Green
        'MEDIUM': '#ffc107',  # Yellow
        'HIGH': '#dc3545'     # Red
    }
    return colors.get(risk_label, '#6c757d')

def calculate_model_confidence(probability, predictions):
    """
    Calculate model confidence based on probability distance from decision boundary.
    
    Args:
        probability: Probability from model
        predictions: Boolean array of predictions
        
    Returns:
        Confidence percentage (0-100)
    """
    # Distance from 0.5 decision boundary
    distance = abs(probability - 0.5)
    confidence = min(100, (distance * 200))  # Scale to 0-100
    return round(confidence, 2)

def format_prediction_result(probability, defect_flag):
    """
    Format prediction result for UI display.
    
    Args:
        probability: Probability score
        defect_flag: Binary prediction
        
    Returns:
        Dictionary with formatted results (JSON serializable)
    """
    # Convert numpy types to Python native types
    probability = float(probability)
    defect_flag = int(defect_flag)
    
    risk_label = get_risk_label(probability)
    confidence = calculate_model_confidence(probability, defect_flag)
    
    return {
        'probability': float(round(probability * 100, 2)),
        'risk_level': str(risk_label),
        'risk_color': str(get_risk_color(risk_label)),
        'confidence': float(confidence),
        'prediction': 'DEFECTIVE' if defect_flag else 'SAFE'
    }
