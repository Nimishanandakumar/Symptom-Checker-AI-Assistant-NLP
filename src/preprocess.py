# Code for cleaning and feature engineering

import pandas as pd
import os

def load_and_preprocess(file_path: str):
    # Load raw data with encoding to avoid decode errors
    df = pd.read_csv(file_path, encoding='latin1')
    
    # Fill missing 'Disease' and 'Count of Disease Occurrence' by forward fill
    df['Disease'] = df['Disease'].fillna(method='ffill')
    df['Count of Disease Occurrence'] = df['Count of Disease Occurrence'].fillna(method='ffill')
    
    # Convert Symptom to string and explode on '^'
    df['Symptom'] = df['Symptom'].astype(str)
    df = df.assign(Symptom=df['Symptom'].str.split('^')).explode('Symptom')
    df['Symptom'] = df['Symptom'].str.strip()
    
    # Create disease mapping with code and name separated
    disease_mapping = df[['Disease']].drop_duplicates().reset_index(drop=True)
    disease_mapping[['Disease_Code', 'Disease_Name']] = disease_mapping['Disease'].str.split('_', n=1, expand=True)
    
    # Create symptom mapping with code and name separated
    symptom_mapping = df[['Symptom']].drop_duplicates().reset_index(drop=True)
    symptom_mapping[['Symptom_Code', 'Symptom_Name']] = symptom_mapping['Symptom'].str.split('_', n=1, expand=True)
    
    # Save mappings to files - create dirs if not exist
    os.makedirs(r"D:\PYTHON\Demo-python\Symptom-Checker-AI-Assistant-NLP\data\mappings", exist_ok=True)
    disease_mapping.to_csv(r"D:\PYTHON\Demo-python\Symptom-Checker-AI-Assistant-NLP\data\mappings\disease_mapping.csv", index=False)
    symptom_mapping.to_csv(r"D:\PYTHON\Demo-python\Symptom-Checker-AI-Assistant-NLP\data\mappings\symptom_mapping.csv", index=False)
    
    # Create symptom matrix (features) with diseases (target)
    symptom_matrix = df.groupby(['Disease', 'Symptom']).size().unstack(fill_value=0).reset_index()
    
    # Remove codes from Disease column for final dataset
    symptom_matrix['Disease'] = symptom_matrix['Disease'].str.split('_', n=1).str[1]
    
    # Remove codes from symptom columns - rename columns to symptom names only
    new_cols = ['Disease']
    for col in symptom_matrix.columns[1:]:
        symptom_name = col.split('_', 1)[1] if '_' in col else col
        new_cols.append(symptom_name)
    symptom_matrix.columns = new_cols
    
    # Save final processed data
    os.makedirs(r"D:\PYTHON\Demo-python\Symptom-Checker-AI-Assistant-NLP\data\preprocessed", exist_ok=True)
    symptom_matrix.to_csv(r"D:\PYTHON\Demo-python\Symptom-Checker-AI-Assistant-NLP\data\preprocessed\processed_symptom_disease_dataset.csv", index=False)
    
    print("✅ Data preprocessing complete.")
    
# Run preprocessing
file_path = r"D:\PYTHON\Demo-python\Symptom-Checker-AI-Assistant-NLP\data\raw\dataset_uncleaned.csv"
load_and_preprocess(file_path)

