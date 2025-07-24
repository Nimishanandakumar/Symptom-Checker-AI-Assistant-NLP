import pandas as pd

df = pd.read_csv('data/preprocessed/cleaned symptom_data.csv')

df['presence'] = 1

ml_data = df.pivot_table(index='disease', columns='symptom', values='presence', fill_value=0).reset_index()

ml_data.to_csv('data/structured/ml_dataset.csv', index=False)
print("ML dataset saved")
