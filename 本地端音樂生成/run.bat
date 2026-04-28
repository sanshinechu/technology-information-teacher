@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 取得批次檔所在目錄的完整路徑
set "PROJECT_DIR=%~dp0"
set "PROJECT_DIR=!PROJECT_DIR:~0,-1!"
cd /d "!PROJECT_DIR!"

REM 驗證目錄
echo 專案目錄：!PROJECT_DIR!
echo 當前目錄：%cd%
echo.

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
call "!PROJECT_DIR!\music_gen_env\Scripts\activate.bat"
python "!PROJECT_DIR!\app.py"

pause
