"""Check the training data class distribution."""

import sys
sys.path.insert(0, '.')
import pandas as pd
from src.data_preprocessing import prepare_data

# Load and check data
X_train, X_test, y_train, y_test, feature_names = prepare_data()

print("="*80)
print("TRAINING DATA ANALYSIS")
print("="*80)

print(f"\nTraining set size: {len(y_train)}")
print(f"Test set size: {len(y_test)}")
print(f"\nClass distribution in training set:")

value_counts = pd.Series(y_train).value_counts().sort_index()
for class_label, count in value_counts.items():
    percentage = (count / len(y_train)) * 100
    print(f"  Class {class_label}: {count} samples ({percentage:.1f}%)")

print(f"\nClass distribution in test set:")
value_counts = pd.Series(y_test).value_counts().sort_index()
for class_label, count in value_counts.items():
    percentage = (count / len(y_test)) * 100
    print(f"  Class {class_label}: {count} samples ({percentage:.1f}%)")

print(f"\nTotal defective (class 1) in training: {sum(y_train == 1)}")
print(f"Total safe (class 0) in training: {sum(y_train == 0)}")
