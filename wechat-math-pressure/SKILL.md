---
name: wechat-math-pressure
description: Download math exam images from WeChat article links, organize paper and answer images into a PDF, and generate a polished pressure-question HTML study page with verified crops, OCR/MathJax solutions, and mobile-friendly reveal panels. Use when the user gives an mp.weixin.qq.com/s link containing Chinese high-school math试题+答案 images and asks to整理成PDF, 提取压轴题, 做HTML, or OCR解析.
---

# WeChat Math Pressure

Use this skill for WeChat public-account articles that embed Chinese math exam papers and answer keys as images.

## Hard Requirements

- **Never reuse an old WeChat cache unless the title and contact sheet prove it is the same article.**
- **Crops must be complete, not tight, and not polluted by neighboring questions.** Every crop must include the full problem number, complete stem, all choices/subparts, diagrams, tables, and final formula/inequality line. For common failure points `7, 11, 19`, open the final `qXX.png` directly after generation.
- **Question crops must have clean margins.** Do not clip the first line, final option, radical bar, or bottom formula. Add a little whitespace when in doubt.
- **Formula text must use robust MathJax.** Use braced forms: `\frac{5}{7}`, `\frac{1}{m}`, `\frac{e}{x}`, `\frac{3}{2}`, `\frac{2}{3}`, `\frac{1}{6}`, `\sqrt{3}`. Never leave `\frac57`, `\frac1m`, `\frac ex`, `\frac32`, `\frac23`, `\frac16`, or `\sqrt3`.
- **Avoid raw `<` before letters inside generated HTML.** In MathJax source embedded in HTML, write `\lt`/`\gt` for inequalities like `E(\xi)\lt c` and `a\lt m\lt b`; otherwise the browser may treat `<c` or `<m` as an HTML tag and hide content.
- **Cards `14` and `19` require explicit formula QA when present.** Expand their reveal panels and verify answers and solutions render without visible raw TeX, missing terms, or `mjx-merror`.
- **If `file://` preview is blocked or unreliable, validate through a local HTTP server** such as `python3 -m http.server <port>` and open `http://127.0.0.1:<port>/...`.

## Workflow

1. Fetch the article with a mobile WeChat user-agent first; desktop `curl` often returns captcha HTML.
   - Example UA: `Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49 NetType/WIFI Language/zh_CN`
   - Verify the HTML contains `msg_title`, `wxw-img`, and the expected exam title/region.
   - If still captcha-blocked, ask the user to pass verification in the in-app browser. Do not bypass CAPTCHAs.
2. Parse article-body images only:
   - Prefer `<img>` elements whose class contains `wxw-img`.
   - Use `data-src` before `src`.
   - Save `manifest.json` with source URL, index, dimensions, `data-w`, and `data-ratio`.
3. Download images into a dedicated directory such as `downloads/wechat_<slug>/images/`, using the same mobile UA and article URL as `Referer`.
4. Build a contact sheet and classify images. Exclude QR codes, avatars, follow banners, and promo strips from the main PDF, but keep them in downloads.
5. Generate an ordered PDF from paper and answer pages only under `output/pdf/`.
6. Select pressure questions. Default to `7, 8, 11, 14, 18, 19`; if the paper structure differs, use the actual final/high-value questions and state the adjustment.
7. Crop each selected question from paper images. Generate `crop_review.jpg`, then open each risky final crop (`q07`, `q11`, `q19` when present) directly.
8. OCR or manually transcribe answer content into clean MathJax text. Prefer OCR tools if available; otherwise transcribe from visually inspected answer images. Keep dense formulas as MathJax, not screenshots, unless exact reconstruction is unsafe.
9. Generate the HTML under `output/`:
   - One card per pressure problem.
   - Question image first.
   - Closed `<details>` reveal panel by default.
   - Inside reveal: answer, red key ideas, OCR/MathJax worked solution, common-error reminder.
   - Relative links, MathJax enabled, readable desktop/mobile layout.
10. Validate before delivery:
   - All image/PDF links resolve.
   - Expected number of cards exists.
   - Reveal panels are closed by default.
   - Expand formula-heavy cards, especially `14` and `19`, and verify `document.querySelectorAll('mjx-merror').length === 0`.
   - Re-inspect final crops after any boundary change.

## Formula QA Search

Before final delivery, search generated HTML for:

- Control characters such as form-feed from accidental `\f`.
- Shorthand/fragile TeX: `frac57`, `frac1m`, `frac ex`, `frac23`, `frac16`, `frac32`, `sqrt3`.
- HTML-swallowed inequalities: `E(\\xi)<c`, `a<m<b`, `<c`, `<m` in formula text. Normal HTML tags such as `<meta>` are fine.
- OCR artifacts: `lqrt`, `1n`, missing braces in `\ln`, `\sqrt{}`.

## Delivery Summary

Report the PDF path, HTML path, raw image download directory, and crop/MathJax validation result.
