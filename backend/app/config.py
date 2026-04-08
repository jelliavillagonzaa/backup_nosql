from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    backup_dir: Path = Path("./backups")
    """Directory where dump files are written (created if missing)."""

    # MongoDB (mongodump) — use if you back up MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodump_path: str = "mongodump"

    # SQL — mysqldump (MySQL / MariaDB)
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = ""
    mysql_password: str = ""
    mysqldump_path: str = "mysqldump"

    # SQL Server — sqlcmd + BACKUP DATABASE
    sqlserver_instance: str = ""  # e.g. localhost or localhost\\SQLEXPRESS
    sqlserver_user: str = ""
    sqlserver_password: str = ""
    sqlcmd_path: str = "sqlcmd"


settings = Settings()
