if (Get-Command scoop -ErrorAction SilentlyContinue) {
    return
}

# input installation directory
$scoopDir = Read-Host -Prompt "Enter the directory where you want to install Scoop (e.g. $env:USERPROFILE\scoop)"
if (-not $scoopDir) { $scoopDir = "$env:USERPROFILE\scoop" }

# create directory
if (-not (Test-Path $scoopDir)) {
    New-Item -Path $scoopDir -ItemType Directory | Out-Null }

$env:SCOOP_HOME = $scoopDir
[Environment]::SetEnvironmentVariable('SCOOP_HOME', $scoopDir, 'User')

# install scoop
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
    Write-Host "Scoop installation failed. Please try again." -ForegroundColor Red
    return
}

# add scoop bucket
$supported_buckets = @(scoop bucket known)

$buckets = (
    "main", "extras", "versions", "games", "nerd-fonts" )

foreach ($bucket in $buckets) {
    if ($supported_buckets -contains $bucket) {
        continue }
    scoop bucket add $bucket
}

# update
scoop update

# install apps
$scoop_app_list = (
    "7zip","altsnap","bat","busybox","cacert",
    "cmake","crystaldiskinfo","crystaldiskmark",
    "dark","everything","ffmpeg","fzf","git",
    "hwmonitor","hxd","ida-free","innounp",
    "nginx","nodejs","ollydbg","potplayer",
    "prince","smartmontools","sudo","sunshine",
    "telnet","vim","wget","wireshark","x64dbg",
    "zoxide", "python"
)

for ($i = 0; $i -lt $scoop_app_list.Length; $i++) {
    if ($i % 5 -eq 0) { Write-Host "" }
    Write-Host "$i.$($scoop_app_list[$i])  " -NoNewline
}

$confirm = Read-Host -Prompt "Applications showed above will be installed. Are you sure you want to install them? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") { return }

$proxy = Read-Host -Prompt "Enter proxy address (e.g. noproxy)"
if ($proxy) { scoop config proxy $proxy }

foreach ($app in $scoop_app_list) {
    scoop search $($app) | Out-Null
    if (-not $?) {
        scoop install $($app) }
}
