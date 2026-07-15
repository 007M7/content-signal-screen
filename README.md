# Content Signal Screen

> 不是所有 AI 内容都是 slop。先看内容有没有信息，再决定要不要继续。

Content Signal Screen 是一个开源 Skill，用四个信号筛查文章、帖子、报告、视频文字稿或 AI 辅助内容中可能存在的低信息量、低投入和批量生产风险。

它不判断“是不是 AI 写的”，也不替你判断内容是真是假。它只做一个有边界的前置筛查：这段内容是否值得继续核验、修改、转发或发布？

## 四个信号

1. **具体收获**：读者能否复述出具体概念、事实、数据、案例、方法或可检验观点？
2. **来源具体性**：是否有可定位的人、研究、数据、日期、链接或案例？
3. **作者痕迹**：换一个账号后，内容是否仍然可以原样发布？
4. **认知推进**：内容是否减少不确定性、提供新角度，而不只是刺激情绪？

输出四个风险等级：

- `low`：目前看不到明显的低信息量风险；
- `medium`：信号混合，存在部分风险；
- `high`：多个信号偏弱，疑似内容污染风险较高；
- `indeterminate`：正文不足、类型特殊或证据冲突，不能负责地判断。

## 它不是什么

- 不是 AI 文本检测器；
- 不是事实核验器；
- 不是作者动机判断器；
- 不是内容审查器；
- 不是阅读注意力决策器；
- 不会自动删除、屏蔽、发布、上传或写入记忆。

AI 参与生产不等于 slop。个人经历没有学术引用，也不等于低质量。文学、讽刺、广告和娱乐内容需要结合内容类型谨慎判断。

## 快速接入

这是一个标准 Skill 目录，必须保留 `SKILL.md`、`references/` 和 `agents/` 等配套文件。

### Codex

Windows PowerShell：

```powershell
git clone https://github.com/007M7/content-signal-screen.git "$HOME\.codex\skills\content-signal-screen"
```

macOS / Linux：

```bash
git clone https://github.com/007M7/content-signal-screen.git ~/.codex/skills/content-signal-screen
```

重启 Codex 或新建任务后，可以直接说：

```text
请使用 $content-signal-screen 检查这段内容是否存在疑似 Slop 风险。
```

### Claude Code

个人级安装：

```bash
git clone https://github.com/007M7/content-signal-screen.git ~/.claude/skills/content-signal-screen
```

项目级安装：

```bash
mkdir -p .claude/skills
git clone https://github.com/007M7/content-signal-screen.git .claude/skills/content-signal-screen
```

启动 Claude Code 后，可以直接调用：

```text
/content-signal-screen
```

## 示例输出

```text
slop_risk: medium
basis: 样本包含少量具体观点，但来源和作者痕迹不足，情绪表达多于认知推进。
input_coverage: sampled_content
inspected_sections: [标题, 开头, 中段, 结尾]
signals:
  concrete_takeaway: mixed
  source_specificity: weak
  author_footprint: unknown
  cognitive_progress: mixed
uncertainty: 只检查了部分正文，未核验外部事实。
not_inferred: 不推断内容由 AI 生成，也不推断内容一定没有阅读价值。
recommended_next_gate: 补充原始来源并人工复核关键论断。
writeback_status: none
```

## 与 Source Triage 的关系

Content Signal Screen 判断“内容质量风险”，Source Triage 判断“现在是否值得分配注意力”。两者可以连续使用，但一个结果不能自动替代另一个结果。

Source Triage：

```text
https://github.com/007M7/source-triage
```

推荐顺序：

```text
内容质量风险筛查（可选）
        ↓
注意力预算决策
        ↓
来源核验、修改或深读
```

## 本地验证

Windows PowerShell：

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_content_signal_screen.py examples/high-risk.source-signal-screen.json
python scripts/validate_content_signal_screen.py examples/indeterminate-short-input.source-signal-screen.json
```

评测文件 `evals/content-signal-screen-evals.json` 包含 24 个边界样本。它用于检查行为边界和解释质量，不是准确率或节省时间的因果证明。

## 隐私与反馈

默认本地处理。没有遥测、没有自动上传来源、没有自动保存用户内容，也不会自动写入任何项目或长期记忆。

## 开源许可

本项目使用 MIT License。详见 `LICENSE` 和 `LICENSE-STATUS.md`。
