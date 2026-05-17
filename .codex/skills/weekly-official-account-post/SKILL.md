---
name: weekly-official-account-post
description: Turn a user's Chinese weekly essay draft and workspace photos/screenshots into a real WeChat Official Account-ready Markdown file through a gated multi-step workflow. Use when the user provides a weekly summary title, recurring personal sections, images in the current sandbox, and asks to create or update an actual Markdown file, automatically find and place workspace images, review privacy risks, correct language issues, polish toward a literary essay style, flag immature or improper expression, and require approval before each step advances.
---

# Weekly Official Account Post

## Goal

Create and iteratively update a real `.md` file in the current workspace sandbox for a WeChat Official Account post. The skill instructions must stay ASCII-only to avoid PowerShell mojibake, but the produced article may contain Chinese text from the user.

## Encoding And Console Rules

- Keep this skill file and its metadata ASCII-only.
- Treat user article files as UTF-8.
- When reading or writing article Markdown files that contain Chinese, use explicit UTF-8 handling.
- Do not trust mojibake shown in PowerShell output as proof that a file is corrupted.
- Never copy garbled terminal output back into article Markdown or skill files.

## Gate Phrase

- The user must explicitly say that it is OK to enter the next step before moving forward.
- Treat the Chinese phrase meaning "OK to enter the next step" as the preferred gate phrase.
- Do not write that Chinese gate phrase in this skill file; keep this file ASCII-only.

## File-First Rules

- Always work on an actual Markdown file in the current workspace sandbox, not only in chat.
- In Step 1, create the Markdown file immediately.
- If the user gives an output path, use it.
- If no output path is given, derive a filename from the weekly title and place it in the current workspace or the most relevant dated subfolder.
- In Steps 2-4, apply approved changes directly to that same Markdown file, then report the updated file path and a brief change summary.
- Do not replace the file wholesale after Step 1 unless necessary. Preserve the current file and make scoped edits that match the user's approvals.
- If the working Markdown file is unclear, ask which `.md` file to continue editing before making changes.

## Workspace Image Discovery

- In Step 1, automatically search the current workspace sandbox for image files before creating the first Markdown draft.
- Include common image extensions: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.heic`, `.bmp`, `.tif`, `.tiff`, `.avif`.
- Ignore obvious dependency, cache, hidden, or generated directories such as `.git`, `.codex`, `node_modules`, `dist`, `build`, `.next`, `.cache`, and similar folders unless the user explicitly points to images there.
- Use file paths, filenames, modification times, embedded timestamps in filenames, folder names, and visual content when available to infer where images belong.
- Insert discovered images into the Markdown in Step 1. Do not wait for a later step to add obvious images.
- If many images are found, group them by likely section or chronology and insert them where confidence is reasonable.
- For uncertain images, place them in a final "Images to confirm" section or ask a targeted question if placement would materially affect the article.
- Use Markdown image syntax with workspace-relative paths when practical, for example `![short factual alt text](relative/path/image.jpg)`.
- Add short, factual alt text. Do not invent details not visible or implied.
- Do not omit images unless they are duplicates, unusable, or clearly unrelated. Report omitted images and reasons outside the post.

## Food Image Captions

- For images placed in the FOOD section, use a caption format that includes:
  1. the Chinese weekday,
  2. the Chinese meal label for breakfast, lunch, dinner, or late-night snack,
  3. a Chinese-style colon,
  4. the dish, place, or concise food description.
- The intended shape is `weekday + meal + colon + dish name`, matching the existing FOOD captions in the 2026-05-10 weekly article.
- Infer the weekday and meal from embedded timestamps, filenames, folder dates, image chronology, article chronology, and visible food context.
- If the dish name is unclear, use the known place or a factual visible description after the colon. If both the meal and dish are uncertain, still include the best inferred weekday and meal, then mention the uncertainty outside the post.
- Do not use bare captions such as only a date, only a food name, or only "lunch" / "dinner" for FOOD images when enough context exists to follow this pattern.

## Core Formatting

- Keep the user's weekly title as the H1.
- Preserve the original section order.
- Convert every original section heading into an H2 in the form `## PART x Original Heading`, where `x` starts at 1.
- Recognize the user's recurring section headings by exact text or meaning, including personal notes, technical learning, thoughts, workout, food, music, and Duolingo sections.
- Reorder paragraphs only within the same section by inferred chronology: dates, weekdays, relative time words, event sequence, image timestamps, and filenames.
- If chronology is ambiguous, keep the original relative order and mention the uncertainty outside the post.
- For the four sections meaning "big events", "small events", "technical learning", and "thoughts", add a standalone bold number line before every body paragraph. Restart numbering from 1 in each of these sections:

```markdown
**1**

Paragraph text.
```

- Automatically fix punctuation usage while generating and updating Markdown, including missing sentence-final punctuation, obvious Chinese/English punctuation mismatches, duplicate punctuation, and spacing around punctuation.
- Treat punctuation fixes as formatting, not as language rewrites requiring approval.

## Four-Step Workflow

### Step 1: Create The First Markdown File

1. Gather the original essay text, desired output path if provided, and any user-provided image notes.
2. Search the current workspace sandbox for image files using the Workspace Image Discovery rules.
3. Build the first Markdown draft using the core formatting, paragraph chronology, automatic punctuation fixes, and discovered image placement.
4. Write the draft to a real `.md` file in the sandbox.
5. Report the file path, the number of images inserted, any images placed with uncertainty, and any images omitted.
6. Stop and ask the user to review the file. Do not start privacy review until the user explicitly allows moving to the next step.

### Step 2: Privacy Review

After the user allows Step 2:

1. Read the current Markdown file from disk with UTF-8 handling.
2. Review the file content and inserted image references for content that may leak privacy if published on a public WeChat Official Account.
3. List possible privacy risks with numeric labels. Include only items with a plausible public-exposure concern, such as:
   - Real names, identifying nicknames, phone numbers, IDs, addresses, workplace or school details, exact routes, or schedules.
   - Screenshots containing usernames, account IDs, order numbers, email addresses, location data, QR codes, payment details, health or fitness data, or personal messages.
   - Photos revealing home, workplace, residential surroundings, documents, screens, license plates, faces of private people, or location clues.
   - Highly specific timing or habits that could enable tracking.
4. Ask which numbered items the user wants to delete or mask.
5. When the user gives numbers or instructions, apply only those privacy edits directly to the Markdown file on disk.
6. Report the updated file path and a concise summary of edits.
7. Repeat this step for additional user edits as needed.
8. Do not proceed to language correction until the user explicitly allows moving to the next step.

### Step 3: Language Correction

After the user allows Step 3:

1. Read the current Markdown file from disk with UTF-8 handling.
2. Identify all obvious language expression errors, typos, grammar issues, awkward phrasing, unclear transitions, or sentences that are clearly not smooth.
3. List each proposed correction with a numeric label, showing the original sentence and the corrected sentence.
4. Keep corrections conservative. Do not change meaning, tone, or style beyond making the sentence correct and smooth.
5. Ask whether the user wants to apply specific numbered corrections or provide alternative edits.
6. Apply only the corrections or custom edits the user approves directly to the Markdown file on disk.
7. Report the updated file path and a concise summary of edits.
8. Repeat this step for additional user edits as needed.
9. Do not proceed to literary polishing until the user explicitly allows moving to the next step.

### Step 4: Literary Polish

After the user allows Step 4:

1. Read the current Markdown file from disk with UTF-8 handling.
2. Propose style edits that make the article more literary, reflective, and essay-like, with a gentle prose atmosphere.
3. Also flag any expression that may seem immature, improper, insensitive, unfair, overconfident, emotionally excessive, socially risky, or unsuitable for a public WeChat Official Account post.
4. For each flagged maturity or propriety concern, explain the risk briefly and propose a more measured alternative.
5. Preserve the user's facts, chronology, section structure, and personal voice.
6. Avoid over-writing, melodrama, ornate cliches, or making casual notes sound artificially grand.
7. List every proposed polish or maturity/propriety edit with a numeric label, showing the original text and the suggested version.
8. Clearly mark whether each item is a style polish, a maturity/propriety concern, or both.
9. Ask whether the user wants to apply specific numbered edits or provide alternative wording.
10. Apply only approved edits directly to the Markdown file on disk.
11. Report the updated file path and a concise summary of edits.
12. Repeat this step for additional user edits as needed.

## Gatekeeping Rules

- Never move from one step to the next based on implied approval.
- Each step may involve multiple rounds of edits. Stay in the current step until the user approves moving on.
- Keep all review lists numbered so the user can approve or reject by number.
- Keep approval questions concise and action-oriented.
- Do not silently apply privacy deletions, language corrections, or literary polish.
- Punctuation fixes and Markdown/image formatting are the only text-level changes that may be applied automatically in Step 1.
- Every approved change in Steps 2-4 must update the real Markdown file in the sandbox.

## Final Response

When the workflow is complete, give a brief status with:

- The final Markdown file path.
- Any images omitted or placed with uncertainty.
- Any unresolved privacy, correction, polish, or maturity/propriety decisions.
