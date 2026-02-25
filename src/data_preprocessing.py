import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DATA_RAW_PATH, DATA_PROCESSED_PATH, FEATURE_NAMES, SCALER_PATH
import joblib

def load_data(filepath=DATA_RAW_PATH):
    """Load raw NASA PROMISE dataset."""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """
    Handle missing values and data cleaning.
    
    Args:
        df: Raw dataframe
        
    Returns:
        Cleaned dataframe
    """
    print("Cleaning data...")
    
    # Drop rows with missing target variable
    if 'defects' in df.columns:
        df = df.dropna(subset=['defects'])
    elif 'buggy' in df.columns:
        df = df.dropna(subset=['buggy'])
    
    # Fill missing values with median for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    print(f"Cleaned dataset shape: {df.shape}")
    return df

def normalize_features(X_train, X_test, save_scaler=True):
    """
    Normalize features using StandardScaler.
    
    Args:
        X_train: Training features
        X_test: Test features
        save_scaler: Whether to save scaler for inference
        
    Returns:
        Normalized X_train, X_test, and scaler
    """
    print("Normalizing features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    if save_scaler:
        joblib.dump(scaler, SCALER_PATH)
        print(f"Scaler saved to {SCALER_PATH}")
    
    return X_train_scaled, X_test_scaled, scaler

def prepare_data(test_size=0.2, random_state=42):
    """
    Full preprocessing pipeline.
    
    Args:
        test_size: Proportion of test set
        random_state: Random seed
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    # Load and clean
    df = load_data()
    df = clean_data(df)
    
    # Rename columns to standardized names (case-insensitive matching)
    column_mapping = {
        'defects': 'target',
        'buggy': 'target',
        'loc': 'loc',
        'wmc': 'wmc',
        'rfc': 'rfc',
        'cbo': 'cbo',
        'lcom': 'lcom',
        'code_churn': 'code_churn',
        'num_developers': 'num_developers',
        'past_defects': 'past_defects'
    }
    
    # Normalize column names
    df.columns = [col.lower().strip() for col in df.columns]
    
    # Rename based on mapping
    df = df.rename(columns=column_mapping)
    
    # Handle target variable variations
    if 'target' not in df.columns:
        for col in df.columns:
            if col.lower() in ['defect', 'defects', 'buggy', 'bug']:
                df['target'] = df[col]
                break
    
    # Select required features
    available_features = [col for col in FEATURE_NAMES if col in df.columns]
    
    if len(available_features) < 2:
        # Use all numeric columns as features if predefined names not found
        available_features = [col for col in df.select_dtypes(include=[np.number]).columns 
                             if col != 'target'][:8]
    
    print(f"Using features: {available_features}")
    
    X = df[available_features].fillna(0)
    
    # Binary target (0 or 1)
    if 'target' in df.columns:
        y = (df['target'] > 0).astype(int)
    else:
        print("Warning: No target column found. Using last numeric column as target.")
        y = (df.iloc[:, -1] > 0).astype(int)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Normalize
    X_train_scaled, X_test_scaled, scaler = normalize_features(X_train, X_test)
    
    # Save processed data
    processed_df = pd.DataFrame(X_train_scaled, columns=available_features)
    processed_df['target'] = y_train.values
    processed_df.to_csv(DATA_PROCESSED_PATH, index=False)
    print(f"Processed data saved to {DATA_PROCESSED_PATH}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, available_features
