param(
    [string]$Pasta = "results-test-separate",
    [string[]]$Opcoes = @('--tokens')
)

$env:PYTHONUTF8 = 1

$Destination = "$PSScriptRoot\testes\resultados\$Pasta"
New-Item -ItemType Directory -Force $Destination | Out-Null

Get-ChildItem "$PSScriptRoot\testes\*.nesti" | ForEach-Object {
  python "$PSScriptRoot\Nesti_main.py" $_.FullName @Opcoes 2>&1 |
    Out-File "$Destination\$($_.BaseName).txt" -Encoding utf8
}

Write-Host "Saídas gravadas em $Destination"