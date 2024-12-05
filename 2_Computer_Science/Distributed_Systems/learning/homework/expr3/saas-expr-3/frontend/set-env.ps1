$env:BK_LOGIN_URL = 'https://ce.bktencent.com/login/'
$env:BK_APP_HOST = 'dev.ce.bktencent.com'
$env:BK_AJAX_URL_PREFIX = '/'
$env:BK_USER_INFO_URL = '/user'

Get-ChildItem Env: | Where-Object { $_.Name -like "BK*" -or $_.Name -like "CORS*" } | Format-Table -AutoSize

Write-Host "Environment variables have been set successfully."