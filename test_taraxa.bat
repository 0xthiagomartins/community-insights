@echo off
echo ========================================
echo   Community Insights - Teste Taraxa
echo ========================================
echo.

echo [1/5] Configurando projeto Taraxa...
cd neural-core
call venv\Scripts\activate
python src/main.py setup-project --name "Taraxa" --group "@taraxa_project"
if %errorlevel% neq 0 (
    echo ERRO: Falha ao configurar projeto
    pause
    exit /b 1
)
echo.

echo [2/5] Solicitando coleta imediata...
python src/main.py collect-now --project "Taraxa"
if %errorlevel% neq 0 (
    echo ERRO: Falha ao solicitar coleta
    pause
    exit /b 1
)
echo.

echo [3/5] Aguardando processamento (30 segundos)...
timeout /t 30 /nobreak > nul
echo.

echo [4/5] Verificando status da coleta...
python src/main.py check-status --project "Taraxa"
echo.

echo [5/5] Gerando resumo com IA...
python src/main.py generate-summary --project "Taraxa" --days 7
if %errorlevel% neq 0 (
    echo ERRO: Falha ao gerar resumo
    pause
    exit /b 1
)
echo.

echo ========================================
echo   Teste concluido com sucesso!
echo ========================================
echo.
echo IMPORTANTE: Oracle Eye deve estar rodando em outro terminal
echo para processar os comandos de coleta.
echo.
pause
