import pandas as pd
import os

# Load dataset
df = pd.read_csv("data/preprocessed/cleaned symptom_data.csv")

# Helper to generate fake codes
def generate_code(name):
    return f"C{hash(name) % 10000000:07d}"

# Generate unique disease codes
df['disease_code'] = df['disease'].apply(generate_code)
df['symptom_code'] = df['symptom'].apply(generate_code)

# Create codes.csv (both diseases and symptoms)
disease_codes = df[['disease', 'disease_code']].drop_duplicates().rename(
    columns={'disease': 'name', 'disease_code': 'code'})
disease_codes['type'] = 'disease'

symptom_codes = df[['symptom', 'symptom_code']].drop_duplicates().rename(
    columns={'symptom': 'name', 'symptom_code': 'code'})
symptom_codes['type'] = 'symptom'

codes_df = pd.concat([disease_codes, symptom_codes], ignore_index=True)

# Save codes.csv
os.makedirs("data/structured", exist_ok=True)
codes_df.to_csv("data/structured/codes.csv", index=False)
print("codes.csv created.")

# Save symptom-disease mapping
map_df = df[['disease_code', 'symptom_code']]
map_df.to_csv("data/structured/symptom_disease_map.csv", index=False)
print("symptom_disease_map.csv created.")
