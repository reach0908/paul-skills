from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=0)
args = parser.parse_args()
handler = partial(SimpleHTTPRequestHandler, directory=str(Path(__file__).resolve().parent))
server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
print('Fixture URL: http://127.0.0.1:%s/' % server.server_port, flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
