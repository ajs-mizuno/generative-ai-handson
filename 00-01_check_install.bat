@echo off
setlocal ENABLEDELAYEDEXPANSION

REM 文字コード変更
chcp 65001

echo ================================
echo 開発環境セットアップ状況チェック
echo ================================

REM チェック用関数
call :check_command "Python" "python --version"
call :check_command "Docker" "docker --version"
call :check_command "Git" "git --version"

echo.
echo チェック完了。Enterキーで終了します。
pause > nul
exit /b

:check_command
set "toolname=%~1"
set "command=%~2"

echo.
echo [%toolname% チェック中...]

%command% > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo → %toolname% はインストールされています。
    %command%
) else (
    echo → %toolname% はインストールされていません、またはPATHが通っていません。
)
exit /b
