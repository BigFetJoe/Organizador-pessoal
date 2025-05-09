@echo off
echo === Compilando main.py para main.exe ===
python -m PyInstaller --onefile --noconsole main.py
echo.
echo === Compilação finalizada ===
echo O executável está em distmain.exe
pause
