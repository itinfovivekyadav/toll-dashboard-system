import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", "8080"))

with open("Toll_Dashboard_Code.py", "r", encoding="utf-8-sig") as f:
    source = f.read()

start = source.find("<!DOCTYPE html>")
if start < 0:
    start = source.find("<html")

end = source.rfind("</html>")

if start >= 0 and end >= 0:
    HTML = source[start:end+7]
else:
    HTML = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Toll Plaza Management System</title></head>
<body><h1>Toll Plaza Management System</h1></body>
</html>"""

class Handler(BaseHTTPRequestHandler):

    def send_html(self):
        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=UTF-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.send_html()

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=UTF-8")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, *args):
        pass

print("Toll Dashboard running on port", PORT)
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
