"""Reprocess nine GSE125511 single-end FASTQs into STAR integer gene counts.

Run fetch_reference.py, fetch_sra_inputs.py, and
convert_sra_to_fastq.py first. Large reference, index, reads, and logs remain
under ignored data/raw; count and mapping-QC tables are written to results.
"""

import csv
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from fetch_reference import DATA, PROJECT, REFERENCE, md5_file
from convert_sra_to_fastq import sha256_file


RESULTS = PROJECT / "results" / "raw_counts"
REFERENCE_DIR = DATA / "reference"


def require_input(path, size, md5):
    if not path.is_file() or path.stat().st_size != size or md5_file(path) != md5:
        raise ValueError(f"Missing or checksum-mismatched input: {path}")


def uncompress(path):
    target = path.with_suffix("")
    if not target.is_file():
        temporary = target.with_name(target.name + ".partial")
        with gzip.open(path, "rb") as source, temporary.open("wb") as output:
            shutil.copyfileobj(source, output)
        temporary.replace(target)
    return target


def reference_files():
    paths = []
    for name, (_, size, md5) in REFERENCE.items():
        compressed = REFERENCE_DIR / name
        require_input(compressed, size, md5)
        paths.append(uncompress(compressed))
    return paths


def build_index(fasta, gtf, overhang):
    index = DATA / f"star_index_gencode_v48_overhang{overhang}"
    if (index / "genomeParameters.txt").is_file() and (index / "Genome").is_file():
        return index
    index.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix="star-index-", dir=index.parent))
    command = [
        "STAR", "--runMode", "genomeGenerate", "--runThreadN", "8",
        "--genomeDir", str(temporary), "--genomeFastaFiles", str(fasta),
        "--sjdbGTFfile", str(gtf), "--sjdbOverhang", str(overhang),
        "--genomeSAsparseD", "3", "--genomeSAindexNbases", "12",
        "--limitGenomeGenerateRAM", "18000000000",
    ]
    print("Building GENCODE v48 STAR index", flush=True)
    with (temporary / "command.stdout.log").open("w") as log:
        subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
    if not (temporary / "genomeParameters.txt").is_file() or not (temporary / "Genome").is_file():
        raise ValueError(f"STAR did not finish writing its index: {temporary}")
    temporary.rename(index)
    return index


def manifest():
    source_manifest = PROJECT / "sra_run_manifest.tsv"
    with source_manifest.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != 9 or len({row["run_accession"] for row in rows}) != 9:
        raise ValueError("Expected nine distinct runs")
    with (PROJECT / "sample_manifest.tsv").open(newline="") as stream:
        samples = list(csv.DictReader(stream, delimiter="\t"))
    sample_index = {row["matrix_column"]: row for row in samples}
    if len(samples) != 9 or len(sample_index) != 9 or any(
        row["matrix_column"] not in sample_index
        or row["geo_accession"] != sample_index[row["matrix_column"]]["geo_accession"]
        or row["control_duplicate_of"] != sample_index[row["matrix_column"]]["duplicate_of"]
        for row in rows
    ):
        raise ValueError("SRA runs do not match the nine sample annotations and reused controls")
    conversion_path = RESULTS / "conversion_receipt.json"
    conversion = json.loads(conversion_path.read_text())
    if (conversion.get("source_manifest_sha256") != sha256_file(source_manifest)
        or conversion.get("pipeline_sha256") != sha256_file(PROJECT / "convert_sra_to_fastq.py")
        or len(conversion.get("fastqs", [])) != len(rows)):
        raise ValueError("SRA conversion receipt does not match the current source files")
    converted = {entry["run_accession"]: entry for entry in conversion["fastqs"]}
    if set(converted) != {row["run_accession"] for row in rows}:
        raise ValueError("SRA conversion receipt does not cover exactly the nine runs")
    if any(
        converted[row["run_accession"]]["control_duplicate_of"] != row["control_duplicate_of"]
        or not isinstance(converted[row["run_accession"]]["read_length_max"], int)
        or not 20 <= converted[row["run_accession"]]["read_length_max"] <= 500
        for row in rows
    ):
        raise ValueError("Conversion receipt lacks valid read lengths or reused-control identity")
    return rows, converted


def align(row, converted, index):
    run = row["run_accession"]
    fastq = DATA / "fastq" / f"{run}.fastq.gz"
    if (not fastq.is_file() or fastq.stat().st_size != converted["fastq_bytes"]
        or sha256_file(fastq) != converted["fastq_sha256"]
        or converted["sra_md5"] != row["sra_md5"]
        or converted["read_count"] != int(row["expected_reads"])):
        raise ValueError(f"Converted FASTQ is missing or differs from its SRA receipt: {fastq}")
    run_dir = DATA / "star_counts" / run
    run_dir.mkdir(parents=True, exist_ok=True)
    counts = run_dir / "ReadsPerGene.out.tab"
    final_log = run_dir / "Log.final.out"
    if counts.is_file() and final_log.is_file():
        return counts, final_log
    command = [
        "STAR", "--genomeDir", str(index), "--runThreadN", "8",
        "--readFilesIn", str(fastq), "--readFilesCommand", "zcat",
        "--quantMode", "GeneCounts", "--outSAMtype", "None",
        "--outFileNamePrefix", str(run_dir) + "/",
    ]
    print(f"Aligning {run}", flush=True)
    with (run_dir / "command.stdout.log").open("w") as log:
        subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
    if not counts.is_file() or not final_log.is_file():
        raise ValueError(f"STAR count or QC output missing for {run}")
    return counts, final_log


def read_counts(path):
    counts = {}
    with path.open(newline="") as stream:
        for row in csv.reader(stream, delimiter="\t"):
            if len(row) != 4:
                raise ValueError(f"Unexpected STAR gene-count row in {path}: {row}")
            if row[0].startswith("N_"):
                continue
            if row[0] in counts:
                raise ValueError(f"Duplicate gene ID in {path}: {row[0]}")
            values = tuple(int(value) for value in row[1:])
            if any(value < 0 for value in values):
                raise ValueError(f"Negative gene count in {path}: {row[0]}")
            counts[row[0]] = values
    return counts


def read_log(path):
    values = {}
    with path.open() as stream:
        for line in stream:
            if "|" in line:
                key, value = line.split("|", 1)
                values[key.strip()] = value.strip()
    return values


def gene_annotation(gtf, genes):
    annotation = {}
    pattern = re.compile(r'(gene_id|gene_name|gene_type) "([^"]+)"')
    with gtf.open() as stream:
        for line in stream:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 9 or fields[2] != "gene":
                continue
            attributes = dict(pattern.findall(fields[8]))
            gene_id = attributes.get("gene_id")
            if gene_id in genes:
                annotation[gene_id] = (attributes.get("gene_name", ""), attributes.get("gene_type", ""))
    if set(annotation) != genes:
        raise ValueError(f"GENCODE annotation did not cover {len(genes - set(annotation))} counted genes")
    return annotation


def compress_result(name):
    source = RESULTS / name
    output = RESULTS / f"{name}.gz"
    temporary = output.with_name(output.name + ".partial")
    with source.open("rb") as raw, temporary.open("wb") as encoded:
        with gzip.GzipFile(filename="", mode="wb", fileobj=encoded, mtime=0, compresslevel=6) as compressed:
            shutil.copyfileobj(raw, compressed, length=1024 * 1024)
    temporary.replace(output)
    source.unlink()
    if output.stat().st_size > 2_000_000:
        raise ValueError(f"Compressed report input exceeds Terputer's per-file publication limit: {output}")
    return output


def main():
    version = subprocess.check_output(["STAR", "--version"], text=True).strip()
    if version != "2.7.11b":
        raise ValueError(f"Expected STAR 2.7.11b; found {version}")
    rows, converted = manifest()
    overhang = max(converted[row["run_accession"]]["read_length_max"] for row in rows) - 1
    fasta, gtf = reference_files()
    index = build_index(fasta, gtf, overhang)
    sample_counts = []
    qc = []
    for row in rows:
        counts_path, log_path = align(row, converted[row["run_accession"]], index)
        sample_counts.append(read_counts(counts_path))
        log = read_log(log_path)
        qc.append({
            "matrix_column": row["matrix_column"], "geo_accession": row["geo_accession"],
            "run_accession": row["run_accession"], "control_duplicate_of": row["control_duplicate_of"],
            "input_reads": log.get("Number of input reads"),
            "uniquely_mapped_reads": log.get("Uniquely mapped reads number"),
            "uniquely_mapped_percent": log.get("Uniquely mapped reads %"),
            "multi_mapped_percent": log.get("% of reads mapped to multiple loci"),
            "too_many_loci_percent": log.get("% of reads mapped to too many loci"),
            "unmapped_too_short_percent": log.get("% of reads unmapped: too short"),
        })
        if any(value is None for value in qc[-1].values()):
            raise ValueError(f"STAR mapping QC is incomplete for {row['run_accession']}")
    genes = set(sample_counts[0])
    if any(set(sample) != genes for sample in sample_counts[1:]):
        raise ValueError("STAR outputs have different gene sets")
    annotation = gene_annotation(gtf, genes)
    RESULTS.mkdir(parents=True, exist_ok=True)
    with (RESULTS / "gene_counts_unstranded.tsv").open("w", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t")
        writer.writerow(["gene_id", *(row["matrix_column"] for row in rows)])
        for gene in sorted(genes):
            writer.writerow([gene, *(sample[gene][0] for sample in sample_counts)])
    with (RESULTS / "star_mapping_qc.tsv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(qc[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(qc)
    with (RESULTS / "gene_annotation.tsv").open("w", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t")
        writer.writerow(["gene_id", "gene_name", "gene_type"])
        for gene in sorted(genes):
            writer.writerow([gene, *annotation[gene]])
    count_bundle = compress_result("gene_counts_unstranded.tsv")
    annotation_bundle = compress_result("gene_annotation.tsv")
    receipt = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "aligner": "STAR", "aligner_version": version,
        "pipeline_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "run_manifest_sha256": sha256_file(PROJECT / "sra_run_manifest.tsv"),
        "sample_manifest_sha256": sha256_file(PROJECT / "sample_manifest.tsv"),
        "conversion_receipt_sha256": sha256_file(RESULTS / "conversion_receipt.json"),
        "read_source": "NCBI SRA archives converted with fasterq-dump",
        "reference": "GENCODE human release 48 GRCh38 primary assembly",
        "reference_files": {name: {"source_md5": item[2], "bytes": item[1]} for name, item in REFERENCE.items()},
        "index_options": {"sjdbOverhang": overhang, "genomeSAsparseD": 3, "genomeSAindexNbases": 12},
        "mapping_options": {"quantMode": "GeneCounts", "outSAMtype": "None", "readFilesCommand": "zcat"},
        "run_accessions": [row["run_accession"] for row in rows],
        "reused_controls": {row["geo_accession"]: row["control_duplicate_of"] for row in rows if row["control_duplicate_of"]},
        "gene_count_column": "STAR ReadsPerGene.out.tab unstranded",
        "gene_count_rows": len(genes),
        "output_sha256": {},
        "limitations": "NCBI SRA and GENCODE MD5 checks establish downloaded-file identity but not biological replicate independence, dose accuracy, reference annotation correctness, or gene-level significance. The three DMSO controls are reused from GSE123856 and both BCP dose contrasts share them.",
    }
    for name in (count_bundle.name, "star_mapping_qc.tsv", annotation_bundle.name):
        receipt["output_sha256"][name] = hashlib.sha256((RESULTS / name).read_bytes()).hexdigest()
    (RESULTS / "processing_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"genes": len(genes), "results": str(RESULTS)}, indent=2))


if __name__ == "__main__":
    main()
