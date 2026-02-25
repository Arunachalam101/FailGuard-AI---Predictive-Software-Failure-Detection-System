import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

def create_polynomial_features(X, degree=2):
    """
    Create polynomial features.
    
    Args:
        X: Input features array
        degree: Polynomial degree
        
    Returns:
        Array with polynomial features
    """
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(X)
    return X_poly, poly

def select_features_by_variance(X, threshold=0.01):
    """
    Remove features with low variance.
    
    Args:
        X: Input features
        threshold: Variance threshold
        
    Returns:
        Filtered features
    """
    variances = np.var(X, axis=0)
    mask = variances > threshold
    return X[:, mask], mask

def calculate_feature_statistics(X, feature_names):
    """
    Calculate statistics for each feature.
    
    Args:
        X: Input features
        feature_names: List of feature names
        
    Returns:
        DataFrame with statistics
    """
    stats = pd.DataFrame({
        'feature': feature_names,
        'mean': X.mean(axis=0),
        'std': X.std(axis=0),
        'min': X.min(axis=0),
        'max': X.max(axis=0)
    })
    return stats

def create_interaction_features(X, feature_names):
    """
    Create interaction features from important metrics.
    
    Args:
        X: Input features
        feature_names: List of feature names
        
    Returns:
        Extended feature array with interactions
    """
    X_interactions = X.copy()
    
    # Common interactions for software metrics
    # LOC * CBO (complexity interaction)
    if 'loc' in feature_names and 'cbo' in feature_names:
        loc_idx = feature_names.index('loc')
        cbo_idx = feature_names.index('cbo')
        interaction = X[:, loc_idx] * X[:, cbo_idx]
        X_interactions = np.column_stack([X_interactions, interaction])
    
    return X_interactions
