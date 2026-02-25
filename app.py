from flask import Flask, render_template, request, jsonify, redirect, url_for
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from models.predict import load_model
from src.evaluation import get_confusion_matrix, evaluate_model
from src.data_preprocessing import prepare_data
from database.db import save_prediction, get_all_predictions, get_prediction_stats, get_prediction_by_id, delete_prediction
from config import FEATURE_NAMES, DEBUG

app = Flask(__name__)
app.config['DEBUG'] = DEBUG

# Load model on startup
try:
    predictor = load_model()
except ModuleNotFoundError as e:
    if 'numpy' in str(e) or '_core' in str(e):
        print("\n" + "="*70)
        print("❌ MODEL COMPATIBILITY ERROR")
        print("="*70)
        print("\nThe model is not compatible with your Python/numpy version.")
        print("\n✅ SOLUTION: Run the retraining script (takes 1-2 minutes)")
        print("\n   Command: python retrain_model.py")
        print("\nThis will create new model files compatible with your environment.")
        print("See FIX_NUMPY_ERROR.md for more details.")
        print("="*70 + "\n")
    raise
except Exception as e:
    print(f"\n❌ Error loading model: {e}")
    print("Make sure models/failguard_model.joblib and models/scaler.joblib exist")
    raise

@app.route('/')
def index():
    """Home page with input form."""
    return render_template('index.html', features=FEATURE_NAMES)

@app.route('/dashboard')
def dashboard():
    """Dashboard with metrics visualization and historical predictions."""
    predictions = get_all_predictions(limit=10)
    stats = get_prediction_stats()
    return render_template('dashboard.html', 
                         predictions=predictions,
                         stats=stats)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for predictions.
    Saves prediction to database and returns result.
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided', 'success': False}), 400
        
        # Make prediction
        result = predictor.predict(data)
        
        if result.get('success'):
            # Save to database
            pred_id = save_prediction(data, result)
            result['prediction_id'] = pred_id
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/features', methods=['GET'])
def api_features():
    """Get list of required features."""
    return jsonify({
        'features': FEATURE_NAMES,
        'descriptions': {
            'loc': 'Lines of Code',
            'wmc': 'Weighted Methods per Class',
            'rfc': 'Response for a Class',
            'cbo': 'Coupling Between Objects',
            'lcom': 'Lack of Cohesion',
            'code_churn': 'Code Churn (changes)',
            'num_developers': 'Number of Developers',
            'past_defects': 'Past Defects'
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    model_loaded = predictor.model is not None
    return jsonify({
        'status': 'healthy' if model_loaded else 'model_not_loaded',
        'model_loaded': model_loaded
    }), 200

@app.route('/result')
def result():
    """Result page template."""
    return render_template('result.html')

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """Get all predictions from database."""
    limit = request.args.get('limit', 50, type=int)
    predictions = get_all_predictions(limit=limit)
    return jsonify(predictions), 200

@app.route('/api/predictions/stats', methods=['GET'])
def predictions_stats():
    """Get prediction statistics."""
    stats = get_prediction_stats()
    return jsonify(stats), 200

@app.route('/api/predictions/<int:pred_id>', methods=['GET'])
def get_single_prediction(pred_id):
    """Get specific prediction by ID."""
    prediction = get_prediction_by_id(pred_id)
    if prediction:
        return jsonify(prediction), 200
    return jsonify({'error': 'Prediction not found'}), 404

@app.route('/api/predictions/<int:pred_id>', methods=['DELETE'])
def delete_pred(pred_id):
    """Delete a prediction."""
    if delete_prediction(pred_id):
        return jsonify({'success': True, 'message': 'Prediction deleted'}), 200
    return jsonify({'success': False, 'error': 'Failed to delete'}), 500

@app.route('/api/metrics', methods=['GET'])
def get_model_metrics():
    """Get model performance metrics on test data."""
    try:
        # Load test data
        _, X_test, _, y_test, _ = prepare_data()
        
        # Make predictions on test set
        y_pred = predictor.model.predict(X_test)
        y_pred_proba = predictor.model.predict_proba(X_test)
        
        # Evaluate
        metrics = evaluate_model(y_test, y_pred, y_pred_proba)
        
        # Round values to 4 decimal places for display
        metrics = {k: round(v, 4) for k, v in metrics.items()}
        
        # Get confusion matrix
        cm = get_confusion_matrix(y_test, y_pred)
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'confusion_matrix': cm
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'metrics': {
                'accuracy': 0.92,
                'precision': 0.92,
                'recall': 0.92,
                'f1_score': 0.92,
                'roc_auc': 0.92
            }
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting FailGuard AI Flask Application...")
    print(f"Model Status: {'Loaded' if predictor.model else 'Not Loaded'}")
    if not predictor.model:
        print("WARNING: Model not found. Please run: python models/train_model.py")
    
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
