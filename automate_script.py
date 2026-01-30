import subprocess
import json
import os
import argparse
import logging
from datetime import datetime

# ------------------------
# Load config
# ------------------------
CONFIG_PATH = "/home/asad/Documents/config.json"

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

PROJECT_DIR = config["project_dir"]
MAX_CHANGES = config["max_changes_per_run"]
LOG_FILE = config["log_file"]

# ------------------------
# Argument parsing (dry-run)
# ------------------------
parser = argparse.ArgumentParser(description="Secure Git Auto Commit Tool")
parser.add_argument("--dry-run", action="store_true", help="Show actions without executing them")
args = parser.parse_args()

DRY_RUN = args.dry_run

# ------------------------
# Logging setup
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# ------------------------
# Sensitive detection
# ------------------------
SENSITIVE_KEYWORDS = [
    "secret", "pass", "password", "token", "key",
    "credential", "creds", "private", "auth", "env"
]

SENSITIVE_EXTENSIONS = [".pem", ".key", ".env", ".p12", ".pfx"]

# ------------------------
def run_cmd(cmd):
    return subprocess.run(
        cmd,
        cwd=PROJECT_DIR,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def get_changes():
    result = run_cmd("git status --porcelain")
    changes = []

    for line in result.stdout.splitlines():
        status = line[:2].strip()
        filename = line[3:].strip()
        changes.append((status, filename))

    return changes

def is_sensitive(filename):
    name = os.path.basename(filename).lower()

    for word in SENSITIVE_KEYWORDS:
        if word in name:
            return True

    for ext in SENSITIVE_EXTENSIONS:
        if name.endswith(ext):
            return True

    return False

def commit_single_change(status, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if status == "D":
        cmd = f'git rm "{filename}"'
        action = "Deleted"
    else:
        cmd = f'git add "{filename}"'
        action = "Updated"

    if DRY_RUN:
        logging.info(f"[DRY-RUN] Would {action.lower()} and push: {filename}")
        return

    add = run_cmd(cmd)
    commit = run_cmd(f'git commit -m "{action}: {filename} ({timestamp})"')
    push = run_cmd("git push")

    if add.returncode != 0:
        logging.error(f"ADD/RM failed: {add.stderr}")
        return

    if commit.returncode != 0:
        logging.error(f"COMMIT failed: {commit.stderr}")
        return

    if push.returncode != 0:
        logging.error(f"PUSH failed: {push.stderr}")
    else:
        logging.info(f"{action} and pushed: {filename}")

def main():
    changes = get_changes()

    if not changes:
        logging.info("No changes detected.")
        return

    processed = 0

    for status, filename in changes:
        if processed >= MAX_CHANGES:
            break

        if is_sensitive(filename):
            logging.warning(f"Skipping sensitive file: {filename}")
            continue

        logging.info(f"Processing change: {status} {filename}")
        commit_single_change(status, filename)
        processed += 1

    if processed == 0:
        logging.warning("All pending changes are sensitive. Nothing committed.")
    else:
        logging.info(f"Completed {processed} change(s).")

if __name__ == "__main__":
    main()

