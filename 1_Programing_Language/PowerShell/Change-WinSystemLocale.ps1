# [ref](https://learn.microsoft.com/zh-cn/windows-hardware/manufacture/desktop/default-input-locales-for-windows-language-packs?view=windows-11)

# change locale of windows system between zh-CN and ja-JP
function Change-WinSystemLocale {
    # get current locale
    $currentLocale = Get-WinSystemLocale
    # change locale
    if ($currentLocale -eq "zh-CN") {
        Set-WinSystemLocale ja-JP
    } else {
        Set-WinSystemLocale zh-CN
    }
    # check if want to restart now
    $restart = Read-Host "Do you want to restart now? (y/[n])"
    if  ($restart -eq 'y') {
        Restart-Computer
    }
}

Change-WinSystemLocale