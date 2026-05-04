# DevEnv-Setup Windows Installer
# One-Click Development Environment Setup Tool

param(
    [switch]$AutoRun  # Auto-run after installation
)

$VERSION = "1.0.0"
$INSTALL_DIR = "$env:LOCALAPPDATA\DevEnv-Setup"
$BIN_DIR = "$env:LOCALAPPDATA\DevEnv-Setup\bin"
$REPO_URL = "https://github.com/KEBANJILONG/DevEnv-Setup"
$RAW_URL = "https://raw.githubusercontent.com/KEBANJILONG/DevEnv-Setup/main"

# Colors
function Write-Banner {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                                                       ║" -ForegroundColor Cyan
    Write-Host "║   🚀 DevEnv-Setup v$VERSION" -ForegroundColor Cyan
    Write-Host "║   One-Click Development Environment Setup             ║" -ForegroundColor Cyan
    Write-Host "║                                                       ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success($message) {
    Write-Host "  ✅ $message" -ForegroundColor Green
}

function Write-Err($message) {
    Write-Host "  ❌ $message" -ForegroundColor Red
}

function Write-Info($message) {
    Write-Host "  ℹ️  $message" -ForegroundColor Cyan
}

function Write-Progress($message) {
    Write-Host "  ⏳ $message" -ForegroundColor Yellow
}

function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python detected: $pythonVersion"
            return $true
        }
    } catch {}
    try {
        $pythonVersion = python3 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python detected: $pythonVersion"
            return $true
        }
    } catch {}
    Write-Err "Python not found. Please install Python 3.8+ from https://python.org"
    return $false
}

function Install-DevEnv {
    Write-Progress "Installing DevEnv-Setup..."

    # Create directories
    New-Item -ItemType Directory -Force -Path $INSTALL_DIR | Out-Null
    New-Item -ItemType Directory -Force -Path "$INSTALL_DIR\src" | Out-Null

    # Download main script
    Write-Progress "Downloading main script..."
    try {
        $progressPreference = 'silentlyContinue'
        $scriptContent = Invoke-WebRequest -Uri "$RAW_URL/src/devenv.py" -UseBasicParsing -TimeoutSec 30
        $scriptContent.Content | Out-File -FilePath "$INSTALL_DIR\src\devenv.py" -Encoding UTF8 -NoNewline
        Write-Success "Script downloaded"
    } catch {
        Write-Err "Failed to download: $_"
        Write-Info "Creating offline scripts instead..."
        Copy-Item -Path ".\src\devenv.py" -Destination "$INSTALL_DIR\src\devenv.py" -Force -ErrorAction SilentlyContinue
    }

    # Copy local files if available
    if (Test-Path ".\src\devenv.py") {
        Copy-Item -Path ".\src\devenv.py" -Destination "$INSTALL_DIR\src\devenv.py" -Force
    }
    if (Test-Path ".\main.py") {
        Copy-Item -Path ".\main.py" -Destination "$INSTALL_DIR\main.py" -Force
    }

    # Create launcher batch file
    @"@echo off
python "%~dp0main.py" %*
"@ | Out-File -FilePath "$INSTALL_DIR\devenv.bat" -Encoding ASCII

    # Add to PATH
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -notlike "*$INSTALL_DIR*") {
        [Environment]::SetEnvironmentVariable("Path", "$userPath;$INSTALL_DIR", "User")
        Write-Info "Added to PATH: $INSTALL_DIR"
    }

    Write-Success "DevEnv-Setup installed successfully!"
}

function Add-ToProfile {
    $profilePath = $PROFILE
    $installCmd = "python `"$INSTALL_DIR\main.py`""

    if (Test-Path $profilePath) {
        $content = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
        if ($content -notlike "*DevEnv-Setup*") {
            Add-Content -Path $profilePath -Value "`n# DevEnv-Setup`nSet-Alias -Name devenv -Value `"$installCmd`""
            Write-Info "Added to PowerShell profile"
        }
    }
}

# Main
Write-Banner

if (-not (Test-Python)) {
    exit 1
}
Write-Host ""

Install-DevEnv

Write-Host ""
Write-Success "Installation complete!"
Write-Host ""
Write-Info "Usage:"
Write-Host "  devenv check          - Check development environment"
Write-Host "  devenv install nodejs  - Install a tool"
Write-Host "  devenv install web-full - Install preset"
Write-Host "  devenv list tools     - List available tools"
Write-Host ""
Write-Info "Restart your terminal or run: refreshenv"
Write-Host ""

if ($AutoRun) {
    python "$INSTALL_DIR\main.py" check
}