import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent
DATA_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "nasa_promise.csv"
DATA_PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_data.csv"
MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "failguard_model.joblib"
SCALER_PATH = MODELS_DIR / "scaler.joblib"

# Model configuration
FEATURE_NAMES = [
    'loc', 'wmc', 'rfc', 'cbo', 'lcom', 'code_churn', 'num_developers', 'past_defects'
]

# Risk thresholds
RISK_THRESHOLDS = {
    'LOW': 0.33,
    'MEDIUM': 0.67,
    'HIGH': 1.0
}

# Flask configuration
DEBUG = True
SECRET_KEY = 'failguard_secret_key_2026'
