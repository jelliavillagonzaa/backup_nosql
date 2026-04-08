import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import settings


def run_mysqldump(database: str) -> Path:
    """
    Backup MySQL/MariaDB using mysqldump (SQL client-style CLI).
    Set MYSQL_USER / MYSQL_PASSWORD (or .env) before calling.
    """
    if not settings.mysql_user:
        raise ValueError("mysql_user is not set (env MYSQL_USER)")

    settings.backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outfile = settings.backup_dir / f"mysql_{database}_{stamp}_{uuid.uuid4().hex[:8]}.sql"

    cmd = [
        settings.mysqldump_path,
        f"--host={settings.mysql_host}",
        f"--port={settings.mysql_port}",
        f"--user={settings.mysql_user}",
        f"--password={settings.mysql_password}",
        "--single-transaction",
        "--routines",
        "--events",
        database,
    ]
    with open(outfile, "w", encoding="utf-8", newline="\n") as f:
        proc = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True, check=False)
    if proc.returncode != 0:
        outfile.unlink(missing_ok=True)
        raise RuntimeError(f"mysqldump failed ({proc.returncode}): {proc.stderr}")
    return outfile


def run_sqlserver_backup(database: str) -> Path:
    """
    SQL Server: run BACKUP DATABASE via sqlcmd (typical Windows / SQLCLIENT style).
    Requires sqlcmd on PATH and SQLSERVER_INSTANCE, SQLSERVER_USER, SQLSERVER_PASSWORD.
    """
    if not settings.sqlserver_instance or not settings.sqlserver_user:
        raise ValueError("sqlserver_instance and sqlserver_user must be set")

    settings.backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bak_name = f"{database}_{stamp}_{uuid.uuid4().hex[:8]}.bak"
    outfile = (settings.backup_dir / bak_name).resolve()

    # BACKUP DATABASE needs a path the SQL Server process can write to; for local dev
    # you may need a folder SQL Server has permission to use (e.g. C:\\SQLBackups).
    backup_sql = f"BACKUP DATABASE [{database}] TO DISK = N'{str(outfile).replace(chr(92), chr(92) * 2)}' WITH FORMAT, INIT, NAME = N'FastAPI backup', SKIP, NOREWIND, NOUNLOAD, STATS = 10"

    cmd = [
        settings.sqlcmd_path,
        "-S",
        settings.sqlserver_instance,
        "-U",
        settings.sqlserver_user,
        "-P",
        settings.sqlserver_password,
        "-Q",
        backup_sql,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"sqlcmd failed ({proc.returncode}): {proc.stderr or proc.stdout}")
    if not outfile.exists():
        raise RuntimeError("BACKUP completed but .bak file not found at expected path")
    return outfile
