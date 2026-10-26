"""Download nine GSE125511 SRA objects and verify NCBI Data Locator MD5s."""

import argparse
import csv
import hashlib
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


PROJECT = Path(__file__).resolve().parent
DATA = PROJECT / "data" / "raw"


def md5_file(path):
    digest = hashlib.md5()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(row):
    accession = row["run_accession"]
    url = row["sra_url"]
    if not accession.startswith("SRR") or not accession[3:].isdigit() or url != f"https://sra-pub-run-odp.s3.amazonaws.com/sra/{accession}/{accession}":
        raise ValueError(f"Unexpected SRA accession or URL: {accession}")
    output = DATA / "sra" / f"{accession}.sra"
    expected_size = int(row["sra_bytes"])
    expected_md5 = row["sra_md5"]
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.stat().st_size == expected_size and md5_file(output) == expected_md5:
        print(f"Verified existing {accession}", flush=True)
        return
    if output.exists() and output.stat().st_size >= expected_size:
        raise ValueError(f"SRA archive has wrong size or checksum: {output}")
    subprocess.run(["curl", "-fsSL", "--retry", "3", "-C", "-", "-o", str(output), url], check=True)
    if output.stat().st_size != expected_size or md5_file(output) != expected_md5:
        raise ValueError(f"SRA archive does not match the NCBI Data Locator record: {output}")
    print(f"Verified {accession}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.workers <= 6:
        parser.error("--workers must be between 1 and 6")
    with (PROJECT / "sra_run_manifest.tsv").open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != 9 or len({row["run_accession"] for row in rows}) != 9:
        raise ValueError("Expected nine distinct SRA runs")
    reused = [row for row in rows if row["control_duplicate_of"]]
    if len(reused) != 3 or any(not row["control_duplicate_of"].startswith("GSM") or "DMSO" not in row["matrix_column"] for row in reused):
        raise ValueError("Expected three DMSO controls reused from GSE123856")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(fetch, rows))


if __name__ == "__main__":
    main()
