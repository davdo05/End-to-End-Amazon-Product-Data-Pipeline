import pandas as pd
import os

folder_path = "../"
csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

dataframes = []

original_rows = 0
dropped_duplicates = 0
dropped_nulls = 0

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    try:
        df = pd.read_csv(file_path)
        original_rows += len(df)

        before_dupes = len(df)
        df.drop_duplicates(subset=["name"], inplace=True)

        dropped_duplicates += before_dupes - len(df)

        before_nulls = len(df)
        df.dropna(subset=["name", "ratings"], inplace=True)
        dropped_nulls += before_nulls - len(df)

        # Keep only numeric ratings
        df = df[pd.to_numeric(df["ratings"], errors="coerce").notna()]


        df["source_file"] = file  # Track origin
        dataframes.append(df)

    except Exception as e:
        print(f"Error loading {file}: {e}")

# Combine all cleaned data
combined_df = pd.concat(dataframes, ignore_index=True)

# remove duplicates across all files based on product name
before_final_dupes = len(combined_df)
combined_df.drop_duplicates(subset=["name"], inplace=True)
final_dropped = before_final_dupes - len(combined_df)

# Sort alphabetically by product name
combined_df.sort_values(by="name", inplace=True)

# Save to CSV
#combined_df.to_csv("combined_amazon_data.csv", index=False)

# Final report
print(" Cleaning Summary:")
print(f"• Files combined           : {len(csv_files)}")
print(f"• Original rows            : {original_rows:,}")
print(f"• Duplicates removed       : {dropped_duplicates + final_dropped:,}")
print(f"• Nulls removed            : {dropped_nulls:,}")
print(f"• Final cleaned rows       : {combined_df.shape[0]:,}")
print(f"• Final number of columns  : {combined_df.shape[1]}")
