import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from src.data_preprocessing import prepare_data
from src.evaluation import evaluate_model, print_evaluation_results, get_confusion_matrix, prepare_evaluation_report
from config import MODEL_PATH, MODELS_DIR

def train_models(X_train, X_test, y_train, y_test):
    """
    Train multiple ML models with class weight balancing for imbalanced data.
    
    Args:
        X_train, X_test: Training and test features
        y_train, y_test: Training and test labels
        
    Returns:
        Dictionary of trained models and their metrics
    """
    # Calculate class weights to handle imbalance
    # More weight for minority class (defective)
    from sklearn.utils.class_weight import compute_class_weight
    class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
    class_weight_dict = {i: w for i, w in enumerate(class_weights)}
    
    print(f"\nClass weights (to balance imbalance): {class_weight_dict}")
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight='balanced'),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42, class_weight='balanced'),
        'XGBoost': XGBClassifier(n_estimators=100, random_state=42, verbosity=0, scale_pos_weight=class_weight_dict[1]/class_weight_dict[0])
    }
    
    trained_models = {}
    results = {}
    
    print("\n" + "="*60)
    print("TRAINING MODELS")
    print("="*60)
    
    for model_name, model in models.items():
        print(f"\nTraining {model_name}...")
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        try:
            y_pred_proba = model.predict_proba(X_test)
        except:
            y_pred_proba = None
        
        # Evaluate
        metrics = evaluate_model(y_test, y_pred, y_pred_proba)
        print_evaluation_results(model_name, metrics, y_test, y_pred)
        
        trained_models[model_name] = model
        results[model_name] = metrics
    
    return trained_models, results

def select_best_model(trained_models, results):
    """
    Select the best performing model.
    
    Args:
        trained_models: Dictionary of trained models
        results: Dictionary of model metrics
        
    Returns:
        Best model and its name
    """
    best_model_name = max(results.keys(), key=lambda x: results[x]['f1_score'])
    best_model = trained_models[best_model_name]
    
    print(f"\n{'='*60}")
    print(f"BEST MODEL: {best_model_name}")
    print(f"F1-Score: {results[best_model_name]['f1_score']:.4f}")
    print(f"{'='*60}")
    
    return best_model, best_model_name

def save_model(model, model_name, filepath=MODEL_PATH):
    """
    Save trained model to disk.
    
    Args:
        model: Trained model
        model_name: Name of the model
        filepath: Path to save
    """
    joblib.dump(model, filepath)
    print(f"\nModel '{model_name}' saved to {filepath}")

def main():
    """Main training pipeline."""
    print("FailGuard AI - Model Training Pipeline")
    print("="*60)
    
    # Load and prepare data
    X_train, X_test, y_train, y_test, feature_names = prepare_data()
    
    print(f"\nTraining set size: {X_train.shape}")
    print(f"Test set size: {X_test.shape}")
    print(f"Number of features: {len(feature_names)}")
    print(f"Class distribution (train): {np.bincount(y_train)}")
    
    # Train models
    trained_models, results = train_models(X_train, X_test, y_train, y_test)
    
    # Select and save best model
    best_model, best_model_name = select_best_model(trained_models, results)
    save_model(best_model, best_model_name)
    
    # Evaluation report
    report = prepare_evaluation_report(results)
    print(f"\nEvaluation Report:")
    print(f"Best Model: {report['best_model']}")
    print(f"Best F1-Score: {report['best_f1']:.4f}")
    
    return best_model, best_model_name, feature_names

if __name__ == "__main__":
    main()
