"""Report generation helper."""

from __future__ import annotations

from pathlib import Path

from .metrics import MetricsReport


def render_report_stub(metrics: MetricsReport) -> str:
    """Return a report that follows the official template exactly."""
    scenario_rows = []
    for s in metrics.scenario_metrics:
        success_str = "True" if s.success else "False"
        row = (
            f"| {s.scenario_id} | {s.expected_route} | {s.actual_route} | "
            f"{success_str} | {s.retry_count} | {s.interrupt_count} |"
        )
        scenario_rows.append(row)
    
    table_content = "\n".join(scenario_rows)

    return f"""# Day 23 Lab Report

## 1. Team / student

- Name: Nguyễn Văn Hiếu
- MSSV: 2A202600454
- Repo/commit: Lab Day 23
- Date: 2026-05-11

## 2. Architecture

The graph consists of 11 nodes (intake, classify, tool, evaluate, approval, retry, answer, etc.) 
connected via conditional edges. It uses priority-based routing and bounded retry loops.

## 3. State schema

| Field | Reducer | Why |
|---|---|---|
| messages | append | audit conversation/events |
| tool_results | append | history of tool outputs |
| errors | append | track failure reasons |
| route | overwrite | current route only |

## 4. Scenario results

| Scenario | Expected route | Actual route | Success | Retries | Interrupts |
|---|---|---|---:|---:|---:|
{table_content}

- **Total Success Rate**: {metrics.success_rate:.2%}
- **Average Nodes Visited**: {metrics.avg_nodes_visited:.2f}

## 5. Failure analysis

1. **Retry or tool failure**: Handled by bounded loops (max_attempts) and evaluate node.
2. **Risky action without approval**: Prevented by mandatory HITL approval node.

## 6. Persistence / recovery evidence

Implemented SqliteSaver in persistence.py. Verified by checkpoints.db generation.

## 7. Extension work

**Persistence (SQLite)**: Implemented robust SQLite checkpointer for state durability.

## 8. Improvement plan

Productionize with LLM-as-judge and exponential backoff.
"""


def write_report(metrics: MetricsReport, output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_report_stub(metrics), encoding="utf-8")
