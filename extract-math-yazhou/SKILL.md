---
name: extract-math-yazhou
description: Extract high-school math challenge problems from exam papers and answer PDFs or images, especially Chinese Gaokao-style final questions. Use when the user gives exam papers and answer keys and wants the pressure questions extracted into a polished "小蓝本"-style HTML study page with clean crops, answers shown immediately or hidden behind a reveal button for self-study, MathJax/MathType-style formulas, original answer diagrams preserved, red key ideas, yellow highlighted derivation steps, student-friendly explanations, and strict crop-quality checks.
---

# Extract Math Yazhou

## Workflow

1. Inventory the workspace with `rg --files` and identify question papers, answer keys, and file formats.
2. For PDFs, render pages to PNG before relying on text extraction. Use text extraction only when the PDF has a real text layer.
3. Locate requested problem numbers visually or by text. For scanned papers, crop the problem regions and answer regions from page images.
   - **Hard requirement:** every crop must be visually verified against the rendered full page before delivery. A crop that is even slightly incomplete or includes unrelated material must be treated as failed work, regenerated, and rechecked.
4. Preserve mathematical fidelity for question stems: embed clean cropped screenshots for formulas, diagrams, tables, and long stems instead of relying on OCR.
5. Do not show objective-question answer-key screenshots by default. Replace them with a clear answer, student-friendly explanation, key idea, and mistake warning.
6. For long-answer questions, prefer beautifully typeset text explanations over raw answer screenshots when the solution can be reconstructed reliably. Use MathJax/LaTeX for all formulas so the result looks like MathType. Keep screenshots only as a fallback for unreadable formulas or exact diagrams.
7. If the official answer includes diagrams, coordinate-system figures, tables, or other visual aids, crop and include them near the matching solution step.
8. Add a concise "题眼 / 关键步骤" section for every problem. Make the key ideas red in the HTML, and keep them actionable rather than decorative.
9. Generate a polished HTML study page with a table of contents and one card per problem. The order inside each card must be: question image, answer strip, highlighted key ideas, worked explanation, common-error reminder. If the user asks to try problems first or not see explanations immediately, wrap everything after the question image in a reveal panel/button.
10. Verify that every requested problem number is present, every image path resolves, and the final page is readable on desktop and mobile widths.

## Default Task Contract

- If the user provides a paper and answer key without extra instructions, extract the pressure questions `7, 8, 11, 14, 18, 19`.
- If the user provides different question numbers, use those instead and keep the same study-page standard.
- Output a single local HTML file under `output/`, with all supporting crops in an adjacent assets folder.
- Treat the page as a student learning artifact, not just an answer dump: it should help the student see the answer, the method, the turning point, and the common trap at a glance.
- If the user asks for delayed answers, self-testing, or "点一下才出现", make answer, analysis, key ideas, and warnings hidden by default behind a clear reveal button.
- Prefer making the artifact directly. Ask questions only when the files or target question numbers are genuinely ambiguous.

## Extraction Guidance

- Default pressure-test problem set for Gaokao-style papers: `7, 8, 11, 14, 18, 19`, unless the user gives a different list.
- If the answer key only gives final answers for objective questions, derive short key ideas from the problem statement and final answer; label them as learning整理 or learning hints rather than official full solutions.
- For long solution problems, reconstruct a clean step-by-step explanation when possible: split by subquestion, state the model or method first, then show the calculation. Keep notation and sequence close to the official answer.
- Use stable output names: place final HTML in `output/` and image assets in a sibling `*_assets/` folder.
- Avoid lossy OCR when formulas are dense. A clean screenshot plus a human-written key-step summary is usually more reliable.

## Explanation Rules

- Put the answer immediately after the question image. In delayed-answer mode, put the reveal button immediately after the question image; inside the revealed area, keep the answer first.
- Use red only for "题眼 / 关键步骤" summary cards.
- Use yellow text for decisive steps inside the worked explanation, such as a model switch, an equivalent transformation, a monotonicity conclusion, a final range, or the key summation identity.
- Render all mathematical expressions in answers, explanations, warnings, and key ideas with MathJax/LaTeX when practical.
- Do not leave rough ASCII such as `3/7`, `C(9,4)`, `X~B(3,1/3)`, `e^(a-4)`, or `f(n+1)/f(n)` in the final HTML when it should be mathematical notation.
- For objective questions, include enough process for a student to learn the method, but do not invent a long official solution if the answer key only provides a final answer.
- For long-answer questions, follow the official answer's sequence and notation as closely as possible while making the typography clearer.

## HTML Requirements

- Build the study page, not a marketing page.
- Use a "小蓝本"-style learning layout: question first, answer immediately after the question, then red key idea, then worked explanation, then common-error reminder.
- In delayed-answer mode, use one obvious control per card, such as `<details class="reveal"><summary>我不会了，展开答案与解析</summary>...</details>`. The default state must be closed; the revealed content order remains answer, red key idea, worked explanation, common-error reminder.
- Use clear section hierarchy, readable Chinese serif or mixed Chinese fonts, warm paper-like background, restrained blue/gold accents, and enough spacing for focused study.
- Mark key steps in red using CSS, for example `.key span { color: #d91f26; font-weight: 800; }`.
- Render formulas with MathJax or an equivalent MathType-like system. Do not leave answer or explanation formulas as rough ASCII when they can be expressed in LaTeX.
- Highlight decisive derivation steps inside explanations with yellow text, while keeping the separate "题眼" area red.
- Keep screenshots full-width inside each card with borders and rounded corners.
- Include source file names in the footer when available.

## Crop Quality Rules

- Inspect every generated question crop visually before final delivery. This is mandatory, not optional.
- A valid crop must include the problem number, complete stem, all subquestions, all choices/blanks, and all diagrams or tables belonging to the problem.
- A valid crop must not include unrelated previous or next questions, section headings, answer-card footers, page numbers, or clipped right-edge text.
- Remove large blank areas below the problem, especially under long-answer question stems, but prefer a little clean white margin over a tight crop that risks cutting formulas or punctuation.
- If a crop has missing top text, clipped right-side text, leftover page footer, unrelated next-section title, or a large blank block below the stem, it fails quality review.
- If a crop is adjusted, regenerate the HTML and re-check the affected image.
- Do not deliver the HTML until every crop passes visual inspection. If even one crop fails, update the crop coordinates or extraction method and rerun the artifact generation.

## Validation Checklist

- Requested question numbers are all included.
- Each card follows this order: question image, answer, red key-step section, worked explanation, warning.
- For delayed-answer mode, each card follows this visible order: question image, reveal button; after opening, answer, red key-step section, worked explanation, warning. Verify all reveal panels are closed by default.
- Objective questions do not display answer-key screenshots unless explicitly requested.
- Long answers are typeset clearly or, when screenshots are necessary, not clipped.
- Formulas in answers render through MathJax/MathType-like notation.
- Explanation formulas also render through MathJax/MathType-like notation.
- Yellow highlights appear on the decisive steps inside explanations.
- Official answer diagrams or tables are included when present.
- Image links are relative to the HTML and open locally.
- Crops have passed visual inspection for completeness and neat boundaries; record or report this validation before final delivery.
- The page remains usable at narrow screen widths.
