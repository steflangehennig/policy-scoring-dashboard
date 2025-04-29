import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
import joblib

# set paths
csv_path = Path("model/classifier/evidence_scores_cleaned.csv")
txt_dir = Path("model/txt-batches/batch_01")
embedding_model = "all-MiniLM-L6-v2"

rubric_columns = [
    "Use of Empirical Research Score",
    "Formal Evidence-Gathering Process Score",
    "Transparency and Accessibility Score",
    "Expert and Stakeholder Input Score",
    "Evaluation and Iteration Score"
]

# load sample of LLM EBP scores
df = pd.read_csv(csv_path)
df = df[["filename"] + rubric_columns].dropna()

# read txt files
def load_text(filename):
    path = txt_dir / filename
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""

df["text"] = df["filename"].apply(load_text)
df = df[df["text"].str.len() > 50]  # remove empties
print(f"Loaded {len(df)} labeled documents with text.")

# generate embeddings
embedder = SentenceTransformer(embedding_model)
X = embedder.encode(df["text"].tolist(), batch_size=32, show_progress_bar=True)

# split into training/testing data
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

# train classifier for each rubric dimension - random forest to start
models = {}
print("Training classifiers per rubric dimension...")
for col in rubric_columns:
    y_train = df_train[col]
    y_test = df_test[col]

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(f"\n{col} — Classification Report")
    print(classification_report(y_test, y_pred))

    models[col] = clf
    joblib.dump(clf, f"crs_model_{col.replace(' ', '_')}.pkl")

# predict and eval model
y_pred = clf.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# save model and embeddings
joblib.dump(embedder, "crs_embedder.pkl")
joblib.dump(rubric_columns, "crs_rubric_columns.pkl")
print("Saved model and embedder.")
