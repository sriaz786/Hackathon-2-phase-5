# fix_environment.ps1
Write-Host "Checking Environment for Phase 5 Deployment..." -ForegroundColor Cyan

# 1. Check Administrator Privileges (Required for Hosts file)
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Warning "[-] NOT running as Administrator."
    Write-Warning "You MUST run this script independently as Administrator to fix the 'hosts' file."
    Write-Host "If you only want to check Docker/Minikube, I will proceed..." -ForegroundColor Yellow
}
else {
    Write-Host "[+] Running as Administrator." -ForegroundColor Green
}

# 2. Check Docker
Write-Host "`nChecking Docker..."
try {
    docker version | Out-Null
    Write-Host "[+] Docker is running." -ForegroundColor Green
}
catch {
    Write-Error "[-] Docker is NOT running or NOT installed."
    Write-Host "ACTION: Please install Docker Desktop and start it." -ForegroundColor Yellow
    exit
}

# 3. Check & Start Minikube
Write-Host "`nChecking Minikube..."
$status = minikube status --format='{{.Host}}' 2>$null
if ($status -ne "Running") {
    Write-Host "[-] Minikube is not running. Attempting to start..." -ForegroundColor Yellow
    try {
        minikube start --cpus 4 --memory 3072
        Write-Host "[+] Minikube started successfully." -ForegroundColor Green
    }
    catch {
        Write-Error "[-] Failed to start Minikube."
        exit
    }
}
else {
    Write-Host "[+] Minikube is already running." -ForegroundColor Green
}

# 4. Update Hosts File
Write-Host "`nUpdating Hosts File..."
if (-not $isAdmin) {
    Write-Error "[-] Skipping Hosts file update because script is not running as Administrator."
    Write-Host "Please manually add this line to C:\Windows\System32\drivers\etc\hosts :" -ForegroundColor Yellow
    $ip = minikube ip
    Write-Host "$ip app.local api.app.local" -ForegroundColor White
}
else {
    $minikubeIp = minikube ip
    $hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
    $entry = "$minikubeIp app.local api.app.local"
    
    $content = Get-Content $hostsPath
    if ($content -match "app.local") {
        Write-Host "[~] Hosts file already configured for app.local." -ForegroundColor Yellow
    }
    else {
        Add-Content -Path $hostsPath -Value "`n$entry"
        Write-Host "[+] Successfully added '$entry' to hosts file." -ForegroundColor Green
    }
}

Write-Host "`nReady! Try accessing http://app.local in your browser." -ForegroundColor Cyan
