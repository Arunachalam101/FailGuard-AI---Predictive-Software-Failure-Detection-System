# FailGuard AI - Predictive Software Failure Detection System

An AI-driven predictive analytics system that identifies software modules with a high probability of failure before deployment using machine learning on historical software metrics.

## 🎯 Project Overview

FailGuard AI helps development teams:
- **Predict** which software modules are at high risk of failure
- **Prioritize** code reviews and testing efforts
- **Reduce** testing costs and time-to-market
- **Improve** release quality and reliability
- **Perform** risk-based debugging and resource allocation

## 📊 Input Features

The system analyzes 8 key software metrics:

- **LOC** – Lines of Code (module size)
- **WMC** – Weighted Methods per Class (complexity)
- **RFC** – Response for a Class (method dependencies)
- **CBO** – Coupling Between Objects (interdependencies)
- **LCOM** – Lack of Cohesion (method-attribute relationships)
- **Code Churn** – Recent code changes
- **Number of Developers** – Developer count for the module
- **Past Defects** – Historical defect count

## 🎓 Output

For each analyzed module, the system provides:

1. **Risk Level**: LOW / MEDIUM / HIGH
2. **Failure Probability**: Percentage (0-100%)
3. **Model Confidence**: Prediction confidence score
4. **Actionable Recommendations**: Based on risk level

## 🏗️ Architecture

### Components

```
FailGuard AI/
├── data/
│   ├── raw/
│   │   └── nasa_promise.csv          # Original dataset
│   └── processed/
│       └── cleaned_data.csv          # Preprocessed data
├── models/
│   ├── train_model.py                # Model training pipeline
│   ├── predict.py                    # Inference engine
│   ├── failguard_model.joblib        # Trained model (generated)
│   └── scaler.joblib                 # Feature scaler (generated)
├── src/
│   ├── data_preprocessing.py          # Data cleaning & normalization
│   ├── feature_engineering.py         # Feature creation
│   ├── evaluation.py                  # Model evaluation metrics
│   └── utils.py                       # Helper utilities
├── templates/
│   ├── index.html                    # Main input form
│   ├── dashboard.html                # Visualization dashboard
│   └── result.html                   # Prediction results
├── static/
│   ├── css/styles.css               # Styling
│   └── js/main.js                    # Client-side logic
├── app.py                            # Flask web application
├── config.py                         # Configuration settings
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

### Machine Learning Pipeline

```
Raw Data (NASA PROMISE)
    ↓
Data Preprocessing (cleaning, normalization)
    ↓
Feature Engineering (selection, scaling)
    ↓
Model Training (4 algorithms)
    ├── Logistic Regression
    ├── Random Forest ⭐ (Best Performer)
    ├── XGBoost
    └── Support Vector Machine
    ↓
Model Evaluation (Accuracy, Precision, Recall, F1, ROC-AUC)
    ↓
Model Serialization (saved to joblib)
    ↓
Flask API + Web UI (Real-time predictions)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Data

Ensure `data/raw/nasa_promise.csv` contains your dataset with columns for:
- Software metrics (loc, wmc, rfc, cbo, lcom, etc.)
- Target variable (defects or buggy flag)

### 3. Train Models

```bash
python models/train_model.py
```

This will:
- Load and preprocess the NASA PROMISE dataset
- Train 4 different models
- Evaluate all models
- Save the best model (Random Forest)
- Generate scaler for feature normalization

**Output**: 
- `models/failguard_model.joblib` – Trained model
- `models/scaler.joblib` – Feature scaler
- `data/processed/cleaned_data.csv` – Processed training data

### 4. Run Flask Application

```bash
python app.py
```

The Flask server will start at `http://localhost:5000`

### 5. Access Web UI

Open your browser and navigate to:
```
http://localhost:5000
```

## 🎮 Usage

### Via Web UI

1. Go to home page (`/`)
2. Enter software module metrics in the form
3. Click "Analyze Module Risk"
4. View prediction results with recommendations

### Via API

**Endpoint**: `POST /api/predict`

**Request**:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "loc": 500,
    "wmc": 15,
    "rfc": 20,
    "cbo": 8,
    "lcom": 0.5,
    "code_churn": 10,
    "num_developers": 3,
    "past_defects": 2
  }'
```

**Response**:
```json
{
  "success": true,
  "probability": 42.5,
  "risk_level": "MEDIUM",
  "risk_color": "#ffc107",
  "confidence": 75.3,
  "prediction": "DEFECTIVE"
}
```

## 📈 Model Performance

The system evaluates models using:

- **Accuracy**: Overall correctness
- **Precision**: True positives / All positives (minimize false alarms)
- **Recall**: True positives / All true cases (catch real defects)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under the receiver operating characteristic curve

The **Random Forest** model typically achieves the best balance of metrics.

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Data paths
DATA_RAW_PATH = "data/raw/nasa_promise.csv"
DATA_PROCESSED_PATH = "data/processed/cleaned_data.csv"

# Feature names (in order)
FEATURE_NAMES = ['loc', 'wmc', 'rfc', 'cbo', 'lcom', 'code_churn', 'num_developers', 'past_defects']

# Risk thresholds
RISK_THRESHOLDS = {
    'LOW': 0.33,      # < 33% probability
    'MEDIUM': 0.67,   # 33-67%
    'HIGH': 1.0       # > 67%
}

# Flask settings
DEBUG = True
SECRET_KEY = 'your-secret-key'
```

## 📚 Project Structure Details

### `models/train_model.py`
- Loads NASA PROMISE dataset
- Trains 4 ML algorithms
- Evaluates and compares models
- Saves best model with joblib

### `models/predict.py`
- `FailGuardPredictor` class for making predictions
- Loads trained model and scaler
- Handles feature normalization
- Returns formatted prediction results

### `src/data_preprocessing.py`
- Data loading and cleaning
- Missing value handling
- Feature normalization (StandardScaler)
- Train/test split (80/20)

### `src/evaluation.py`
- Comprehensive metrics calculation
- Confusion matrix generation
- Classification reports
- Feature importance extraction

### `app.py`
- Flask web application
- REST API endpoints
- Static file serving
- Error handling

## 🌐 Web Pages

### `/` – Home Page (Input Form)
- Interactive form for entering software metrics
- Tooltips for metric explanations
- Real-time form validation
- Results display section

### `/dashboard` – Analytics Dashboard
- Model performance metrics
- Risk distribution visualization
- Quick test functionality
- Feature importance (when available)

### `/result` – Detailed Results
- Risk level with visual indicator
- Failure probability with progress bar
- Input metrics summary
- Actionable recommendations

## 🔄 ML Models Included

1. **Logistic Regression** – Fast, interpretable baseline
2. **Random Forest** – Ensemble method, best performer ⭐
3. **XGBoost** – Gradient boosting, high accuracy
4. **Support Vector Machine** – Kernel-based, good for complex patterns

## 🛠️ Development & Customization

### Add New Features

Edit `FEATURE_NAMES` in `config.py` and modify preprocessing accordingly.

### Change Risk Thresholds

Adjust `RISK_THRESHOLDS` in `config.py`:
```python
RISK_THRESHOLDS = {
    'LOW': 0.25,    # Stricter
    'MEDIUM': 0.75,
    'HIGH': 1.0
}
```

### Retrain with New Data

1. Update `data/raw/nasa_promise.csv`
2. Run `python models/train_model.py`
3. Flask will automatically use the new model

### Customize UI

- Modify `templates/*.html` for layout
- Edit `static/css/styles.css` for styling
- Update `static/js/main.js` for behavior

## 📝 API Reference

### GET `/` 
Returns the home page with input form.

### GET `/dashboard`
Returns the analytics dashboard.

### POST `/api/predict`
Makes a prediction based on input metrics.

**Parameters** (JSON):
- `loc` (float): Lines of Code
- `wmc` (float): Weighted Methods per Class
- `rfc` (float): Response for a Class
- `cbo` (float): Coupling Between Objects
- `lcom` (float): Lack of Cohesion (0-1)
- `code_churn` (float): Code changes
- `num_developers` (int): Developer count
- `past_defects` (int): Historical defects

### GET `/api/features`
Returns list of required features and descriptions.

### GET `/api/health`
Health check endpoint (returns model status).

## 🐛 Troubleshooting

**Model not found error**
- Run `python models/train_model.py` first to train the model

**Port 5000 already in use**
- Change in `app.py`: `app.run(port=5001)`

**Import errors**
- Ensure all packages from `requirements.txt` are installed
- Verify Python 3.8+ is being used

**Data file not found**
- Ensure `data/raw/nasa_promise.csv` exists with proper columns
- Check file path and column naming

## 🎓 Technical Stack

- **Python 3.8+**
- **scikit-learn** – ML algorithms
- **XGBoost** – Gradient boosting
- **Flask** – Web framework
- **Pandas** – Data processing
- **NumPy** – Numerical operations
- **Plotly** – Interactive visualizations

## 📊 Dataset

The system is trained on the **NASA PROMISE dataset**, which contains:
- Software module metrics from real projects
- Defect histories
- Multiple programming languages and project types

Source: http://promise.site.uottawa.ca/

## 🤝 Contributing

To improve the system:

1. Add more models in `models/train_model.py`
2. Enhance feature engineering in `src/feature_engineering.py`
3. Improve UI in `templates/` and `static/`
4. Add more evaluation metrics in `src/evaluation.py`

## 📄 License

This project is provided as-is for educational and commercial use.

## 🙏 Acknowledgments

- NASA PROMISE dataset contributors
- scikit-learn and XGBoost communities
- Flask development team

## 📞 Support

For issues or questions:
1. Check configuration in `config.py`
2. Review logs from Flask output
3. Ensure all dependencies are installed
4. Verify dataset format matches expected columns

---

**FailGuard AI** - Predict and prevent software failures before they reach production. 🛡️
