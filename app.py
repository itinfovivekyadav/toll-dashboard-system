import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", "8080"))

with open("Toll_Dashboard_Code.py", "r", encoding="utf-8") as f:
    SOURCE = f.read()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            start = SOURCE.find("<!DOCTYPE html>")
            if start == -1:
                start = SOURCE.find("<html")

            end = SOURCE.rfind("</html>")

            if start >= 0 and end >= 0:
                html = SOURCE[start:end + 7]
            else:
                html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Toll Plaza Management System</title>
</head>
<body>
<h1>Toll Plaza Management System</h1>
<p>Dashboard is running.</p>
</body>
</html>"""

            data = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        except Exception as e:
            data = ("Server Error: " + str(e)).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    def log_message(self, format, *args):
        print(format % args)

print(f"Starting Toll Dashboard on 0.0.0.0:{PORT}")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
