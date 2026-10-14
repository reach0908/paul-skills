#!/usr/bin/env python3
"""Recollect final-source receipts without starting any model process."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import collect

collect.HERE = HERE
collect.RAW = collect.RAW / 'recovery'
collect.OUT = HERE / 'evidence'
collect.CASES = json.loads((HERE / 'cases.json').read_text())['cases']
collect.main()
