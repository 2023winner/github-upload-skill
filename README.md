# GitHub Upload Skill

从 Trea IDE 上传文件到 GitHub 仓库的智能技能，自动完成仓库创建、文件上传、认证处理等操作。

## ✨ 功能特点

- ✅ 智能体自主上传（无需用户手动操作）
- ✅ 自动创建新的 GitHub 仓库
- ✅ 批量上传单个或多个文件到 GitHub
- ✅ 智能处理 GitHub 认证（支持多种认证方式）
- ✅ 自动解决常见的上传问题
- ✅ 支持环境变量、配置文件和 Git 设置等多种配置方式

## 📦 安装

1. 克隆此仓库：
```bash
git clone https://github.com/2023winner/github-upload-skill.git
cd github-upload-skill
```

2. 安装依赖：
```bash
pip install requests
```

3. 配置 GitHub 令牌（可选，技能已配置默认令牌）：
```bash
# Windows PowerShell
$env:GITHUB_TOKEN="your_token"
$env:GITHUB_OWNER="your_username"
```
## 🚀 使用方法

### 方法一：智能体自主上传（推荐）

智能体将自动完成以下步骤：
1. 检测用户需求
2. 收集必要信息（令牌、用户名、仓库名、文件路径）
3. 执行上传操作
4. 返回结果

### 方法二：使用 Python 脚本上传

```bash
# 上传单个文件
python scripts/upload_to_github.py --repo 仓库名 --file 要上传的文件

# 上传目录
python scripts/upload_to_github.py --repo 仓库名 --directory 目录路径

# 创建仓库并上传
python scripts/upload_to_github.py --repo 仓库名 --file 要上传的文件 --create-repo
```
## 🛠️ 技术栈

- Python
- GitHub API
- Requests

## 📁 目录结构

```
github-upload-skill/
├── src/              # 源代码目录
├── docs/             # 文档目录
├── tests/            # 测试文件
├── examples/         # 示例代码
├── README.md         # 项目说明
└── .gitignore        # Git 忽略文件
```

## ⚠️ 注意事项

不要在代码中硬编码 GitHub 个人访问令牌，建议使用环境变量或配置文件。
## 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件
