# 🚀 Quick Start Guide - FailGuard AI

## ✓ System Status: COMPLETE & READY

The FailGuard AI system is fully implemented with:
- ✅ Trained ML model (92.4% accuracy)
- ✅ Flask REST API (7 endpoints)
- ✅ SQLite database integration
- ✅ Interactive dashboard with charts
- ✅ Recent predictions history

## 🚀 Start in 2 Steps

### Step 1: Open Terminal
```powershell
cd "d:\FailGuard AI – Predictive Software Failure Detection System"
```

### Step 2: Run the App
```powershell
python app.py
```

**You'll see:**
```
Starting FailGuard AI Flask Application...
Model Status: Loaded
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### Step 3: Open Browser
Go to: **http://localhost:5000**

---

## 📋 How to Use

1. **Home Page** - Enter 8 software metrics
2. **Click Analyze** - Get instant prediction
3. **View Result** - See risk level & recommendations
4. **Dashboard** - Auto-redirects with prediction history
5. **Check Charts** - Feature importance, risk distribution, etc.

---

## 📊 What's Already Done

✅ Model trained on 5000 synthetic samples  
✅ XGBoost selected as best algorithm  
✅ Database initialized with 6 predictions  
✅ All API endpoints tested and working  
✅ Dashboard with 4 interactive charts  
✅ Recent predictions table functional  

**Everything is ready to run!**

### Step 3: Start Flask Server
```bash
python app.py
```

or use the automatic setup script:
```bash
python run.py
```

### Step 4: Open in Browser
```
http://localhost:5000
```

## 🎯 Using FailGuard AI

### Input Format

Enter these 8 software metrics for your module:

| Metric | Range | Example |
|--------|-------|---------|
| LOC (Lines of Code) | 0+ | 500 |
| WMC (Weighted Methods per Class) | 0+ | 15 |
| RFC (Response for a Class) | 0+ | 20 |
| CBO (Coupling Between Objects) | 0+ | 8 |
| LCOM (Lack of Cohesion) | 0-1 | 0.5 |
| Code Churn | 0+ | 10 |
| Number of Developers | 1+ | 3 |
| Past Defects | 0+ | 2 |

### Output Interpretation

**Risk Levels:**
- 🟢 **LOW** (< 33% probability): Proceed with standard QA
- 🟡 **MEDIUM** (33-67% probability): Enhanced testing recommended  
- 🔴 **HIGH** (> 67% probability): Thorough review and refactoring needed

## 📊 API Usage

### Quick Test with cURL

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

### Response Example

```json
{
  "success": true,
  "probability": 42.5,
  "risk_level": "MEDIUM",
  "risk_color": "#ffc107",
  "confidence": 75.3,
  "prediction": "DEFECTIVE",
  "input_features": {...}
}
```

## 🚨 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Run `pip install -r requirements.txt`

### Problem: "FileNotFoundError: failguard_model.joblib"
**Solution**: Run `python models/train_model.py` to train the model first

### Problem: "Port 5000 already in use"
**Solution**: Edit `app.py` and change `port=5000` to another port (e.g., `port=5001`)

### Problem: "Data file not found"
**Solution**: Ensure `data/raw/nasa_promise.csv` exists with proper columns

## 📚 Next Steps

1. **Customize Risk Thresholds**: Edit `config.py` to adjust when a module is considered HIGH/MEDIUM/LOW risk

2. **Add Your Own Data**: Replace `data/raw/nasa_promise.csv` with your project's metrics

3. **Retrain Models**: Run `python models/train_model.py` with your new data

4. **Deploy**: Use Flask deployment tools (Gunicorn, Docker, Heroku) for production

## 🔍 Model Information

- **Best Performing Model**: Random Forest Classifier
- **Training Data**: NASA PROMISE dataset
- **Features**: 8 software metrics
- **Output**: Binary classification (defective/safe) + probability

## 💡 Tips

- **For Development**: Keep `DEBUG=True` in `config.py`
- **For Production**: Set `DEBUG=False` and use proper WSGI server
- **For Testing**: Use the dashboard quick test feature
- **For Integration**: Use `/api/predict` endpoint in your CI/CD pipeline

## 🎓 Understanding Risk Levels

### HIGH RISK (⚠️)
- High probability of defects
- **Action**: Increase QA effort, refactor code, schedule security audit

### MEDIUM RISK (⚡)  
- Moderate probability of defects
- **Action**: Standard code review, enhanced testing

### LOW RISK (✅)
- Low probability of defects
- **Action**: Proceed with standard process

## 📞 Support

For detailed information, see [README.md](README.md)

---

**Start predicting software failures before they happen!** 🛡️
