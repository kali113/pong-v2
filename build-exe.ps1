# ============================================================================
# Windows EXE Auto-Builder for Pong AI V2
# Builds a standalone executable with all dependencies
# ============================================================================

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "  Pong AI V2 - Windows EXE Auto-Builder" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python installation
Write-Host "[1/7] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+)") {
        $version = [version]$matches[1]
        if ($version.Major -lt 3 -or ($version.Major -eq 3 -and $version.Minor -lt 10)) {
            Write-Host "ERROR: Python 3.10+ required. Found: $pythonVersion" -ForegroundColor Red
            Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "  Python version OK: $pythonVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "ERROR: Python not found in PATH" -ForegroundColor Red
    Write-Host "Install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Step 2: Check if main.py exists
Write-Host "[2/7] Checking project files..." -ForegroundColor Yellow
if (-Not (Test-Path "main.py")) {
    Write-Host "ERROR: main.py not found. Run this script from project root." -ForegroundColor Red
    exit 1
}
if (-Not (Test-Path "icon.ico")) {
    Write-Host "WARNING: icon.ico not found. Executable will have no icon." -ForegroundColor Yellow
    $icon_arg = ""
} else {
    Write-Host "  Found main.py and icon.ico" -ForegroundColor Green
    $icon_arg = "--icon=icon.ico"
}

# Step 3: Install/upgrade pip
Write-Host "[3/7] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to upgrade pip" -ForegroundColor Red
    exit 1
}
Write-Host "  pip upgraded successfully" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host "[4/7] Installing game dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt --quiet
} else {
    pip install pygame numpy --quiet
}
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "  Dependencies installed" -ForegroundColor Green

# Step 5: Install PyInstaller
Write-Host "[5/7] Installing PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install PyInstaller" -ForegroundColor Red
    exit 1
}
Write-Host "  PyInstaller installed" -ForegroundColor Green

# Step 6: Clean old builds
Write-Host "[6/7] Cleaning old builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }
Write-Host "  Old builds removed" -ForegroundColor Green

# Step 7: Build executable
Write-Host "[7/7] Building executable (this may take 2-5 minutes)..." -ForegroundColor Yellow
Write-Host "  Options: Single file, windowed, with icon" -ForegroundColor Cyan

$buildCmd = "pyinstaller --onefile --windowed --name=PongAI-Neon"
if ($icon_arg) { $buildCmd += " $icon_arg" }
$buildCmd += " main.py"

Invoke-Expression $buildCmd | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed. Check errors above." -ForegroundColor Red
    exit 1
}

# Verify output
if (Test-Path "dist\PongAI-Neon.exe") {
    $fileSize = (Get-Item "dist\PongAI-Neon.exe").Length / 1MB
    Write-Host ""
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host ""
    Write-Host "  Output: dist\PongAI-Neon.exe" -ForegroundColor Cyan
    Write-Host "  Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To run: .\dist\PongAI-Neon.exe" -ForegroundColor Yellow
    Write-Host ""
    
    # Ask if user wants to run it
    $response = Read-Host "Run the game now? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Start-Process ".\dist\PongAI-Neon.exe"
    }
} else {
    Write-Host "ERROR: Executable not found after build" -ForegroundColor Red
    exit 1
}
