import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import settings


def run_mongodump(database: str | None = None) -> Path:
    """
    Backup MongoDB using the mongodump CLI (same idea as mongo shell: you target a DB).
    Requires mongodump on PATH (MongoDB Database Tools).
    """
    settings.backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = settings.backup_dir / f"mongo_{database or 'all'}_{stamp}_{uuid.uuid4().hex[:8]}"
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        settings.mongodump_path,
        "--uri",
        settings.mongodb_uri,
        "--out",
        str(out_dir),
    ]
    if database:
        cmd.extend(["--db", database])

    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"mongodump failed ({proc.returncode}): {proc.stderr or proc.stdout}"
        )
    return out_dir
