---
name: content-signal-screen
description: Screen an article, post, transcript, report, or AI-assisted content for bounded low-information and mass-production risk using four content signals. Use when the user asks whether content is suspiciously slop, content-farm-like, low-information, algorithmically produced, or worth quality-checking before sharing or publishing. Do not use as an AI detector, fact checker, reading-attention triage, or author-intent judge.
---

# Content Signal Screen

Screen content quality risk before the user invests further attention, forwards a post, or publishes a draft. Return one bounded risk level, four signal assessments, evidence, uncertainty, and a next gate.

This Skill is intentionally adjacent to `source-triage`:

- `content-signal-screen`: does this content show low-information or mass-production risk?
- `source-triage`: should this source receive attention now?

Do not merge the two decisions. A high content-risk result is not proof that a source is false or not worth reading.

## Trigger boundary

Use this Skill when the user asks:

- “这篇内容是不是 slop？”
- “这段内容是不是信息垃圾或内容农场？”
- “帮我检查这批 AI 文案的信息质量风险。”
- “发布前帮我做一次内容质量筛查。”

Do not use it as the primary Skill when the user asks:

- “这篇文章值得我现在读吗？”
- “这份报告和我的项目相关吗？”
- “我只有十分钟，应该看哪些部分？”

Those are `source-triage` tasks. If the user asks both questions, answer them as two separate gates.

## Required workflow

1. Confirm that the requested judgment is content-quality risk, not truth, authorship, or reading priority.
2. Establish input coverage. Use the available full content or sample; do not infer from a title, thumbnail, account name, or AI disclosure alone.
3. Assess all four signals, each with `rating`, `evidence`, and `confidence`:
   - `concrete_takeaway`: can a reader state a concrete concept, fact, case, data point, method, or testable claim?
   - `source_specificity`: are people, studies, data, dates, links, cases, or other locatable sources provided when appropriate?
   - `author_footprint`: does the content contain concrete experience, responsibility, process detail, or judgment that cannot be swapped to any account unchanged?
   - `cognitive_progress`: does it reduce uncertainty or add a usable angle rather than only stimulate emotion?
4. Aggregate conservatively into one `slop_risk`: `low`, `medium`, `high`, or `indeterminate`.
5. Always state uncertainty and what was not inferred.
6. Recommend a next gate, such as source verification, human review, revision, or `source-triage`.
7. Stop after the bounded screen. Do not automatically fact-check, route, delete, publish, upload, or write memory.

## Aggregation guardrails

- Use `high` only when input coverage is sufficient, at least three signals are `weak`, no obvious content-type exception applies, and the evidence is stated.
- Use `medium` for mixed signals or incomplete but usable evidence.
- Use `low` when concrete information, sources, author-specific detail, or cognitive progress are broadly present.
- Use `indeterminate` when the sample is insufficient, the content type makes the heuristic unsuitable, or the signals conflict materially.
- Do not use numeric scores in v0.1. There is no calibrated weighting or validated classifier.

## Hard boundaries

- AI participation does not equal slop.
- Suspicious slop risk does not equal falsehood, malicious intent, or zero reading value.
- Missing sources are evidence limits, not proof of low quality; personal experience and creative work do not need academic citations for every claim.
- Emotional content is not automatically low quality; record whether it also advances understanding.
- Anonymous content is not automatically low quality; treat author footprint as unknown when appropriate.
- Do not expose private source text in public artifacts, examples, or telemetry.

## Output contract

Return the following fields in readable text or the v0.1 JSON form in `references/output-templates.md`:

```text
slop_risk:
basis:
input_coverage:
inspected_sections:
signals:
uncertainty:
not_inferred:
recommended_next_gate:
writeback_status: none
```

`signals` must contain the four named signals. Each signal must include a rating, evidence, and confidence.

## Resources

- Read `references/signal-rules.md` for detailed signal rules and content-type exceptions.
- Read `references/output-templates.md` when producing or validating JSON artifacts.
- Run `scripts/validate_content_signal_screen.py` for mechanical artifact validation.

No network, telemetry, automatic upload, automatic writeback, or installation step is required by this Skill.
