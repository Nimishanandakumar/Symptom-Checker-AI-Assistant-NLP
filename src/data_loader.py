#Code to load raw data into a dataframe


import os
import pandas as pd

def load_and_preprocess(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding='latin1')
    
    # Fill missing values in Disease and Count columns
    df['Disease'] = df['Disease'].fillna(method='ffill')
    df['Count of Disease Occurrence'] = df['Count of Disease Occurrence'].fillna(method='ffill')
    df['Symptom'] = df['Symptom'].astype(str)
    
    # Explode multiple symptoms separated by '^' into separate rows
    df = df.assign(Symptom=df['Symptom'].str.split('^')).explode('Symptom')
    df['Symptom'] = df['Symptom'].str.strip()

    # Create symptom presence matrix: Disease vs Symptom
    symptom_matrix = df.groupby(['Disease', 'Symptom']).size().unstack(fill_value=0).reset_index()
    
    return df, symptom_matrix

def extract_mappings(df: pd.DataFrame):
    # Extract disease codes and descriptions
    df['Disease_Code'] = df['Disease'].str.split('_').str[0]
    df['Disease_Desc'] = df['Disease'].str.split('_').str[1]
    disease_mapping = df[['Disease_Code', 'Disease_Desc']].drop_duplicates().reset_index(drop=True)

    # Extract symptom codes and descriptions
    df['Symptom_Code'] = df['Symptom'].str.split('_').str[0]
    df['Symptom_Desc'] = df['Symptom'].str.split('_').str[1]
    symptom_mapping = df[['Symptom_Code', 'Symptom_Desc']].drop_duplicates().reset_index(drop=True)
    
    return disease_mapping, symptom_mapping


# Paths - UPDATE if needed
raw_file_path = "D:/PYTHON/Demo-python/Symptom-Checker-AI-Assistant-NLP/data/raw/dataset_uncleaned.csv"
preprocessed_dir = "D:/PYTHON/Demo-python/Symptom-Checker-AI-Assistant-NLP/data/preprocessed/"
mapping_dir = "D:/PYTHON/Demo-python/Symptom-Checker-AI-Assistant-NLP/data/mappings/"

# Create output folders if not present
os.makedirs(preprocessed_dir, exist_ok=True)
os.makedirs(mapping_dir, exist_ok=True)

if not os.path.exists(raw_file_path):
    print(f"❌ Raw data file NOT found at: {raw_file_path}")
else:
    # Load and preprocess data
    full_df, symptom_matrix = load_and_preprocess(raw_file_path)

    # Save the processed symptom-disease matrix CSV
    symptom_matrix.to_csv(preprocessed_dir + "processed_symptom_disease_dataset.csv", index=False)
    print(f"✅ Processed symptom-disease matrix saved to {preprocessed_dir}")

    # Extract and save the mappings CSV files
    disease_mapping, symptom_mapping = extract_mappings(full_df)
    disease_mapping.to_csv(mapping_dir + "disease_mappings.csv", index=False)
    symptom_mapping.to_csv(mapping_dir + "symptom_mappings.csv", index=False)
    print(f"✅ Disease and Symptom mappings saved to {mapping_dir}")

