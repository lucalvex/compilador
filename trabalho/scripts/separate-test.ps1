param(
  [string]$Pasta = "results-test-separate",
  [string[]]$Opcoes = @('--tokens')
)

$env:PYTHONUTF8 = 1
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Raiz = Split-Path $PSScriptRoot -Parent
$Destino = "$Raiz\testes\resultados\$Pasta"
New-Item -ItemType Directory -Force $Destino | Out-Null

Get-ChildItem "$Raiz\testes\*.nesti" | ForEach-Object {
    python "$Raiz\Nesti_main.py" $_.FullName @Opcoes 2>&1 |
      Out-File "$Destino\$($_.BaseName).txt" -Encoding utf8
}

Write-Host "Saídas gravadas em $Destino"