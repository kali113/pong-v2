param(
    [switch]$OneFile,
    [string]$OutputDir = "dist"
)

$pyinstaller = Join-Path $PSScriptRoot "..\.venv\Scripts\pyinstaller.exe"
if (-not (Test-Path $pyinstaller)) {
    $pyinstaller = "pyinstaller"
}

$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot

try {
    $args = @(
        "main.py",
        "--name", "PongAI-Neon",
        "--noconsole",
        "--clean",
        "--hidden-import", "pygame",
        "--hidden-import", "numpy",
        "--distpath", $OutputDir,
        "--workpath", "build"
    )

    if ($OneFile.IsPresent) {
        $args += "--onefile"
    }

    & $pyinstaller @args
}
finally {
    Pop-Location
}
