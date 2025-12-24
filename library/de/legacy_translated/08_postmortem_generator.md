---
title: "Postmortem Generator"
language: "de"
source_path: "08_postmortem_generator.md"
category_ai4: "ai4_work"
tags: ["workflow", "automation", "sop", "ops", "legacy", "translated"]
updated: "2025-12-24"
---

# Postmortem Generator

## Wofür ist das?
Schreibt Incident-Postmortems ohne Schuldzuweisung.

## Inputs (bitte ausfüllen)
- Incident Timeline
- Impact
- Root Cause (falls bekannt)
- Was lief gut?
- Was fehlte?

## Prompt (kopieren)

**Rolle:** SRE/Operations Facilitator.

**Aufgabe:** Schreibe ein Postmortem.

**Enthalten:**
- Zusammenfassung
- Impact
- Timeline
- Root Cause (Hypothesen markieren)
- Maßnahmen (Prevent/Detect/Respond)
- Lessons Learned

**Regeln:** Blameless, konkret.

## Output-Format
- Postmortem Template ausgefüllt