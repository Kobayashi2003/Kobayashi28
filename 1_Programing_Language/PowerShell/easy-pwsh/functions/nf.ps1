# Quick File Creation
function nf { param($name) New-Item -ItemType "file" -Path . -Name $name }