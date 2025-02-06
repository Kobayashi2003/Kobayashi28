#Requires -RunAsAdministrator

<#
.SYNOPSIS
    Hibernates the computer and wakes it up at a specified time
.DESCRIPTION
    This PowerShell script hibernates the computer and sets it to wake up at a specified time.
    The date defaults to today, and the time must be specified.
.PARAMETER Date
    Specifies the wake-up date (format: "yyyy-MM-dd"). Defaults to today's date.
.PARAMETER Time
    Specifies the wake-up time (format: "HH:mm:ss"). This parameter is mandatory.
.EXAMPLE
    PS> ./hibernate-until.ps1 -Time "14:30:00"
.EXAMPLE
    PS> ./hibernate-until.ps1 -Date "2025-02-07" -Time "08:00:00"
#>

param(
    [string]$Date = (Get-Date).ToString("yyyy-MM-dd"),
    [Parameter(Mandatory=$true)]
    [string]$Time
)

$taskName = "WakeAtSpecificTime"

try {
    $wakeTimeString = "$Date $Time"
    $wakeDateTime = [DateTime]::ParseExact($wakeTimeString, "yyyy-MM-dd HH:mm:ss", $null)

    if ($wakeDateTime -le (Get-Date)) {
        throw "Wake-up time must be in the future"
    }

    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -Command `"Write-Host 'System woke up as scheduled.'`""
    $trigger = New-ScheduledTaskTrigger -Once -At $wakeDateTime
    $settings = New-ScheduledTaskSettingsSet -WakeToRun
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null

    Write-Host "Hibernating until $($wakeDateTime.ToString('yyyy-MM-dd HH:mm:ss'))"

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