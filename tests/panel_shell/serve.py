"""A stand-in for AstrBot's web panel, to try "她的脑子" in the panel without AstrBot.

    python tests/panel_shell/serve.py [port]      (prints the address; 127.0.0.1 only)

What it copies from AstrBot 4.29.3 (read in its source, dashboard/):
- the plugin page is served under /api/v1/plugins/<plugin>/views/<page>/_t/<token>/,
  only from that page's own folder (pages/dashboard/ here);
- every .html it serves gets a bridge script added before </body> (here shell/bridge.js,
  a small stand-in for AstrBot's plugin_page_bridge.js);
- every page answer carries X-Frame-Options SAMEORIGIN and
  Content-Security-Policy "frame-ancestors 'self'; object-src 'none'; base-uri 'self'";
- the shell page (/) puts the plugin page in an iframe sandboxed
  "allow-scripts allow-forms allow-downloads", and answers the bridge's reads with
  invented data (shell/host.js, from the brain map's own sample generator).

Nothing here is real: no QQ numbers, names or chats.
"""
import http.server
import mimetypes
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PAGE = ROOT / 'pages' / 'dashboard'
SAMPLE = ROOT / 'tools' / 'brain' / 'src' / 'page' / 'sample.js'
VIEW = '/api/v1/plugins/ams_life/views/dashboard/_t/made-up-token/'
HEADERS = {
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    'Cross-Origin-Resource-Policy': 'cross-origin',
    'Access-Control-Allow-Origin': '*',
    'X-Frame-Options': 'SAMEORIGIN',
    'Content-Security-Policy': "frame-ancestors 'self'; object-src 'none'; base-uri 'self'",
}
BRIDGE_TAG = b'<script src="/shell/bridge.js"></script>'
TYPES = {'.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json',
         '.md': 'text/plain', '.txt': 'text/plain', '.png': 'image/png', '.svg': 'image/svg+xml'}


def inside(path, root):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path.split('?', 1)[0]
        if url == '/':
            return self.send(HERE / 'shell.html', {})
        if url == '/shell/sample.js':
            return self.send(SAMPLE, {})
        if url.startswith('/shell/'):
            f = HERE / url[len('/shell/'):]
            return self.send(f, {}) if inside(f, HERE) else self.missing()
        if url.startswith(VIEW):
            rel = url[len(VIEW):] or 'index.html'
            f = PAGE / rel
            # like AstrBot: a page reads only its own folder
            return self.send(f, HEADERS, inject=f.suffix == '.html') if inside(f, PAGE) else self.missing()
        return self.missing()

    def send(self, f, headers, inject=False):
        if not f.is_file():
            return self.missing()
        body = f.read_bytes()
        if inject:
            body = body.replace(b'</body>', BRIDGE_TAG + b'</body>', 1) if b'</body>' in body else body + BRIDGE_TAG
        self.send_response(200)
        # fixed types first: Windows' registry can map .js to text/plain, which nosniff refuses
        kind = TYPES.get(f.suffix) or mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
        self.send_header('Content-Type', kind + ('; charset=utf-8' if kind.startswith(('text/', 'application/javascript')) else ''))
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def missing(self):
        self.send_response(404)
        self.end_headers()

    def log_message(self, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    server = http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print('http://127.0.0.1:%d/' % server.server_address[1], flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
