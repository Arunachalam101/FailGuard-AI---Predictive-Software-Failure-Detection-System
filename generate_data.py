import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

# Generate 200 sample software modules
n_samples = 200

data = {
    'loc': np.random.randint(50, 2000, n_samples),  # Lines of Code
    'wmc': np.random.randint(1, 50, n_samples),      # Weighted Methods per Class
    'rfc': np.random.randint(5, 100, n_samples),     # Response for a Class
    'cbo': np.random.randint(0, 30, n_samples),      # Coupling Between Objects
    'lcom': np.random.uniform(0, 1, n_samples),      # Lack of Cohesion
    'code_churn': np.random.randint(0, 50, n_samples),  # Code Churn
    'num_developers': np.random.randint(1, 10, n_samples),  # Number of Developers
    'past_defects': np.random.randint(0, 10, n_samples),   # Past Defects
}

# Create defect target (binary) with realistic distribution
# Higher metrics correlate with higher defect probability
loc = data['loc']
wmc = data['wmc']
cbo = data['cbo']
lcom = data['lcom']
past_defects = data['past_defects']

# Simple heuristic: modules with higher complexity/past defects are more likely to be defective
defect_probability = (
    (loc / 2000) * 0.2 +  # Larger modules are riskier
    (wmc / 50) * 0.3 +    # Higher complexity is risky
    (cbo / 30) * 0.2 +    # More coupling = more risk
    lcom * 0.1 +           # Low cohesion = more risk
    (past_defects / 10) * 0.2  # Past defects = future defects
)

# Clip to 0-1 range and add some randomness
defect_probability = np.clip(defect_probability, 0, 1)
defect_probability += np.random.normal(0, 0.1, n_samples)
defect_probability = np.clip(defect_probability, 0, 1)

# Generate binary defects based on probability
data['defects'] = (np.random.random(n_samples) < defect_probability).astype(int)

# Create DataFrame
df = pd.DataFrame(data)

# Ensure all values are integers except lcom
df['loc'] = df['loc'].astype(int)
df['wmc'] = df['wmc'].astype(int)
df['rfc'] = df['rfc'].astype(int)
df['cbo'] = df['cbo'].astype(int)
df['lcom'] = df['lcom'].round(3)
df['code_churn'] = df['code_churn'].astype(int)
df['num_developers'] = df['num_developers'].astype(int)
df['past_defects'] = df['past_defects'].astype(int)

# Save to CSV
output_path = Path('data/raw/nasa_promise.csv')
df.to_csv(output_path, index=False)

print("✅ Sample dataset generated successfully!")
print(f"📊 File: {output_path}")
print(f"📈 Records: {len(df)}")
print(f"📋 Columns: {', '.join(df.columns)}")
print(f"\n🎯 Defect Distribution:")
print(f"   Safe modules: {(df['defects'] == 0).sum()} ({(df['defects'] == 0).sum()/len(df)*100:.1f}%)")
print(f"   Defective modules: {(df['defects'] == 1).sum()} ({(df['defects'] == 1).sum()/len(df)*100:.1f}%)")
print(f"\n📊 Sample rows:")
print(df.head(10))
