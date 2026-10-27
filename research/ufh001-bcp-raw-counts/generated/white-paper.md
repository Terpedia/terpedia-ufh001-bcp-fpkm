# β-Caryophyllene in hypoxic UFH-001: raw-read reprocessing and two count-based dose contrasts

> Generated evidence brief. Each statement is linked to a claim record; scientific interpretation still requires review.

**Research question:** Which metabolic and signaling responses to terpene exposure are reproducible, and which depend on cellular context or a specific target?

**Notebook:** `notebooks/terputer-ufh001-bcp-raw-counts.ipynb` · SHA-256 `5e904ebc762d3e7eb95cc17115864ab3f3850e3af91b002391fe5201f7df9652` · 4 executed code cells

## Abstract

**Source-reported:** GSE125511 labels three UFH-001 DMSO controls, three 20 µM β-caryophyllene libraries, and three 200 µM β-caryophyllene libraries after 16 hours at 1% oxygen. The three controls are reused from GSE123856. (claim R01; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [2](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123856))

**Observed in notebook:** Nine checksum-verified SRA archives were converted to FASTQ and aligned to GENCODE v48 GRCh38. Per-library unique mapping ranges from 87.59% to 89.30%; the unstranded count matrix contains 78,894 genes. (claim R02; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [3](https://www.gencodegenes.org/human/release_48.html))

**Observed in notebook:** The prespecified three-arm PyDESeq2 count model tests 14,312 genes at 20 µM and 14,312 at 200 µM against the same three DMSO controls. BH-adjusted p < 0.05 occurs for 0 and 139 genes, respectively; 0 and 40 also have absolute log2 fold change at least one. (claim R03; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511))

## Background

**Source-reported:** GSE125511 labels three UFH-001 DMSO controls, three 20 µM β-caryophyllene libraries, and three 200 µM β-caryophyllene libraries after 16 hours at 1% oxygen. The three controls are reused from GSE123856. (claim R01; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [2](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123856))

**Source-reported:** The source article reports a cholesterol-biosynthesis response and altered β-caryophyllene sensitivity after HMGCR inhibition. (claim R06; [4](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/))

## Methods

**Observed in notebook:** Nine checksum-verified SRA archives were converted to FASTQ and aligned to GENCODE v48 GRCh38. Per-library unique mapping ranges from 87.59% to 89.30%; the unstranded count matrix contains 78,894 genes. (claim R02; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [3](https://www.gencodegenes.org/human/release_48.html)) Artifacts: [research/ufh001-bcp-fpkm/results/raw_counts/analysis_sample_qc.tsv](../../ufh001-bcp-fpkm/results/raw_counts/analysis_sample_qc.tsv), [research/ufh001-bcp-fpkm/results/raw_counts/analysis_summary.json](../../ufh001-bcp-fpkm/results/raw_counts/analysis_summary.json).

**Observed in notebook:** The prespecified three-arm PyDESeq2 count model tests 14,312 genes at 20 µM and 14,312 at 200 µM against the same three DMSO controls. BH-adjusted p < 0.05 occurs for 0 and 139 genes, respectively; 0 and 40 also have absolute log2 fold change at least one. (claim R03; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511)) Artifacts: [research/ufh001-bcp-fpkm/results/raw_counts/analysis_summary.json](../../ufh001-bcp-fpkm/results/raw_counts/analysis_summary.json), [research/ufh001-bcp-fpkm/results/raw_counts/deseq2_bcp20_vs_vehicle.tsv](../../ufh001-bcp-fpkm/results/raw_counts/deseq2_bcp20_vs_vehicle.tsv), [research/ufh001-bcp-fpkm/results/raw_counts/deseq2_bcp200_vs_vehicle.tsv](../../ufh001-bcp-fpkm/results/raw_counts/deseq2_bcp200_vs_vehicle.tsv).

## Results

**Observed in notebook:** The prespecified three-arm PyDESeq2 count model tests 14,312 genes at 20 µM and 14,312 at 200 µM against the same three DMSO controls. BH-adjusted p < 0.05 occurs for 0 and 139 genes, respectively; 0 and 40 also have absolute log2 fold change at least one. (claim R03; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511)) Artifacts: [research/ufh001-bcp-fpkm/results/raw_counts/analysis_summary.json](../../ufh001-bcp-fpkm/results/raw_counts/analysis_summary.json), [research/ufh001-bcp-fpkm/results/raw_counts/deseq2_bcp20_vs_vehicle.tsv](../../ufh001-bcp-fpkm/results/raw_counts/deseq2_bcp20_vs_vehicle.tsv), [research/ufh001-bcp-fpkm/results/raw_counts/deseq2_bcp200_vs_vehicle.tsv](../../ufh001-bcp-fpkm/results/raw_counts/deseq2_bcp200_vs_vehicle.tsv). **Limitation:** The two dose contrasts share controls. These are within-study model estimates, not two independent replications or a pathway test.

**Observed in notebook:** Prespecified cholesterol marker HMGCR: HMGCR log2 fold change -0.119, BH-adjusted p 1 at 20 µM; HMGCR log2 fold change +1.543, BH-adjusted p 1.74e-07 at 200 µM. (claim R04; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [4](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/)) Artifacts: [research/ufh001-bcp-fpkm/results/raw_counts/prespecified_genes.tsv](../../ufh001-bcp-fpkm/results/raw_counts/prespecified_genes.tsv). **Limitation:** HMGCR transcript abundance is not cholesterol synthesis flux, enzyme activity, or direct β-caryophyllene binding.

**Observed in notebook:** Prespecified signaling marker PGF: PGF log2 fold change -0.905, BH-adjusted p 1 at 20 µM; PGF log2 fold change -0.525, BH-adjusted p unavailable at 200 µM. (claim R05; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [5](https://github.com/Terpedia/terpedia-hepg2-bcp-rsem/blob/f0e0a56ae1b510fa622a11e218fe6b3b8d2f8d54/research/hepg2-bcp-raw-counts/generated/white-paper.md)) Artifacts: [research/ufh001-bcp-fpkm/results/raw_counts/prespecified_genes.tsv](../../ufh001-bcp-fpkm/results/raw_counts/prespecified_genes.tsv). **Limitation:** Dose, time, oxygen, vehicle, and cell identity differ from HepG2; these estimates alone cannot isolate a cell-context interaction.

## Interpretation

**Observed in notebook:** Prespecified cholesterol marker HMGCR: HMGCR log2 fold change -0.119, BH-adjusted p 1 at 20 µM; HMGCR log2 fold change +1.543, BH-adjusted p 1.74e-07 at 200 µM. (claim R04; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [4](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/)) Artifacts: [research/ufh001-bcp-fpkm/results/raw_counts/prespecified_genes.tsv](../../ufh001-bcp-fpkm/results/raw_counts/prespecified_genes.tsv). **Limitation:** HMGCR transcript abundance is not cholesterol synthesis flux, enzyme activity, or direct β-caryophyllene binding.

**Observed in notebook:** Prespecified signaling marker PGF: PGF log2 fold change -0.905, BH-adjusted p 1 at 20 µM; PGF log2 fold change -0.525, BH-adjusted p unavailable at 200 µM. (claim R05; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [5](https://github.com/Terpedia/terpedia-hepg2-bcp-rsem/blob/f0e0a56ae1b510fa622a11e218fe6b3b8d2f8d54/research/hepg2-bcp-raw-counts/generated/white-paper.md)) Artifacts: [research/ufh001-bcp-fpkm/results/raw_counts/prespecified_genes.tsv](../../ufh001-bcp-fpkm/results/raw_counts/prespecified_genes.tsv). **Limitation:** Dose, time, oxygen, vehicle, and cell identity differ from HepG2; these estimates alone cannot isolate a cell-context interaction.

**Source-reported:** The source article reports a cholesterol-biosynthesis response and altered β-caryophyllene sensitivity after HMGCR inhibition. (claim R06; [4](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/)) **Limitation:** This count-model notebook does not reproduce the intervention experiment or establish direct ligand binding.

## Limitations

**Claim R01 (source-reported):** GSE125511 labels three UFH-001 DMSO controls, three 20 µM β-caryophyllene libraries, and three 200 µM β-caryophyllene libraries after 16 hours at 1% oxygen. The three controls are reused from GSE123856. **Limitation:** The reused controls are one shared comparison group, not an independent cohort; no normoxic treated arm exists. ([1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [2](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123856))

**Claim R03 (observed):** The prespecified three-arm PyDESeq2 count model tests 14,312 genes at 20 µM and 14,312 at 200 µM against the same three DMSO controls. BH-adjusted p < 0.05 occurs for 0 and 139 genes, respectively; 0 and 40 also have absolute log2 fold change at least one. **Limitation:** The two dose contrasts share controls. These are within-study model estimates, not two independent replications or a pathway test. ([1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511))

**Claim R04 (observed):** Prespecified cholesterol marker HMGCR: HMGCR log2 fold change -0.119, BH-adjusted p 1 at 20 µM; HMGCR log2 fold change +1.543, BH-adjusted p 1.74e-07 at 200 µM. **Limitation:** HMGCR transcript abundance is not cholesterol synthesis flux, enzyme activity, or direct β-caryophyllene binding. ([1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [4](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/))

**Claim R05 (observed):** Prespecified signaling marker PGF: PGF log2 fold change -0.905, BH-adjusted p 1 at 20 µM; PGF log2 fold change -0.525, BH-adjusted p unavailable at 200 µM. **Limitation:** Dose, time, oxygen, vehicle, and cell identity differ from HepG2; these estimates alone cannot isolate a cell-context interaction. ([1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [5](https://github.com/Terpedia/terpedia-hepg2-bcp-rsem/blob/f0e0a56ae1b510fa622a11e218fe6b3b8d2f8d54/research/hepg2-bcp-raw-counts/generated/white-paper.md))

## Next research steps

**Proposed:** Follow the separately executed HepG2–UFH-001 cross-context comparison with a matched factorial experiment using shared vehicle, oxygen, dose, time, viability controls, biological replicates, and HMGCR or PGF perturbations. (claim R07; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [5](https://github.com/Terpedia/terpedia-hepg2-bcp-rsem/blob/f0e0a56ae1b510fa622a11e218fe6b3b8d2f8d54/research/hepg2-bcp-raw-counts/generated/white-paper.md), [4](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/))

## Data and code availability

The source specification is `research/ufh001-bcp-fpkm/raw-count-report-spec.json` (SHA-256 `c45a7acc84c6e6a7b01b84c90fa54b23f752186ac3b6725da1c9f16632f64e74`). The claim ledger and generation receipt accompany this report. File hashes identify the report files and cited result artifacts. External data inputs require their own pinned URLs and checksums. The [notebook execution receipt](../../execution-receipts/terputer-ufh001-bcp-raw-counts.json) matches the saved notebook and records hashes for result files written during its fresh-kernel run. It also pins 8 declared local input files by SHA-256. It records the Python version and installed package versions. Notebook execution does not independently validate scientific interpretation.

## References

[1] GEO GSE125511 series and samples. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511
[2] GEO GSE123856 reused control source. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123856
[3] GENCODE human release 48. https://www.gencodegenes.org/human/release_48.html
[4] Original UFH-001 β-caryophyllene study. https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/
[5] HepG2 raw-count white paper. https://github.com/Terpedia/terpedia-hepg2-bcp-rsem/blob/f0e0a56ae1b510fa622a11e218fe6b3b8d2f8d54/research/hepg2-bcp-raw-counts/generated/white-paper.md
