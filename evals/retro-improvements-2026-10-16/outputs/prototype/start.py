"""Local comparison only: python3 start.py"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
print("Fieldnotes prototype: http://127.0.0.1:8769/?variant=A", flush=True)
ThreadingHTTPServer(("127.0.0.1", 8769), SimpleHTTPRequestHandler).serve_forever()
