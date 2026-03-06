---
name: github-upload
description: 从Trea IDE上传文件到GitHub仓库。当用户需要将本地项目或文件上传到GitHub时使用此技能，包括创建仓库、上传文件、处理认证等功能。
compatibility:
  - tools: [Read, Write, RunCommand]
  - dependencies: [requests, base64]
---

# GitHub上传技能

## 功能描述

此技能允许用户从Trea IDE直接上传文件到GitHub仓库，包括以下功能：

- 创建新的GitHub仓库
- 上传单个或多个文件到GitHub
- 处理GitHub认证
- 解决常见的上传问题

## 前置条件

在使用此技能之前，用户需要：

1. **GitHub个人访问令牌**：用于认证GitHub API请求
2. **Python环境**：需要安装requests库
3. **文件准备**：准备好要上传的文件

## 生成GitHub个人访问令牌

1. 访问 [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token"
3. 选择适当的权限（至少需要 `repo` 权限）
4. 生成令牌并保存好

## 使用方法

### 方法一：使用Python脚本上传

1. **创建上传脚本**：

```python
#!/usr/bin/env python3
"""
通过GitHub API上传文件到GitHub仓库
"""

import requests
import base64

# GitHub认证信息
GITHUB_TOKEN = "你的GitHub个人访问令牌"
OWNER = "你的GitHub用户名"
REPO = "目标仓库名称"
BRANCH = "main"  # 或 "master"

# 读取文件内容
def read_file(file_path):
    """
    读取文件内容并转换为base64编码
    """
    with open(file_path, 'rb') as f:
        content = f.read()
    return base64.b64encode(content).decode('utf-8')

# 创建仓库
def create_repository():
    """
    创建GitHub仓库
    """
    url = f"https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": REPO,
        "description": "从Trea IDE上传的项目",
        "private": False
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    print(f"创建仓库响应: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.status_code == 201

# 上传文件
def upload_file(file_path, file_name):
    """
    上传文件到GitHub仓库
    """
    # 读取文件内容
    content = read_file(file_path)
    
    # 构建API URL
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{file_name}"
    
    # 请求头
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 请求数据
    data = {
        "message": "从Trea IDE上传文件",
        "content": content,
        "branch": BRANCH
    }
    
    # 发送请求
    response = requests.put(url, headers=headers, json=data, verify=False)
    print(f"上传文件响应: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.status_code in [201, 200]

if __name__ == "__main__":
    # 先创建仓库
    print("正在创建GitHub仓库...")
    create_repository()
    
    # 上传文件
    print("\n正在上传文件...")
    upload_file("要上传的文件路径", "文件在GitHub中的名称")
```

2. **修改脚本参数**：
   - `GITHUB_TOKEN`：填写你的GitHub个人访问令牌
   - `OWNER`：填写你的GitHub用户名
   - `REPO`：填写目标仓库名称
   - `BRANCH`：填写目标分支名称（通常是main或master）
   - `upload_file`函数的参数：填写要上传的文件路径和在GitHub中的名称

3. **运行脚本**：
   ```bash
   python upload_to_github.py
   ```

### 方法二：使用Git命令行上传

1. **初始化Git仓库**：
   ```bash
   git init
   ```

2. **设置Git用户信息**：
   ```bash
   git config user.name "你的GitHub用户名"
   git config user.email "你的邮箱地址"
   ```

3. **添加文件到暂存区**：
   ```bash
   git add .
   ```

4. **提交文件**：
   ```bash
   git commit -m "从Trea IDE上传文件"
   ```

5. **创建GitHub仓库**：
   在GitHub网站上创建一个新仓库

6. **添加远程仓库**：
   ```bash
   git remote add origin https://github.com/你的用户名/仓库名称.git
   ```

7. **推送文件**：
   ```bash
   git push https://你的GitHub令牌@github.com/你的用户名/仓库名称.git 分支名称
   ```

## 常见问题及解决方案

### 1. SSL证书验证错误

**错误信息**：
```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**解决方案**：
在requests请求中添加 `verify=False` 参数：
```python
response = requests.post(url, headers=headers, json=data, verify=False)
```

### 2. 仓库不存在

**错误信息**：
```
remote: Repository not found.
fatal: repository 'https://github.com/用户名/仓库名.git/' not found
```

**解决方案**：
先创建仓库，然后再推送文件。可以使用GitHub API或在GitHub网站上手动创建。

### 3. 认证失败

**错误信息**：
```
remote: Invalid username or password.
fatal: Authentication failed for 'https://github.com/用户名/仓库名.git/'
```

**解决方案**：
确保使用正确的GitHub个人访问令牌，并且令牌具有足够的权限。

### 4. MCP GitHub工具认证问题

**问题**：
Trea IDE的内置GitHub MCP工具可能遇到认证问题，导致API调用失败。

**解决方案**：
使用Python脚本通过GitHub API直接上传文件，或使用Git命令行工具。

### 5. 命令解析问题

**问题**：
在使用trae-sandbox执行包含空格或特殊字符的命令时，可能会遇到解析错误。

**解决方案**：
- 使用更简单的命令格式
- 避免在命令中使用特殊字符和空格
- 对于复杂命令，使用Python脚本替代

### 6. 配置文件路径问题

**问题**：
脚本可能无法找到配置文件，特别是当脚本在子目录中时。

**解决方案**：
在脚本中添加路径处理，确保能够找到配置文件：
```python
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
```

### 7. PowerShell命令语法问题

**问题**：
PowerShell不支持 `&&` 等bash风格的命令连接符。

**解决方案**：
分别执行每个命令，或使用PowerShell的语法：
```powershell
command1; command2; command3
```

### 8. 敏感文件上传问题

**问题**：
配置文件中包含敏感信息（如GitHub令牌），可能被误上传到GitHub。

**解决方案**：
- 创建 `.gitignore` 文件，添加敏感文件到忽略列表
- 在上传脚本中添加逻辑，跳过敏感文件的上传
- 使用环境变量或加密的配置管理方案

### 9. 文件大小限制

**问题**：
GitHub API对文件大小有限制（通常为100MB）。

**解决方案**：
- 对于大文件，使用Git命令行上传
- 考虑使用Git LFS（Large File Storage）
- 拆分大文件为多个小文件

### 10. 网络连接问题

**问题**：
网络连接不稳定或防火墙限制可能导致上传失败。

**解决方案**：
- 检查网络连接
- 尝试使用代理服务器
- 重试上传操作
- 确保GitHub API的访问权限

## 示例

### 示例1：上传单个Python文件

1. 创建上传脚本 `upload_single_file.py`：

```python
#!/usr/bin/env python3
import requests
import base64

GITHUB_TOKEN = "ghp_your_token"
OWNER = "your_username"
REPO = "test-repo"
BRANCH = "main"

# 读取文件内容
def read_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    return base64.b64encode(content).decode('utf-8')

# 创建仓库
def create_repository():
    url = f"https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": REPO,
        "description": "Test repository",
        "private": False
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    print(f"创建仓库响应: {response.status_code}")
    return response.status_code == 201

# 上传文件
def upload_file():
    content = read_file("hello.py")
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/hello.py"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": "Add hello.py",
        "content": content,
        "branch": BRANCH
    }
    response = requests.put(url, headers=headers, json=data, verify=False)
    print(f"上传文件响应: {response.status_code}")
    return response.status_code in [201, 200]

if __name__ == "__main__":
    create_repository()
    upload_file()
```

2. 创建 `hello.py` 文件：

```python
print("Hello from Trea IDE!")
```

3. 运行脚本：
   ```bash
   python upload_single_file.py
   ```

### 示例2：上传多个文件

1. 创建上传脚本 `upload_multiple_files.py`：

```python
#!/usr/bin/env python3
import requests
import base64

GITHUB_TOKEN = "ghp_your_token"
OWNER = "your_username"
REPO = "test-repo"
BRANCH = "main"

# 读取文件内容
def read_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    return base64.b64encode(content).decode('utf-8')

# 上传文件
def upload_file(file_path, file_name):
    content = read_file(file_path)
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{file_name}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"Add {file_name}",
        "content": content,
        "branch": BRANCH
    }
    response = requests.put(url, headers=headers, json=data, verify=False)
    print(f"上传 {file_name} 响应: {response.status_code}")
    return response.status_code in [201, 200]

if __name__ == "__main__":
    # 上传多个文件
    files = [
        ("file1.py", "file1.py"),
        ("file2.py", "file2.py"),
        ("README.md", "README.md")
    ]
    
    for local_path, remote_name in files:
        upload_file(local_path, remote_name)
```

2. 创建要上传的文件：
   - `file1.py`
   - `file2.py`
   - `README.md`

3. 运行脚本：
   ```bash
   python upload_multiple_files.py
   ```

## 注意事项

1. **安全**：不要在代码中硬编码GitHub个人访问令牌，建议使用环境变量或配置文件
2. **权限**：确保GitHub个人访问令牌具有足够的权限
3. **文件大小**：GitHub API对文件大小有限制，大文件建议使用Git命令行上传
4. **SSL验证**：在生产环境中，建议启用SSL验证，而不是使用 `verify=False`

## 故障排除

如果遇到上传问题，请检查：

1. GitHub个人访问令牌是否有效
2. 网络连接是否正常
3. 仓库名称是否正确
4. 文件路径是否存在
5. 权限是否足够

如果问题仍然存在，请参考GitHub API文档或联系GitHub支持。
