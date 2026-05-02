# Mini C Compiler - Local Deployment Script
# Run this script to quickly set up and launch the project locally

Write-Host "🚀 Mini C Compiler - Local Setup & Launch" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "`n📌 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.7+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Verify project files exist
Write-Host "`n📌 Verifying project files..." -ForegroundColor Yellow
$requiredFiles = @("ui.py", "compiler.exe", "lexer.l", "parser.y")
$allFilesExist = $true

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file found" -ForegroundColor Green
    } else {
        Write-Host "⚠️  $file NOT found" -ForegroundColor Yellow
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host "`n⚠️  Some files are missing. Continuing anyway..." -ForegroundColor Yellow
}

# Install Python dependencies (if needed)
Write-Host "`n📌 Checking Python packages..." -ForegroundColor Yellow
# tkinter is built-in with Python, no pip installation needed for desktop version

# Check if Streamlit is needed for web version
if (Test-Path "app.py") {
    Write-Host "📦 Web version detected (app.py)" -ForegroundColor Cyan
    
    $installStreamlit = Read-Host "Install Streamlit for web version? (y/n)"
    if ($installStreamlit -eq "y") {
        Write-Host "Installing Streamlit..." -ForegroundColor Yellow
        pip install streamlit --quiet
        Write-Host "✅ Streamlit installed" -ForegroundColor Green
    }
}

# Choose deployment method
Write-Host "`n🎯 Choose deployment method:" -ForegroundColor Cyan
Write-Host "1. Desktop App (tkinter UI - Recommended)" -ForegroundColor Green
Write-Host "2. Web App (Streamlit - Requires Streamlit)" -ForegroundColor Green
Write-Host "3. Exit" -ForegroundColor Gray

$choice = Read-Host "Enter your choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`n🚀 Launching Desktop Application..." -ForegroundColor Green
        python ui.py
    }
    "2" {
        Write-Host "`n🚀 Launching Web Application..." -ForegroundColor Green
        streamlit run app.py
    }
    "3" {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "❌ Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n✅ Application closed successfully" -ForegroundColor Green
