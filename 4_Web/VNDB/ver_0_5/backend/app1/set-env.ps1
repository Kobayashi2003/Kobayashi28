# Database configuration
$env:DB_NAME = "test4"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "postgres"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"

# Redis configuration
$env:REDIS_HOST = "localhost"
$env:REDIS_PORT = "6379"
$env:REDIS_CACHE_DB = "0"
$env:REDIS_CELERY_BROKER_DB = "1"
$env:REDIS_CELERY_BACKEND_DB = "2"

# Flask configurations
$env:DEBUG = "False"
$env:USE_RELOADER = "False"
$env:SECRET_KEY = "dev"
$env:APP_PORT = "5000"

# Data folder configuration
$env:DATA_FOLDER = Join-Path $PSScriptRoot "..\..\DATA"

# Print the set environment variables
Write-Host "Environment variables set for this session:"
Get-ChildItem Env: | Where-Object { $_.Name -in @('DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'REDIS_HOST', 'REDIS_PORT', 'REDIS_CACHE_DB', 'REDIS_CELERY_BROKER_DB', 'REDIS_CELERY_BACKEND_DB', 'DEBUG', 'USE_RELOADER', 'SECRET_KEY', 'APP_PORT', 'DATA_FOLDER') } | Format-Table -AutoSize