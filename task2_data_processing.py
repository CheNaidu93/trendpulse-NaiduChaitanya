import pandas as pd
import os

import glob
import os

files = glob.glob("data/trends_*.json")

if not files:
    print("No JSON files found in data/ folder. Run Task 1 first.")
    exit()

latest_file = max(files, key=os.path.getctime)

file_path = latest_file

# Check if file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit()

# Load JSON into DataFrame
df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")

# -------------------------------
# Step 2: Clean the Data
# -------------------------------

# 1. Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove rows with missing critical fields
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Convert data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 4. Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Strip whitespace from title
df["title"] = df["title"].str.strip()

# -------------------------------
# Step 3: Save as CSV
# -------------------------------

output_path = "data/trends_clean.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")

# -------------------------------
# Summary: Stories per category
# -------------------------------

print("\nStories per category:")
print(df["category"].value_counts())
