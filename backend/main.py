import gzip
import os
import shutil
import subprocess

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

# --- STEP 1: ENABLE CORS ---
# Allows Flutter Web (different origin/port) to call the API without browser blocks.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL connection (override with env vars in production)
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3307")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "1234")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "student")


@app.get("/")
def root():
    return {"message": "Database Backup Server is Running"}


# --- STEP 2: SQL BACKUP (mysqldump — same idea as mongodump, but for MySQL/MariaDB) ---
@app.get("/download-student-backup")
def backup_student_db():
    # 1. Find mysqldump on PATH (install MySQL client / Server and add bin to PATH)
    dump_tool = shutil.which("mysqldump")
    if not dump_tool:
        raise HTTPException(
            status_code=500,
            detail=(
                "mysqldump not found. Install MySQL or MariaDB client tools "
                "and add the bin folder to your PATH."
            ),
        )

    work_dir = os.getcwd()
    sql_name = "student_backup.sql"
    gz_name = "student_backup.gz"
    sql_path = os.path.join(work_dir, sql_name)
    gz_path = os.path.join(work_dir, gz_name)

    for path in (sql_path, gz_path):
        if os.path.exists(path):
            os.remove(path)

    try:
        # 2. Dump SQL to a file (--result-file works well on Windows; no shell redirect)
        command = [
            dump_tool,
            f"--host={MYSQL_HOST}",
            f"--port={MYSQL_PORT}",
            f"--user={MYSQL_USER}",
            f"--password={MYSQL_PASSWORD}",
            "--single-transaction",
            "--routines",
            "--events",
            f"--result-file={sql_path}",
            MYSQL_DATABASE,
        ]

        subprocess.run(command, check=True)

        if not os.path.exists(sql_path) or os.path.getsize(sql_path) == 0:
            raise HTTPException(
                status_code=500,
                detail="Backup file was not created or is empty.",
            )

        # 3. Gzip the .sql so the download matches the original assignment shape (.gz)
        with open(sql_path, "rb") as f_in:
            with gzip.open(gz_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        try:
            os.remove(sql_path)
        except OSError:
            pass

        return FileResponse(
            path=gz_path,
            filename="student_backup.gz",
            media_type="application/gzip",
        )

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"mysqldump failed (exit {e.returncode}). Check host, port, user, password, and database name.",
        ) from e
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e
