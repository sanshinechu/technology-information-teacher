@echo off
chcp 65001 >nul
cd /d "%~dp0"

REM 檢查虛擬環境
if not exist "music_gen_env" (
    echo ❌ 虛擬環境不存在！
    echo 請先執行 install.bat 進行安裝
    pause
    exit /b 1
)

REM 檢查 app.py
if not exist "app.py" (
    echo ❌ app.py 不存在！
    pause
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

REM 激活虛擬環境並執行應用
call music_gen_env\Scripts\activate.bat
python app.py

pause
