# GitHub上传技能 2.0

此技能允许智能体从Trea IDE直接上传文件到GitHub仓库，智能体将自主完成仓库创建、文件上传、认证处理等操作。

## 功能特性

- ✅ 智能体自主上传（无需用户手动操作）
- ✅ 自动创建新的GitHub仓库
- ✅ 批量上传单个或多个文件到GitHub
- ✅ 智能处理GitHub认证（支持多种认证方式）
- ✅ 自动解决常见的上传问题
- ✅ 支持命令行参数
- ✅ 详细的使用文档
- ✅ 支持环境变量、配置文件和Git设置等多种配置方式

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

### 方法一：智能体自主上传（推荐）

**智能体将自动完成以下步骤**：

1. **检测用户需求**：识别用户想要上传文件到GitHub的请求
2. **收集必要信息**：
   - GitHub个人访问令牌（从环境变量、配置文件或用户输入获取）
   - GitHub用户名（从环境变量、配置文件、Git设置或用户输入获取）
   - 目标仓库名称（从用户输入获取）
   - 要上传的文件或目录路径（从用户输入或当前目录获取）
3. **执行上传操作**：
   - 自动创建GitHub仓库（如果不存在）
   - 批量上传文件到GitHub
   - 处理上传过程中的错误和异常
4. **返回结果**：
   - 上传成功的文件列表和GitHub链接
   - 遇到的问题和解决方案

**用户只需提供**：
- GitHub个人访问令牌（首次使用时）
- 目标仓库名称
- 要上传的文件或目录路径

### 方法二：使用Python脚本

```bash
# 上传单个文件
python scripts/upload_to_github.py --repo 仓库名 --file 要上传的文件

# 上传目录
python scripts/upload_to_github.py --repo 仓库名 --directory 目录路径

# 创建仓库并上传
python scripts/upload_to_github.py --repo 仓库名 --file 要上传的文件 --create-repo
```

### 方法三：使用Git命令行

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

### 示例1：智能体自主上传

**用户请求**：
```
请帮我将当前项目上传到GitHub，仓库名称为 "my-project"
```

**智能体操作**：
1. 检测用户需求：需要将当前项目上传到GitHub
2. 收集信息：
   - 从环境变量或配置文件获取GitHub令牌和用户名
   - 确认仓库名称："my-project"
   - 确定要上传的目录：当前目录
3. 执行操作：
   - 检查是否存在名为 "my-project" 的仓库
   - 如果不存在，创建新仓库
   - 批量上传当前目录中的所有文件
   - 处理上传过程中的错误
4. 返回结果：
   ```
   成功将项目上传到GitHub仓库 "my-project"！
   
   上传的文件：
   - README.md → https://github.com/your-username/my-project/blob/main/README.md
   - main.py → https://github.com/your-username/my-project/blob/main/main.py
   - requirements.txt → https://github.com/your-username/my-project/blob/main/requirements.txt
   
   仓库地址：https://github.com/your-username/my-project
   ```

### 示例2：智能体上传指定文件

**用户请求**：
```
请帮我将 "data.csv" 文件上传到GitHub仓库 "my-datasets"
```

**智能体操作**：
1. 检测用户需求：需要上传指定文件到GitHub
2. 收集信息：
   - 从环境变量或配置文件获取GitHub令牌和用户名
   - 确认仓库名称："my-datasets"
   - 确认要上传的文件："data.csv"
3. 执行操作：
   - 检查是否存在名为 "my-datasets" 的仓库
   - 如果不存在，创建新仓库
   - 上传 "data.csv" 文件
   - 处理上传过程中的错误
4. 返回结果：
   ```
   成功将文件 "data.csv" 上传到GitHub仓库 "my-datasets"！
   
   文件地址：https://github.com/your-username/my-datasets/blob/main/data.csv
   仓库地址：https://github.com/your-username/my-datasets
   ```

### 示例3：使用Python脚本上传

1. **上传单个文件**：
   ```bash
   python scripts/upload_to_github.py --repo test-repo --file hello.py
   ```

2. **创建仓库并上传**：
   ```bash
   python scripts/upload_to_github.py --repo new-repo --file hello.py --create-repo --repo-description "测试仓库"
   ```

3. **上传目录**：
   ```bash
   python scripts/upload_to_github.py --repo my-project --directory .
   ```

## 常见问题

### 1. SSL证书验证错误

**解决方案**：在requests请求中添加 `verify=False` 参数

### 2. 仓库不存在

**解决方案**：使用 `--create-repo` 参数创建仓库

### 3. 认证失败

**解决方案**：检查GitHub个人访问令牌是否有效，并且具有足够的权限

## 配置

### 配置方法

脚本会按以下顺序查找配置：
1. **命令行参数**：用户直接提供的参数
2. **环境变量**：GITHUB_TOKEN、GITHUB_OWNER、GITHUB_EMAIL
3. **配置文件**：config.py中的设置
4. **Git设置**：本地Git的user.name和user.email

### 方法一：使用配置文件

创建一个本地配置文件 `config.py`，存储你的GitHub令牌和用户名：

```python
# config.py
GITHUB_TOKEN = "你的GitHub个人访问令牌"
GITHUB_OWNER = "你的GitHub用户名"
GITHUB_EMAIL = "你的邮箱地址"
```

### 方法二：使用环境变量

```bash
# Windows
set GITHUB_TOKEN=你的令牌
set GITHUB_OWNER=你的用户名
set GITHUB_EMAIL=你的邮箱

# Linux/Mac
export GITHUB_TOKEN=你的令牌
export GITHUB_OWNER=你的用户名
export GITHUB_EMAIL=你的邮箱
```

### 方法三：使用Git设置

```bash
# 设置Git信息
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"

# 查看当前Git设置
git config user.name
git config user.email
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
