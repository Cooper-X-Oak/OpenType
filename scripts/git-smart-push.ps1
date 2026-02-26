# scripts/git-smart-push.ps1
# Git Smart Push for China Network Environment
param([string[]]$GitArgs); $ErrorActionPreference = "Stop"
function Write-Color { param([string]$Message, [ConsoleColor]$Color = "White"); Write-Host $Message -ForegroundColor $Color }
Write-Color "`n🚀 Trae Smart Push: Initializing Network Optimization..." "Cyan"
$CandidatePorts = @(7890, 7897, 10808, 1080, 51837); $ActiveProxy = $null
Write-Color "🔍 Scanning for local proxy (Clash/v2ray)..." "Gray"
foreach ($Port in $CandidatePorts) { if (Test-NetConnection -ComputerName 127.0.0.1 -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue) { $ActiveProxy = "http://127.0.0.1:$Port"; Write-Color "✅ Found active proxy on port: $Port" "Green"; break } }
$GitCommand = "git"; $GitParams = @(); if ($ActiveProxy) { Write-Color "🌐 Using Proxy: $ActiveProxy" "Green"; $GitParams += "-c", "http.proxy=$ActiveProxy", "-c", "https.proxy=$ActiveProxy" } else { Write-Color "⚠️  No local proxy detected. Attempting Direct Connection..." "Yellow" }
$GitParams += "push"; if ($GitArgs) { $GitParams += $GitArgs }; $CmdString = "$GitCommand " + ($GitParams -join " "); Write-Color "exec: $CmdString" "DarkGray"
try { & $GitCommand $GitParams; if ($LASTEXITCODE -eq 0) { Write-Color "`n✨ Push Successful!" "Green"; exit 0 } else { throw "Git push exited with code $LASTEXITCODE" } } catch { Write-Color "`n❌ Push Failed." "Red"; exit 1 }
