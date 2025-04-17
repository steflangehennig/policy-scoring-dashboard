import pandas as pd

# Pull in scoring model results
scores = pd.read_csv("evidence_scores.csv")
scores["number"] = scores["filename"].str.replace(".txt", "", regex=False)

# Pull in CRS metadata for merge
reports_meta = pd.read_csv("reports.csv")

# Merge by CRS report number - doublecheck it matches meta data
merged_df = scores.merge(reports_meta, on="number", how="left")

# Save final enriched data
merged_df.to_csv("scored_crs_reports.csv", index=False) 