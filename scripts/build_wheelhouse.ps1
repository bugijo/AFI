Param(
    [string]$Root = (Resolve-Path "$PSScriptRoot\..").Path
)

$wheelhouse = Join-Path $Root "wheelhouse"
New-Item -ItemType Directory -Force -Path $wheelhouse | Out-Null

py -m pip download --dest $wheelhouse -r (Join-Path $Root "requirements.txt")

$zipPath = Join-Path $Root "wheels.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}
Compress-Archive -Path (Join-Path $wheelhouse "*") -DestinationPath $zipPath
