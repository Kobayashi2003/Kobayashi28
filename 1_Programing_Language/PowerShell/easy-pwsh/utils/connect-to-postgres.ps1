<#
.SYNOPSIS
    Connect to postgres database using harlequin.

.PARAMETER hostname
    Specifies the host name of the machine on which the server is running.
    If the value begins with a slash, it is used as the directory for the
    Unix-domain socket.
.PARAMETER port
    Port number to connect tot at the server host, or socket file name
    extension for Unix-domain connections.
.PARAMETER dbname
    The database name to use when connecting with the Postgres server.
.PARAMETER username
    PostgresSQL user name to connect as.
.PARAMETER password
    Password to be used if the server demands password authentication.
#>

param(
    [Parameter(Mandatory=$false)]
    [alias("h")] $hostname = "localhost",

    [Parameter(Mandatory=$false)]
    [alias("p")] $port = 5432,

    [Parameter(Mandatory=$false)]
    [alias("d")] $dbname = "postgres",

    [Parameter(Mandatory=$false)]
    [alias("u")] $username = "postgres",

    [Parameter(Mandatory=$false)]
    [alias("pw")] $password = "postgres"
)

$cur_dir = Get-Location
$script_path = Split-Path $MyInvocation.MyCommand.Path
$python_script_folder = Join-Path -Path $script_path -ChildPath "harlequin-postgres"

if (-not (Test-Path -Path $python_script_folder)) {
    Write-Host "Please put harlequin-postgres folder in the same directory with this script" -ForegroundColor Red
    exit 1
}

if (-not $path) {
    $path = $cur_dir
}

if (-not (Test-Path -Path $path)) {
    New-Item -Path $path -ItemType Directory | Out-Null
}

$abs_path = Resolve-Path -Path $path

Set-Location $python_script_folder

& pixi run harlequin --adapter postgres --host $hostname --port $port --dbname $dbname --username $username --password $password --no-download-tzdata

Set-Location $cur_dir

