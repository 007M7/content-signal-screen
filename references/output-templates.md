# Content Signal Screen 输出契约 v0.1

```json
{
  "schema_version": "0.1",
  "run_id": "optional-local-id",
  "created_at": "2026-07-15T00:00:00Z",
  "source": {
    "title": "",
    "path_or_url": "",
    "source_type": "article|post|video_transcript|report|other",
    "sensitivity": "public|private|unknown"
  },
  "slop_risk": "low|medium|high|indeterminate",
  "basis": "",
  "input_coverage": "metadata_only|sampled_content|full_content|other",
  "inspected_sections": [],
  "signals": {
    "concrete_takeaway": {
      "rating": "strong|mixed|weak|unknown",
      "evidence": "",
      "confidence": "low|medium|high"
    },
    "source_specificity": {
      "rating": "strong|mixed|weak|unknown",
      "evidence": "",
      "confidence": "low|medium|high"
    },
    "author_footprint": {
      "rating": "strong|mixed|weak|unknown",
      "evidence": "",
      "confidence": "low|medium|high"
    },
    "cognitive_progress": {
      "rating": "strong|mixed|weak|unknown",
      "evidence": "",
      "confidence": "low|medium|high"
    }
  },
  "uncertainty": "",
  "not_inferred": "",
  "recommended_next_gate": "",
  "writeback_status": "none"
}
```

规则：

- `schema_version` 必须为 `0.1`。
- `signals` 必须恰好包含四个规定信号。
- 每个信号必须包含 `rating`、`evidence`、`confidence`。
- `metadata_only` 可以为空 `inspected_sections`；其他 coverage 必须列出实际检查范围。
- `uncertainty`、`not_inferred`、`recommended_next_gate` 必须非空。
- `writeback_status` 必须为 `none`。
- 不得出现 `ai_generated`、`truth_score`、`author_intent`、`automatic_action`、`telemetry`、`upload_source`、`durable_writeback` 等越界字段。
- `source` 可以是本地文件或用户提供的链接；validator 不访问来源，也不上传内容。
