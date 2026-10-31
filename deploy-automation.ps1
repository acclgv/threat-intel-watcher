<#
.SYNOPSIS
    Script automatizado para inicializar y desplegar el pipeline de automatización en la nube.
.DESCRIPTION
    Inicializa el repositorio Git para threat-intel-watcher, configura la identidad canónica,
    crea el commit inicial con los datos de telemetría y el workflow de GitHub Actions,
    y prepara la vinculación con el repositorio remoto https://github.com/GarciaVillenaLuis/threat-intel-watcher.git.
#>

[CmdletBinding()]
param (
    [string]$RemoteUrl = "https://github.com/GarciaVillenaLuis/threat-intel-watcher.git"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Despliegue del Pipeline de Automatización Cloud-Native   " -ForegroundColor Cyan
Write-Host "  Threat Intel & Cloud Vulnerability Watcher              " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Asegurar directorio de trabajo
Set-Location -Path $PSScriptRoot

# 2. Inicializar repositorio Git si no existe
if (-not (Test-Path ".git")) {
    Write-Host "[+] Inicializando repositorio Git local..." -ForegroundColor Green
    git init -b main
} else {
    Write-Host "[*] Repositorio Git existente detectado." -ForegroundColor Yellow
}

# 3. Configurar identidad canónica
git config user.name "Luis Garcia Villena"
git config user.email "luisysuagia@gmail.com"
Write-Host "[+] Identidad de autor configurada: Luis Garcia Villena <luisysuagia@gmail.com>" -ForegroundColor Green

# 4. Comprobar o añadir remoto
$remotes = git remote
if ($remotes -contains "origin") {
    $existingRemote = git remote get-url origin
    Write-Host "[*] Remoto origin existente: $existingRemote" -ForegroundColor Yellow
    if ($existingRemote -ne $RemoteUrl) {
        git remote set-url origin $RemoteUrl
        Write-Host "[+] Remoto origin actualizado a: $RemoteUrl" -ForegroundColor Green
    }
} else {
    Write-Host "[+] Vinculando repositorio remoto origin: $RemoteUrl" -ForegroundColor Green
    git remote add origin $RemoteUrl
}

# 5. Añadir archivos y realizar commit
git add .
$status = git status --porcelain
if ($status) {
    Write-Host "[+] Creando commit inicial del pipeline de automatización..." -ForegroundColor Green
    git commit -m "feat(pipeline): initialize cloud-native threat intel watcher with CISA KEV feed and GitHub Actions"
} else {
    Write-Host "[*] No hay cambios pendientes de commit." -ForegroundColor Yellow
}

Write-Host "`n[i] Para activar la automatización 100% en la nube:" -ForegroundColor Cyan
Write-Host " 1. Crea el repositorio 'threat-intel-watcher' (puede ser Privado o Público) en https://github.com/new" -ForegroundColor White
Write-Host " 2. Ejecuta en esta terminal: git push -u origin main" -ForegroundColor Green
Write-Host "`nUna vez subido, GitHub Actions se ejecutará automáticamente en la nube todos los días a las 05:37 UTC." -ForegroundColor Yellow
Write-Host "¡No tendrás que encender tu ordenador ni hacer nada más nunca jamás!" -ForegroundColor Green
