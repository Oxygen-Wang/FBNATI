@echo off
chcp 65001 >nul
echo ========================================
echo 上传 FBNATI1 到 GitHub
echo ========================================
echo.

REM 检查 Git 是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Git，请先安装 Git
    echo 下载地址: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/6] 初始化 Git 仓库...
if exist .git (
    echo Git 仓库已存在，跳过初始化
) else (
    git init
    if errorlevel 1 (
        echo [错误] Git 初始化失败
        pause
        exit /b 1
    )
    echo Git 仓库初始化成功
)

echo.
echo [2/6] 添加所有文件...
git add .
if errorlevel 1 (
    echo [错误] 添加文件失败
    pause
    exit /b 1
)
echo 文件添加成功

echo.
echo [3/6] 提交更改...
git commit -m "Initial commit: FBNATI Python version"
if errorlevel 1 (
    echo [警告] 提交失败，可能是没有更改或已提交
)

echo.
echo [4/6] 设置主分支为 main...
git branch -M main
if errorlevel 1 (
    echo [警告] 分支设置失败，可能已经是 main 分支
)

echo.
echo [5/6] 添加远程仓库...
git remote remove origin 2>nul
git remote add origin https://github.com/Oxygen-Wang/FBNATI.git
if errorlevel 1 (
    echo [错误] 添加远程仓库失败
    pause
    exit /b 1
)
echo 远程仓库添加成功

echo.
echo [6/6] 推送到 GitHub...
echo 请确保您已经配置了 GitHub 认证（Personal Access Token 或 SSH 密钥）
git push -u origin main
if errorlevel 1 (
    echo.
    echo [错误] 推送失败
    echo 可能的原因：
    echo 1. 未配置 GitHub 认证
    echo 2. 仓库不存在或没有权限
    echo 3. 网络连接问题
    echo.
    echo 请检查后重试
    pause
    exit /b 1
)

echo.
echo ========================================
echo 上传成功！
echo ========================================
echo 仓库地址: https://github.com/Oxygen-Wang/FBNATI.git
pause

