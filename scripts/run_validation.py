import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, "-m", "pytest", "python/tests", "-q"], cwd=root, check=True)
