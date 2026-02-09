import subprocess
import sys

def ingest_daily():
    subprocess.run(
        [sys.executable, "ingestions/ingest_daily.py"],
        check=False
    )

def ingest_wishlist():
    subprocess.run(
        [sys.executable, "ingestions/ingest_wishlist.py"],
        check=False
    )