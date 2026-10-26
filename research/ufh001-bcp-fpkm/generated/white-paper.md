# β-Caryophyllene in hypoxic UFH-001: an executed FPKM dose audit

> Generated evidence brief. Each statement is linked to a claim record; scientific interpretation still requires review.

**Research question:** Which metabolic and signaling responses to terpene exposure are reproducible, and which depend on cellular context or a specific target?

**Notebook:** `notebooks/terputer-ufh001-bcp-fpkm.ipynb` · SHA-256 `74f363843bac5e6637515eeb4bfc1569762bd95ed293c49e2eab4a251a3a124b` · 1 executed code cells

## Abstract

**Source-reported:** GSE125511 contains three DMSO vehicle, three 20 µM β-caryophyllene, and three 200 µM β-caryophyllene UFH-001 bulk RNA-seq libraries, all under 1% oxygen for 16 hours. (claim C01; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511))

**Observed in notebook:** The pinned matrix contains 60,603 unique feature rows and nine complete nonnegative FPKM columns. A pinned one-to-one approved HGNC crosswalk maps 40,641 rows; 14,055 mapped rows have mean FPKM at least 1 in an arm. (claim C03; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [4](https://www.genenames.org/download/))

**Observed in notebook:** At 200 µM, mean HMGCR FPKM is 163.36 versus 56.71 in vehicle (descriptive log2 ratio +1.525 with a 0.1 pseudocount); SCD, SQLE, FDFT1, HMGCS1, INSIG1, and STARD4 also show higher mean FPKM. These markers have little mean change at 20 µM. (claim C06; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [4](https://www.genenames.org/download/))

## Background

**Source-reported:** GSE125511 contains three DMSO vehicle, three 20 µM β-caryophyllene, and three 200 µM β-caryophyllene UFH-001 bulk RNA-seq libraries, all under 1% oxygen for 16 hours. (claim C01; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511))

**Source-reported:** The three vehicle libraries are the same libraries deposited as GSM3514416, GSM3514418, and GSM3514420 in GSE123856. (claim C02; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [2](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123856))

**Source-reported:** The source article reports a cholesterol-biosynthesis response and increased β-caryophyllene sensitivity when HMGCR is blocked. (claim C07; [5](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/))

## Methods

**Observed in notebook:** The pinned matrix contains 60,603 unique feature rows and nine complete nonnegative FPKM columns. A pinned one-to-one approved HGNC crosswalk maps 40,641 rows; 14,055 mapped rows have mean FPKM at least 1 in an arm. (claim C03; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [4](https://www.genenames.org/download/)) Artifacts: [research/ufh001-bcp-fpkm/results/analysis_summary.json](../results/analysis_summary.json), [research/ufh001-bcp-fpkm/results/sample_qc.tsv](../results/sample_qc.tsv).

**Observed in notebook:** Median pairwise Pearson correlations of log1p(FPKM) are 0.9855 within vehicle, 0.9863 within 20 µM, and 0.9866 within 200 µM libraries. (claim C04; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz)) Artifacts: [research/ufh001-bcp-fpkm/results/sample_correlations.tsv](../results/sample_correlations.tsv), [research/ufh001-bcp-fpkm/results/analysis_summary.json](../results/analysis_summary.json).

**Observed in notebook:** Among the 14,055 filtered mapped rows, descriptive mean-FPKM ratios with a 0.1 pseudocount place 250 higher and 226 lower by at least twofold at 20 µM, versus 364 higher and 263 lower at 200 µM. With a 1.0 pseudocount the respective counts are 188/184 and 259/194. (claim C05; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [4](https://www.genenames.org/download/)) Artifacts: [research/ufh001-bcp-fpkm/results/descriptive_effects.tsv](../results/descriptive_effects.tsv), [research/ufh001-bcp-fpkm/results/analysis_summary.json](../results/analysis_summary.json).

## Results

**Observed in notebook:** Median pairwise Pearson correlations of log1p(FPKM) are 0.9855 within vehicle, 0.9863 within 20 µM, and 0.9866 within 200 µM libraries. (claim C04; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz)) Artifacts: [research/ufh001-bcp-fpkm/results/sample_correlations.tsv](../results/sample_correlations.tsv), [research/ufh001-bcp-fpkm/results/analysis_summary.json](../results/analysis_summary.json). **Limitation:** Similar global profiles do not establish treatment equivalence or support a differential-expression claim.

**Observed in notebook:** Among the 14,055 filtered mapped rows, descriptive mean-FPKM ratios with a 0.1 pseudocount place 250 higher and 226 lower by at least twofold at 20 µM, versus 364 higher and 263 lower at 200 µM. With a 1.0 pseudocount the respective counts are 188/184 and 259/194. (claim C05; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [4](https://www.genenames.org/download/)) Artifacts: [research/ufh001-bcp-fpkm/results/descriptive_effects.tsv](../results/descriptive_effects.tsv), [research/ufh001-bcp-fpkm/results/analysis_summary.json](../results/analysis_summary.json). **Limitation:** These threshold counts are pseudocount-sensitive descriptions, not statistically tested DEGs. Both contrasts share the same three controls.

**Observed in notebook:** At 200 µM, mean HMGCR FPKM is 163.36 versus 56.71 in vehicle (descriptive log2 ratio +1.525 with a 0.1 pseudocount); SCD, SQLE, FDFT1, HMGCS1, INSIG1, and STARD4 also show higher mean FPKM. These markers have little mean change at 20 µM. (claim C06; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [4](https://www.genenames.org/download/)) Artifacts: [research/ufh001-bcp-fpkm/results/marker_effects.tsv](../results/marker_effects.tsv), [research/ufh001-bcp-fpkm/results/analysis_summary.json](../results/analysis_summary.json). **Limitation:** Marker directions alone do not establish pathway significance, flux, cholesterol synthesis, or direct HMGCR binding.

**Observed in notebook:** PGF mean FPKM is 0.483 in vehicle and 0.333 at 200 µM, below the predeclared FPKM filter; its 0.1-pseudocount log2 ratio is -0.429. (claim C08; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [6](https://github.com/Terpedia/terpedia-hepg2-bcp-rsem)) Artifacts: [research/ufh001-bcp-fpkm/results/marker_effects.tsv](../results/marker_effects.tsv). **Limitation:** Low expression and differing cell context, oxygen, dose, time, vehicle, and quantification prevent a PGF replication claim across GSE125511 and GSE276099.

## Interpretation

**Observed in notebook:** At 200 µM, mean HMGCR FPKM is 163.36 versus 56.71 in vehicle (descriptive log2 ratio +1.525 with a 0.1 pseudocount); SCD, SQLE, FDFT1, HMGCS1, INSIG1, and STARD4 also show higher mean FPKM. These markers have little mean change at 20 µM. (claim C06; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [4](https://www.genenames.org/download/)) Artifacts: [research/ufh001-bcp-fpkm/results/marker_effects.tsv](../results/marker_effects.tsv), [research/ufh001-bcp-fpkm/results/analysis_summary.json](../results/analysis_summary.json). **Limitation:** Marker directions alone do not establish pathway significance, flux, cholesterol synthesis, or direct HMGCR binding.

**Source-reported:** The source article reports a cholesterol-biosynthesis response and increased β-caryophyllene sensitivity when HMGCR is blocked. (claim C07; [5](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/)) **Limitation:** The notebook does not reproduce the intervention experiment, and the reported interaction does not prove direct ligand binding to HMGCR.

**Observed in notebook:** PGF mean FPKM is 0.483 in vehicle and 0.333 at 200 µM, below the predeclared FPKM filter; its 0.1-pseudocount log2 ratio is -0.429. (claim C08; [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [6](https://github.com/Terpedia/terpedia-hepg2-bcp-rsem)) Artifacts: [research/ufh001-bcp-fpkm/results/marker_effects.tsv](../results/marker_effects.tsv). **Limitation:** Low expression and differing cell context, oxygen, dose, time, vehicle, and quantification prevent a PGF replication claim across GSE125511 and GSE276099.

## Limitations

**Claim C02 (source-reported):** The three vehicle libraries are the same libraries deposited as GSM3514416, GSM3514418, and GSM3514420 in GSE123856. **Limitation:** These controls must not be counted as an independent cohort in a synthesis. ([1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [2](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123856))

**Claim C03 (observed):** The pinned matrix contains 60,603 unique feature rows and nine complete nonnegative FPKM columns. A pinned one-to-one approved HGNC crosswalk maps 40,641 rows; 14,055 mapped rows have mean FPKM at least 1 in an arm. **Limitation:** Mapping coverage depends on the pinned 2026 HGNC snapshot. FPKM is processed abundance, not raw integer counts. ([3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [4](https://www.genenames.org/download/))

**Claim C05 (observed):** Among the 14,055 filtered mapped rows, descriptive mean-FPKM ratios with a 0.1 pseudocount place 250 higher and 226 lower by at least twofold at 20 µM, versus 364 higher and 263 lower at 200 µM. With a 1.0 pseudocount the respective counts are 188/184 and 259/194. **Limitation:** These threshold counts are pseudocount-sensitive descriptions, not statistically tested DEGs. Both contrasts share the same three controls. ([3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [4](https://www.genenames.org/download/))

**Claim C08 (observed):** PGF mean FPKM is 0.483 in vehicle and 0.333 at 200 µM, below the predeclared FPKM filter; its 0.1-pseudocount log2 ratio is -0.429. **Limitation:** Low expression and differing cell context, oxygen, dose, time, vehicle, and quantification prevent a PGF replication claim across GSE125511 and GSE276099. ([3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz), [6](https://github.com/Terpedia/terpedia-hepg2-bcp-rsem))

## Next research steps

**Proposed:** Reprocess raw libraries with a pinned reference and replicate-aware count model, then compare cholesterol and signaling effects with the processed-matrix directions. (claim C09; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [3](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz))

**Proposed:** Cross UFH-001 and HepG2 cells with matched β-caryophyllene doses, oxygen conditions, vehicle, exposure time, and HMGCR or PGF perturbations to estimate context and target interactions. (claim C10; [1](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511), [6](https://github.com/Terpedia/terpedia-hepg2-bcp-rsem), [5](https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/))

## Data and code availability

The source specification is `research/ufh001-bcp-fpkm/report-spec.json` (SHA-256 `ebb347d5836363fd73149ee700bd184fe626e5f46c3cb0c4bef4658be1b02aa9`). The claim ledger and generation receipt accompany this report. File hashes identify the report files and cited result artifacts. 2 externally sourced input files have a source URL and hash listed below. The [notebook execution receipt](../../execution-receipts/terputer-ufh001-bcp-fpkm.json) matches the saved notebook and records hashes for result files written during its fresh-kernel run. It also pins 5 declared local input files by SHA-256. It records the Python version and installed package versions. Notebook execution does not independently validate scientific interpretation.

### External data files

The following download locations and file hashes match inputs pinned by the notebook execution receipt. The generator does not download these files or verify that the URLs remain live.

| Input | Download | SHA-256 |
| --- | --- | --- |
| `research/ufh001-bcp-fpkm/data/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz` | [Source file](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz) | `662960a32245e6b64b20879215e42d340ba19a5c6c16a0b79fbef0ef6c88d415` |
| `research/ufh001-bcp-fpkm/data/hgnc_complete_set.txt` | [Source file](https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt) | `12363916be36f8f6f91879b0faade4eeaac973722de7136ec61329b77f2c2f91` |

## References

[1] GEO GSE125511 series and nine samples. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125511
[2] GEO GSE123856 control source. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123856
[3] GSE125511 supplementary FPKM matrix. https://ftp.ncbi.nlm.nih.gov/geo/series/GSE125nnn/GSE125511/suppl/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz
[4] HGNC complete approved gene set. https://www.genenames.org/download/
[5] Original UFH-001 β-caryophyllene breast-cancer study. https://pmc.ncbi.nlm.nih.gov/articles/PMC8561761/
[6] Independent HepG2 processed-count audit. https://github.com/Terpedia/terpedia-hepg2-bcp-rsem
