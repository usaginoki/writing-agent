"""Ephemeral review UI. One page, one submission, then the server exits.

  python3 server.py --job <job_dir> --data <page.json> [--port 0] [--no-open] [--timeout 3600]

The writer runs this in the background; the process exits when the user submits (or on timeout),
which notifies the agent. The submission is saved to <job>/feedback/<timestamp>-<name>.json and its
path is printed on the last stdout line as `FEEDBACK <path>`. On timeout it prints `TIMEOUT`.

page.json:
  {"name": "structure-review", "title": "...", "intro": "markdown-ish text",
   "sections": [ {"type": "questions"|"hunks"|"structure"|"meaning"|"variants", ...}, ... ]}
Section schemas are documented in templates/review.html (renderers) and the writing:ui skill.
Stdlib only.
"""

import argparse
import datetime as dt
import http.server
import json
import threading
import webbrowser
from pathlib import Path

TEMPLATE = Path(__file__).parent / "templates" / "review.html"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--timeout", type=int, default=3600)
    a = ap.parse_args()

    job = Path(a.job)
    data = json.loads(Path(a.data).read_text())
    page = TEMPLATE.read_text().replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
    done = threading.Event()
    result: dict = {}

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            self._send(200, page.encode(), "text/html; charset=utf-8")

        def do_POST(self):
            if self.path != "/submit":
                return self._send(404, b"not found", "text/plain")
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n) or b"{}")
            ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            out = job / "feedback" / f"{ts}-{data.get('name', 'review')}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({"page": data.get("name"), "submitted": ts, **payload},
                                      indent=1, ensure_ascii=False))
            result["path"] = str(out)
            self._send(200, b'{"ok": true}', "application/json")
            done.set()

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", a.port), H)
    url = f"http://127.0.0.1:{srv.server_address[1]}/"
    print(f"UI {url}", flush=True)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    if not a.no_open:
        webbrowser.open(url)
    finished = done.wait(a.timeout)
    srv.shutdown()
    print(f"FEEDBACK {result['path']}" if finished else "TIMEOUT", flush=True)


if __name__ == "__main__":
    main()
