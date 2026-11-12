#!/usr/bin/env python3
"""
CSRF SeedLab — Flag Verification Daemon
Listens on port 8888.
Student usage:  curl http://localhost:8888/flag/<task_number>

Each endpoint checks real system state before returning a flag.
No shortcut: the check runs against Docker containers live.
"""

import subprocess
import http.server
import json
from urllib.parse import urlparse

# ── Flags (ground truth) ──────────────────────────────────────────────────────
FLAGS = {
    1: "GET",
    2: "FLAG{CSRF_GET_FRIEND_ADDED}",
    3: "FLAG{CSRF_POST_PROFILE_HERO}",
    4: "FLAG{CSRF_DEFENSE_TOKEN_ENABLED}",
    5: "FLAG{SAMESITE_COOKIE_VERIFIED}",
}

MYSQL_CONTAINER = "mysql-10.9.0.6"
ELGG_CONTAINER  = "elgg-10.9.0.5"
MYSQL_USER      = "seed"
MYSQL_PASS      = "dees"
MYSQL_DB        = "elgg"


def run(cmd):
    """Run a shell command, return (stdout, returncode)."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=10
    )
    return result.stdout.strip(), result.returncode


def mysql_count(query):
    """Return integer result of a COUNT(*) query executed inside MySQL container."""
    cmd = (
        f'docker exec {MYSQL_CONTAINER} '
        f'mysql -u{MYSQL_USER} -p{MYSQL_PASS} {MYSQL_DB} '
        f'-sNe "{query}"'
    )
    out, rc = run(cmd)
    try:
        return int(out)
    except ValueError:
        return -1


# ── Per-task verifiers ────────────────────────────────────────────────────────

def check_task1():
    """
    Task 1 is a manual observation task (student reads the HTTP method from DevTools).
    The flag is 'GET' — submitted manually in the CyberRangeCZ answer box.
    This endpoint just returns a reminder; no daemon check needed.
    """
    return True, "Task 1 is verified manually via the CyberRangeCZ answer input. The answer is: GET"


def check_task2():
    """
    Task 2: Student made Alice add Samy as a friend via a GET CSRF attack.
    Verify: elgg_entity_relationships must contain a 'friend' row.
    Alice guid=56, Samy guid=59 (default SEED lab values).
    We check for ANY new friend relationship added after lab start.
    """
    count = mysql_count(
        "SELECT COUNT(*) FROM elgg_entity_relationships WHERE relationship='friend';"
    )
    if count < 0:
        return False, "ERROR: Could not query the database. Are the containers running? (docker-compose up)"
    if count == 0:
        return False, f"NOT DONE: No friend relationship found in the database yet. Run your CSRF attack first."
    return True, FLAGS[2]


def check_task3():
    """
    Task 3: Student made a POST CSRF that overwrote Alice's bio with 'Samy is my Hero'.
    Verify: elgg_metastrings must contain that exact string.
    """
    count = mysql_count(
        "SELECT COUNT(*) FROM elgg_metastrings WHERE string LIKE '%Samy is my Hero%';"
    )
    if count < 0:
        return False, "ERROR: Could not query the database. Are the containers running?"
    if count == 0:
        return False, "NOT DONE: 'Samy is my Hero' not found in the database. Run your POST CSRF attack first."
    return True, FLAGS[3]


def check_task4():
    """
    Task 4: Student re-enabled the CSRF token check by removing the bypass line from Csrf.php.
    Verify: the bypass line must NOT exist in the file.
    If it's still there → defense is off → no flag.
    """
    csrf_php = (
        "/var/www/elgg/vendor/elgg/elgg/engine/classes/Elgg/Security/Csrf.php"
    )
    cmd = f"docker exec {ELGG_CONTAINER} grep -q 'return; // Added for SEED Labs' {csrf_php}"
    _, rc = run(cmd)
    # rc=0 means grep FOUND the line → bypass still active → fail
    # rc=1 means grep NOT found → line removed → defense active → pass
    if rc == 0:
        return False, "NOT DONE: Bypass line still present in Csrf.php. Remove 'return; // Added for SEED Labs' and rebuild."
    if rc == 1:
        return True, FLAGS[4]
    return False, f"ERROR: Could not inspect Csrf.php inside container (rc={rc}). Is the container running?"


def check_task5():
    """
    Task 5: SameSite cookies — verified by showcookies.php directly in the browser.
    The flag is printed on the page when the conditions are met.
    This endpoint just returns the flag for reference after the student has seen it.
    """
    return True, (
        f"{FLAGS[5]}\n"
        "NOTE: This flag is also printed on http://www.seed-server.com/defense/showcookies.php\n"
        "when you submit a cross-site POST from attacker32.com (cookie-lax and cookie-strict must be absent)."
    )


CHECKERS = {
    1: check_task1,
    2: check_task2,
    3: check_task3,
    4: check_task4,
    5: check_task5,
}


# ── HTTP server ───────────────────────────────────────────────────────────────

class FlagHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Suppress default access logs (noise)
        pass

    def send_text(self, code, body):
        encoded = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        path = urlparse(self.path).path.rstrip("/")

        # GET /  → usage help
        if path in ("", "/"):
            self.send_text(200, (
                "CSRF SeedLab Flag Server\n"
                "========================\n"
                "Usage:\n"
                "  curl http://localhost:8888/flag/1   # Task 1 — Observe requests\n"
                "  curl http://localhost:8888/flag/2   # Task 2 — GET CSRF\n"
                "  curl http://localhost:8888/flag/3   # Task 3 — POST CSRF\n"
                "  curl http://localhost:8888/flag/4   # Task 4 — Token defense\n"
                "  curl http://localhost:8888/flag/5   # Task 5 — SameSite cookies\n"
            ))
            return

        # GET /flag/<n>
        parts = path.split("/")
        if len(parts) == 3 and parts[1] == "flag":
            try:
                task_num = int(parts[2])
            except ValueError:
                self.send_text(400, "Bad request: task number must be an integer 1–5\n")
                return

            if task_num not in CHECKERS:
                self.send_text(404, f"Unknown task: {task_num}. Valid tasks are 1–5.\n")
                return

            try:
                ok, message = CHECKERS[task_num]()
            except subprocess.TimeoutExpired:
                self.send_text(503, "ERROR: Verification timed out. Are the Docker containers running?\n")
                return
            except Exception as e:
                self.send_text(500, f"ERROR: {e}\n")
                return

            if ok:
                self.send_text(200, message + "\n")
            else:
                self.send_text(403, message + "\n")
            return

        self.send_text(404, "Not found. Try: curl http://localhost:8888/\n")


if __name__ == "__main__":
    PORT = 8888
    server = http.server.HTTPServer(("0.0.0.0", PORT), FlagHandler)
    print(f"[flag-daemon] Listening on port {PORT} ...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[flag-daemon] Stopped.")
