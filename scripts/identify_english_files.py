#!/usr/bin/env python3
"""
Identifiziert englische Dateien, die übersetzt werden müssen.
"""
import os
from pathlib import Path

LEGACY_DIR = Path("/home/user/alphamint-prompts/library/de/legacy_translated")

def is_english_content(content: str) -> bool:
    """Prüft, ob der Inhalt hauptsächlich englisch ist."""
    # Entferne YAML Frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    content_lower = content.lower()

    # Englische Indikatoren
    english_words = [
        " the ", " and ", " you ", " are ", " is ", " to ", " for ",
        " with ", " that ", " this ", " your ", " can ", " will ",
        "step", "output", "input", "follow", "create", "analyze",
        "ensure", "provide", "include"
    ]

    # Deutsche Indikatoren
    german_words = [
        " und ", " oder ", " der ", " die ", " das ", " ist ", " sind ",
        " für ", " mit ", " auf ", " bei ", " von ", " zu ", " ein ",
        "Aufgabe", "Rolle", "Ziel", "Ausgabe"
    ]

    english_count = sum(1 for w in english_words if w in content_lower)
    german_count = sum(1 for w in german_words if w in content_lower)

    return english_count > german_count + 2

def main():
    english_files = []
    german_files = []

    for md_file in LEGACY_DIR.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            if is_english_content(content):
                english_files.append(md_file.name)
            else:
                german_files.append(md_file.name)
        except:
            continue

    print(f"Englische Dateien: {len(english_files)}")
    print(f"Deutsche Dateien: {len(german_files)}")

    # Speichere Liste
    with open("/tmp/english_to_translate.txt", "w") as f:
        for name in english_files:
            f.write(name + "\n")

    with open("/tmp/german_already.txt", "w") as f:
        for name in german_files:
            f.write(name + "\n")

    print(f"\nListen gespeichert in /tmp/english_to_translate.txt und /tmp/german_already.txt")

if __name__ == "__main__":
    main()
