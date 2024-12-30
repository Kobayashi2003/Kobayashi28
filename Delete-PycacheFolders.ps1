# Function to delete __pycache__ folders
function Delete-PycacheFolders {
    $pycacheFolders = Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue

    foreach ($folder in $pycacheFolders) {
        try {
            Remove-Item $folder.FullName -Recurse -Force
            Write-Host "Deleted __pycache__ folder: $($folder.FullName)"
        }
        catch {
            Write-Host "Error deleting __pycache__ folder $($folder.FullName): $_"
        }
    }
}

# Main execution
Write-Host "Searching for and deleting __pycache__ folders..."
Delete-PycacheFolders
Write-Host "Cleanup complete."