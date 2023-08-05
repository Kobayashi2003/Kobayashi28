# 取自：https://www.cnblogs.com/yinghualuowu/p/11418577.html

function Set-Wallpaper($image){
$source = @"
using System;
using System.Runtime.InteropServices;

public class Params
{
    [DllImport("User32.dll",CharSet=CharSet.Unicode)]
    public static extern int SystemParametersInfo (Int32 uAction,
                                                    Int32 uParam,
                                                    String lpvParam,
                                                    Int32 fuWinIni);
}
"@

Add-Type -TypeDefinition $source

$SPI_SETDESKWALLPAPER = 0x0014
$UpdateIniFile = 0x01
$SendChangeEvent = 0x02

$fWinIni = $UpdateIniFile -bor $SendChangeEvent

$ret = [Params]::SystemParametersInfo($SPI_SETDESKWALLPAPER, 0, $Image, $fWinIni)
}

Set-Wallpaper 'D:\BaiduNetdiskDownload\KOBAYASHI\Z\EC0AC931DAAD9BF1C780753D5F3D7B28.png'