param([string]$Service)

$FILENAME = "$Service.txt"
Write-Host "Saving logs $Service to $FILENAME..." -ForegroundColor Green

$ComposeFile = Get-ChildItem -Path . -Recurse -Filter "docker-compose*.yaml" | Select-Object -First 1
if (-not $ComposeFile) {
    Write-Error "docker-compose.yaml not found"
    exit 1
}

docker compose -f $ComposeFile.FullName logs --no-color --tail=500 $Service | Out-File -FilePath $FILENAME -Encoding ASCII

$SizeKB = (Get-Item $FILENAME).Length / 1KB
Write-Host "Done: $FILENAME ($([math]::Round($SizeKB,1)) KB)" -ForegroundColor Green
Write-Host "Last 5 lines:" -ForegroundColor Yellow
Get-Content $FILENAME -Tail 5