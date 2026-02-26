---
name: git-smart-commit
description: Generate conventional commit messages in Chinese and handle Push with network proxy intelligence. Use when user wants to commit or push code.
---

# Git Smart Workflow (Commit & Push)

This skill handles the full Git workflow: Staging -> Committing -> Pushing.
It is specifically optimized for network environments in China (e.g., using Clash).

## Steps

### 1. Smart Commit (提交)

1.  **Check Staged**: Run `git diff --cached --name-only`.
    - If empty, ask user to stage files first (or offer to stage all).
2.  **Generate Message**: Analyze `git diff --cached` and generate a Conventional Commit message in **Chinese**.
    - Format: `<type>(<scope>): <subject>`
3.  **Confirm & Commit**: Show message and ask to commit.
    - Command: `git commit -m "<message>"`

### 2. Smart Push (推送)

Ask user: "Should I push the changes?"

If **Yes**:

1.  **Self-Healing Check (Dependency Installation)**:
    - Check if `scripts/git-smart-push.ps1` exists.
    - **If missing**: Automatically create it using the `Write` tool with the following content (do not ask user, just do it):
      ```powershell
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
      ```

2.  **Execute Smart Push**:
    - Run: `powershell -ExecutionPolicy Bypass -File scripts/git-smart-push.ps1`
    - (The script handles proxy detection and injection automatically).

## Usage Example

User: "提交代码"
Agent:

1. Generates "feat(sidebar): 增加折叠功能"
2. Commits.
3. Asks "Push?" -> User "Yes"
4. Tries direct push -> Fails -> Tries proxy push (7890) -> Success!
