param (
    [string]$inputArg
)

if (-not $inputArg) {
    Write-Output "Usage: .\robocopy_from_ondrive.ps1 <disk drive letter>"
    exit 1
}

# Test if $inputArg is exactly one letter (case-insensitive)
if ($inputArg -match '^[a-zA-Z]$') {
    Write-Output "Target drive received: $inputArg"
} else {
    Write-Output "Error: Parameter must be a single letter (A-Z or a-z)."
    exit 1
}

$driveRoot = "${inputArg}:"
$baseDirectory = '/Yannick/Development/'
$currentDir = (Get-Location).Path
$lastDirectory = Split-Path -Path $currentDir -Leaf
# Join $inputArg as the first segment
$pathWithInput = Join-Path -Path $driveRoot -ChildPath $baseDirectory

# Then join the last directory
$finalPath = Join-Path -Path $pathWithInput -ChildPath $lastDirectory
# Write-Output $finalPath

Write-Output "Copy started."

robocopy $currentDir $finalPath /xd node_modules /xd dist /e /ts 

Write-Output "Copy completed!"
# Pause the script (wait for user input)
Read-Host -Prompt "Press Enter to continue"