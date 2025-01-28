function Test-CommandExists {
    param($command)
    $exists = $null -ne (Get-Command $command -ErrorAction SilentlyContinue)
    return $exists
}

Set-Alias -Name 'test' -Value 'Test-CommandExists'