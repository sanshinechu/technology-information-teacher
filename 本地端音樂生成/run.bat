@echo off
setlocal
chcp 65001 >nul

REM 改變到批次檔所在目錄
cd /d "%~dp0"

REM 檢查虛擬環境
if not exist "music_gen_env\Scripts\python.exe" (
    echo.
    echo ❌ 虛擬環境不存在或未完整安裝！
    echo 請先執行 install.bat 進行安裝
    echo.
    pause
    endlocal
    exit /b 1
)

REM 檢查 app.py
if not exist "app.py" (
    echo.
    echo ❌ app.py 不存在！
    echo.
    pause
    endlocal
    exit /b 1
)

echo.
echo ========================================
echo 🎵 啟動本地端音樂生成器
echo ========================================
echo.
echo 正在啟動應用...
echo 請稍候，約需 10-20 秒加載模型...
echo.

REM 直接使用虛擬環境的 Python 執行應用
music_gen_env\Scripts\python.exe app.py

pause
endlocal
