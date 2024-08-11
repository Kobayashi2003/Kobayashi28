$IMAGE_TYPES = @(
    'bmp','gif','ico','jpg','jpeg','png',
    'tif','tiff','webp','svg'
)

$TEXT_TYPES = @(
    'md','markdown','mdown','mkd','txt','bat',
    'c','cc','h','hh','java','py',
    'rb','sh','vim','yaml','yml','xml',
    'json','csv','tsv','log','out','err',
    'html','htm','css','js','php','pl',
    'ps0','psm1','psd1','ps1xml','psm1xml','psd1xml',
    'ps1xml'
)

$VIDEO_TYPES = @(
    'avi','flv','mkv','mov','mp4','mpeg',
    'mpg','rm','swf','vob','wmv'
)

$AUDIO_TYPES = @(
    'aac','flac','m4a','mp3','ogg','opus',
    'wav','webm'
)

$ARCHIVE_TYPES = @(
    '7z','bz2','gz','rar','tar','zip'
)

$BINARY_TYPES = @(
    'exe'
)


function Get-MimeType {
<#
    .SYNOPSIS
        Get file mime type
    .EXAMPLE
        PS> Get-MimeType $file_path
#>

    param (
        [Parameter(Mandatory=$true)]
        [string] $file_path
    )

    $fileInfo = Get-Item -LiteralPath $file_path
    $mimeType = $fileInfo.Extension
    if (-not $mimeType) {
        $mimeType = 'unknown'
    }
    $mimeType = $mimeType.Substring(1)
    return $mimeType
}


function Show-ImageType {
<#
    .SYNOPSIS
        Show image files by chafa
    .EXAMPLE
        PS> Show-ImageType C:/img.jpg 100 100
#>
    param (
        [Parameter(Mandatory=$true)]
        [string] $file_path,
        [Parameter(Mandatory=$true)]
        [int] $preview_width,
        [Parameter(Mandatory=$true)]
        [int] $preview_height
    )

    try {
        Add-Type -AssemblyName System.Drawing
        $image = [System.Drawing.Image]::FromFile($file_path)
        $image_width  = $image.Width
        $image_height = $image.Height

        Write-Output "Image: $file_path"
        chafa -s $preview_width"x"$preview_height $file_path --optimize 9 --fill all
        Write-Output "mSize: ${image_width}x${image_height}"
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
    }

}


function Show-TextType {
<#
    .SYNOPSIS
        Show text files
    .EXAMPLE
        PS> Show-TextType C:/text.txt 100 100
#>
    param (
        [Parameter(Mandatory=$true)]
        [string] $file_path,
        [Parameter(Mandatory=$true)]
        [int] $preview_width,
        [Parameter(Mandatory=$true)]
        [int] $preview_height
    )

    try {
        Write-Output "Text: $file_path"
        $text = Get-Content $file_path -Raw
        Write-Output $text
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
    }

}


function Show-VideoType {
<#
    .SYNOPSIS
        Show video files
    .EXAMPLE
        PS> Show-VideoType C:/video.mp4 100 100
#>
    param (
        [Parameter(Mandatory=$true)]
        [string] $file_path,
        [Parameter(Mandatory=$true)]
        [int] $preview_width,
        [Parameter(Mandatory=$true)]
        [int] $preview_height
    )

    try {

        $file = Get-Item -LiteralPath $file_path
        $file_name = $file.Name
        $file_type = $file.Extension
        $file_size = $file.Length
        $file_time = $file.LastWriteTime

        Write-Output "Name: $file_name"
        Write-Output "Type: $file_type"
        Write-Output "Size: $file_size"
        Write-Output "Time: $file_time"

        throw "Video Format Not Implemented"

    } catch {
        Write-Host "Error: $($_.Exception.Message)"
    }
}


function Show-AudioType {
<#
    .SYNOPSIS
        Show audio files
    .EXAMPLE
        PS> Show-AudioType C:/audio.mp3 100 100
#>
    param (
        [Parameter(Mandatory=$true)]
        [string] $file_path,
        [Parameter(Mandatory=$true)]
        [int] $preview_width,
        [Parameter(Mandatory=$true)]
        [int] $preview_height
    )

    try {
        $file = Get-Item -LiteralPath $file_path
        $file_name = $file.Name
        $file_type = $file.Extension
        $file_size = $file.Length
        $file_time = $file.LastWriteTime

        Write-Output "Name: $file_name"
        Write-Output "Type: $file_type"
        Write-Output "Size: $file_size"
        Write-Output "Time: $file_time"

        throw "Audio Format Not Implemented"
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
    }
}


function Show-ArchiveType {
<#
    .SYNOPSIS
        Show the files in an archive
    .EXAMPLE
        PS> Show-ArchiveType C:/archive.zip 100 100
#>
    param (
        [Parameter(Mandatory=$true)]
        [string] $file_path,
        [Parameter(Mandatory=$true)]
        [int] $preview_width,
        [Parameter(Mandatory=$true)]
        [int] $preview_height
    )

    try {
        $content = (& "7z" "l" "-ba" "$file_path")
        Write-Output "Archive: $file_path"
        foreach ($line in $content) {
            Write-Output $line
        }
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
    }
}


function Show-BinaryType {
<#
    .SYNOPSIS
        Show binary files in Hex
    .EXAMPLE
        PS> Show-BinaryType C:/binary.exe 100 100
#>
    param (
        [Parameter(Mandatory=$true)]
        [string] $file_path,
        [Parameter(Mandatory=$true)]
        [int] $preview_width,
        [Parameter(Mandatory=$true)]
        [int] $preview_height
    )

    try {
        get-hex-dump $file_path
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
    }
}


try {

    $previewer_script_path  = $args[0]
    $file_path              = $args[1]
    $previewer_width        = $args[2]
    $previewer_height       = $args[3]

    $file_type = Get-MimeType $file_path

    if ($IMAGE_TYPES -contains $file_type) {
        Show-ImageType $file_path $previewer_width $previewer_height
        return
    }

    if ($TEXT_TYPES -contains $file_type) {
        Show-TextType $file_path $previewer_width $previewer_height
        return
    }

    if ($VIDEO_TYPES -contains $file_type) {
        Show-VideoType $file_path $previewer_width $previewer_height
        return
    }

    if ($AUDIO_TYPES -contains $file_type) {
        Show-AudioType $file_path $previewer_width $previewer_height
        return
    }

    if ($ARCHIVE_TYPES -contains $file_type) {
        Show-ArchiveType $file_path $previewer_width $previewer_height
        return
    }

    Show-BinaryType $file_path $previewer_width $previewer_height

} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
