---
name: math-error-book
description: Build reusable high-school math error books from scanned wrong-problem notebooks, exam PDFs, answer keys, or cropped problem images. Use when Codex needs to organize student math mistakes into a structured question bank, classify by高中数学模块/知识点/错因, generate a low-pressure multi-page web study book, create module-specific printable PDFs for专项练习, or update an existing error book with new problems.
---

# Math Error Book

## Workflow

1. Inventory all inputs with `rg --files` or `find`: scanned notebook pages, exam papers, answer keys, existing crops, and prior output folders.
2. Convert PDFs to page images before relying on text extraction. Preserve formula-heavy stems as clean screenshots rather than lossy OCR.
3. Split every page into one problem per record. A record should include the full stem, diagrams/tables, answer, key idea, worked explanation, warning, source, module, topic, and update status.
4. Store the maintainable source of truth as JSON or spreadsheet data before generating pages. See `references/question_bank_schema.md`.
5. Classify first by the six high-school math modules, then by topic and mistake cause:
   - 函数与导数
   - 三角函数与解三角形
   - 数列
   - 立体几何与平面向量
   - 解析几何
   - 概率统计与计数原理
6. Generate the web version as a category home page plus one independent page per module. The home page should show only module cards and counts, not all problems.
7. In each module page, show one card per problem. Keep answers and explanations collapsed by default with `<details>`. Add top navigation and make problem-card tags link back to the page top.
8. Generate printable material as:
   - an all-in-one version when requested;
   - separate module PDFs for专项练习 by default.
   Each print file should put the problem booklet first and the answer/explanation booklet second.
9. When adding new problems, append to the question bank, copy assets into the existing assets folder, regenerate the web pages and module print files, then validate links.

## Output Contract

Place outputs under `output/` unless the user specifies another location:

- `题库.json` or `.xlsx`: maintainable question bank.
- `web/` or a clearly named web home HTML file: category home plus module pages.
- `print_modules/`: one HTML and one PDF per module.
- `assets/`: cropped question images and answer figures referenced by relative paths.

Prefer stable IDs: `<student-or-source>-<module-code>-<number>`, for example `NB-函数-001` or `S01-WH-08`.

## Reusable Script

Use `scripts/build_error_book.py` when the task already has a clean JSON question bank and image assets. It generates:

- a category-home web page;
- one web page per module;
- one printable HTML per module.

The script does not crop images or derive mathematical explanations; do that upstream, then write the JSON.

Example:

```bash
python3 scripts/build_error_book.py \
  --input /path/to/question_bank.json \
  --output /path/to/output \
  --title "张同学高中数学错题本"
```

After HTML generation, export PDFs with a browser automation tool such as Playwright/Chrome. Verify every PDF visually or with `pdfinfo`.

## Student Experience Rules

- Do not put all problems on the first web page. The first page is only a module menu.
- Make the learner choose one module at a time; this lowers cognitive pressure.
- Keep answers hidden by default for self-testing.
- Put answer, key idea, worked explanation, and common mistake in that order after reveal.
- Use real problem screenshots for dense formulas and diagrams.
- Use MathJax/LaTeX for typed answers and explanations where practical.
- In print versions, leave a small line for 订正日期、是否掌握、错因.

## Validation Checklist

- Every problem belongs to exactly one first-level module.
- Home page contains module cards, not problem cards.
- Each module page contains only its module's problems.
- All image references resolve relative to the HTML file.
- All reveal panels are closed by default.
- Problem-card tag links return to the current page top.
- Each module print PDF exists, uses A4, and has nonblank images.
- Updating from a new scan changes the question bank first, then regenerated outputs.
