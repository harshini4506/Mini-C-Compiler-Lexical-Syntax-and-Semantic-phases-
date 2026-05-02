# Mini C Compiler - Azure Deployment Script
# Prerequisites: Azure CLI must be installed (https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

param(
    [string]$ResourceGroup = "mini-c-compiler",
    [string]$AppName = "mini-c-compiler-app",
    [string]$Location = "eastus",
    [string]$GitHubRepo = "https://github.com/harshini4506/Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases-"
)

Write-Host "☁️  Mini C Compiler - Azure Deployment" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Check if Azure CLI is installed
Write-Host "`n📌 Checking Azure CLI installation..." -ForegroundColor Yellow
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not found!" -ForegroundColor Red
    Write-Host "Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit 1
}

# Login to Azure
Write-Host "`n📌 Logging into Azure..." -ForegroundColor Yellow
az login

# Create resource group
Write-Host "`n📌 Creating resource group: $ResourceGroup" -ForegroundColor Yellow
az group create --name $ResourceGroup --location $Location
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create resource group" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Resource group created" -ForegroundColor Green

# Create App Service Plan
Write-Host "`n📌 Creating App Service Plan (B1 - Free tier compatible)..." -ForegroundColor Yellow
az appservice plan create --name "$AppName-plan" `
    --resource-group $ResourceGroup --sku B1 --is-linux
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create App Service Plan" -ForegroundColor Red
    exit 1
}
Write-Host "✅ App Service Plan created" -ForegroundColor Green

# Create Web App
Write-Host "`n📌 Creating Web App: $AppName..." -ForegroundColor Yellow
az webapp create --resource-group $ResourceGroup `
    --plan "$AppName-plan" --name $AppName --runtime "PYTHON|3.9"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create Web App" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Web App created" -ForegroundColor Green

# Configure GitHub deployment
Write-Host "`n📌 Configuring GitHub deployment..." -ForegroundColor Yellow
az webapp deployment source config --name $AppName `
    --resource-group $ResourceGroup --repo-url $GitHubRepo `
    --branch main --manual-integration
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to configure GitHub deployment" -ForegroundColor Red
    exit 1
}
Write-Host "✅ GitHub deployment configured" -ForegroundColor Green

# Get the app URL
Write-Host "`n📌 Retrieving app URL..." -ForegroundColor Yellow
$appUrl = "https://$AppName.azurewebsites.net"

# Display completion message
Write-Host "`n" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`n🌐 Your application is live at:" -ForegroundColor Cyan
Write-Host "   $appUrl" -ForegroundColor Yellow
Write-Host "`n📊 Management URL:" -ForegroundColor Cyan
Write-Host "   https://portal.azure.com" -ForegroundColor Yellow
Write-Host "`n📝 Resource Group:" -ForegroundColor Cyan
Write-Host "   $ResourceGroup" -ForegroundColor Yellow
Write-Host "`n⏱️  Initial deployment may take 2-5 minutes" -ForegroundColor Cyan
Write-Host "`n📖 View logs:" -ForegroundColor Cyan
Write-Host "   az webapp log tail --name $AppName --resource-group $ResourceGroup" -ForegroundColor Yellow
Write-Host "`n" -ForegroundColor Green

# Offer to open the app in browser
$openApp = Read-Host "Open app in browser now? (y/n)"
if ($openApp -eq "y") {
    Start-Process $appUrl
}

Write-Host "`n✅ Deployment script completed!" -ForegroundColor Green
