# Roda o compilador em todos os testes e grava tudo em um único arquivo.
# Uso: .\scripts\all-test.ps1
#      .\scripts\all-test.ps1 -Opcoes '--ast'

param(
  [string]$Saida = "results-all.txt",
  [string[]]$Opcoes = @('--tokens')
)

$env:PYTHONUTF8 = 1
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Raiz = Split-Path $PSScriptRoot -Parent
$PastaResultados = "$Raiz\testes\resultados"
New-Item -ItemType Directory -Force $PastaResultados | Out-Null
$Arquivo = "$PastaResultados\$Saida"

Get-ChildItem "$Raiz\testes\*.nesti" | ForEach-Object {
  "=== $($_.Name)"
  python "$Raiz\Nesti_main.py" $_.FullName @Opcoes 2>&1
  ""
} | Out-File $Arquivo -Encoding utf8

Write-Host "Resultados gravados em $Arquivo"