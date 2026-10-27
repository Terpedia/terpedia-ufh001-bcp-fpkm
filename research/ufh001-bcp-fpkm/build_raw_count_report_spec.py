"""Build a claim-ledger report specification from executed UFH-001 count results."""

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "research/ufh001-bcp-fpkm"
RAW = PROJECT / "results/raw_counts"
OUTPUT = PROJECT / "raw-count-report-spec.json"


def claim(identifier, kind, text, sources, limitation, artifacts=None):
    item = {"id": identifier, "class": kind, "text": text,
            "sources": sources, "limitation": limitation}
    if artifacts:
        item["artifacts"] = artifacts
    return item


def relative(path):
    return path.relative_to(ROOT).as_posix()


def marker_text(frame, gene, dose):
    matches = frame.loc[frame.gene_name.eq(gene) & frame.contrast.eq(dose)]
    if len(matches) != 1:
        raise ValueError(f"Expected one prespecified {gene} row at {dose}, found {len(matches)}")
    row = matches.iloc[0]
    if pd.isna(row.log2FoldChange):
        return f"{gene} has no finite log2 fold-change estimate"
    padj = "unavailable" if pd.isna(row.padj) else f"{row.padj:.3g}"
    return f"{gene} log2 fold change {row.log2FoldChange:+.3f}, BH-adjusted p {padj}"


def main():
    receipt_path = ROOT / "research/execution-receipts/terputer-ufh001-bcp-raw-counts.json"
    receipt = json.loads(receipt_path.read_text())
    summary = json.loads((RAW / "analysis_summary.json").read_text())
    qc = pd.read_csv(RAW / "analysis_sample_qc.tsv", sep="\t")
    genes = pd.read_csv(RAW / "prespecified_genes.tsv", sep="\t")
    if summary["study"] != "GSE125511" or len(qc) != 9:
        raise ValueError("Unexpected study or library count")
    expected = [RAW / name for name in (
        "analysis_summary.json", "analysis_sample_qc.tsv", "prespecified_genes.tsv",
        "deseq2_bcp20_vs_vehicle.tsv", "deseq2_bcp200_vs_vehicle.tsv")]
    if not all(relative(path) in receipt["artifacts_written"] for path in expected):
        raise ValueError("Execution receipt does not pin all cited count results")
    if set(summary["tested_genes"]) != {"bcp20", "bcp200"}:
        raise ValueError("Both prespecified dose contrasts are required")
    mapped = qc.uniquely_mapped_reads / qc.input_reads * 100
    if mapped.isna().any() or mapped.le(0).any() or mapped.gt(100).any():
        raise ValueError("Invalid mapping fraction")
    result20 = relative(RAW / "deseq2_bcp20_vs_vehicle.tsv")
    result200 = relative(RAW / "deseq2_bcp200_vs_vehicle.tsv")
    summary_path = relative(RAW / "analysis_summary.json")
    markers_path = relative(RAW / "prespecified_genes.tsv")
    claims = [
        claim("R01", "source-reported", "GSE125511 labels three UFH-001 DMSO controls, three 20 µM β-caryophyllene libraries, and three 200 µM β-caryophyllene libraries after 16 hours at 1% oxygen. The three controls are reused from GSE123856.", ["geo", "controls"], "The reused controls are one shared comparison group, not an independent cohort; no normoxic treated arm exists."),
        claim("R02", "observed", f"Nine checksum-verified SRA archives were converted to FASTQ and aligned to GENCODE v48 GRCh38. Per-library unique mapping ranges from {mapped.min():.2f}% to {mapped.max():.2f}%; the unstranded count matrix contains {summary['genes_in_count_matrix']:,} genes.", ["geo", "gencode"], "Mapping quality does not establish independent biological replication or rule out batch effects.", [relative(RAW / "analysis_sample_qc.tsv"), summary_path]),
        claim("R03", "observed", f"The prespecified three-arm PyDESeq2 count model tests {summary['tested_genes']['bcp20']:,} genes at 20 µM and {summary['tested_genes']['bcp200']:,} at 200 µM against the same three DMSO controls. BH-adjusted p < 0.05 occurs for {summary['fdr_below_0_05']['bcp20']:,} and {summary['fdr_below_0_05']['bcp200']:,} genes, respectively; {summary['fdr_below_0_05_abs_log2fc_at_least_1']['bcp20']:,} and {summary['fdr_below_0_05_abs_log2fc_at_least_1']['bcp200']:,} also have absolute log2 fold change at least one.", ["geo"], "The two dose contrasts share controls. These are within-study model estimates, not two independent replications or a pathway test.", [summary_path, result20, result200]),
        claim("R04", "observed", "Prespecified cholesterol marker HMGCR: " + marker_text(genes, "HMGCR", "bcp20") + " at 20 µM; " + marker_text(genes, "HMGCR", "bcp200") + " at 200 µM.", ["geo", "paper"], "HMGCR transcript abundance is not cholesterol synthesis flux, enzyme activity, or direct β-caryophyllene binding.", [markers_path]),
        claim("R05", "observed", "Prespecified signaling marker PGF: " + marker_text(genes, "PGF", "bcp20") + " at 20 µM; " + marker_text(genes, "PGF", "bcp200") + " at 200 µM.", ["geo", "hepg2"], "Dose, time, oxygen, vehicle, and cell identity differ from HepG2; these estimates alone cannot isolate a cell-context interaction.", [markers_path]),
        claim("R06", "source-reported", "The source article reports a cholesterol-biosynthesis response and altered β-caryophyllene sensitivity after HMGCR inhibition.", ["paper"], "This count-model notebook does not reproduce the intervention experiment or establish direct ligand binding."),
        claim("R07", "proposed", "Follow the separately executed HepG2–UFH-001 cross-context comparison with a matched factorial experiment using shared vehicle, oxygen, dose, time, viability controls, biological replicates, and HMGCR or PGF perturbations.", ["geo", "hepg2", "paper"], "The completed cross-study comparison is descriptive while experimental conditions differ; a target-specific interaction requires direct genetic or biochemical evidence."),
    ]
    spec = {
        "schema_version": 2,
        "slug": "ufh001-bcp-raw-counts",
        "title": "β-Caryophyllene in hypoxic UFH-001: raw-read reprocessing and two count-based dose contrasts",
        "question": "Which metabolic and signaling responses to terpene exposure are reproducible, and which depend on cellular context or a specific target?",
        "notebook": "notebooks/terputer-ufh001-bcp-raw-counts.ipynb",
        "execution_receipt": relative(receipt_path),
        "sources": [
            {"id": "geo", "title": "GEO GSE125511 series and samples", "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511"},
            {"id": "controls", "title": "GEO GSE123856 reused control source", "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123856"},
            {"id": "gencode", "title": "GENCODE human release 48", "url": "https://www.gencodegenes.org/human/release_48.html"},
            {"id": "paper", "title": "Original UFH-001 β-caryophyllene study", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/"},
            {"id": "hepg2", "title": "HepG2 raw-count white paper", "url": "https://github.com/Terpedia/terpedia-hepg2-bcp-rsem/blob/f0e0a56ae1b510fa622a11e218fe6b3b8d2f8d54/research/hepg2-bcp-raw-counts/generated/white-paper.md"},
        ],
        "claims": claims,
        "abstract": ["R01", "R02", "R03"],
        "sections": {"background": ["R01", "R06"], "methods": ["R02", "R03"],
                     "results": ["R03", "R04", "R05"], "interpretation": ["R04", "R05", "R06"],
                     "limitations": ["R01", "R03", "R04", "R05"], "next_steps": ["R07"]},
    }
    OUTPUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
