import pandas as pd
import os

# Load raw data
df = pd.read_csv("data/raw/dataset_uncleaned.csv", encoding='latin1')

# Fill forward missing Disease and Count values
df['Disease'] = df['Disease'].fillna(method='ffill')
df['Count of Disease Occurrence'] = df['Count of Disease Occurrence'].fillna(method='ffill')

# Split disease into code and name
df[['Disease_Code', 'Disease_Desc']] = df['Disease'].str.split('_', 1, expand=True)

# Split multiple symptoms by ^ and explode into rows
df['Symptom'] = df['Symptom'].astype(str)
df = df.assign(Symptom=df['Symptom'].str.split('^')).explode('Symptom')

# Split symptom into code and name
df[['Symptom_Code', 'Symptom_Desc']] = df['Symptom'].str.split('_', 1, expand=True)

# === Create codes.csv ===
disease_codes = df[['Disease_Code', 'Disease_Desc']].drop_duplicates().rename(
    columns={'Disease_Code': 'code', 'Disease_Desc': 'name'})
disease_codes['type'] = 'disease'

symptom_codes = df[['Symptom_Code', 'Symptom_Desc']].drop_duplicates().rename(
    columns={'Symptom_Code': 'code', 'Symptom_Desc': 'name'})
symptom_codes['type'] = 'symptom'

codes_df = pd.concat([disease_codes, symptom_codes], ignore_index=True)

# === Create symptom_disease_map.csv ===
map_df = df[['Disease_Code', 'Symptom_Code']].drop_duplicates().rename(
    columns={'Disease_Code': 'disease_code', 'Symptom_Code': 'symptom_code'})

# === Save files ===
output_dir = "data/structured"
os.makedirs(output_dir, exist_ok=True)

codes_df.to_csv(f"{output_dir}/codes.csv", index=False)
map_df.to_csv(f"{output_dir}/symptom_disease_map.csv", index=False)

print("codes.csv and symptom_disease_map.csv saved to:", output_dir)

