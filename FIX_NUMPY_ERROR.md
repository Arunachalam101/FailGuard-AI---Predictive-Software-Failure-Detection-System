# ❌ Fix: "ModuleNotFoundError: No module named 'numpy._core'"

## 🔍 What's the Problem?

This error happens when:
- The pre-trained model was created with an older version of numpy
- You're running a newer version of Python/numpy
- The saved model files are not compatible with your environment

## ✅ Quick Fix (1 Minute)

### For Windows (PowerShell/CMD):
```powershell
python retrain_model.py
```

### For Mac/Linux (Terminal):
```bash
python retrain_model.py
```

**That's it!** This script will:
1. Load the training data
2. Train 4 models on your machine
3. Save them in a way compatible with YOUR environment
4. Test that everything works

### After Running:
```powershell
python app.py
```

Now the Flask app should start with no errors!

---

## 🔧 What Does `retrain_model.py` Do?

- Loads the 5000 training samples
- Trains Logistic Regression, Random Forest, XGBoost, and SVM
- Picks the best model
- Saves it in a format your Python version understands
- Tests everything works

**Retraining takes 1-2 minutes.**

---

## 💡 Why Does This Happen?

Newer versions of NumPy changed their internal structure. When the old pickle file tries to load, it can't find the old numpy modules. By retraining on your machine, we create pickle files that work with YOUR numpy version.

---

## 🎯 Alternative: Update Packages

If you want to keep the old models, update your packages to older versions:

```powershell
pip install --upgrade scikit-learn xgboost numpy
```

But **retraining is recommended** - it ensures everything is compatible.

---

## ❓ Still Having Issues?

1. Make sure you're in the project folder:
   ```powershell
   cd "FailGuard AI – Predictive Software Failure Detection System"
   ```

2. Make sure you ran `pip install -r requirements.txt`

3. Try retraining again:
   ```powershell
   python retrain_model.py
   ```

4. Then start the app:
   ```powershell
   python app.py
   ```

---

**Everything should work now!** 🚀
