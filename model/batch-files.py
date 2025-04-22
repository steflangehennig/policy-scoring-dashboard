import os
from pathlib import Path
import shutil

# Batching final files to prep for modeling in Colab
# Using "final" files from data/crs-filter-final.py - deleted after batched to clear up space
    # Run again if final files are needed again

# Set paths
base_dir = Path.cwd()
source_dir = base_dir / "data/txt-final"
batch_root = base_dir / "model/txt-batches"
batch_root.mkdir(parents=True, exist_ok=True)

# Set up batch size and file paths
batch_size = 2000
txt_files = sorted(source_dir.glob("*.txt"))

print(f"Found {len(txt_files)} .txt files in {source_dir}")

if not txt_files:
    print("No .txt files found. Double-check path or permissions.")
else:
    for i in range(0, len(txt_files), batch_size):
        batch_num = i // batch_size + 1
        batch_dir = batch_root / f"batch_{batch_num:02d}"
        batch_dir.mkdir(exist_ok=True)
        
        batch_files = txt_files[i:i + batch_size]
        print(f"Creating {batch_dir} with {len(batch_files)} files...")

        for file in batch_files:
            try:
                shutil.copy2(file, batch_dir / file.name)
            except Exception as e:
                print(f"Failed to copy {file.name}: {e}")

    print(f"Finished: {len(list(batch_root.glob('batch_*')))} batches created.")
