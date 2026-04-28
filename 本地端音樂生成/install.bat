@echo off
chcp 65001 >nul

echo.
echo ========================================
echo 🎵 本地端 AI 音樂生成系統安裝
echo ========================================
echo.

REM 改變到批次檔所在目錄
cd /d "%~dp0"
echo 安裝目錄：%cd%
echo.

REM 檢查虛擬環境是否存在
if not exist "music_gen_env" (
    echo ❌ 虛擬環境不存在，正在創建...
    python -m venv music_gen_env
    if errorlevel 1 (
        echo ❌ 虛擬環境創建失敗！
        pause
        exit /b 1
    )
    echo ✅ 虛擬環境已創建
) else (
    echo ✅ 虛擬環境已存在
)

echo.
echo ========================================
echo 📦 安裝套件...
echo ========================================
echo.

REM 使用虛擬環境的 Python 和 pip
set "PYTHON=%cd%\music_gen_env\Scripts\python.exe"
set "PIP=%cd%\music_gen_env\Scripts\pip.exe"

REM 升級 pip
echo [1/4] 升級 pip...
"%PIP%" install --upgrade pip
if errorlevel 1 (
    echo ⚠️ pip 升級失敗，繼續嘗試...
)

REM 安裝 PyTorch (CUDA)
echo.
echo [2/4] 安裝 PyTorch (CUDA 12.1 版本)...
echo 這會下載約 2-3 GB，請耐心等待...
"%PIP%" install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 (
    echo ❌ PyTorch 安裝失敗！
    pause
    exit /b 1
)
echo ✅ PyTorch 安裝完成

REM 安裝 AudioCraft
echo.
echo [3/4] 安裝 AudioCraft...
"%PIP%" install audiocraft
if errorlevel 1 (
    echo ❌ AudioCraft 安裝失敗！
    pause
    exit /b 1
)
echo ✅ AudioCraft 安裝完成

REM 安裝 Gradio
echo.
echo [4/4] 安裝 Gradio...
"%PIP%" install gradio
if errorlevel 1 (
    echo ❌ Gradio 安裝失敗！
    pause
    exit /b 1
)
echo ✅ Gradio 安裝完成

echo.
echo ========================================
echo ✅ 所有套件安裝完成！
echo ========================================
echo.
echo 接下來的步驟：
echo 1. 確保 app.py 已在專案目錄中
echo 2. 執行 run.bat 來啟動應用
echo 3. 在瀏覽器中打開 http://127.0.0.1:7860
echo.
pause
