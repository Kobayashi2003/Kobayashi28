# Set environment variables for a BK (BlueKing) application

# Set the application ID and secret
$env:BKPAAS_APP_ID = "saas-expr-2"
$env:BKPAAS_APP_SECRET = "VrhcQDUe9XGBf4LoVbwof70gn913yyCtC6Qs"

# Set the major version of BKPAAS
$env:BKPAAS_MAJOR_VERSION = "3"

# Set URLs for various BK services
$env:BK_PAAS2_URL = "https://ce.bktencent.com"
$env:BK_COMPONENT_API_URL = "https://bkapi.ce.bktencent.com"
$env:BKPAAS_LOGIN_URL = "https://ce.bktencent.com/login/"

# Set CORS allowed origin
# Note: For production, change this to https://apps.ce.bktencent.com
$env:CORS_ALLOWED_ORIGIN = "http://dev.ce.bktencent.com:5000"

# Output the set environment variables (optional, for verification)
Get-ChildItem Env: | Where-Object { $_.Name -like "BK*" -or $_.Name -like "CORS*" } | Format-Table -AutoSize

Write-Host "Environment variables have been set successfully."