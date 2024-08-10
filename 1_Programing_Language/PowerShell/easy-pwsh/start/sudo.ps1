if ((Get-Command 'sudo' -ErrorAction SilentlyContinue)) { return }

function sudo {

<#
    .SYNOPSIS
        Runs a command as the super user.
    .PARAMETER Command
        The command to run.
    .PARAMETER Arguments
        The arguments to pass to the command.
    .EXAMPLE
        PS> sudo whoami
#>

    $command = $args[0]
    $arguments = $args[1..$args.length]

    $tempFile = New-TemporaryFile
    $powershell_path = (Get-Command powershell).Source

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