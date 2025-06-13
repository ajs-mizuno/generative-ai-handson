@echo off
setlocal ENABLEDELAYEDEXPANSION

REM 文字コード変更
chcp 65001

REM ==== 設定 ====
set "VENV_DIR=venv"

echo ================================
echo Git 設定と Python 仮想環境の状態確認
echo ================================

REM Gitインストール確認
git --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Git が見つかりません。PATHが通っているか確認してください。
) else (
    echo.
    echo [Git のバージョンと設定情報]
    git --version
    echo ユーザー名: 
    git config --get user.name
    echo メールアドレス: 
    git config --get user.email
    echo デフォルトブランチ: 
    git config --get init.defaultBranch
)

REM 仮想環境存在確認
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo.
    echo 仮想環境 "%VENV_DIR%" が見つかりません。
    echo 環境がセットアップされていない可能性があります。
    pause
    exit /b 1
)

echo.
echo [Python 仮想環境のパッケージ一覧]

REM 仮想環境の有効化とpip freeze
call %VENV_DIR%\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo 仮想環境の有効化に失敗しました。
    pause
    exit /b 1
)

python --version
pip list

echo.
echo チェック完了。Enterキーで終了します。
pause > nul
exit /b
