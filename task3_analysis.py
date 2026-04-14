import pandas as pd
import numpy as np
import os

# -------------------------------
# Step 1: Load and Explore Data
# -------------------------------

file_path = "data/trends_clean.csv"

# Check if file exists
if not os.path.exists(file_path):
    print("Clean CSV file not found. Please run Task 2 first.")
    exit()

# Load CSV
df = pd.read_csv(file_path)

# Print shape
print(f"Loaded data: {df.shape}")

# Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")

# -------------------------------
# Step 2: NumPy Analysis
# -------------------------------

scores = df["score"].values
comments = df["num_comments"].values

print("\n--- NumPy Stats ---")

# Mean, Median, Std
print(f"Mean score   : {np.mean(scores):.2f}")
print(f"Median score : {np.median(scores):.2f}")
print(f"Std deviation: {np.std(scores):.2f}")

# Max and Min
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with most comments
max_comment_index = np.argmax(comments)
top_story_title = df.iloc[max_comment_index]["title"]
top_story_comments = df.iloc[max_comment_index]["num_comments"]

print(f"\nMost commented story: \"{top_story_title}\" — {top_story_comments} comments")

# -------------------------------
# Step 3: Add New Columns
# -------------------------------

# Engagement = num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = score > average score
df["is_popular"] = df["score"] > avg_score

# -------------------------------
# Step 4: Save to CSV
# -------------------------------

output_path = "data/trends_analysed.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")
