"""Convert nine MD5-verified GSE125511 SRA archives into gzip FASTQs."""

import csv
import gzip
import hashlib
import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from fetch_sra_inputs import DATA, PROJECT, md5_file


RESULTS = PROJECT / "results" / "raw_counts"


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    version = subprocess.check_output(["fasterq-dump", "--version"], text=True).strip()
    with (PROJECT / "sra_run_manifest.tsv").open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != 9 or len({row["run_accession"] for row in rows}) != 9:
        raise ValueError("Expected nine distinct SRA runs")
    if len([row for row in rows if row["control_duplicate_of"]]) != 3:
        raise ValueError("Expected three reused DMSO controls")
    results = []
    RESULTS.mkdir(parents=True, exist_ok=True)
    fastq_dir = DATA / "fastq"
    fastq_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        accession = row["run_accession"]
        archive = DATA / "sra" / f"{accession}.sra"
        if not archive.is_file() or archive.stat().st_size != int(row["sra_bytes"]) or md5_file(archive) != row["sra_md5"]:
            raise ValueError(f"SRA archive is missing or differs from its NCBI MD5: {archive}")
        output = fastq_dir / f"{accession}.fastq.gz"
        sidecar = RESULTS / f"{accession}-conversion.json"
        if output.exists():
            if not sidecar.is_file():
                raise ValueError(f"Existing FASTQ has no conversion receipt: {output}")
            existing = json.loads(sidecar.read_text())
            if (existing.get("matrix_column") != row["matrix_column"]
                or existing.get("geo_accession") != row["geo_accession"]
                or existing.get("run_accession") != accession
                or existing.get("control_duplicate_of") != row["control_duplicate_of"]
                or existing.get("sra_md5") != row["sra_md5"]
                or existing.get("read_count") != int(row["expected_reads"])
                or not isinstance(existing.get("read_length_min"), int)
                or not isinstance(existing.get("read_length_max"), int)
                or existing["read_length_min"] < 1
                or existing["read_length_max"] < existing["read_length_min"]
                or existing.get("fastq_bytes") != output.stat().st_size
                or existing.get("fastq_sha256") != sha256_file(output)):
                raise ValueError(f"Existing FASTQ differs from its conversion receipt: {output}")
            results.append(existing)
            print(f"Verified existing conversion {accession}", flush=True)
            continue
        with tempfile.TemporaryDirectory(prefix=f"{accession}-", dir=DATA) as temporary_name:
            temporary = Path(temporary_name)
            scratch = temporary / "scratch"
            scratch.mkdir()
            command = ["fasterq-dump", str(archive), "--split-3", "--threads", "8", "--outdir", str(temporary), "--temp", str(scratch)]
            print(f"Converting {accession}", flush=True)
            with (RESULTS / f"{accession}-fasterq.log").open("w") as log:
                subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
            raw = temporary / f"{accession}.fastq"
            if not raw.is_file():
                raise ValueError(f"fasterq-dump did not create a single-end FASTQ for {accession}")
            summary = subprocess.check_output([
                "awk",
                'NR%4==2 {n=length($0); if (min==0 || n<min) min=n; if (n>max) max=n} END {if (NR%4!=0) exit 2; printf "%.0f %d %d\\n", NR/4, min, max}',
                str(raw),
            ], text=True).split()
            read_count, read_length_min, read_length_max = map(int, summary)
            if read_count != int(row["expected_reads"]) or read_length_min < 1:
                raise ValueError(f"FASTQ record count or length differs from ENA run metadata for {accession}: {read_count}")
            partial = output.with_name(output.name + ".partial")
            with raw.open("rb") as source, partial.open("wb") as encoded:
                with gzip.GzipFile(filename="", mode="wb", fileobj=encoded, mtime=0, compresslevel=6) as compressed:
                    shutil.copyfileobj(source, compressed, length=1024 * 1024)
            partial.replace(output)
        converted = {
            "matrix_column": row["matrix_column"], "geo_accession": row["geo_accession"],
            "run_accession": accession, "sra_md5": row["sra_md5"],
            "control_duplicate_of": row["control_duplicate_of"],
            "fastq_bytes": output.stat().st_size, "fastq_sha256": sha256_file(output),
            "read_count": read_count, "read_length_min": read_length_min,
            "read_length_max": read_length_max,
        }
        sidecar.write_text(json.dumps(converted, indent=2) + "\n")
        results.append(converted)
    receipt = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "converter": "NCBI fasterq-dump", "converter_version": version,
        "source": "NCBI SRA Data Locator normalized SRA archives",
        "source_manifest_sha256": sha256_file(PROJECT / "sra_run_manifest.tsv"),
        "pipeline_sha256": sha256_file(Path(__file__)),
        "fastqs": results,
    }
    (RESULTS / "conversion_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Converted {len(results)} verified runs")


if __name__ == "__main__":
    main()
