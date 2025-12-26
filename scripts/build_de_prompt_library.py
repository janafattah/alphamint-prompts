#!/usr/bin/env python3
"""
Script to merge all German prompt CSVs from library/de/ into a single file.

This script:
1. Recursively finds all CSV files under library/de/
2. Reads and combines them into a single DataFrame
3. Standardizes columns to the target schema
4. Filters for German language prompts
5. Removes duplicates
6. Saves the result to library/de/notion_prompts_de_full.csv
"""

import os
import re
from pathlib import Path

import pandas as pd

# Target columns in the correct order
TARGET_COLUMNS = [
    "Title",
    "PromptURL",
    "Description",
    "Category",
    "Level",
    "PromptTags",
    "Updated"
]

# Column mapping for different CSV structures
COLUMN_MAPPINGS = {
    "RawURL": "PromptURL",
    "Tags": "PromptTags",
    "Path": None,  # Ignore
    "SourcePath": None,  # Ignore
}

# German indicators for language detection
GERMAN_UMLAUTS = set("äöüÄÖÜß")
GERMAN_WORDS = {
    "und", "für", "mit", "der", "die", "das", "ein", "eine", "ist", "sind",
    "wird", "werden", "hat", "haben", "kann", "können", "auf", "bei", "nach",
    "über", "unter", "zwischen", "durch", "ohne", "gegen", "bis", "seit",
    "projekt", "ziele", "finanzen", "bericht", "analyse", "erstellen",
    "entwicklung", "strategie", "unternehmen", "mitarbeiter", "kunden",
    "produkt", "prozess", "lösung", "anwendung", "beispiel", "schritt",
    "aufgabe", "inhalt", "zusammenfassung", "bewertung", "planung",
    "optimierung", "verbesserung", "umsetzung", "einführung", "nutzung",
    "bereich", "aspekt", "faktor", "methode", "ansatz", "konzept",
    "anforderung", "empfehlung", "entscheidung", "herausforderung",
}


def is_german_text(text: str) -> bool:
    """
    Check if the given text is likely German using heuristics.

    Args:
        text: The text to check

    Returns:
        True if the text appears to be German
    """
    if not text or not isinstance(text, str):
        return False

    text_lower = text.lower()

    # Check for German umlauts
    if any(char in text for char in GERMAN_UMLAUTS):
        return True

    # Check for German words
    words = set(re.findall(r'\b\w+\b', text_lower))
    german_word_count = len(words & GERMAN_WORDS)

    # If at least 2 German words are found, consider it German
    if german_word_count >= 2:
        return True

    # Single German word with certain length
    if german_word_count >= 1 and len(text) > 20:
        return True

    return False


def is_german_row(row: pd.Series) -> bool:
    """
    Check if a row contains German content by examining Title and Description.

    Args:
        row: A pandas Series representing a row

    Returns:
        True if the row appears to contain German content
    """
    title = str(row.get("Title", ""))
    description = str(row.get("Description", ""))

    # Check both Title and Description
    return is_german_text(title) or is_german_text(description)


def extract_category_from_path(file_path: Path, base_path: Path) -> str:
    """
    Extract category from the file path based on parent folder.

    Args:
        file_path: Path to the CSV file
        base_path: Base path (library/de/)

    Returns:
        Category string derived from folder name
    """
    try:
        relative = file_path.relative_to(base_path)
        parts = relative.parts
        if len(parts) > 1:
            # Return the first subdirectory as category
            return parts[0]
    except ValueError:
        pass
    return ""


def standardize_columns(df: pd.DataFrame, source_file: Path, base_path: Path) -> pd.DataFrame:
    """
    Standardize DataFrame columns to match the target schema.

    Args:
        df: Input DataFrame
        source_file: Path to the source file (for category extraction)
        base_path: Base path for relative category extraction

    Returns:
        DataFrame with standardized columns
    """
    # Apply column mappings
    rename_map = {}
    for old_col, new_col in COLUMN_MAPPINGS.items():
        if old_col in df.columns and new_col is not None:
            rename_map[old_col] = new_col

    if rename_map:
        df = df.rename(columns=rename_map)

    # Ensure all target columns exist
    for col in TARGET_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    # Fill missing Category from folder name
    folder_category = extract_category_from_path(source_file, base_path)
    if folder_category:
        # Only fill where Category is empty
        df["Category"] = df["Category"].apply(
            lambda x: folder_category if pd.isna(x) or str(x).strip() == "" else x
        )

    # Select only target columns in the correct order
    result = df[TARGET_COLUMNS].copy()

    # Fill NaN with empty strings
    result = result.fillna("")

    return result


def find_csv_files(base_path: Path) -> list:
    """
    Recursively find all CSV files under the base path.

    Args:
        base_path: Path to search in

    Returns:
        List of Path objects for CSV files
    """
    csv_files = []
    for csv_file in base_path.rglob("*.csv"):
        # Skip the output file if it already exists
        if csv_file.name == "notion_prompts_de_full.csv":
            continue
        csv_files.append(csv_file)
    return sorted(csv_files)


def main():
    """Main function to build the German prompt library."""
    # Determine paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    library_de_path = repo_root / "library" / "de"
    output_file = library_de_path / "notion_prompts_de_full.csv"

    print(f"Base path: {library_de_path}")
    print(f"Output file: {output_file}")
    print("-" * 60)

    # Find all CSV files
    csv_files = find_csv_files(library_de_path)
    print(f"Found {len(csv_files)} CSV files:")
    for f in csv_files:
        print(f"  - {f.relative_to(library_de_path)}")
    print("-" * 60)

    # Read and combine all CSVs
    all_dfs = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, encoding="utf-8")
            if df.empty:
                print(f"  Skipping empty file: {csv_file.name}")
                continue

            # Standardize columns
            df = standardize_columns(df, csv_file, library_de_path)

            # Add source file info for debugging
            df["_source_file"] = csv_file.name

            all_dfs.append(df)
            print(f"  Read {len(df)} rows from {csv_file.name}")
        except Exception as e:
            print(f"  Error reading {csv_file.name}: {e}")

    if not all_dfs:
        print("No data found. Exiting.")
        return

    # Combine all DataFrames
    combined_df = pd.concat(all_dfs, ignore_index=True)
    rows_before_filter = len(combined_df)
    print("-" * 60)
    print(f"Total rows before filtering: {rows_before_filter}")

    # Filter for German content
    german_mask = combined_df.apply(is_german_row, axis=1)
    german_df = combined_df[german_mask].copy()
    rows_after_german_filter = len(german_df)
    print(f"Rows after German filter: {rows_after_german_filter}")

    # Remove duplicates by PromptURL first
    before_url_dedup = len(german_df)
    german_df = german_df.drop_duplicates(subset=["PromptURL"], keep="first")
    after_url_dedup = len(german_df)
    print(f"Rows after PromptURL deduplication: {after_url_dedup} (removed {before_url_dedup - after_url_dedup})")

    # Normalize titles and remove duplicates
    german_df["_title_normalized"] = german_df["Title"].str.lower().str.strip()
    before_title_dedup = len(german_df)
    german_df = german_df.drop_duplicates(subset=["_title_normalized"], keep="first")
    after_title_dedup = len(german_df)
    print(f"Rows after Title deduplication: {after_title_dedup} (removed {before_title_dedup - after_title_dedup})")

    # Remove helper columns
    german_df = german_df.drop(columns=["_source_file", "_title_normalized"])

    # Ensure correct column order
    german_df = german_df[TARGET_COLUMNS]

    # Sort by Category and Title for better organization
    german_df = german_df.sort_values(["Category", "Title"]).reset_index(drop=True)

    # Save result
    german_df.to_csv(output_file, index=False, encoding="utf-8")

    print("-" * 60)
    print("SUMMARY:")
    print(f"  Files processed: {len(csv_files)}")
    print(f"  Rows before filtering: {rows_before_filter}")
    print(f"  Rows after German filter: {rows_after_german_filter}")
    print(f"  Rows after deduplication: {len(german_df)}")
    print(f"  Output file: {output_file}")
    print("-" * 60)

    # Show category distribution
    print("\nCategory distribution:")
    category_counts = german_df["Category"].value_counts()
    for category, count in category_counts.items():
        print(f"  {category}: {count}")


if __name__ == "__main__":
    main()
