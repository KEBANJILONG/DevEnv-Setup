# 🚀 DevEnv-Setup

<div align="center">

![CI](https://github.com/KEBANJILONG/DevEnv-Setup/workflows/CI/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Stars](https://img.shields.io/github/stars/KEBANJILONG/DevEnv-Setup.svg?style=social)

**一键开发环境配置工具 | One-Click Development Environment Setup**

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 🎯 项目简介

DevEnv-Setup 是一个强大的跨平台开发环境自动化配置工具，解决程序员最头疼的问题：

- ✅ 新电脑/重装系统后的环境配置
- ✅ 多项目管理与依赖版本冲突
- ✅ 团队开发环境统一化
- ✅ 开发工具自动安装与配置

### ⚡ 核心功能

#### 1️⃣ 智能环境检测
- 自动检测已安装的开发工具
- 分析系统环境变量配置
- 识别潜在冲突和问题

#### 2️⃣ 一键安装开发工具
支持主流开发工具链：

| 类别 | 工具 |
|------|------|
| **编程语言** | Node.js, Python, Go, Rust, Java, PHP, Ruby |
| **包管理器** | npm, yarn, pnpm, pip, conda, cargo, go mod |
| **版本管理** | nvm, pyenv, rustup, sdkman |
| **编辑器** | VS Code, JetBrains IDEs, Vim, Neovim |
| **数据库** | MySQL, PostgreSQL, MongoDB, Redis |
| **容器** | Docker, Podman, Kubernetes |
| **Git工具** | Git, GitHub CLI, GitLab CLI |

#### 3️⃣ 配置文件管理
- 自动备份现有配置
- 一键恢复开发环境
- 支持 `.env`, `.gitconfig`, SSH keys 等

### 🚀 快速开始

#### Windows (PowerShell)
```powershell
# 管理员权限运行
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/KEBANJILONG/DevEnv-Setup/main/install.ps1'))
```

#### macOS/Linux (Bash)
```bash
curl -fsSL https://raw.githubusercontent.com/KEBANJILONG/DevEnv-Setup/main/install.sh | bash
```

### 📖 使用示例

```bash
# 检测当前环境
devenv check

# 安装 Node.js 开发环境
devenv install nodejs

# 安装 Python 开发环境
devenv install python --version 3.11

# 安装完整 Web 开发环境
devenv install web-full

# 配置 Git
devenv config git --name "Your Name" --email "your@email.com"

# 备份当前配置
devenv backup --output ~/dev-env-backup.tar.gz

# 从备份恢复
devenv restore --input ~/dev-env-backup.tar.gz

# 生成项目模板
devenv new react my-app
devenv new django my-backend
```

### 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

### ⭐ Star History

如果这个项目对你有帮助，请给个 Star ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=KEBANJILONG/DevEnv-Setup&type=Date)](https://star-history.com/#KEBANJILONG/DevEnv-Setup&Date)

---

## English

### 🎯 Overview

DevEnv-Setup is a powerful cross-platform development environment automation tool that solves the most common headaches for developers:

- ✅ Environment setup after getting a new PC / reinstalling OS
- ✅ Multi-project management and dependency version conflicts
- ✅ Team development environment standardization
- ✅ Automated development tool installation and configuration

### ⚡ Core Features

#### 1️⃣ Smart Environment Detection
- Automatically detect installed development tools
- Analyze system environment variable configuration
- Identify potential conflicts and issues

#### 2️⃣ One-Click Tool Installation
Supports mainstream development toolchains:

| Category | Tools |
|----------|-------|
| **Languages** | Node.js, Python, Go, Rust, Java, PHP, Ruby |
| **Package Managers** | npm, yarn, pnpm, pip, conda, cargo, go mod |
| **Version Managers** | nvm, pyenv, rustup, sdkman |
| **Editors** | VS Code, JetBrains IDEs, Vim, Neovim |
| **Databases** | MySQL, PostgreSQL, MongoDB, Redis |
| **Containers** | Docker, Podman, Kubernetes |
| **Git Tools** | Git, GitHub CLI, GitLab CLI |

#### 3️⃣ Configuration File Management
- Automatic backup of existing configurations
- One-click environment restoration
- Support for `.env`, `.gitconfig`, SSH keys, etc.

### 🚀 Quick Start

#### Windows (PowerShell)
```powershell
# Run with administrator privileges
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/KEBANJILONG/DevEnv-Setup/main/install.ps1'))
```

#### macOS/Linux (Bash)
```bash
curl -fsSL https://raw.githubusercontent.com/KEBANJILONG/DevEnv-Setup/main/install.sh | bash
```

### 📖 Usage Examples

```bash
# Check current environment
devenv check

# Install Node.js development environment
devenv install nodejs

# Install Python development environment
devenv install python --version 3.11

# Install complete web development environment
devenv install web-full

# Configure Git
devenv config git --name "Your Name" --email "your@email.com"

# Backup current configuration
devenv backup --output ~/dev-env-backup.tar.gz

# Restore from backup
devenv restore --input ~/dev-env-backup.tar.gz

# Generate project template
devenv new react my-app
devenv new django my-backend
```

### 🤝 Contributing

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests.

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

### ⭐ Show Your Support

If this project helped you, please give it a ⭐ star!

---

<div align="center">

**Made with ❤️ by [KEBANJILONG](https://github.com/KEBANJILONG)**

</div>
