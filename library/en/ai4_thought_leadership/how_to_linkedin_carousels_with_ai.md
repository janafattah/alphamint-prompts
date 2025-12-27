# How to (finally) create LinkedIn carousels with AI
**Category:** AI 4 Thought Leadership
**Language:** EN
**Use case:** Turn any YouTube video into a high-retention LinkedIn carousel using Gemini + Gamma.

## 🎯 What this prompt is for

This playbook shows you how to:
- pick an actionable YouTube video
- extract the "meat" with Gemini
- turn it into a 10-slide LinkedIn carousel
- design it in Gamma and export as a 4:5 PDF

Result: you can turn almost any solid video into a LinkedIn carousel in **under 5 minutes**.
No templates, no Canva, no design skills.

---

## 🧩 Step 1 – Pick your source video

1. Go to **YouTube**.
2. Find an **actionable** video (teaches a framework, process, or clear lesson).
3. Copy the **URL**.

A good carousel is an *opinionated statement*:
it teaches, challenges, or reframes something – not just „info dump".

---

## 🧠 Step 2 – Extract the key information with Gemini

Open **Gemini** (use the Thinking model) and paste this prompt:

```text
Act like an expert Content Strategist and Senior Editor for a leading digital publication. Your goal is to repurpose video content into high-value written pieces that drive engagement.

Please analyze the following YouTube video: [YOUTUBE LINK].

Part 1: The Extraction
First, provide a comprehensive breakdown of the video content. Do not just summarize; extract the "meat" of the content using the following structure:
- Core Thesis: What is the single most important argument or lesson in one sentence?
- Key Data/Facts: List specific numbers, case studies, or hard facts mentioned.
- Golden Quotes: Extract 3–5 verbatim quotes that are punchy or profound.
- The Framework: If the speaker uses a specific step-by-step process or mental model, outline it clearly.

Part 2: The Angles
Based only on the extraction above, pitch 5 narrow, specific article angles.
Constraint: Avoid generic titles like "Summary of [Video Name]."
Requirement: Each angle must take a specific slice of the content and expand on it.
Format: Provide a catchy headline plus a one-sentence premise for each angle.

Example of a "Narrow Angle"
Bad: How to do Sales.
Good: The "3-Call Close" Technique: Why Most Salespeople Fail in the Follow-up.
```

Gemini will return:

* one detailed extraction
* 5 narrow angles you can use as potential carousels.

Pick **one** angle you want to turn into a carousel
(in the original example: "The Thesis Stack").

---

## 🧱 Step 3 – Turn the angle into a 10-slide carousel outline

Follow up in Gemini with:

```text
You are a specialized Ghostwriter for Thought Leaders on LinkedIn. Your task is to turn a specific angle into a high-retention, 10-slide carousel outline.

The Input Angle: [WHAT YOU CHOSE ON THE PREVIOUS PROMPT]

You must strictly focus on this angle, as closely as possible.

The Source Material: The YouTube video I shared.

Your Formatting Rules:

No Fluff: Every slide must provide a specific insight, a lightbulb moment, or a counter-intuitive fact.

The Slide Breakdown:
Slide 1: The Hook. A polarizing or curiosity-gap headline that stops the scroll.
Slide 2: The Stakes. Why does this matter right now? What is the cost of inaction?
Slide 3: The Insight. The core thesis or the Golden Quote from the video.
Slides 4–8: The Value Meat. Break down the framework or facts into one aha moment per slide. Use specific data or steps from the video.
Slide 9: The Summary. A TL;DR checklist for readers to save or screenshot.
Slide 10: The CTA. A low-friction question to spark comments (e.g., Which of these 3 steps is your biggest bottleneck?).

Structure each slide as:
[Slide #] [Slide headline]
[Text Content]

You will write 10 slides, made for a LinkedIn carousel.
```

Output = a clean 10-slide outline that's ready to design.

---

## 🎨 Step 4 – Design in Gamma.app

1. Go to **[https://gamma.app](https://gamma.app)**
2. Click **"Create with AI"**
3. Choose **"Studio mode (beta)"**
4. Settings:

   * Type: **Social**
   * Cards: **10 cards**
   * Mode: **Studio BETA**
   * Size: **Portrait / 1080 × 1350 (4:5)**
5. Paste Gemini's 10-slide outline into the main prompt box.
6. Text setting: **"Just vibes"** (short, punchy copy per slide).
7. Select:

   * Theme: your LinkedIn visual style
   * AI images: **Nano Banana Pro** or similar model

Click **Generate** → review slides → tweak if needed → export as **PDF**.

This PDF is your LinkedIn carousel.

---

## 🧾 What is a LinkedIn carousel? (quick reference)

* A **PDF document** uploaded as a LinkedIn post
* Format: **1080 × 1350 px (4:5)**
* Typically **6–14 slides**
* One of the highest engagement formats (saves, shares, dwell time)

---

## ⚙️ Ultra-short workflow recap

1. Pick YouTube video → copy URL
2. Gemini Extraction prompt → get "meat" + 5 angles
3. Gemini Ghostwriter prompt → get 10-slide outline
4. Paste into Gamma Studio (Social, Portrait, Just vibes)
5. Export PDF → upload as LinkedIn carousel

From raw video → finished carousel in under 5 minutes.
No templates. No Canva. No design degree.
