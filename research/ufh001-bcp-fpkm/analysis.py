"""Descriptive audit of GSE125511 UFH-001 β-caryophyllene processed FPKM."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import csv
import gzip
import hashlib
import json
import math
import statistics

ROOT = Path('research/ufh001-bcp-fpkm')
MATRIX = ROOT / 'data/GSE125511_FPKM_geneMatrix_NORMALIZED.txt.gz'
HGNC = ROOT / 'data/hgnc_complete_set.txt'
MAP = ROOT / 'hgnc_crosswalk.tsv'
MANIFEST = ROOT / 'sample_manifest.tsv'
RESULTS = ROOT / 'results'
RESULTS.mkdir(parents=True, exist_ok=True)
EXPECTED = {
    MATRIX: '662960a32245e6b64b20879215e42d340ba19a5c6c16a0b79fbef0ef6c88d415',
    HGNC: '12363916be36f8f6f91879b0faade4eeaac973722de7136ec61329b77f2c2f91',
    MAP: 'd38e83b643c29cbb2ff7b20dc6aa8d57702f885ed8b8fcd3ae4af6d6369b998b',
    MANIFEST: 'd2016d14b9534124fe2fd387a1b8e391b4b2660b3b27e06c2145778a6ef17b9b',
}
for path, expected in EXPECTED.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path
with MANIFEST.open(newline='') as stream:
    samples = list(csv.DictReader(stream, delimiter='\t'))
columns = [s['matrix_column'] for s in samples]
assert len(samples) == 9 and [s['arm'] for s in samples] == ['vehicle', 'bcp20', 'bcp200'] * 3
assert all(s['time'] == '16 h' and s['oxygen'] == '1% O2' for s in samples)
assert [s['duplicate_of'] for s in samples if s['arm'] == 'vehicle'] == ['GSM3514416', 'GSM3514418', 'GSM3514420']
arm_indices = {arm: [i for i, s in enumerate(samples) if s['arm'] == arm] for arm in ('vehicle', 'bcp20', 'bcp200')}
with MAP.open(newline='') as stream:
    crosswalk = {r['ensembl_gene_id']: (r['entrez_id'], r['symbol'], r['hgnc_id']) for r in csv.DictReader(stream, delimiter='\t')}
assert len(crosswalk) == 41850
with HGNC.open(newline='') as stream:
    approved = [r for r in csv.DictReader(stream, delimiter='\t') if r['status'] == 'Approved' and r['entrez_id'] and r['ensembl_gene_id']]
entrez_frequency = Counter(r['entrez_id'] for r in approved)
ensembl_frequency = Counter(r['ensembl_gene_id'] for r in approved)
derived_crosswalk = {
    r['ensembl_gene_id']: (r['entrez_id'], r['symbol'], r['hgnc_id'])
    for r in approved
    if entrez_frequency[r['entrez_id']] == 1 and ensembl_frequency[r['ensembl_gene_id']] == 1
}
assert crosswalk == derived_crosswalk, 'Committed crosswalk differs from the pinned HGNC source'
rows = []
with gzip.open(MATRIX, 'rt', newline='') as stream:
    reader = csv.DictReader(stream, delimiter='\t')
    assert reader.fieldnames == ['tracking_id', *columns]
    for row in reader:
        gene = row['tracking_id']
        values = [float(row[c]) for c in columns]
        assert all(math.isfinite(v) and v >= 0 for v in values)
        rows.append((gene, values))
assert len(rows) == 60603 and len({gene for gene, _ in rows}) == len(rows)

with (RESULTS / 'sample_qc.tsv').open('w', newline='') as stream:
    writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
    writer.writerow(['matrix_column', 'geo_accession', 'arm', 'dose', 'duplicate_of', 'median_fpkm', 'nonzero_features'])
    for i, sample in enumerate(samples):
        writer.writerow([columns[i], sample['geo_accession'], sample['arm'], sample['dose'], sample['duplicate_of'], f'{statistics.median(values[i] for _, values in rows):.6f}', sum(values[i] > 0 for _, values in rows)])

log_rows = [[math.log1p(v) for v in values] for _, values in rows]
correlations = []
for i, j in combinations(range(9), 2):
    arm_a, arm_b = samples[i]['arm'], samples[j]['arm']
    group = f'{arm_a}:{arm_b}' if arm_a <= arm_b else f'{arm_b}:{arm_a}'
    corr = statistics.correlation([v[i] for v in log_rows], [v[j] for v in log_rows])
    correlations.append((columns[i], columns[j], group, corr))
with (RESULTS / 'sample_correlations.tsv').open('w', newline='') as stream:
    writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
    writer.writerow(['sample_a', 'sample_b', 'arm_pair', 'pearson_log1p_fpkm'])
    for a, b, group, value in correlations:
        writer.writerow([a, b, group, f'{value:.8f}'])

# Predeclared source-paper lipid markers and HepG2 paper markers, independent of observed directions.
markers = ['HMGCR', 'SCD', 'SQLE', 'FDFT1', 'HMGCS1', 'LDLR', 'INSIG1', 'STARD4', 'SREBF2', 'PGF', 'NR4A1', 'CSF1R', 'ARTN', 'CACNA1E']
effects = []
for gene, values in rows:
    means = {arm: statistics.mean(values[i] for i in indices) for arm, indices in arm_indices.items()}
    included = max(means.values()) >= 1
    ratios = {f'{arm}_{pc}': math.log2((means[arm] + pc) / (means['vehicle'] + pc)) for arm in ('bcp20', 'bcp200') for pc in (0.1, 1.0)}
    mapped = crosswalk.get(gene, ('', '', ''))
    effects.append((gene, *mapped, *[means[arm] for arm in ('vehicle', 'bcp20', 'bcp200')], included, *[ratios[f'{arm}_{pc}'] for arm in ('bcp20', 'bcp200') for pc in (0.1, 1.0)]))
with (RESULTS / 'descriptive_effects.tsv').open('w', newline='') as stream:
    writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
    writer.writerow(['ensembl_gene_id', 'entrez_id', 'symbol', 'hgnc_id', 'mean_vehicle_fpkm', 'mean_bcp20_fpkm', 'mean_bcp200_fpkm', 'included_max_arm_mean_fpkm_ge_1', 'bcp20_log2_ratio_pc_0_1', 'bcp20_log2_ratio_pc_1', 'bcp200_log2_ratio_pc_0_1', 'bcp200_log2_ratio_pc_1'])
    for gene, entrez, symbol, hgnc, vehicle, low, high, included, low01, low1, high01, high1 in effects:
        writer.writerow([gene, entrez, symbol, hgnc, *[f'{v:.6f}' for v in (vehicle, low, high)], included, *[f'{v:.6f}' for v in (low01, low1, high01, high1)]])
marker_rows = [r for r in effects if r[2] in markers]
with (RESULTS / 'marker_effects.tsv').open('w', newline='') as stream:
    writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
    writer.writerow(['ensembl_gene_id', 'entrez_id', 'symbol', 'mean_vehicle_fpkm', 'mean_bcp20_fpkm', 'mean_bcp200_fpkm', 'bcp20_log2_ratio_pc_0_1', 'bcp200_log2_ratio_pc_0_1'])
    for gene, entrez, symbol, _, vehicle, low, high, _, low01, _, high01, _ in marker_rows:
        writer.writerow([gene, entrez, symbol, *[f'{v:.6f}' for v in (vehicle, low, high, low01, high01)]])

selected = [r for r in effects if r[7]]
summary = {
    'source_accession': 'GSE125511', 'assay': 'bulk RNA-seq normalized FPKM',
    'matrix_sha256': EXPECTED[MATRIX], 'hgnc_source_sha256': EXPECTED[HGNC], 'hgnc_crosswalk_sha256': EXPECTED[MAP],
    'matrix_feature_rows': len(rows), 'sample_count': len(samples),
    'approved_one_to_one_hgnc_crosswalk_rows': len(crosswalk),
    'matrix_rows_with_one_to_one_hgnc_map': sum(gene in crosswalk for gene, _ in rows),
    'included_feature_rows_max_arm_mean_fpkm_ge_1': len(selected),
    'median_log1p_fpkm_correlation_by_arm_pair': {g: statistics.median(v for _, _, group, v in correlations if group == g) for g in sorted({x[2] for x in correlations})},
    'twofold_descriptive_counts': {arm: {str(pc): {'higher': sum(r[8 if arm == 'bcp20' else 10] >= 1 for r in selected) if pc == 0.1 else sum(r[9 if arm == 'bcp20' else 11] >= 1 for r in selected), 'lower': sum(r[8 if arm == 'bcp20' else 10] <= -1 for r in selected) if pc == 0.1 else sum(r[9 if arm == 'bcp20' else 11] <= -1 for r in selected)} for pc in (0.1, 1.0)} for arm in ('bcp20', 'bcp200')},
    'marker_rows': {symbol: [{'ensembl_gene_id': r[0], 'entrez_id': r[1], 'mean_vehicle_fpkm': r[4], 'mean_bcp20_fpkm': r[5], 'mean_bcp200_fpkm': r[6], 'bcp20_log2_ratio_0_1': r[8], 'bcp200_log2_ratio_0_1': r[10]} for r in marker_rows if r[2] == symbol] for symbol in markers},
    'limitations': ['Processed FPKM, no new differential expression or adjusted p-values', 'All libraries are UFH-001 under 1% oxygen for 16 h', 'Vehicle controls are identical to three GSE123856 libraries and must not be counted twice', 'Shared control makes dose contrasts correlated', 'Different cell line, oxygen, dose, time, and vehicle than GSE276099'],
}
(RESULTS / 'analysis_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k not in ('marker_rows', 'median_log1p_fpkm_correlation_by_arm_pair')}, indent=2))
