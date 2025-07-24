import pandas as pd
import os

# Load raw data
df = pd.read_csv("data/raw/dataset_uncleaned.csv", encoding='latin1')

# === Clean missing data ===
df['Disease'] = df['Disease'].ffill()
df['Count of Disease Occurrence'] = df['Count of Disease Occurrence'].ffill()

# === Split disease into code and description ===
df[['Disease_Code', 'Disease_Desc']] = df['Disease'].str.split(pat='_', n=1, expand=True)

# === Split symptoms with multiple entries (^ symbol) ===
df['Symptom'] = df['Symptom'].astype(str)  # Ensure string type
df = df.assign(Symptom=df['Symptom'].str.split('^')).explode('Symptom')

# === Split symptom into code and description ===
df[['Symptom_Code', 'Symptom_Desc']] = df['Symptom'].str.split(pat='_', n=1, expand=True)

# === Remove 'UMLS:' prefix if it exists ===
df['Disease_Code'] = df['Disease_Code'].str.replace('UMLS:', '', regex=False)
df['Symptom_Code'] = df['Symptom_Code'].str.replace('UMLS:', '', regex=False)

# === Create codes.csv ===
disease_codes = df[['Disease_Code', 'Disease_Desc']].drop_duplicates().rename(
    columns={'Disease_Code': 'code', 'Disease_Desc': 'name'})
disease_codes['type'] = 'disease'

symptom_codes = df[['Symptom_Code', 'Symptom_Desc']].drop_duplicates().rename(
    columns={'Symptom_Code': 'code', 'Symptom_Desc': 'name'})
symptom_codes['type'] = 'symptom'

codes_df = pd.concat([disease_codes, symptom_codes], ignore_index=True)

# === Create mapping file ===
map_df = df[['Disease_Code', 'Symptom_Code']].drop_duplicates().rename(
    columns={'Disease_Code': 'disease_code', 'Symptom_Code': 'symptom_code'})

# === Save output files ===
output_dir = "data/structured"
os.makedirs(output_dir, exist_ok=True)

codes_df.to_csv(f"{output_dir}/codes.csv", index=False)
map_df.to_csv(f"{output_dir}/symptom_disease_map.csv", index=False)

print("codes.csv and symptom_disease_map.csv saved to:", output_dir)

