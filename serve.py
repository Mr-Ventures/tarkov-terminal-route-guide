"""Local editing server: serves the site and lets the page save route.json.

Run:  python serve.py   then open http://127.0.0.1:8765/
Only route.json can be written, and only from this machine.
"""
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
ROUTE = os.path.join(ROOT, "route.json")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        if self.path.endswith((".m3u8", ".json", ".html", "/")):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_PUT(self):
        if self.path.split("?")[0] != "/route.json":
            return self.send_error(403)
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        try:
            data = json.loads(body)
            assert isinstance(data.get("chapters"), list)
        except Exception:
            return self.send_error(400, "Not a valid route.json")
        tmp = ROUTE + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, ROUTE)
        self.send_response(204)
        self.end_headers()


if __name__ == "__main__":
    print("Serving on http://127.0.0.1:8765/")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
