# Question Bank Schema

Use one record per problem. JSON is the easiest interchange format, but the same fields can live in a spreadsheet.

## Required Fields

- `id`: stable unique ID.
- `source`: student, notebook, school, or exam name.
- `number`: original problem number or page-local number.
- `type`: 单选题 / 多选题 / 填空题 / 解答题 / 其他.
- `module`: one of the six first-level高中数学 modules.
- `topic`: concise second-level knowledge point.
- `title`: short learning title, not just the original problem number.
- `question_image`: path to cropped question image relative to the question bank or output assets root.
- `answer`: final answer, preferably with LaTeX where useful.
- `key_ideas`: list of actionable key steps.
- `analysis`: list of explanation steps, or `solution_parts` for long-answer problems.
- `warning`: common mistake or correction reminder.

## Optional Fields

- `difficulty`: 基础 / 中档 / 压轴题.
- `mistake_cause`: 概念不清 / 计算错误 / 审题错误 / 方法不会 / 表达不规范.
- `answer_images`: auxiliary official-answer figures.
- `student_status`: 未练 / 已练 / 已订正 / 已掌握.
- `review_dates`: list of planned or completed review dates.
- `source_page`: original scan page or PDF page.

## Minimal Example

```json
[
  {
    "id": "S01-WH-08",
    "source": "武汉5G",
    "number": "8",
    "type": "单选题",
    "module": "函数与导数",
    "topic": "函数对称 / 恒成立",
    "title": "先确定外层函数的阈值",
    "question_image": "assets/wuhan5g/q08.png",
    "answer": "\\(B\\)",
    "key_ideas": [
      "由对称关系先推出中心和阈值。",
      "把恒成立问题转成参数范围。"
    ],
    "analysis": [
      "先利用函数单调性确定等价条件。",
      "再取特殊值获得必要条件，并证明充分性。"
    ],
    "warning": "不要一上来硬求函数解析式。"
  }
]
```
