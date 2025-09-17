@echo off
echo ========================================
echo   Oracle Eye - Servico de Coleta
echo ========================================
echo.

echo Iniciando Oracle Eye Service...
echo.
echo IMPORTANTE: 
echo - Mantenha este terminal aberto
echo - O servico ira coletar mensagens automaticamente
echo - Use outro terminal para comandos do Neural Core
echo.

cd oracle-eye
call venv\Scripts\activate
python src/main.py

echo.
echo Oracle Eye Service finalizado.
pause
