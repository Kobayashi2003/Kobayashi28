#Requires -RunAsAdministrator

<#
.SYNOPSIS
    Hibernates the computer for a specified duration
.DESCRIPTION
    This PowerShell script hibernates the computer for a specified number of minutes and then wakes it up.
.PARAMETER Minutes
    Specifies the number of minutes to hibernate. If not provided, the script will prompt for input.
.EXAMPLE
    PS> ./hibernate-for.ps1 30
    Hibernating for 30 minutes. Expected wake time: 2025-02-06 13:00:00
#>

param([int]$Minutes = 0)

$taskName = "WakeFromHibernate"

try {
    if ($Minutes -le 0) {
        $Minutes = Read-Host "Enter the number of minutes to hibernate"
        if ($Minutes -le 0) { throw "Hibernation time must be greater than 0 minutes" }
    }

    $wakeTime = (Get-Date).AddMinutes($Minutes)

    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -Command `"Write-Host 'System woke up as scheduled.'`""
    $trigger = New-ScheduledTaskTrigger -Once -At $wakeTime
    $settings = New-ScheduledTaskSettingsSet -WakeToRun
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null

    Write-Host "Hibernating for $Minutes minutes. Expected wake time: $($wakeTime.ToString('yyyy-MM-dd HH:mm:ss'))"

    Start-Sleep -Seconds 5
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Application]::SetSuspendState("Hibernate", $false, $false)

    if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }

    exit 0 # Success
} catch {
    Write-Host "Error: $($Error[0])" -ForegroundColor Red
    exit 1
}