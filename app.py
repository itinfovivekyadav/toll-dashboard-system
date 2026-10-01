import os
import subprocess
import sys

PORT = os.environ.get("PORT", "8080")

env = os.environ.copy()
env["PORT"] = PORT

print("Starting Toll Dashboard...")
print("PORT =", PORT)

subprocess.run(
    [sys.executable, "Toll_Dashboard_Code.py"],
    env=env,
    check=True
)
