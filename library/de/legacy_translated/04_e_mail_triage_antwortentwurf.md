---
title: "E-Mail Triage & Antwortentwurf"
language: "de"
source_path: "04_e_mail_triage_antwortentwurf.md"
category_ai4: "ai4_work"
tags: ["workflow", "automation", "sop", "ops", "legacy", "translated"]
updated: "2025-12-24"
---

# E-Mail Triage & Antwortentwurf

## Wofür ist das?
Sortiert Inbox nach Dringlichkeit und erzeugt Antwortentwürfe mit Tonregeln.

## Inputs (bitte ausfüllen)
- E-Mail Text (oder mehrere)
- Dein Ziel (kurz)
- Ton (neutral/freundlich/direkt)
- Was darf NICHT versendet werden?
- Kontext (Projekt/Stakeholder)

## Prompt (kopieren)

**Rolle:** Executive Assistant für Inbox.

**Aufgabe:**
1) Klassifiziere jede Mail: Dringend/Wichtig/Warten/Delegieren.
2) Gib pro Mail: Zusammenfassung (1 Satz), empfohlene Aktion, Draft-Antwort.
3) Wenn Infos fehlen: stelle 1–2 Rückfragen.

**Regeln:** Keine Zusagen, wenn unklar. Keine sensiblen Daten erfinden.

## Output-Format
- Tabelle (Mail | Klasse | Summary | Aktion | Draft)
- Rückfragen