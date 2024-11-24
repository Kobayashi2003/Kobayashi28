<#
.SYNOPSIS
    Displays information about recent PowerShell commands with millisecond precision
.DESCRIPTION
    This PowerShell script accepts a parameter for the number of recent commands to display.
    It returns the command content, start time, end time, and total duration (in milliseconds) for each command.
.PARAMETER Count
    The number of recent commands to display. Defaults to 5 if not specified.
.EXAMPLE
    PS> ./get-recent-commands -Count 3
    Displaying last 3 commands:

    Command: Get-Process
    Start Time: 2023-05-20 10:15:30.123
    End Time: 2023-05-20 10:15:31.456
    Duration: 1333 ms

    Command: Get-ChildItem
    Start Time: 2023-05-20 10:16:45.789
    End Time: 2023-05-20 10:16:46.012
    Duration: 223 ms

    Command: Get-Date
    Start Time: 2023-05-20 10:17:30.345
    End Time: 2023-05-20 10:17:30.378
    Duration: 33 ms
.NOTES
    Author: KOBAYASHI
#>

param(
    [int]$Count = 5
)

try {
    $history = Get-History -Count $Count
    if ($history.Count -eq 0) {
        throw "No command history available."
    }

    "Displaying last $($history.Count) command$(if($history.Count -ne 1){'s'}):`n"

    foreach ($command in $history) {
        $duration = $command.EndExecutionTime - $command.StartExecutionTime
        $durationMs = [math]::Round($duration.TotalMilliseconds)

        "Command: $($command.CommandLine)"
        "Start Time: $($command.StartExecutionTime.ToString('yyyy-MM-dd HH:mm:ss.fff'))"
        "End Time: $($command.EndExecutionTime.ToString('yyyy-MM-dd HH:mm:ss.fff'))"
        "Duration: $durationMs ms`n"
    }

    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}