if ((Get-Command 'sudo' -ErrorAction SilentlyContinue) -and ((Get-Command 'sudo').Source -ne 'C:\WINDOWS\system32\sudo.exe')) {
<# .Notes
    https://github.com/sudo-pwsh/sudo-pwsh
#>
    return
}

if (Get-Command 'gsudo' -ErrorAction SilentlyContinue) {
<# .Notes
    https://github.com/gerardog/gsudo
#>
    Set-Alias -Name 'sudo' -Value 'gsudo' -Scope Global -Force
    return
}

function global:sudo {
<#
.SYNOPSIS
    Run a command as sudo

.PARAMETER command
    Command to run
.PARAMETER arguments
    Arguments to pass to the command

.EXAMPLE
    sudo -command "ipconfig"
#>

    $command = $args[0]
    $arguments = $args[1..$args.length]

    $tempFile = New-TemporaryFile
    $powershell_path = (Get-Process -Id $PID | Select-Object -ExpandProperty Path)

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $powershell_path
    $psi.CreateNoWindow = $true
    $psi.Arguments = "-windowstyle hidden
                        -nologo
                        -noninteractive
                        -noprofile
                        -command $command $arguments > $tempFile"
    $psi.Verb = "runas"

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    $process.Start() | Out-Null
    $process.WaitForExit()

    $contents = Get-Content -Path $tempFile
    Remove-Item -Path $tempFile

    return $contents
}