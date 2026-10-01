import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", "8080"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open("Toll_Dashboard_Code.py", "r", encoding="utf-8") as f:
                source = f.read()

            # Existing Python file contains the dashboard/server code.
            # Execute it only when this entry point is started directly.
            if self.path == "/" or self.path.startswith("/"):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()

                # Extract the HTML portion from the existing file.
                start = source.find("<!DOCTYPE html>")
                if start == -1:
                    start = source.find("<html")
                end = source.rfind("</html>")

                if start != -1 and end != -1:
                    html = source[start:end + 7]
                else:
                    html = "<h1>Toll Plaza Management System</h1><p>Dashboard is running.</p>"

                self.wfile.write(html.encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))

if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
