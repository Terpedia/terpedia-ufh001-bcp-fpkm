"""Execute the cross-context notebook with UFH-001 inputs and outputs pinned."""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RAW = "research/ufh001-bcp-fpkm/results/raw_counts"
ARTIFACTS = [
    f"{RAW}/cross_context/gene_effects_hepg2_vs_ufh_20uM.tsv",
    f"{RAW}/cross_context/gene_effects_hepg2_vs_ufh_200uM.tsv",
    f"{RAW}/cross_context/comparison_summary.tsv",
    f"{RAW}/cross_context/comparison_summary.json",
]
INPUTS = [
    "research/execution-receipts/terputer-ufh001-bcp-raw-counts.json",
    f"{RAW}/deseq2_bcp20_vs_vehicle.tsv",
    f"{RAW}/deseq2_bcp200_vs_vehicle.tsv",
]


def main() -> None:
    command = [
        sys.executable, str(ROOT / "notebook-runner.py"),
        "notebooks/terputer-bcp-cross-context.ipynb", str(ROOT), "300",
        json.dumps(ARTIFACTS), json.dumps(INPUTS),
    ]
    subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
