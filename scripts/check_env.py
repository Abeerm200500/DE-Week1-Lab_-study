"""
The Market: environment check. Run from the repo's top folder:
    Windows:  py -3.11 scripts/check_env.py
    Mac:      python3.11 scripts/check_env.py
"""
import os
import shutil
import subprocess
import sys

OK, FAIL, WARN = "OK  ", "FAIL", "WARN"
problems = 0


def report(status, message):
    global problems
    if status == FAIL:
        problems += 1
    print(f"{status}  {message}")


# 1. Python version
v = sys.version_info
report(OK if (v.major, v.minor) == (3, 11) else FAIL, f"Python {v.major}.{v.minor}.{v.micro} (the course uses 3.11)")

# 2. Python packages: everything listed in requirements.txt, at the exact version
from importlib.metadata import version, PackageNotFoundError
if not os.path.exists("requirements.txt"):
    report(FAIL, "requirements.txt not found. Run this script from the repo's top folder")
else:
    missing, wrong = [], []
    for line in open("requirements.txt"):
        line = line.split("#")[0].strip()          # ignore comments and blank lines
        if "==" not in line:
            continue
        name, wanted = line.split("==")
        try:
            installed = version(name)
            if installed != wanted:
                wrong.append(f"{name} {installed} (needs {wanted})")
        except PackageNotFoundError:
            missing.append(name)
    if missing or wrong:
        report(FAIL, f"packages not as in requirements.txt: {', '.join(missing + wrong)}. "
                     "Run: py -3.11 -m pip install -r requirements.txt")
    else:
        report(OK, "Python packages match requirements.txt")

# 3. .env with real passwords
if not os.path.exists(".env"):
    report(FAIL, ".env not found. Copy .env.example to .env and set your passwords (run this script from the repo's top folder)")
    settings = {}
else:
    try:
        from dotenv import dotenv_values
        settings = dotenv_values(".env")
    except ImportError:
        settings = {}
        report(FAIL, ".env found but cannot be read: python-dotenv is not installed (see check 2)")
    else:
        needed = ["MARKET_DB_PASSWORD", "MONGO_PASSWORD", "PGADMIN_PASSWORD"]
        empty = [k for k in needed if not settings.get(k)]
        default = [k for k in needed if settings.get(k) == "change_me"]
        if empty:
            report(FAIL, f".env is missing values for: {', '.join(empty)}")
        elif default:
            report(WARN, f".env still uses change_me for: {', '.join(default)}. Choose your own before the first start")
        else:
            report(OK, ".env found with your passwords")

# 4. Docker running
if shutil.which("docker") is None:
    report(FAIL, "Docker is not installed or not on PATH")
else:
    r = subprocess.run(["docker", "info"], capture_output=True, text=True)
    report(OK if r.returncode == 0 else FAIL, "Docker is running" if r.returncode == 0 else "Docker is not running. Start Docker Desktop and wait for 'Engine running'")

# 5. PostgreSQL: market-db on localhost:5433
try:
    import psycopg2
    conn = psycopg2.connect(host="localhost", port=5433, dbname="market", user="postgres",
                            password=settings.get("MARKET_DB_PASSWORD", ""), connect_timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM sales")
    n = cur.fetchone()[0]
    conn.close()
    report(OK, f"market-db reachable on localhost:5433 ({n:,} sales)")
except Exception as e:
    first_line = str(e).strip().splitlines()[0] if str(e).strip() else type(e).__name__
    hint = " (if you changed .env after the first start, see Troubleshooting in README.md)" if "password authentication failed" in str(e) else ""
    report(FAIL, f"market-db not reachable on localhost:5433: {first_line}{hint}")

# 6. MongoDB: mongo on localhost:27018
try:
    from pymongo import MongoClient
    client = MongoClient(host="localhost", port=27018, username="root", password=settings.get("MONGO_PASSWORD", ""),
                         authSource="admin", serverSelectionTimeoutMS=5000)
    n = client["market"]["website_reviews"].count_documents({})
    report(OK, f"mongo reachable on localhost:27018 ({n:,} website reviews)")
except Exception as e:
    first_line = str(e).strip().splitlines()[0][:120] if str(e).strip() else type(e).__name__
    hint = " (if you changed .env after the first start, see Troubleshooting in README.md)" if "Authentication failed" in str(e) else ""
    report(FAIL, f"mongo not reachable on localhost:27018: {first_line}{hint}")

print()
print("All checks passed." if problems == 0 else f"{problems} check(s) failed. Fix them, or bring this output to office hours.")
sys.exit(0 if problems == 0 else 1)