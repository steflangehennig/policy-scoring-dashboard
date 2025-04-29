import pandas as pd
from pathlib import Path
import joblib
from sentence_transformers import SentenceTransformer
import os

# load embedder and rubric
embedder = joblib.load("crs_embedder.pkl")
rubric_columns = joblib.load("crs_rubric_columns.pkl")

# load classifiers (.pkl files from classifier)
models = {}
for col in rubric_columns:
    model_path = f"crs_model_{col.replace(' ', '_')}.pkl"
    models[col] = joblib.load(model_path)

# path to full CRS report corpus
txt_dir = Path("data/txt")
txt_files = sorted([f for f in txt_dir.glob("*.txt") if f.stat().st_size > 50])

# extract filenames and text
docs = []
for f in txt_files:
    try:
        text = f.read_text(encoding="utf-8", errors="ignore")
        docs.append({"filename": f.name, "text": text})
    except Exception as e:
        print(f"Error reading {f.name}: {e}")

df = pd.DataFrame(docs)
print(f"Loaded {len(df)} documents.")

# embed all texts
print("Embedding texts...")
embeddings = embedder.encode(df["text"].tolist(), batch_size=32, show_progress_bar=True)

# get prredictions for each rubric dimension
print("Predicting scores...")
for col in rubric_columns:
    clf = models[col]
    df[col] = clf.predict(embeddings)

# calculate total score across dimensions
df["Total Score"] = df[rubric_columns].sum(axis=1)

# assign a summary classification
def classify(total_score):
    if total_score >= 13:
        return "Robust"
    elif total_score >= 9:
        return "Strong"
    elif total_score >= 5:
        return "Moderate"
    else:
        return "Weak"

df["Summary Classification"] = df["Total Score"].apply(classify)

# save predictions
output_path = "model/classifier/crs_predictions.csv"
df[["filename"] + rubric_columns + ["Total Score", "Summary Classification"]].to_csv(output_path, index=False)
print(f"Predictions saved to {output_path}")
