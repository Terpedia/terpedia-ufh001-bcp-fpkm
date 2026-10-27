"""Build a claim-linked report from the executed cross-context notebook."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "research/ufh001-bcp-fpkm"
COMPARISON = PROJECT / "results/raw_counts/cross_context"
RECEIPT = ROOT / "research/execution-receipts/terputer-bcp-cross-context.json"


def claim(identifier, evidence_class, text, sources, limitation, artifacts=None):
    result = {"id": identifier, "class": evidence_class, "text": text,
              "sources": sources, "limitation": limitation}
    if artifacts:
        result["artifacts"] = artifacts
    return result


def main():
    summary_path = COMPARISON / "comparison_summary.json"
    summary = json.loads(summary_path.read_text())
    receipt = json.loads(RECEIPT.read_text())
    if receipt["notebook"] != "notebooks/terputer-bcp-cross-context.ipynb":
        raise ValueError("Unexpected execution receipt")
    if receipt["artifacts_written"].get(summary_path.relative_to(ROOT).as_posix()) is None:
        raise ValueError("Comparison summary is not pinned to notebook execution")
    by_dose = {row["dose"]: row for row in summary["comparisons"]}
    low, high = by_dose["20uM"], by_dose["200uM"]
    if low["common_tested_genes"] != high["common_tested_genes"]:
        raise ValueError("Comparison universes differ")
    artifacts = [path for path in receipt["artifacts_written"] if path.startswith("research/ufh001-bcp-fpkm/results/raw_counts/cross_context/")]
    claims = [
        claim("C01", "source-reported", "The UFH-001 source has one shared three-library DMSO control group and 20 µM and 200 µM β-caryophyllene arms under hypoxia; the independent HepG2 study used different culture and exposure conditions.", ["ufh", "hepg2"], "Cell identity, oxygen, dose, time, and vehicle are confounded across studies."),
        claim("C02", "observed", f"The receipt-pinned count-model comparison joins {low['common_tested_genes']:,} genes tested in both studies by versioned gene ID. The HepG2 contrast has {high['hepg2_fdr05_in_common_universe']:,} BH-FDR < 0.05 genes in this common universe; UFH-001 has {low['ufh_fdr05_in_common_universe']} at 20 µM and {high['ufh_fdr05_in_common_universe']} at 200 µM.", ["ufh", "hepg2"], "The contrast significance counts depend on within-study sample size, dispersion, and exposure; their difference is not a formal interaction test.", artifacts),
        claim("C03", "observed", f"At 200 µM in UFH-001, {high['both_fdr05']} genes meet BH-FDR < 0.05 in both studies: {high['both_fdr05_same_direction']} have matching fold-change signs and {high['both_fdr05_opposite_direction']} have opposite signs. Across all common tested genes, Spearman fold-change correlations are {low['all_common_spearman_log2fc']:.3f} at 20 µM and {high['all_common_spearman_log2fc']:.3f} at 200 µM.", ["ufh", "hepg2"], "These descriptive comparisons do not establish reproducibility of a pathway, a cellular-context interaction, or target specificity.", artifacts),
        claim("C04", "proposed", "Run a matched factorial study in both cell lines with shared vehicle, oxygen, exposure time, dose and viability controls, biological replicates, and HMGCR or PGF perturbations; prespecify pathway and interaction tests.", ["ufh", "hepg2"], "Target attribution also needs genetic rescue or orthogonal binding and functional evidence."),
    ]
    spec = {
        "schema_version": 2,
        "slug": "bcp-cross-context-counts",
        "title": "β-Caryophyllene transcriptomics across HepG2 and hypoxic UFH-001: a descriptive count-model comparison",
        "question": "Which metabolic and signaling responses to terpene exposure are reproducible, and which depend on cellular context or a specific target?",
        "notebook": receipt["notebook"],
        "execution_receipt": RECEIPT.relative_to(ROOT).as_posix(),
        "sources": [
            {"id": "ufh", "title": "GEO GSE125511", "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511"},
            {"id": "hepg2", "title": "HepG2 GSE276099 raw-count report", "url": "https://github.com/Terpedia/terpedia-hepg2-bcp-rsem/blob/f0e0a56ae1b510fa622a11e218fe6b3b8d2f8d54/research/hepg2-bcp-raw-counts/generated/white-paper.md"},
        ],
        "claims": claims,
        "abstract": ["C01", "C02", "C03"],
        "sections": {"background": ["C01"], "methods": ["C02"], "results": ["C02", "C03"],
                     "interpretation": ["C03"], "limitations": ["C01", "C02", "C03"],
                     "next_steps": ["C04"]},
    }
    path = PROJECT / "cross-context-report-spec.json"
    path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print(path)


if __name__ == "__main__":
    main()
