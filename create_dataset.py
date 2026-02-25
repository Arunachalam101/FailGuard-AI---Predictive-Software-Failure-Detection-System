import pandas as pd
import numpy as np
from pathlib import Path

print("📊 Generating 5000 synthetic software module samples...")
print("=" * 70)

np.random.seed(42)

# Generate 5000 samples with all feature combinations
data = {
    'loc': np.clip(np.random.lognormal(mean=5.5, sigma=1.2, size=5000).astype(int), 10, 15000),
    'wmc': np.clip(np.random.gamma(shape=3, scale=5, size=5000).astype(int), 1, 100),
    'rfc': np.clip(np.random.gamma(shape=2, scale=8, size=5000).astype(int), 1, 150),
    'cbo': np.clip(np.random.gamma(shape=2, scale=4, size=5000).astype(int), 0, 80),
    'lcom': np.clip(np.random.uniform(0, 1, size=5000), 0, 1),
    'code_churn': np.clip(np.random.exponential(scale=8, size=5000).astype(int), 0, 200),
    'num_developers': np.clip(np.random.poisson(lam=3, size=5000), 1, 20),
    'past_defects': np.clip(np.random.poisson(lam=2, size=5000), 0, 50),
}

df = pd.DataFrame(data)

# Generate defect label based on complexity metrics
complexity_score = (
    (df['loc'] / df['loc'].max()) * 0.2 +
    (df['wmc'] / df['wmc'].max()) * 0.25 +
    (df['rfc'] / df['rfc'].max()) * 0.2 +
    (df['cbo'] / df['cbo'].max()) * 0.15 +
    df['lcom'] * 0.1 +
    (df['code_churn'] / df['code_churn'].max()) * 0.1
)

defect_probability = (
    0.3 * complexity_score +
    0.1 * (df['past_defects'] / (df['past_defects'].max() + 1))
)

defect_probability += np.random.normal(0, 0.05, size=5000)
defect_probability = np.clip(defect_probability, 0, 1)

df['defects'] = (np.random.random(size=5000) < defect_probability).astype(int)

# Save to CSV
Path('data/raw').mkdir(parents=True, exist_ok=True)
df.to_csv('data/raw/nasa_promise.csv', index=False)

print(f"✅ Generated 5000 samples with all feature combinations")
print(f"   Shape: {df.shape}")
print(f"   Defect Rate: {df['defects'].sum()} samples ({df['defects'].mean()*100:.1f}%)")
print(f"   File: data/raw/nasa_promise.csv")
print(f"   Size: {Path('data/raw/nasa_promise.csv').stat().st_size / 1024:.1f} KB")

print("\n📊 Dataset Statistics:")
print("=" * 70)
print(df.describe().T.to_string())

print("\n📋 Sample Data (first 5 rows):")
print(df.head().to_string())

print("\n✅ Data generation complete! Ready to train models.")
