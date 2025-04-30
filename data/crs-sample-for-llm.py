import os
import random
import shutil
import csv

# set paths
root_dir = "C:/Users/Stefani.Langehennig/OneDrive - University of Denver/Documents/research/du/EBP/my-first-react-app/model/txt-batches/"
output_dir = os.path.join(root_dir, "sample-for-llm")
log_file = os.path.join(output_dir, "sampled-files-log.csv")

# create output directory
os.makedirs(output_dir, exist_ok=True)

# for logging
sampled_records = []

# loop through each batch folder
for i in range(1, 11):
    batch_name = f"batch_{i:02d}"
    batch_path = os.path.join(root_dir, batch_name)

    if not os.path.exists(batch_path):
        print(f"Skipping missing folder: {batch_path}")
        continue

    txt_files = [f for f in os.listdir(batch_path) if f.endswith('.txt')]

    if len(txt_files) < 50:
        print(f"Not enough files in {batch_name}, found {len(txt_files)}")
        continue

    sampled_files = random.sample(txt_files, 50)

    for filename in sampled_files:
        src = os.path.join(batch_path, filename)
        dst = os.path.join(output_dir, filename)  # Preserve original filename
        shutil.copy(src, dst)

        sampled_records.append({"batch": batch_name, "filename": filename})

    print(f"Sampled and copied 50 files from {batch_name}")

# write the log to CSV
with open(log_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["batch", "filename"])
    writer.writeheader()
    writer.writerows(sampled_records)
print(f"Sampling complete. Log saved to: {log_file}")
