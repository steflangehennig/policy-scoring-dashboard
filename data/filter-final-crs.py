import pandas as pd
import re
from pathlib import Path
from shutil import copy2

# Paths
project_dir = Path("data")
txt_dir = project_dir / "txt"
metadata_file = project_dir / "reports.csv"
output_dir = project_dir / "txt_final"
output_dir.mkdir(exist_ok=True)

# Extract metadata from text files
def extract_metadata(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    report_id_match = re.search(r"Order Code\s+([A-Z0-9\-]+)", content)
    report_id = report_id_match.group(1).strip() if report_id_match else filepath.stem

    date_match = re.search(r"(Updated\s+)?([A-Z][a-z]+ \d{1,2}, \d{4})", content)
    pub_date = date_match.group(2).strip() if date_match else None

    return {
        "filename": filepath.name,
        "report_id": report_id,
        "publication_date": pub_date
    }

print("Extracting metadata from .txt files...")
txt_files = list(txt_dir.glob("*.txt"))
metadata = pd.DataFrame([extract_metadata(f) for f in txt_files])

# Load and prep CRS metadata
print("Loading reports.csv...")
crs_meta = pd.read_csv(metadata_file)
crs_meta["number"] = crs_meta["number"].astype(str).str.upper().str.strip()
metadata["report_id"] = metadata["report_id"].astype(str).str.upper().str.strip()

# Merge text metadata with CRS metadata
merged = metadata.merge(crs_meta, how="left", left_on="report_id", right_on="number")

# Drop duplicates and keep latest publication date per report ID var
print("Filtering to latest version per report...")
merged["latestPubDate"] = pd.to_datetime(merged["latestPubDate"], errors="coerce")
final_versions = (
    merged.sort_values("latestPubDate")
    .drop_duplicates(subset="report_id", keep="last")
    .dropna(subset=["latestPubDate"])
)

# Copy final versions to a new folder
print(f"Copying {len(final_versions)} final version .txt files to {output_dir}...")
for _, row in final_versions.iterrows():
    src = txt_dir / row["filename"]
    dst = output_dir / row["filename"]
    if src.exists():
        copy2(src, dst)

print("Done. Final version of reports ready.")
