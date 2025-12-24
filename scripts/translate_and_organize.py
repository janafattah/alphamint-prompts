#!/usr/bin/env python3
"""
Skript zur Übersetzung und Organisation von Markdown-Prompts
in die AI4 Kategorien-Struktur.
"""

import os
import re
import shutil
import csv
from datetime import date
from pathlib import Path

# Konfiguration
ROOT_DIR = Path("/home/user/alphamint-prompts")
LIBRARY_DE = ROOT_DIR / "library" / "de"
LEGACY_DIR = LIBRARY_DE / "legacy_translated"
TODAY = date.today().strftime("%Y-%m-%d")

# Ausgeschlossene Ordner
EXCLUDED_DIRS = {".git", "node_modules", "dist", "build", "library", "scripts"}

# AI4 Kategorie-Mapping (Keywords -> Kategorie)
CATEGORY_MAPPING = {
    "ai4_enablement": [
        "enablement", "adoption", "change", "training", "copilot", "usage gap",
        "champion", "rollout", "onboarding", "policy", "kpi", "dashboard"
    ],
    "ai4_work": [
        "workflow", "automation", "sop", "process", "reporting", "jira",
        "meeting", "email", "ticket", "postmortem", "qa", "backlog",
        "project", "task", "productivity", "office", "work"
    ],
    "ai4_wealth": [
        "finance", "wealth", "investing", "etf", "portfolio", "stock",
        "trading", "investment", "vermögen", "aktien", "fonds", "dividende",
        "real estate", "immobilie"
    ],
    "ai4_financial_wellbeing": [
        "money mindset", "budget", "stress", "habits", "cashflow",
        "schulden", "debt", "savings", "sparen", "notgroschen",
        "financial wellness", "finanz"
    ],
    "ai4_retail": [
        "fashion", "style", "fit", "retail", "returns", "shopping",
        "ecommerce", "store", "product", "closella", "kleidung"
    ],
    "ai4_kids": [
        "kids", "school", "learning", "parents", "children", "education",
        "teaching", "kinder", "schule", "lernen", "homeschool"
    ],
    "ai4_thought_leadership": [
        "linkedin", "speaking", "story", "personal brand", "content",
        "newsletter", "podcast", "youtube", "social media", "influencer",
        "thought leader", "keynote"
    ],
    "ai4_literacy": [
        "literacy", "basics", "myths", "fact check", "safety", "ethics",
        "fundamentals", "introduction", "beginner", "grundlagen"
    ],
    "ai4_free_education": [
        "free", "freebie", "challenge", "template", "resource hub",
        "mini course", "guide", "tutorial", "how to", "kostenlos"
    ]
}


def detect_language(content: str) -> str:
    """Erkennt die Sprache basierend auf YAML-Frontmatter oder Inhaltsanalyse."""
    # Prüfe YAML Frontmatter
    if 'language: "de"' in content or "language: 'de'" in content:
        return "de"
    if 'language: "en"' in content or "language: 'en'" in content:
        return "en"

    # Heuristische Spracherkennung basierend auf deutschen Wörtern
    german_indicators = [
        " und ", " oder ", " der ", " die ", " das ", " ist ", " sind ",
        " für ", " mit ", " auf ", " bei ", " von ", " zu ", " ein ", " eine ",
        "Aufgabe", "Rolle", "Ziel", "Ausgabe", "Beispiel", "Hinweis"
    ]
    content_lower = content.lower()
    german_count = sum(1 for word in german_indicators if word.lower() in content_lower)

    return "de" if german_count >= 3 else "en"


def extract_title(content: str, filename: str) -> str:
    """Extrahiert den Titel aus der Datei oder generiert ihn aus dem Dateinamen."""
    # Suche in YAML Frontmatter
    match = re.search(r'^title:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Suche nach erster H1-Überschrift
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Generiere aus Dateiname
    name = filename.replace(".md", "").replace("_", " ").replace("-", " ")
    return name.title()


def determine_category(content: str, filename: str) -> str:
    """Bestimmt die AI4-Kategorie basierend auf Inhalt und Dateiname."""
    # Prüfe existierende Kategorie im Frontmatter
    match = re.search(r'category_ai4:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
    if match:
        cat = match.group(1).strip().lower()
        for key in CATEGORY_MAPPING.keys():
            if key.replace("ai4_", "") in cat.replace(" ", "_").lower():
                return key

    # Analysiere Inhalt und Dateiname
    search_text = (content + " " + filename).lower()

    scores = {}
    for category, keywords in CATEGORY_MAPPING.items():
        score = sum(1 for kw in keywords if kw in search_text)
        if score > 0:
            scores[category] = score

    if scores:
        return max(scores, key=scores.get)

    return "ai4_other"


def extract_existing_frontmatter(content: str) -> tuple:
    """Extrahiert existierendes Frontmatter und den restlichen Inhalt."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[1].strip(), parts[2].strip()
    return None, content


def create_frontmatter(title: str, source_path: str, category: str,
                       existing_tags: list = None) -> str:
    """Erstellt YAML Frontmatter für die übersetzte Datei."""
    tags = existing_tags or []
    if "legacy" not in tags:
        tags.append("legacy")
    if "translated" not in tags:
        tags.append("translated")

    tags_str = '["' + '", "'.join(tags) + '"]'

    return f'''---
title: "{title}"
language: "de"
source_path: "{source_path}"
category_ai4: "{category}"
tags: {tags_str}
updated: "{TODAY}"
---'''


def process_file(source_path: Path) -> dict:
    """Verarbeitet eine einzelne Markdown-Datei."""
    try:
        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Fehler beim Lesen von {source_path}: {e}")
        return None

    # Relativer Pfad vom Root
    rel_path = source_path.relative_to(ROOT_DIR)

    # Extrahiere Informationen
    language = detect_language(content)
    title = extract_title(content, source_path.name)
    category = determine_category(content, source_path.name)

    # Extrahiere existierendes Frontmatter
    existing_fm, body = extract_existing_frontmatter(content)

    # Extrahiere existierende Tags
    existing_tags = []
    if existing_fm:
        tag_match = re.search(r'tags:\s*\[([^\]]*)\]', existing_fm)
        if tag_match:
            existing_tags = [t.strip().strip('"\'') for t in tag_match.group(1).split(",")]

    return {
        "source_path": str(rel_path),
        "filename": source_path.name,
        "title": title,
        "language": language,
        "category": category,
        "body": body,
        "existing_tags": existing_tags,
        "original_content": content
    }


def get_all_markdown_files() -> list:
    """Findet alle zu verarbeitenden Markdown-Dateien."""
    files = []

    for item in ROOT_DIR.rglob("*.md"):
        # Prüfe Ausschlüsse
        parts = item.relative_to(ROOT_DIR).parts
        if any(exc in parts for exc in EXCLUDED_DIRS):
            continue

        # Überspringe alphamint_core_prompt_library_de
        if "alphamint_core_prompt_library_de" in str(item):
            continue

        files.append(item)

    return files


def write_legacy_file(file_info: dict, translated_body: str = None) -> Path:
    """Schreibt die Datei in den legacy_translated Ordner."""
    source_path = file_info["source_path"]

    # Ziel-Pfad in legacy_translated
    target_path = LEGACY_DIR / source_path
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Erstelle neues Frontmatter
    frontmatter = create_frontmatter(
        file_info["title"],
        file_info["source_path"],
        file_info["category"],
        file_info["existing_tags"]
    )

    # Verwende übersetzten Body oder Original
    body = translated_body if translated_body else file_info["body"]

    # Schreibe Datei
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + "\n\n" + body)

    return target_path


def copy_to_ai4_folder(legacy_path: Path, category: str) -> Path:
    """Kopiert die Datei in den entsprechenden AI4-Ordner."""
    ai4_dir = LIBRARY_DE / category
    ai4_dir.mkdir(parents=True, exist_ok=True)

    target_path = ai4_dir / legacy_path.name

    # Bei Namenskollision: Suffix hinzufügen
    counter = 1
    while target_path.exists():
        stem = legacy_path.stem
        target_path = ai4_dir / f"{stem}_{counter}.md"
        counter += 1

    shutil.copy2(legacy_path, target_path)
    return target_path


def generate_category_readme(category: str, files: list) -> None:
    """Erstellt README.md für eine Kategorie."""
    readme_path = LIBRARY_DE / category / "README.md"

    # Kategorie-Beschreibungen
    descriptions = {
        "ai4_enablement": "Prompts für AI-Einführung, Training und Change Management in Organisationen.",
        "ai4_work": "Prompts für Workflow-Automatisierung, Produktivität und operative Prozesse.",
        "ai4_wealth": "Prompts für Investitionen, Vermögensaufbau und Finanzplanung.",
        "ai4_financial_wellbeing": "Prompts für finanzielle Gesundheit, Budgetierung und Money Mindset.",
        "ai4_retail": "Prompts für Retail, Fashion und E-Commerce.",
        "ai4_kids": "Prompts für Bildung, Lernen und Eltern-Kind-Themen.",
        "ai4_thought_leadership": "Prompts für Personal Branding, Content Creation und Social Media.",
        "ai4_literacy": "Prompts für AI-Grundlagen, Sicherheit und Ethik.",
        "ai4_free_education": "Kostenlose Ressourcen, Templates und Mini-Kurse.",
        "ai4_other": "Weitere Prompts, die keiner spezifischen Kategorie zugeordnet sind."
    }

    desc = descriptions.get(category, "Sammlung von Prompts in dieser Kategorie.")

    content = f"""# {category.replace("_", " ").title()}

{desc}

## Enthaltene Prompts

| Titel | Datei |
|-------|-------|
"""

    for file_info in sorted(files, key=lambda x: x.get("title", "")):
        title = file_info.get("title", "Unbenannt")
        filename = file_info.get("filename", "")
        content += f"| {title} | {filename} |\n"

    content += f"\n---\n*Letzte Aktualisierung: {TODAY}*\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_notion_csv(all_files: list) -> Path:
    """Erstellt die Notion-Import CSV."""
    csv_path = LIBRARY_DE / "notion_index_de.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Category", "Tags", "Path", "SourcePath", "Updated", "RawURL"])

        for file_info in all_files:
            if file_info.get("legacy_path"):
                rel_path = Path(file_info["legacy_path"]).relative_to(ROOT_DIR)
                raw_url = f"https://raw.githubusercontent.com/janafattah/prompts/main/{rel_path}"

                tags = ", ".join(file_info.get("existing_tags", []))

                writer.writerow([
                    file_info.get("title", ""),
                    file_info.get("category", ""),
                    tags,
                    str(rel_path),
                    file_info.get("source_path", ""),
                    TODAY,
                    raw_url
                ])

    return csv_path


def main():
    """Hauptfunktion für die Verarbeitung."""
    print("=" * 60)
    print("Starte Verarbeitung der Markdown-Dateien...")
    print("=" * 60)

    # Finde alle Dateien
    files = get_all_markdown_files()
    print(f"\nGefundene Dateien: {len(files)}")

    # Verarbeite jede Datei
    processed = []
    category_files = {}

    for i, source_path in enumerate(files):
        if (i + 1) % 100 == 0:
            print(f"Verarbeite Datei {i + 1}/{len(files)}...")

        file_info = process_file(source_path)
        if not file_info:
            continue

        # Schreibe in legacy_translated
        legacy_path = write_legacy_file(file_info)
        file_info["legacy_path"] = legacy_path

        # Kopiere in AI4-Ordner
        ai4_path = copy_to_ai4_folder(legacy_path, file_info["category"])
        file_info["ai4_path"] = ai4_path

        processed.append(file_info)

        # Gruppiere nach Kategorie
        cat = file_info["category"]
        if cat not in category_files:
            category_files[cat] = []
        category_files[cat].append(file_info)

    # Generiere READMEs
    print("\nErstelle READMEs...")
    for category, files_list in category_files.items():
        generate_category_readme(category, files_list)

    # Generiere CSV
    print("Erstelle Notion CSV...")
    csv_path = generate_notion_csv(processed)

    # Statistik
    print("\n" + "=" * 60)
    print("ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"Verarbeitete Dateien: {len(processed)}")
    print(f"\nDateien pro Kategorie:")
    for cat in sorted(category_files.keys()):
        print(f"  {cat}: {len(category_files[cat])}")
    print(f"\nNotion CSV: {csv_path}")
    print("=" * 60)

    return processed, category_files


if __name__ == "__main__":
    main()
