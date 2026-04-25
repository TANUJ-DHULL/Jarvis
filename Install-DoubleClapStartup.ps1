$startupFolder = [Environment]::GetFolderPath("Startup")
$targetPath = Join-Path $PSScriptRoot "Start-DoubleClapJarvis.bat"
$shortcutPath = Join-Path $startupFolder "Jarvis Double Clap Launcher.lnk"

if (-not (Test-Path $targetPath)) {
    Write-Host "Launcher batch file not found: $targetPath"
    exit 1
}

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.WorkingDirectory = $PSScriptRoot
$shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,2"
$shortcut.Save()

Write-Host "Startup shortcut created:"
Write-Host $shortcutPath
