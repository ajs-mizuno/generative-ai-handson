@echo off
setlocal ENABLEDELAYEDEXPANSION

REM 文字コード変更
chcp 65001

REM ==== 初期設定 ====
set "VENV_DIR=venv"
set "REQUIREMENTS_FILE=requirements.txt"

echo ================================
echo Python仮想環境セットアップ
echo ================================

REM Python インストール確認
python --version > nul 2>&1
if not %ERRORLEVEL%==0 (
    echo Python が見つかりません。PATHが通っているか確認してください。
    pause
    exit /b 1
)

REM 既存仮想環境の確認
if exist "%VENV_DIR%\" (
    echo 既に仮想環境 "%VENV_DIR%" は存在しています。
) else (
    echo 仮想環境 "%VENV_DIR%" を作成します...
    python -m venv %VENV_DIR%
    if %ERRORLEVEL% NEQ 0 (
        echo 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
)

REM 仮想環境の有効化
echo 仮想環境を有効化します...
call %VENV_DIR%\Scripts\activate.bat

REM pip 最新化
echo pipをアップグレードしています...
python -m pip install --upgrade pip

REM 必要パッケージのインストール
if exist "%REQUIREMENTS_FILE%" (
    echo "%REQUIREMENTS_FILE%" に基づきパッケージをインストール中...
    pip install -r %REQUIREMENTS_FILE%
) else (
    echo "%REQUIREMENTS_FILE%" が見つかりません。パッケージインストールはスキップします。
)

echo.
echo 仮想環境のセットアップが完了しました。
echo 仮想環境を有効化するには以下を実行してください：
echo     call %VENV_DIR%\Scripts\activate.bat
pause
exit /b
