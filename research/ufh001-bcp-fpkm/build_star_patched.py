"""Build pinned STAR 2.7.11b with the upstream outQuant initialization fix.

The uninitialized flag can make GeneCounts open /geneInfo.tab on Apple Silicon.
See https://github.com/alexdobin/STAR/issues/1953 .
"""

import hashlib
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

from fetch_reference import DATA


ARCHIVE_URL = "https://github.com/alexdobin/STAR/archive/refs/tags/2.7.11b.tar.gz"
ARCHIVE_SHA256 = "3f65305e4112bd154c7e22b333dcdaafc681f4a895048fa30fa7ae56cac408e7"
TARGET = DATA / "tools" / "STAR-2.7.11b-patched"
PATCHES = {
    "ParametersGenome.cpp": (
        "transform.outYes = transform.outSAM = transform.outSJ = false;",
        "transform.outYes = transform.outSAM = transform.outSJ = transform.outQuant = false;",
    ),
    "ParametersGenome.h": (
        "bool outYes, outSAM, outSJ, outQuant;",
        "bool outYes=false, outSAM=false, outSJ=false, outQuant=false;",
    ),
}


def main():
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="star-build-", dir=DATA) as temporary:
        root = Path(temporary)
        archive = root / "STAR-2.7.11b.tar.gz"
        subprocess.run(["curl", "-fL", "--retry", "3", "-o", str(archive), ARCHIVE_URL], check=True)
        if hashlib.sha256(archive.read_bytes()).hexdigest() != ARCHIVE_SHA256:
            raise ValueError("STAR source archive SHA256 does not match pinned release")
        subprocess.run(["tar", "-xzf", str(archive), "-C", str(root)], check=True)
        source = root / "STAR-2.7.11b" / "source"
        for name, (old, new) in PATCHES.items():
            path = source / name
            text = path.read_text()
            if text.count(old) != 1:
                raise ValueError(f"STAR source patch context changed: {name}")
            path.write_text(text.replace(old, new))
        if platform.system() == "Darwin":
            command = ["make", "-C", str(source), "-j4", "STARforMacStatic",
                       "CXX=g++-15", "CXXFLAGS_SIMD=",
                       "LDFLAGS_Mac_static=-pthread -lz htslib/libhts.a", "BUILD_DATE=2026-10-26"]
        elif platform.system() == "Linux":
            command = ["make", "-C", str(source), "-j4", "STAR", "CXXFLAGS_SIMD="]
        else:
            raise ValueError(f"Unsupported build platform: {platform.system()}")
        with (TARGET.parent / "star_build.log").open("w") as log:
            subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
        binary = source / "STAR"
        if subprocess.check_output([str(binary), "--version"], text=True).strip() != "2.7.11b":
            raise ValueError("Patched STAR binary has the wrong version")
        shutil.copy2(binary, TARGET)
        TARGET.chmod(0o755)
        print(f"Built {TARGET}; SHA256={hashlib.sha256(TARGET.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
