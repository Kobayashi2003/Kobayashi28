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

function Show-FileInfo {
<#
.SYNOPSIS
    Show file info
.EXAMPLE
    PS> Get-FileInfo $file_path
#>

    param (
        [Parameter(Mandatory=$true)]
        [string] $file_path
    )

    $esc = [char]27

    try {
        $fileInfo = Get-Item -LiteralPath $file_path
        $file_name = $fileInfo.Name
        $file_extension = $fileInfo.Extension
        $file_length = $fileInfo.Length
        $file_lastWriteTime = $fileInfo.LastWriteTime

        # format file size to B KB MB or GB
        if ($file_length -gt 1GB) {
            $file_size = "{0:N2} GB" -f ($file_length / 1GB)
        } elseif ($file_length -gt 1MB) {
            $file_size = "{0:N2} MB" -f ($file_length / 1MB)
        } elseif ($file_length -gt 1KB) {
            $file_size = "{0:N2} KB" -f ($file_length / 1KB)
        } else {
            $file_size = "{0:N2} B" -f $file_length
        }

        Write-Host "${esc}[33mFile Path: ${file_path}${esc}[0m"
        Write-Host "${esc}[33mFile Name: ${file_name}${esc}[0m"
        Write-Host "${esc}[33mFile Extension: ${file_extension}${esc}[0m"
        Write-Host "${esc}[33mFile Size: ${file_size}${esc}[0m"
        Write-Host "${esc}[33mFile LastWriteTime: ${file_lastWriteTime}${esc}[0m"
    } catch {
        Write-Host "${esc}[31mError: $($_.Exception.Message)${esc}[0m"
    }

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
        $esc = [char]27
        Write-Host "${esc}[31mError: $($_.Exception.Message)${esc}[0m"
        Write-Host ""
        Show-FileInfo $file_path
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

    $esc = [char]27

    try {
        Write-Output "Text: $file_path"
        if (-not (Get-Command 'bat' -ErrorAction SilentlyContinue)) {
            & bat $file_path
        } else {
            Get-Content $file_path
        }
    } catch {
        Write-Host "${esc}[31mError: $($_.Exception.Message)${esc}[0m"
        Write-Host ""
        Show-FileInfo $file_path
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

    $esc = [char]27

    try {
        throw "Video Format Not Implemented"
    } catch {
        Write-Host "${esc}[31mError: $($_.Exception.Message)${esc}[0m"
        Write-Host ""
        Show-FileInfo $file_path
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

    $esc = [char]27

    try {
        throw "Audio Format Not Implemented"
    } catch {
        Write-Host "${esc}[31mError: $($_.Exception.Message)${esc}[0m"
        Write-Host ""
        Show-FileInfo $file_path
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

    $esc = [char]27

    try {
        $content = (& "7z" "l" "-ba" "$file_path")
        Write-Output "Archive: $file_path"
        foreach ($line in $content) {
            Write-Output $line
        }
    } catch {
        Write-Host "${esc}[31mError: $($_.Exception.Message)${esc}[0m"
        Write-Host ""
        Show-FileInfo $file_path
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

    $esc = [char]27

    try {
        Write-Output "Binary: $file_path"
        if (Get-Command 'get-hex-dump' -ErrorAction SilentlyContinue) {
            get-hex-dump $file_path
        } elseif (Get-Command 'Format-Hex' -ErrorAction SilentlyContinue) {
            if ($global:PSVERSION -gt 6.0) {
                Format-Hex $file_path -Count ($preview_width * $preview_height)
            } else {
                Format-Hex $file_path
            }
        } else {
            throw "Binary Format Not Implemented"
        }
    } catch {
        # Write-Host "Error: $($_.Exception.Message)"
        Write-Host "${esc}[31mError: $($_.Exception.Message)${esc}[0m"
        Write-Host ""
        Show-FileInfo $file_path
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
