<#
.SYNOPSIS
	Converts a .md file into a pdf file
.DESCRIPTION
	This PowerShell script converts a .md file into a pdf file.
.PARAMETER Path
	Specifies the path to the .md file
.EXAMPLE
	PS> ./convert-md2pdf.ps1 -Path "C:\Users\Markus\Documents\PowerShell\README.md"
#>

param([string]$Path = "")

try {
    # pandoc and latex are required for this script to work
    if (-not (Get-Command "pandoc" -ErrorAction SilentlyContinue)) {
        throw "Pandoc is required for this script to work"
    }
    if (-not (Get-Command "latex" -ErrorAction SilentlyContinue)) {
        throw "Latex is required for this script to work"
    }

	if ($Path -eq "" ) { $Path = read-host "Enter path to markdown file" }

    $pdfPath = $Path -replace ".md$", ".pdf"

    & pandoc --pdf-engine=xelatex `
             -f markdown-raw_tex `
             -f markdown-implicit_figures `
             -V CJKmainfont="KaiTi" `
             -V geometry:"top=2cm, bottom=1.5cm, left=2cm, right=2cm" `
             --highlight-style=tango `
             --toc `
             -t pdf `
             -o $pdfPath `
             $Path `
             *>$null

    if ($lastExitCode -ne "0") { throw "Pandoc failed with exit code $lastExitCode" }

    "✔️ Converted $Path to $pdfPath"
	exit 0 # success
} catch {
	"⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}