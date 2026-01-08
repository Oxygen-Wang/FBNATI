# GitHub 上传指南

## 前置要求

### 1. 安装 Git

如果您的系统中没有安装 Git，请先下载安装：

**Windows 下载地址**: https://git-scm.com/download/win

安装完成后，重启命令行窗口。

### 2. 配置 Git（首次使用）

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. GitHub 认证设置

您需要配置 GitHub 认证才能推送代码。有两种方式：

#### 方式一：使用 Personal Access Token（推荐）

1. 登录 GitHub
2. 进入 Settings → Developer settings → Personal access tokens → Tokens (classic)
3. 点击 "Generate new token (classic)"
4. 设置权限：至少勾选 `repo` 权限
5. 生成后复制 token（只显示一次，请保存好）

推送时，用户名输入您的 GitHub 用户名，密码输入刚才生成的 token。

#### 方式二：使用 SSH 密钥

1. 生成 SSH 密钥：
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

2. 将公钥添加到 GitHub：
   - 复制 `~/.ssh/id_ed25519.pub` 的内容
   - GitHub → Settings → SSH and GPG keys → New SSH key
   - 粘贴公钥并保存

3. 将远程仓库 URL 改为 SSH 格式：
```bash
git remote set-url origin git@github.com:Oxygen-Wang/FBNATI.git
```

## 上传步骤

### 方法一：使用批处理脚本（最简单）

1. 确保已安装 Git
2. 双击运行 `upload_to_github.bat`
3. 按照提示操作

### 方法二：手动执行命令

在 PowerShell 或命令提示符中，进入 `FBNATI1` 目录：

```bash
# 1. 初始化 Git 仓库
git init

# 2. 添加所有文件
git add .

# 3. 提交更改
git commit -m "Initial commit: FBNATI Python version"

# 4. 设置主分支为 main
git branch -M main

# 5. 添加远程仓库
git remote add origin https://github.com/Oxygen-Wang/FBNATI.git

# 6. 推送到 GitHub
git push -u origin main
```

**注意**：第 6 步会要求输入用户名和密码：
- 用户名：您的 GitHub 用户名
- 密码：使用 Personal Access Token（不是 GitHub 密码）

### 方法三：使用 GitHub Desktop（图形界面）

1. 下载安装 GitHub Desktop: https://desktop.github.com/
2. 登录您的 GitHub 账户
3. File → Add Local Repository → 选择 FBNATI1 文件夹
4. 点击 "Publish repository" 按钮
5. 输入仓库名称：FBNATI
6. 点击 "Publish repository"

## 常见问题

### Q: 提示 "remote origin already exists"
A: 执行以下命令删除后重新添加：
```bash
git remote remove origin
git remote add origin https://github.com/Oxygen-Wang/FBNATI.git
```

### Q: 推送时提示认证失败
A: 确保使用 Personal Access Token 而不是 GitHub 密码。如果使用 SSH，确保已配置 SSH 密钥。

### Q: 提示 "failed to push some refs"
A: 如果远程仓库已有内容，先拉取：
```bash
git pull origin main --allow-unrelated-histories
```
然后再推送。

## 验证上传

上传成功后，访问以下地址查看：
https://github.com/Oxygen-Wang/FBNATI

