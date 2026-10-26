# Terpedia UFH-001 β-caryophyllene transcriptomics audit

This forkable project analyzes the processed FPKM matrix deposited with [GEO GSE125511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511). It contains an [executed Jupyter notebook](notebooks/terputer-ufh001-bcp-fpkm.ipynb), [generated white paper](research/ufh001-bcp-fpkm/generated/white-paper.md), [claim ledger](research/ufh001-bcp-fpkm/generated/claim-ledger.tsv), [result tables](research/ufh001-bcp-fpkm/results), and [execution receipt](research/execution-receipts/terputer-ufh001-bcp-fpkm.json).

The nine bulk RNA-seq libraries are UFH-001 cells under 1% oxygen for 16 hours, with three DMSO controls and three libraries at each of 20 µM and 200 µM β-caryophyllene. The three controls are reused from [GSE123856](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123856); they are not an independent cohort. The notebook reports sample quality, correlations, pseudocount-sensitive mean-FPKM ratios, and predeclared cholesterol and signaling markers. It does not estimate differential expression or pathway significance.

The [ENA raw-run manifest](research/ufh001-bcp-fpkm/raw_run_manifest.tsv) maps all nine libraries to single-end FASTQs, and the [NCBI SRA manifest](research/ufh001-bcp-fpkm/sra_run_manifest.tsv) pins the normalized SRA archives and Data Locator MD5 values for faster retrieval. Those reads have not been downloaded or analyzed in this project. The three reused control libraries remain the same biological samples as in GSE123856.

An [unexecuted raw-count notebook](notebooks/terputer-ufh001-bcp-raw-counts.ipynb) now specifies QC and separate PyDESeq2 contrasts for the two BCP doses against their shared DMSO controls. Its [dependency lock](requirements-raw-counts.lock.txt) describes the analysis environment. The existing white paper still reports only the deposited FPKM audit; the raw-count notebook is a method draft until the reads, mapping QC, model outputs, and execution receipt exist.

At 200 µM, HMGCR and several cholesterol-associated transcript means are higher than vehicle. This is a processed-matrix observation that agrees in direction with a [source article](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/); it does not establish increased cholesterol flux or direct binding of β-caryophyllene to HMGCR. The [HepG2 audit](https://github.com/Terpedia/terpedia-hepg2-bcp-rsem) differs in cell type, oxygen, dose, time, vehicle, and quantification. Its PGF pattern therefore cannot be called biologically replicated here.

## Reproduce

Use Python 3.10 or newer and Node.js:

```sh
python -m pip install -r requirements.txt
python restore-inputs.py research/ufh001-bcp-fpkm/report-spec.json
python notebook-runner.py notebooks/terputer-ufh001-bcp-fpkm.ipynb . 120 '["research/ufh001-bcp-fpkm/results/analysis_summary.json","research/ufh001-bcp-fpkm/results/sample_qc.tsv","research/ufh001-bcp-fpkm/results/sample_correlations.tsv","research/ufh001-bcp-fpkm/results/descriptive_effects.tsv","research/ufh001-bcp-fpkm/results/marker_effects.tsv"]' '["research/ufh001-bcp-fpkm/analysis.py","research/ufh001-bcp-fpkm/sample_manifest.tsv","research/ufh001-bcp-fpkm/hgnc_crosswalk.tsv","research/ufh001-bcp-fpkm/data/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz","research/ufh001-bcp-fpkm/data/hgnc_complete_set.txt"]'
node report-generator.mjs research/ufh001-bcp-fpkm/report-spec.json
```

Both external downloads are checksum pinned and excluded from Git. HGNC publishes its complete set at a mutable URL; if its bytes change, restoration will fail closed until an archived copy matching the pinned hash is available or the crosswalk is deliberately updated and rerun. The derived [one-to-one crosswalk](research/ufh001-bcp-fpkm/hgnc_crosswalk.tsv) is committed for inspection.

To attach a fork to a `terpedia-report` workspace, use the `add_research_project_submodule` tool with slug `ufh001-bcp-fpkm`; its path is `projects/ufh001-bcp-fpkm`.
