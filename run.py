#!/usr/bin/env python
"""
FailGuard AI - Setup and Launch Script

This script helps you get started with FailGuard AI by:
1. Checking dependencies
2. Training the ML model (if not already trained)
3. Starting the Flask web server
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed."""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'sklearn', 'xgboost', 'flask', 'joblib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("\nInstalling missing packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully!")
    else:
        print("\n✅ All dependencies are installed!")
    
    return True

def check_data():
    """Check if data file exists."""
    print("\n📊 Checking data files...")
    data_path = Path('data/raw/nasa_promise.csv')
    
    if data_path.exists():
        print(f"  ✅ NASA PROMISE dataset found: {data_path}")
        return True
    else:
        print(f"  ❌ Data file not found: {data_path}")
        print("     Please ensure nasa_promise.csv exists in data/raw/")
        return False

def check_model():
    """Check if model is already trained."""
    print("\n🤖 Checking models...")
    model_path = Path('models/failguard_model.joblib')
    scaler_path = Path('models/scaler.joblib')
    
    model_exists = model_path.exists()
    scaler_exists = scaler_path.exists()
    
    if model_exists:
        print(f"  ✅ Model found: {model_path}")
    else:
        print(f"  ❌ Model not found: {model_path}")
    
    if scaler_exists:
        print(f"  ✅ Scaler found: {scaler_path}")
    else:
        print(f"  ❌ Scaler not found: {scaler_path}")
    
    return model_exists and scaler_exists

def train_model():
    """Train the ML model."""
    print("\n🚀 Training ML models...")
    print("=" * 60)
    
    try:
        subprocess.check_call([sys.executable, 'models/train_model.py'])
        print("=" * 60)
        print("✅ Model training completed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("=" * 60)
        print("❌ Model training failed!")
        return False

def start_flask():
    """Start the Flask application."""
    print("\n🌐 Starting Flask application...")
    print("=" * 60)
    print("FailGuard AI will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    try:
        subprocess.call([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n✅ Flask server stopped.")

def main():
    """Main execution flow."""
    print("\n" + "=" * 60)
    print("🛡️  FailGuard AI - Predictive Software Failure Detection")
    print("=" * 60 + "\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check data
    if not check_data():
        sys.exit(1)
    
    # Check and train model
    if not check_model():
        print("\n⚠️  Model not found. Training new model...")
        if not train_model():
            sys.exit(1)
    else:
        print("\n✅ Model is ready!")
    
    # Ask user if they want to start Flask
    print("\n" + "=" * 60)
    print("Setup Complete! ✅")
    print("=" * 60)
    print("\nYou can now start the Flask server to use FailGuard AI.")
    print("\nOptions:")
    print("1. Start Flask server now")
    print("2. Exit (start Flask manually later with: python app.py)")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == '1':
        start_flask()
    else:
        print("\nTo start the Flask server later, run:")
        print("  python app.py")
        print("\nThen open http://localhost:5000 in your browser.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
