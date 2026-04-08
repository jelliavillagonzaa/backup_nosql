Param(
  [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$root = "C:\backup_nosql"
Set-Location $root

$py = Join-Path $root "venv\Scripts\python.exe"
if (!(Test-Path $py)) {
  throw "Python venv not found at $py. Create it first: python -m venv venv; .\\venv\\Scripts\\pip install -r backend\\requirements.txt"
}

Write-Host "Starting FastAPI on http://127.0.0.1:$Port" -ForegroundColor Cyan

# --app-dir makes imports work even if someone runs from a different folder.
& $py -m uvicorn --app-dir $root main:app --reload --host 127.0.0.1 --port $Port
