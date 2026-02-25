import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)
import json

def evaluate_model(y_true, y_pred, y_pred_proba=None):
    """
    Comprehensive model evaluation.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_pred_proba: Probability predictions (optional)
        
    Returns:
        Dictionary of all metrics
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1_score': f1_score(y_true, y_pred, zero_division=0),
    }
    
    # ROC-AUC requires probability predictions
    if y_pred_proba is not None:
        try:
            if len(y_pred_proba.shape) > 1:
                proba = y_pred_proba[:, 1]
            else:
                proba = y_pred_proba
            metrics['roc_auc'] = roc_auc_score(y_true, proba)
        except:
            metrics['roc_auc'] = 0.0
    else:
        metrics['roc_auc'] = 0.0
    
    return metrics

def get_confusion_matrix(y_true, y_pred):
    """Get confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    return {
        'tn': int(cm[0, 0]),
        'fp': int(cm[0, 1]),
        'fn': int(cm[1, 0]),
        'tp': int(cm[1, 1])
    }

def get_classification_report(y_true, y_pred):
    """Get detailed classification report."""
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    return report

def print_evaluation_results(model_name, metrics, y_true, y_pred):
    """Print evaluation results."""
    print(f"\n{'='*50}")
    print(f"Model: {model_name}")
    print(f"{'='*50}")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1-Score:  {metrics['f1_score']:.4f}")
    print(f"ROC-AUC:   {metrics['roc_auc']:.4f}")
    
    # Confusion Matrix
    cm = get_confusion_matrix(y_true, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"  TN: {cm['tn']:4d}  FP: {cm['fp']:4d}")
    print(f"  FN: {cm['fn']:4d}  TP: {cm['tp']:4d}")

def get_feature_importance(model, feature_names):
    """
    Extract feature importance from tree-based models.
    
    Args:
        model: Trained model with feature_importances_
        feature_names: List of feature names
        
    Returns:
        Sorted list of (feature, importance) tuples
    """
    try:
        importances = model.feature_importances_
        feature_importance = sorted(
            zip(feature_names, importances),
            key=lambda x: x[1],
            reverse=True
        )
        return feature_importance
    except AttributeError:
        return []

def prepare_evaluation_report(models_results):
    """
    Prepare comprehensive evaluation report.
    
    Args:
        models_results: Dict of model names to their metrics
        
    Returns:
        Formatted report
    """
    report = {
        'models': {},
        'best_model': None,
        'best_f1': 0
    }
    
    for model_name, metrics in models_results.items():
        report['models'][model_name] = {
            'accuracy': round(metrics['accuracy'], 4),
            'precision': round(metrics['precision'], 4),
            'recall': round(metrics['recall'], 4),
            'f1_score': round(metrics['f1_score'], 4),
            'roc_auc': round(metrics['roc_auc'], 4)
        }
        
        if metrics['f1_score'] > report['best_f1']:
            report['best_f1'] = metrics['f1_score']
            report['best_model'] = model_name
    
    return report
