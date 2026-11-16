# Roda o compilador em todos os testes e grava tudo em um único arquivo.
# Uso: .\all-test.ps1

param(
  [string]$Saida = "results-all.txt",
  [string[]]$Opcoes = @('--tokens')
)

$env:PYTHONUTF8 = 1

Get-ChildItem "$PSScriptRoot\testes\*.nesti" | ForEach-Object {
  "=== $($_.Name)"
  python "$PSScriptRoot\Nesti_main.py" $_.FullName @Opcoes 2>&1
  ""
} | Out-File "testes\resultados\$Saida" -Encoding utf8

Write-Host "Resultados gravados em $Saida"