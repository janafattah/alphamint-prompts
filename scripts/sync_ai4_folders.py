#!/usr/bin/env python3
"""
Synchronisiert die übersetzten Dateien aus legacy_translated in die AI4-Ordner.
Regeneriert READMEs und CSV.
"""
import os
import re
import csv
import shutil
from pathlib import Path
from datetime import date

ROOT_DIR = Path("/home/user/alphamint-prompts")
LIBRARY_DE = ROOT_DIR / "library" / "de"
LEGACY_DIR = LIBRARY_DE / "legacy_translated"
TODAY = date.today().strftime("%Y-%m-%d")

AI4_FOLDERS = [
    "ai4_enablement", "ai4_work", "ai4_wealth", "ai4_financial_wellbeing",
    "ai4_retail", "ai4_kids", "ai4_thought_leadership", "ai4_literacy",
    "ai4_free_education", "ai4_other"
]

def extract_category(content: str) -> str:
    """Extrahiert die AI4-Kategorie aus dem YAML Frontmatter."""
    match = re.search(r'category_ai4:\s*["\']?([^"\'\n]+)["\']?', content)
    if match:
        cat = match.group(1).strip().lower().replace(" ", "_")
        for folder in AI4_FOLDERS:
            if folder in cat or cat in folder:
                return folder
    return "ai4_other"

def extract_title(content: str, filename: str) -> str:
    """Extrahiert den Titel."""
    match = re.search(r'^title:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return filename.replace(".md", "").replace("_", " ").title()

def sync_to_ai4():
    """Kopiert alle Dateien aus legacy_translated in die AI4-Ordner."""
    # Leere AI4-Ordner (außer README.md)
    for folder in AI4_FOLDERS:
        folder_path = LIBRARY_DE / folder
        folder_path.mkdir(exist_ok=True)
        for f in folder_path.glob("*.md"):
            if f.name != "README.md":
                f.unlink()

    # Kopiere Dateien
    category_files = {f: [] for f in AI4_FOLDERS}

    for md_file in LEGACY_DIR.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            category = extract_category(content)
            title = extract_title(content, md_file.name)

            # Kopiere in AI4-Ordner
            target = LIBRARY_DE / category / md_file.name
            counter = 1
            while target.exists():
                target = LIBRARY_DE / category / f"{md_file.stem}_{counter}.md"
                counter += 1

            shutil.copy2(md_file, target)
            category_files[category].append({"title": title, "filename": md_file.name, "path": str(target)})
        except Exception as e:
            print(f"Fehler bei {md_file}: {e}")

    return category_files

def generate_readmes(category_files: dict):
    """Generiert README.md für jede Kategorie."""
    descriptions = {
        "ai4_enablement": "Prompts für AI-Einführung, Training und Change Management.",
        "ai4_work": "Prompts für Workflow-Automatisierung und Produktivität.",
        "ai4_wealth": "Prompts für Investitionen und Vermögensaufbau.",
        "ai4_financial_wellbeing": "Prompts für finanzielle Gesundheit und Budgetierung.",
        "ai4_retail": "Prompts für Retail, Fashion und E-Commerce.",
        "ai4_kids": "Prompts für Bildung und Kinder-Themen.",
        "ai4_thought_leadership": "Prompts für Personal Branding und Content Creation.",
        "ai4_literacy": "Prompts für AI-Grundlagen und Sicherheit.",
        "ai4_free_education": "Kostenlose Ressourcen und Templates.",
        "ai4_other": "Weitere Prompts."
    }

    for category, files in category_files.items():
        readme_path = LIBRARY_DE / category / "README.md"
        desc = descriptions.get(category, "Sammlung von Prompts.")

        content = f"""# {category.replace("_", " ").title()}

{desc}

## Enthaltene Prompts ({len(files)})

| Titel | Datei |
|-------|-------|
"""
        for f in sorted(files, key=lambda x: x["title"]):
            content += f"| {f['title']} | {f['filename']} |\n"

        content += f"\n---\n*Aktualisiert: {TODAY}*\n"

        with open(readme_path, "w", encoding="utf-8") as out:
            out.write(content)

def generate_csv(category_files: dict) -> Path:
    """Generiert die Notion CSV."""
    csv_path = LIBRARY_DE / "notion_index_de.csv"

    all_files = []
    for category, files in category_files.items():
        for f in files:
            rel_path = Path(f["path"]).relative_to(ROOT_DIR)
            all_files.append({
                "title": f["title"],
                "category": category,
                "path": str(rel_path),
                "raw_url": f"https://raw.githubusercontent.com/janafattah/prompts/main/{rel_path}"
            })

    with open(csv_path, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(["Title", "Category", "Tags", "Path", "SourcePath", "Updated", "RawURL"])

        for f in sorted(all_files, key=lambda x: x["title"]):
            writer.writerow([
                f["title"],
                f["category"],
                "legacy, translated",
                f["path"],
                "",
                TODAY,
                f["raw_url"]
            ])

    return csv_path

def main():
    print("Synchronisiere AI4-Ordner...")
    category_files = sync_to_ai4()

    print("Generiere READMEs...")
    generate_readmes(category_files)

    print("Generiere CSV...")
    csv_path = generate_csv(category_files)

    print("\n" + "="*50)
    print("ZUSAMMENFASSUNG")
    print("="*50)
    total = sum(len(files) for files in category_files.values())
    print(f"Gesamt: {total} Dateien")
    for cat in sorted(category_files.keys()):
        print(f"  {cat}: {len(category_files[cat])}")
    print(f"\nCSV: {csv_path}")

if __name__ == "__main__":
    main()
