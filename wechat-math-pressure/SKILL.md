---
name: wechat-math-pressure
description: Download math exam images from WeChat article links, organize the original paper and answer images into a PDF, and generate a polished pressure-question HTML study page with verified crops, OCR/MathJax solutions, and mobile-friendly reveal panels. Use when the user gives an mp.weixin.qq.com/s link containing Chinese high-school math试题+答案 images and asks to整理成PDF, 提取压轴题, 做HTML, or OCR解析.
---

# WeChat Math Pressure

Use this skill for WeChat public-account articles that embed exam-paper and answer-key pages as images.

## Hard Requirements

These are mandatory, learned from repeated corrections:

- **Question crops must be complete and not tight.** For every requested problem, especially common pressure items such as `7, 11, 19`, the crop must include the full problem number, complete stem, all choices/subparts, diagrams, and final inequality/formula line. It must not clip the first line, final option, or square-root bar. Add clean top/bottom margin if needed.
- **Question crops must not include unrelated previous-problem leftovers.** If a crop includes choices or formulas from the previous question, recrop it. Do not deliver a crop just because the target question is visible somewhere inside it.
- **After any crop adjustment, regenerate the asset and visually inspect it again.** Open the final `qXX.png`, not only the contact sheet. Report that the crop was checked.
- **Answer formulas must use robust MathJax, never shorthand.** Use `\frac{5}{7}`, `\frac{1}{m}`, `\frac{e}{x}`, `\frac{3}{2}`, `\frac{2}{3}`, `\frac{1}{6}`, and `\sqrt{3}`. Do not leave shorthand such as `\frac57`, `\frac1m`, `\frac ex`, `\frac32`, `\frac23`, `\frac16`, or `\sqrt3`.
- **Formula-heavy answer strips must be explicitly checked.** Always inspect answer sections for problem `14` and problem `19` when present, because they often contain fraction and radical OCR errors. Expand their reveal panels and verify MathJax renders without visible raw TeX or `mjx-merror`.
- **If browser preview cannot use `file://`, use a local HTTP server.** Validate the generated HTML through `http://127.0.0.1:<port>/...`, expand the relevant cards, and check `document.querySelectorAll('mjx-merror').length === 0`.

## Core Workflow

1. Fetch the WeChat article with a mobile WeChat user-agent first. A normal desktop `curl` often returns a captcha page.
   - Example UA: `Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49 NetType/WIFI Language/zh_CN`
   - Verify the returned HTML contains `msg_title`, `wxw-img`, and article text such as the exam region/title.
   - If the response is still a captcha page, use the in-app browser and ask the user to pass the verification. Do not bypass CAPTCHAs.
2. Parse only article-body images:
   - Prefer `<img>` elements with class containing `wxw-img`.
   - Use `data-src` before `src`.
   - Preserve a `manifest.json` with source URL, image index, dimensions, `data-w`, and `data-ratio`.
3. Download every body image into a dedicated directory such as `downloads/wechat_<slug>/images/`.
   - Use the same WeChat mobile UA and the original article URL as `Referer`.
   - Convert animated GIF banners to a first-frame PNG if needed.
4. Build a contact sheet and visually classify images.
   - Exclude QR codes, author avatars, follow banners, and promotional strips from the main PDF.
   - Keep excluded images in the download directory for traceability.
5. Generate a PDF from the ordered paper and answer pages only, under `output/pdf/`.
6. Identify the pressure-question set.
   - Default to `7, 8, 11, 14, 18, 19`.
   - If the paper has a different structure, use the actual final/high-value questions and explain the adjustment.
7. Crop each requested question from the paper images.
   - Every crop must include the problem number, full stem, all subquestions, choices/blanks, diagrams, and tables.
   - Remove unrelated previous/next questions, but prefer a little clean margin over clipping.
   - For `q7`, `q11`, and `q19`, open the final crop image directly after generation; these are common failure points for missing choices, previous-question residue, or tight top boundaries.
   - Make a `crop_review.jpg` and visually inspect it before delivery.
8. OCR the answer/key content into clean MathJax text.
   - Use a local OCR engine if available; otherwise manually transcribe from the answer images after visual inspection.
   - Preserve formulas with MathJax, using braced forms such as `\frac{2}{3}` instead of ambiguous `\frac23`.
   - Do not leave OCR artifacts like `\sqrt3` from source images as final text if it should be `\sqrt{3}`.
   - Prefer braced fractions for all single-character numerators/denominators too: `\frac{1}{m}`, `\frac{e}{x}`, `\frac{c}{a}`.
9. Generate a polished HTML page under `output/` with:
   - One card per pressure problem.
   - Question image first.
   - A closed `<details>` reveal panel by default.
   - Inside the reveal panel: answer, red key ideas, OCR/MathJax worked solution, common-error reminder.
   - Relative image links, MathJax enabled, readable desktop/mobile layout.
10. Validate:
   - All image and PDF links resolve.
   - The HTML has the expected number of cards.
   - Reveal panels are closed by default.
   - Open representative reveal panels and verify `mjx-merror` count is `0`.
   - When cards `14` or `19` exist, open those reveal panels specifically and verify their answer strips and solution formulas render.
   - Inspect corrected crops after any boundary change.

## WeChat Extraction Notes

Use a dedicated output slug based on the exam title, not a generic cache folder. Never reuse an old `tmp/wechat_*` directory unless the title and contact sheet prove it is the same article.

When parsing image order, expect:

- QR/follow images before or after the real content.
- A banner image near the top.
- Paper pages followed by answer pages.
- All real pages often share the same dimensions and ratio.

## HTML Style Contract

Follow the “小蓝本” study-page pattern:

- Header and table of contents.
- Warm paper-like background, restrained blue/gold accents, red key-idea box.
- Cards with radius 8px or less.
- Question screenshots full width.
- Answers hidden by default unless the user asks to show them immediately.
- Formula-heavy explanations should be OCR/MathJax text, not only answer screenshots.

## Formula QA Checklist

Before final delivery, search the generated HTML for common artifacts:

- Control characters such as form-feed from accidental `\f`.
- Unbraced shorthand likely to render poorly: `frac57`, `frac1m`, `frac ex`, `frac23`, `frac16`, `frac32`.
- OCR source artifacts such as `sqrt3`, `lqrt`, `1n`, or missing braces in `\ln`, `\sqrt{}`.

Then open or preview the HTML and check that MathJax reports no `<mjx-merror>` nodes after expanding at least the most formula-heavy cards. If the paper includes questions `14` and `19`, those cards must be included in this check.

## Delivery Summary

Report:

- PDF path.
- HTML path.
- Raw image download directory.
- Crop and MathJax validation result.
