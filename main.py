#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"


def _check_env() -> None:
    missing = []
    if not (BACKEND_DIR / "package.json").exists():
        missing.append(str(BACKEND_DIR / "package.json"))
    if not (FRONTEND_DIR / "package.json").exists():
        missing.append(str(FRONTEND_DIR / "package.json"))
    if missing:
        raise FileNotFoundError(f"Missing required files: {', '.join(missing)}")

    if not (BACKEND_DIR / "node_modules").exists():
        print("[WARN] backend/node_modules not found. Run: cd backend && npm install")
    if not (FRONTEND_DIR / "node_modules").exists():
        print("[WARN] frontend/node_modules not found. Run: cd frontend && npm install")


def _spawn(cmd: list[str], cwd: Path) -> subprocess.Popen:
    return subprocess.Popen(
        cmd,
        cwd=str(cwd),
        env=os.environ.copy(),
        stdout=None,
        stderr=None,
        start_new_session=True,
    )


def _terminate(proc: subprocess.Popen, name: str) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except Exception as exc:
        print(f"[WARN] Failed to terminate {name}: {exc}")


def main() -> int:
    try:
        _check_env()
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    try:
        backend = _spawn(["npm", "run", "dev"], BACKEND_DIR)
        frontend = _spawn(["npm", "run", "dev"], FRONTEND_DIR)
    except FileNotFoundError:
        print("[ERROR] npm not found. Please install Node.js and npm.")
        return 1
    except Exception as exc:
        print(f"[ERROR] Failed to start processes: {exc}")
        return 1

    print("[INFO] Backend starting: http://localhost:4000")
    print("[INFO] Frontend starting: http://localhost:5173")
    print("[INFO] Press Ctrl+C to stop both.")

    try:
        while True:
            b_code = backend.poll()
            f_code = frontend.poll()
            if b_code is not None or f_code is not None:
                print(f"[INFO] Process exited. backend={b_code}, frontend={f_code}")
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[INFO] Stopping services...")
    finally:
        _terminate(backend, "backend")
        _terminate(frontend, "frontend")
        time.sleep(0.3)

    return 0


if __name__ == "__main__":
    sys.exit(main())

