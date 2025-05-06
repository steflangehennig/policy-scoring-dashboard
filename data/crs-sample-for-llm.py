import os
import random
import shutil
import csv

# === CONFIGURATION ===
current_round = 2  # <--- upodate for each new sampling round (needed to add more data)

# set paths
root_dir = "C:/Users/Stefani.Langehennig/OneDrive - University of Denver/Documents/research/du/EBP/my-first-react-app/model/txt-batches/"
output_dir = os.path.join(root_dir, "sample-for-llm")
log_file = os.path.join(output_dir, "sampled-files-log.csv")

# create output directory
os.makedirs(output_dir, exist_ok=True)

# load already sampled filenames to avoid repeats
already_sampled = set()
if os.path.exists(log_file):
    with open(log_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            already_sampled.add(row["filename"])

# for logging
new_sampled_records = []

# loop through each batch folder
for i in range(1, 11):
    batch_name = f"batch_{i:02d}"
    batch_path = os.path.join(root_dir, batch_name)

    if not os.path.exists(batch_path):
        print(f"Skipping missing folder: {batch_path}")
        continue

    txt_files = [f for f in os.listdir(batch_path) if f.endswith('.txt')]
    available_files = list(set(txt_files) - already_sampled)

    if len(txt_files) < 50:
        print(f"Not enough files in {batch_name}, found {len(txt_files)}")
        continue

    sampled_files = random.sample(txt_files, 50)

    for filename in sampled_files:
        src = os.path.join(batch_path, filename)
        dst = os.path.join(output_dir, filename)  # keep OG filename
        shutil.copy(src, dst)

        new_sampled_records.append({"batch": batch_name, "filename": filename, "round_id": current_round})

    print(f"Sampled and copied 50 files from {batch_name}")


# write header only if the log file doesn't exist yet
write_header = not os.path.exists(log_file)

# append to existin log file
with open(log_file, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["batch", "filename", "round_id"])
    if write_header:
        writer.writeheader()
    writer.writerows(new_sampled_records)

print(f"Round {current_round} sampling complete. {len(new_sampled_records)} new files added.")