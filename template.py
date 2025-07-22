import os

folders = [
    "data/raw",
    "data/preprocessed",
    "notebooks",
    "src",
    "app",
    "config",
    "tests"
    ]

files_with_content = {
    "src/__init__.py":"",
    "src/data_loader.py":"#Code to load raw data into a dataframe\n",
    "src/preprocess.py":"# Code for cleaning and feature engineering\n",
    "src/train.py":"#Code to train and save the ML model\n",
    "src/model.py":"#Define custom ML models or wrappers\n",
    "src/evaluate.py": "# Evaluate trained model (accuracy, confusion matrix)\n",
    "src/predict.py": "# Load model and make predictions\n",

    "app/__init__.py": "",
    "app/main.py": "# FastAPI or Streamlit app to serve predictions\n",
    "app/requirements.txt": "# Minimal dependencies for the deployed app\n",

    "config/config.yaml": "# Optional: add paths and hyperparameters\n",

    "notebooks/eda.ipynb": "",

    "tests/test_pipeline.py": "# Tests for data pipeline and model\n",

    "README.md": "# NLP Project\n\nThis project does classification with end-to-end deployment.",
    "requirements.txt": "# Project-wide Python dependencies\n",
    "run.py": "# Optional: script to run full training pipeline\n"
}

for folder in folders:
    os.makedirs(folder,exist_ok=True)

for file_path,content in files_with_content.items():
    with open(file_path,'w') as f:
        f.write(content)

print("Project Structure created successfully")