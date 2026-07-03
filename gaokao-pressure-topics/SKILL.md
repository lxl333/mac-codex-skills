---
name: gaokao-pressure-topics
description: Build Gaokao math pressure-problem topic pages from exam PDFs or images. Use when the user wants Codex to infer the final two problems from each paper section, crop original questions, solve or reconstruct answers, and output a polished MathJax HTML self-study page with hidden answers, red key ideas, yellow decisive steps, and strict visual QA.
---

# Gaokao Pressure Topics

## Purpose

Create a focused "高考压轴题专题" from a complete math exam paper. This skill is for the broader workflow learned from the 2000 Guangdong paper: determine the paper's sections, select the final two problems from each section, preserve original question fidelity with crops, self-solve when no answer key is available, and deliver a student-friendly HTML page.

## Default Contract

- Input can be a PDF, scanned images, or a folder containing papers and optional answer keys.
- If the user says "每个部分的最后两道题", infer sections from the paper, commonly:
  - 选择题: last two multiple-choice problems.
  - 填空题: last two fill-in problems.
  - 解答题: last two worked-response problems.
- If a section count differs, follow the visible paper structure and state the selected problem numbers in the page subtitle or footer.
- Output one HTML file under `output/` with a sibling assets folder for crops.
- Default study mode: show only the original question image first; keep answer, key ideas, explanation, and warning hidden in a closed `<details>` reveal panel.
- Ask the user only when the paper structure or target question set cannot be inferred safely.

## Workflow

1. Inventory files with `rg --files`; identify the target paper and any answer key.
2. Render PDFs to page images before relying on text extraction. Use the visual page as the authority for sections, diagrams, and formulas.
3. Locate section boundaries and choose the final two problems in each section. Record the selected numbers before solving.
4. Crop each selected question from the original page image. A crop must include the problem number, all subquestions, all choices/blanks, and all attached diagrams or tables.
5. If answer keys exist, use them to anchor final answers and reconstruct cleaner explanations. If not, solve independently and label the work as newly整理 or self-solved, not official.
6. Generate a polished HTML page:
   - table of contents,
   - one card per problem,
   - question image first,
   - closed reveal panel immediately after the image,
   - inside reveal: answer, red "题眼 / 关键步骤", worked explanation, common-error reminder.
7. Verify the artifact locally: all images resolve, all reveal panels are closed by default, formulas render through MathJax, and the layout is readable on desktop and mobile widths.

## Solving Rules

- Preserve dense formulas in the question through screenshots; do not trust OCR for the stem when notation is complex.
- For objective and fill-in problems, provide enough reasoning for a student to learn the method, not just the answer.
- For worked-response problems, split by subquestion and keep the official or natural mathematical sequence.
- Use vectors, coordinates, parameters, or standard transformations when they make a pressure problem shorter and less fragile.
- State key substitutions or model switches explicitly, then highlight the decisive step in yellow.
- Do not leave rough ASCII in final explanations when MathJax can express it: write `\(\frac{1}{n}\)`, `\(\sqrt[4]{2}\)`, `\(\sum_{k=1}^n\)`, and similar notation.

## HTML Standard

- Build a study page, not a report or marketing page.
- Use restrained "小蓝本" styling: warm paper background, readable Chinese serif or mixed font, blue/gold accents, red key idea blocks, and yellow highlights only for decisive derivation steps.
- Use relative image paths so the HTML can be moved with its assets folder.
- Include source file names and selected problem numbers in the footer.
- Do not include `open` on `<details>` unless the user explicitly asks for visible answers.

## Crop QA

A crop fails if it has any of these issues:

- missing problem number or left edge,
- clipped right edge,
- missing diagram, table, choices, or subquestions,
- includes unrelated next problem, answer footer, or section heading,
- contains a large blank block that makes the card visually noisy.

After adjusting any crop, re-open it visually and regenerate or refresh the HTML if filenames changed.

## Validation Checklist

- Selected problem numbers match the final two problems in each inferred section.
- Every selected problem appears exactly once in the HTML.
- Every image path resolves locally.
- Reveal panels are closed by default and directly follow the question image.
- Revealed content order is answer, red key idea, worked explanation, warning.
- Answers are mathematically checked, especially when no official answer key was available.
- MathJax renders formulas; no important formula is left as rough plain text.
- The final page has been opened through a local preview or equivalent check.
