# 快速上传到 GitHub

## ⚠️ 当前状态

您的系统当前**未安装 Git**，需要先安装才能上传代码。

## 🚀 三种安装 Git 的方法

### 方法 1：官方安装（推荐，5分钟）

1. 访问：https://git-scm.com/download/win
2. 下载 Windows 版本
3. 运行安装程序（全部使用默认选项即可）
4. **重要**：安装完成后**关闭并重新打开**命令行窗口
5. 验证安装：运行 `git --version`

### 方法 2：通过 conda 安装（如果您有管理员权限）

```bash
conda install -c conda-forge git
```

### 方法 3：通过 Chocolatey 安装（如果已安装 Chocolatey）

```bash
choco install git
```

## 📤 安装 Git 后的上传步骤

安装 Git 后，在 `FBNATI1` 目录下执行：

### 最简单的方式：双击运行
```
upload_to_github.bat
```

### 或者手动执行：

```bash
git init
git add .
git commit -m "Initial commit: FBNATI Python version"
git branch -M main
git remote add origin https://github.com/Oxygen-Wang/FBNATI.git
git push -u origin main
```

## 🔐 GitHub 认证

推送时会要求输入：
- **用户名**：您的 GitHub 用户名
- **密码**：使用 Personal Access Token（不是 GitHub 密码）

### 如何获取 Personal Access Token：

1. 登录 GitHub
2. 点击右上角头像 → Settings
3. 左侧菜单 → Developer settings
4. Personal access tokens → Tokens (classic)
5. Generate new token (classic)
6. 勾选 `repo` 权限
7. 生成后复制 token（只显示一次）

## ✅ 验证上传成功

访问：https://github.com/Oxygen-Wang/FBNATI

---

**需要帮助？** 查看 `GITHUB_UPLOAD_GUIDE.md` 获取详细说明。

