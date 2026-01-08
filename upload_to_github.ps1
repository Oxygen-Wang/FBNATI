# GitHub 上传脚本 (PowerShell)
# 编码: UTF-8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "上传 FBNATI1 到 GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 查找 Git 可执行文件
$gitPaths = @(
    "C:\Program Files\Git\bin\git.exe",
    "C:\Program Files (x86)\Git\bin\git.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\git.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Git\bin\git.exe",
    "$env:ProgramFiles\Git\bin\git.exe",
    "$env:ProgramFiles(x86)\Git\bin\git.exe"
)

$gitExe = $null
foreach ($path in $gitPaths) {
    if (Test-Path $path) {
        $gitExe = $path
        Write-Host "[找到] Git 位于: $path" -ForegroundColor Green
        break
    }
}

# 如果没找到，尝试在 PATH 中查找
if (-not $gitExe) {
    try {
        $gitVersion = & git --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $gitExe = "git"
            Write-Host "[找到] Git 在系统 PATH 中" -ForegroundColor Green
        }
    } catch {
        # Git 不在 PATH 中
    }
}

# 如果仍然没找到
if (-not $gitExe) {
    Write-Host "[错误] 未找到 Git 安装" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装 Git:" -ForegroundColor Yellow
    Write-Host "1. 访问: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "2. 下载并安装 Git" -ForegroundColor Yellow
    Write-Host "3. 安装完成后，关闭并重新打开此窗口" -ForegroundColor Yellow
    Write-Host "4. 再次运行此脚本" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按 Enter 键退出"
    exit 1
}

# Git 命令包装函数
function Invoke-Git {
    param([string[]]$Arguments)
    if ($gitExe -eq "git") {
        & git $Arguments
    } else {
        & $gitExe $Arguments
    }
}

# 1. 初始化 Git 仓库
Write-Host "[1/6] 初始化 Git 仓库..." -ForegroundColor Yellow
if (Test-Path .git) {
    Write-Host "Git 仓库已存在，跳过初始化" -ForegroundColor Gray
} else {
    Invoke-Git @("init")
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] Git 初始化失败" -ForegroundColor Red
        Read-Host "按 Enter 键退出"
        exit 1
    }
    Write-Host "Git 仓库初始化成功" -ForegroundColor Green
}

# 2. 配置 Git 用户信息
Write-Host ""
Write-Host "[配置] 设置 Git 用户信息..." -ForegroundColor Yellow
Invoke-Git @("config", "--global", "user.name", "Oxygen-Wang")
Invoke-Git @("config", "--global", "user.email", "653345983@qq.com")
Write-Host "Git 用户信息配置完成" -ForegroundColor Green

# 3. 添加所有文件
Write-Host ""
Write-Host "[2/6] 添加所有文件..." -ForegroundColor Yellow
Invoke-Git @("add", ".")
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 添加文件失败" -ForegroundColor Red
    Read-Host "按 Enter 键退出"
    exit 1
}
Write-Host "文件添加成功" -ForegroundColor Green

# 4. 提交更改
Write-Host ""
Write-Host "[3/6] 提交更改..." -ForegroundColor Yellow
Invoke-Git @("commit", "-m", "Initial commit: FBNATI Python version")
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 提交失败，可能是没有更改或已提交" -ForegroundColor Yellow
}

# 5. 设置主分支
Write-Host ""
Write-Host "[4/6] 设置主分支为 main..." -ForegroundColor Yellow
Invoke-Git @("branch", "-M", "main")
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 分支设置失败，可能已经是 main 分支" -ForegroundColor Yellow
}

# 6. 添加远程仓库
Write-Host ""
Write-Host "[5/6] 添加远程仓库..." -ForegroundColor Yellow
Invoke-Git @("remote", "remove", "origin") | Out-Null
Invoke-Git @("remote", "add", "origin", "https://github.com/Oxygen-Wang/FBNATI.git")
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 添加远程仓库失败" -ForegroundColor Red
    Read-Host "按 Enter 键退出"
    exit 1
}
Write-Host "远程仓库添加成功" -ForegroundColor Green

# 7. 推送到 GitHub
Write-Host ""
Write-Host "[6/6] 推送到 GitHub..." -ForegroundColor Yellow
Write-Host "请确保您已经配置了 GitHub 认证（Personal Access Token）" -ForegroundColor Cyan
Write-Host "如果提示输入密码，请使用 Personal Access Token，而不是 GitHub 密码" -ForegroundColor Cyan
Write-Host ""
Invoke-Git @("push", "-u", "origin", "main")
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[错误] 推送失败" -ForegroundColor Red
    Write-Host "可能的原因：" -ForegroundColor Yellow
    Write-Host "1. 未配置 GitHub 认证（需要 Personal Access Token）" -ForegroundColor Yellow
    Write-Host "2. 仓库不存在或没有权限" -ForegroundColor Yellow
    Write-Host "3. 网络连接问题" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "如何获取 Personal Access Token:" -ForegroundColor Cyan
    Write-Host "1. 登录 GitHub → Settings → Developer settings" -ForegroundColor Cyan
    Write-Host "2. Personal access tokens → Tokens (classic)" -ForegroundColor Cyan
    Write-Host "3. Generate new token (classic) → 勾选 repo 权限" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "上传成功！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "仓库地址: https://github.com/Oxygen-Wang/FBNATI.git" -ForegroundColor Cyan
Write-Host ""
Read-Host "按 Enter 键退出"

