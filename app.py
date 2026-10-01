import os
import runpy

# Render/Gunicorn compatibility entry point
# Existing dashboard server is in Toll_Dashboard_Code.py
if __name__ == "__main__":
    runpy.run_path("Toll_Dashboard_Code.py", run_name="__main__")
