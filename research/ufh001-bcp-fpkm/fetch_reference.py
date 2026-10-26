"""Fetch the checksum-pinned GENCODE v48 GRCh38 primary assembly reference."""

import hashlib
import subprocess

from fetch_sra_inputs import DATA, PROJECT


REFERENCE = {
    "GRCh38.primary_assembly.genome.fa.gz": (
        "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_48/GRCh38.primary_assembly.genome.fa.gz",
        845635028,
        "42e38e8dd5027dd2ae8aeb8f3a990d07",
    ),
    "gencode.v48.primary_assembly.annotation.gtf.gz": (
        "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_48/gencode.v48.primary_assembly.annotation.gtf.gz",
        59094311,
        "1b68ecb47fd4cc3946819fec58a59d8f",
    ),
}


def md5_file(path):
    digest = hashlib.md5()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    destination = DATA / "reference"
    destination.mkdir(parents=True, exist_ok=True)
    for name, (url, expected_size, expected_md5) in REFERENCE.items():
        output = destination / name
        if output.exists() and output.stat().st_size == expected_size and md5_file(output) == expected_md5:
            print(f"Verified existing {output}", flush=True)
            continue
        if output.exists() and output.stat().st_size >= expected_size:
            raise ValueError(f"Reference has wrong size or MD5: {output}")
        subprocess.run(["curl", "-fsSL", "--retry", "3", "-C", "-", "-o", str(output), url], check=True)
        if output.stat().st_size != expected_size or md5_file(output) != expected_md5:
            raise ValueError(f"Reference differs from the GENCODE release 48 MD5SUMS record: {output}")
        print(f"Verified {output}", flush=True)


if __name__ == "__main__":
    main()
