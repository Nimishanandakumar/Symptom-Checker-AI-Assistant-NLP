# Code for cleaning 

import csv
import os
import pandas as pd


input_file = './data/dataset_uncleaned.csv'
output_file = './data/preprocessed/cleaned symptom_data.csv'

def clean_symptom(symptom):
    # Remove UMLS codes and split ^ symbols
    if '^' in symptom:
        parts = symptom.split('^')
        return [p.split('_', 1)[-1].strip().lower() for p in parts]
    return [symptom.split('_', 1)[-1].strip().lower()]

def preprocess_raw_data():
    with open(input_file, 'r', encoding='latin1') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        
        data = []
        current_disease = None
        current_count = None

        for row in reader:
            disease, count, symptom_raw = row
            if disease:
                current_disease = disease.split('_', 1)[-1].strip().lower()
                current_count = int(count)
            
            if symptom_raw:
                cleaned_symptoms = clean_symptom(symptom_raw)
                for sym in cleaned_symptoms:
                    data.append({
                        'disease': current_disease,
                        'count': current_count,
                        'symptom': sym
                    })

    # Convert to DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f" Cleaned data written to {output_file}")

if __name__ == "__main__":
    preprocess_raw_data()


