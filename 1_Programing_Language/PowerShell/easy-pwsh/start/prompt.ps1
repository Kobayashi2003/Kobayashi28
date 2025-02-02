function global:prompt {
    $lst_cmd_state = $?
    $esc = $([char]27)
    if ((Get-History).count -ge 1) {
        $executionTime = ((Get-History)[-1].EndExecutionTime - (Get-History)[-1].StartExecutionTime).TotalMilliseconds
    } else {
        $executionTime = 0
    }
    $executionTime = [math]::Round($executionTime,2)
    $time = (Get-Date -Format "HH:mm:ss")
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal] $identity
    $adminRole = [Security.Principal.WindowsBuiltInRole]::Administrator
    $isAdmin = $principal.IsInRole($adminRole)
    $curUser = $env:USERNAME

    $promptChar = if ($isAdmin) { "#" } else { "$" }

    $promptString = ""

    if ($env:CONDA_DEFAULT_ENV) {
        $promptString += "$esc[1;33m($env:CONDA_DEFAULT_ENV)$esc[0m "
    }

    if (Test-Path variable:/PSDebugContext) {
        $promptString += "$esc[1;32m[D]$esc[0m "
    } elseif ($isAdmin) {
        $promptString += "$esc[1;31m[A]$esc[0m "
    } else {
        $promptString += "$esc[1;30m[$($curUser[0])]$esc[0m "
    }

    if ($lst_cmd_state) {
        $promptString += "$esc[1;32m$esc[1;4m$($executionTime)ms$esc[0m "
    } else {
        $promptString += "$esc[1;31m$esc[1;4m$($executionTime)ms$esc[0m "
    }

    $path = ($PWD.Path)
    $folderIcons = @{
        $env:USERPROFILE = "🏠"
        "$env:USERPROFILE\Documents" = "📄"
        "$env:USERPROFILE\Downloads" = "📥"
        "$env:USERPROFILE\Pictures" = "📸"
        "$env:USERPROFILE\Videos" = "📹"
        "$env:USERPROFILE\Music" = "🎵"
        "$env:USERPROFILE\Desktop" = "🖥️"
        "$env:USERPROFILE\OneDrive" = "☁️"
        "$env:USERPROFILE\.ssh" = "🔐"
        "$env:USERPROFILE\.config" = "⚙️"
        "C:\Program Files" = "📦"
        "C:\Program Files (x86)" = "📦"
        "C:\Windows" = "🪟"
        "C:\Users" = "👥"
        "C:\Temp" = "🗑️"
        "C:\ProgramData" = "🗄️"
    }

    # Add development-related folders
    $devFolders = @(
        "src", "source", "lib", "test", "tests", "docs", "scripts",
        "node_modules", "venv", ".venv", "build", "dist", "target"
    )

    foreach ($folder in $devFolders) {
        if ($path -match "\\$folder$") {
            $folderIcons[$path] = switch ($folder) {
                "src" { "🧾" }
                "source" { "🧾" }
                "lib" { "📚" }
                "docs" { "📖" }
                "scripts" { "📜" }
                "node_modules" { "📦" }
                ".git" { "🌿" }
                "config" { "⚙️" }
                "bin" { "🗃️" }
                "include" { "📎" }
                "data" { "💾" }
                "assets" { "🖼️" }
                "public" { "🌐" }
                "private" { "🔒" }
                "tools" { "🔧" }
                "utils" { "🛠️" }
                "vendor" { "🏪" }
                "packages" { "📦" }
                "resources" { "📦" }
                { $_ -in "test","tests" } { "🧪" }
                { $_ -in "venv",".venv" } { "🐍" }
                { $_ -in "build","dist","target" } { "🎯" }
                default { "📁" }
            }
            break
        }
    }

    if ($folderIcons.ContainsKey($path)) {
        $path = $folderIcons[$path]
    } else {
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0 -and $path.StartsWith($gitRoot)) {
            $path = "🌿 $($path.Substring($gitRoot.Length))"
        } else {
            $path += " 📂"
        }
    }

    while ($path.Length -gt 30) {
        # $path = "..\" + $path.Substring($path.LastIndexOf("\") + 1)
        $path = "..\" + $path.Substring($path.IndexOf("\", $path.IndexOf("\") + 1) + 1)
    }
    $promptString += "$esc[1;33m$path$esc[0m "

    if ($NestedPromptLevel -ge 1) {
        $colors_code = @{
            0 = "$esc[1;31m"; 1 = "$esc[1;32m"
            2 = "$esc[1;33m"; 3 = "$esc[1;34m"
            4 = "$esc[1;35m"; 5 = "$esc[1;36m"
        }
        for ($i = 0; $i -lt $NestedPromptLevel; $i++) {
            $promptString += "$($colors_code[$i % 6])$promptChar$esc[0m"
        }
    }
    $promptString += if ($isAdmin) { "$esc[1;31m$promptChar$esc[0m " } else { "$esc[1;34m$promptChar$esc[0m " }

    return $promptString
}