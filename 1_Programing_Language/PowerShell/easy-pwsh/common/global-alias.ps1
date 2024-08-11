$alias_map = @{
    'll'   = 'Get-ChildItemList'
    'la'   = 'Get-ChildItemAll'
    'mkcd' = 'mkdir-cd'
    'open' = 'explorer'
    'reload' = 'Reload-Script'
}

foreach ($key in $alias_map.Keys) {
    Set-Alias -Name $key -Value $alias_map[$key] -Scope Global
}