$baseDirectory = "C:/Users/yjaquier/OneDrive - STMicroelectronics/Yannick/Development/"
$currentDir = (Get-Location).Path
# Write-Output $currentDir
$lastDirectory = Split-Path -Path $currentDir -Leaf

Write-Output "Copy started."

robocopy $currentDir (Join-Path -Path $baseDirectory -ChildPath $lastDirectory) /xd node_modules /xd dist /e /ts

Write-Output "Copy completed!"
# Pause the script (wait for user input)
Read-Host -Prompt "Press Enter to continue"