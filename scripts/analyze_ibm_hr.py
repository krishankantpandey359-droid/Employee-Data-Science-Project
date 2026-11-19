"""Generate descriptive outputs for the IBM HR attrition benchmark."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ibm_hr_data import load_ibm_hr_data, summarize_attrition

DEFAULT_DATA = ROOT / "data" / "raw" / "ibm_hr_attrition.csv"
DEFAULT_OUTPUT = ROOT / "outputs"


def run_analysis(data_path: str | Path = DEFAULT_DATA,
                 output_dir: str | Path = DEFAULT_OUTPUT) -> dict:
    """Run validation, summary tables, and reproducible chart exports."""
    data_path = Path(data_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frame = load_ibm_hr_data(data_path)
    summary = summarize_attrition(frame)
    serializable = {
        key: value.to_dict(orient="records") if isinstance(value, pd.DataFrame) else value
        for key, value in summary.items()
    }
    serializable["numeric_summary"] = summary["numeric_summary"].to_dict()
    (output_dir / "attrition_summary.json").write_text(
        json.dumps(serializable, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )

    table_files = {
        "by_department": summary["by_department"],
        "by_job_role": summary["by_job_role"],
        "by_overtime": summary["by_overtime"],
        "by_job_satisfaction_code": summary["by_job_satisfaction_code"],
        "by_income_quartile": summary["by_income_quartile"],
    }
    for name, table in table_files.items():
        table.to_csv(output_dir / f"{name}.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.countplot(data=frame, x="Attrition", hue="Attrition", legend=False, ax=ax)
    ax.set(title="Attrition label count in the IBM benchmark",
           xlabel="Attrition label", ylabel="Record count")
    fig.tight_layout()
    fig.savefig(output_dir / "attrition_overall.png", dpi=160)
    plt.close(fig)

    department = summary["by_department"].sort_values("attrition_share_percent")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(department["Department"], department["attrition_share_percent"])
    ax.set(title="Attrition share by department in the benchmark",
           xlabel="Attrition share (%)", ylabel="Department")
    fig.tight_layout()
    fig.savefig(output_dir / "attrition_by_department.png", dpi=160)
    plt.close(fig)

    income = summary["by_income_quartile"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(income["income_quartile"].astype(str), income["attrition_share_percent"])
    ax.set(title="Attrition share across benchmark income quartiles",
           xlabel="Sample-defined income quartile", ylabel="Attrition share (%)")
    fig.tight_layout()
    fig.savefig(output_dir / "attrition_by_income_quartile.png", dpi=160)
    plt.close(fig)

    print(f"Validated records: {summary['records']}")
    print(f"Fields: {summary['fields']}")
    print(f"Attrition records: {summary['attrition_records']}")
    print(f"Attrition share (%): {summary['attrition_share_percent']}")
    print(f"Saved tables, JSON and charts to: {output_dir}")
    return serializable


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(DEFAULT_DATA), help="Path to IBM HR CSV.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT),
                        help="Output directory for reports and charts.")
    args = parser.parse_args()
    run_analysis(args.data, args.output_dir)


if __name__ == "__main__":
    main()
