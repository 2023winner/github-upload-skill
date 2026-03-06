# GitHub上传技能

此技能允许用户从Trea IDE直接上传文件到GitHub仓库，包括创建仓库、上传文件、处理认证等功能。

## 功能特性

- ✅ 创建新的GitHub仓库
- ✅ 上传单个或多个文件到GitHub
- ✅ 处理GitHub认证
- ✅ 解决常见的上传问题
- ✅ 支持命令行参数
- ✅ 详细的使用文档

## 前置条件

- GitHub个人访问令牌
- Python环境（需要安装requests库）
- 准备好要上传的文件

## 安装

1. 克隆此仓库：
   ```bash
   git clone https://github.com/2023winner/github-upload-skill.git
   ```

2. 安装依赖：
   ```bash
   pip install requests
   ```

## 使用方法

### 方法一：使用Python脚本

```bash
# 上传单个文件
python scripts/upload_to_github.py --token 你的令牌 --owner 你的用户名 --repo 仓库名 --file 要上传的文件

# 创建仓库并上传
python scripts/upload_to_github.py --token 你的令牌 --owner 你的用户名 --repo 仓库名 --file 要上传的文件 --create-repo
```

### 方法二：使用Git命令行

```bash
# 初始化仓库
git init
git config user.name "你的用户名"
git config user.email "你的邮箱"

# 添加和提交文件
git add .
git commit -m "从Trea IDE上传文件"

# 推送文件
git push https://你的令牌@github.com/你的用户名/仓库名.git main
```

## 示例

### 示例1：上传单个文件

```bash
python scripts/upload_to_github.py --token ghp_your_token --owner 2023winner --repo test-repo --file test_upload.py
```

### 示例2：创建仓库并上传

```bash
python scripts/upload_to_github.py --token ghp_your_token --owner 2023winner --repo new-repo --file test_upload.py --create-repo --repo-description "测试仓库"
```

## 常见问题

### 1. SSL证书验证错误

**解决方案**：在requests请求中添加 `verify=False` 参数

### 2. 仓库不存在

**解决方案**：使用 `--create-repo` 参数创建仓库

### 3. 认证失败

**解决方案**：检查GitHub个人访问令牌是否有效，并且具有足够的权限

## 配置

为了方便使用，你可以创建一个本地配置文件 `config.py`，存储你的GitHub令牌和用户名：

```python
# config.py
GITHUB_TOKEN = "你的GitHub个人访问令牌"
GITHUB_OWNER = "你的GitHub用户名"
```

然后修改上传脚本使用这些配置：

```python
# 在upload_to_github.py中
import config

# 使用配置
token = config.GITHUB_TOKEN
owner = config.GITHUB_OWNER
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
