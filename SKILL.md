---
name: github-upload
description: 从Trea IDE上传文件到GitHub仓库。当用户需要将本地项目或文件上传到GitHub时使用此技能，智能体将自主完成仓库创建、文件上传、认证处理等操作。
compatibility:
  - tools: [Read, Write, RunCommand]
  - dependencies: [requests, base64]
---

# GitHub上传技能

## 功能描述

此技能允许智能体从Trea IDE直接上传文件到GitHub仓库，包括以下功能：

- 自动创建新的GitHub仓库
- 批量上传单个或多个文件到GitHub
- 智能处理GitHub认证
- 自动解决常见的上传问题
- 支持环境变量、配置文件和Git设置等多种认证方式

## 前置条件

在使用此技能之前，需要：

1. **GitHub个人访问令牌**：用于认证GitHub API请求
2. **Python环境**：需要安装requests库
3. **文件准备**：准备好要上传的文件

## 生成GitHub个人访问令牌

1. 访问 [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token"
3. 选择适当的权限（至少需要 `repo` 权限）
4. 生成令牌并保存好

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

### 方法二：使用Python脚本上传

1. **使用通用上传脚本**：
   ```bash
   # 上传单个文件
   python scripts/upload_to_github.py --repo 仓库名 --file 要上传的文件
   
   # 上传目录
   python scripts/upload_to_github.py --repo 仓库名 --directory 目录路径
   
   # 创建仓库并上传
   python scripts/upload_to_github.py --repo 仓库名 --file 要上传的文件 --create-repo
   ```

2. **配置选项**：
   - `--token`：GitHub个人访问令牌
   - `--owner`：GitHub用户名
   - `--repo`：仓库名称（必填）
   - `--branch`：分支名称，默认main
   - `--file`：要上传的文件路径
   - `--directory`：要上传的目录路径
   - `--commit-message`：提交信息
   - `--create-repo`：是否创建新仓库
   - `--repo-description`：仓库描述

### 方法三：使用Git命令行上传

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

### 9. 文件夹权限问题

**问题**：
在搬运其他项目后，可能遇到文件夹权限问题，导致无法写入skill文件。

**解决方案**：
- 以管理员身份运行Trea IDE
- 检查文件夹权限设置，确保有写入权限
- 尝试在其他目录中创建和使用skill
- 使用环境变量存储配置信息，避免写入文件

### 10. 本地设置检测问题

**问题**：
无法得知本地的GitHub设置，如用户名、邮箱等，导致上传时出现问题。

**解决方案**：
- 上传脚本会自动检测本地Git设置：
  ```bash
  # 查看当前Git设置
  git config user.name
  git config user.email
  
  # 设置Git信息
  git config --global user.name "你的用户名"
  git config --global user.email "你的邮箱"
  ```
- 使用环境变量存储配置：
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
- 脚本会按以下顺序查找配置：
  1. 命令行参数
  2. 环境变量
  3. 配置文件（config.py）
  4. Git本地设置

### 11. 文件大小限制

**问题**：
GitHub API对文件大小有限制（通常为100MB）。

**解决方案**：
- 对于大文件，使用Git命令行上传
- 考虑使用Git LFS（Large File Storage）
- 拆分大文件为多个小文件

### 12. 网络连接问题

**问题**：
网络连接不稳定或防火墙限制可能导致上传失败。

**解决方案**：
- 检查网络连接
- 尝试使用代理服务器
- 重试上传操作
- 确保GitHub API的访问权限

### 13. GitHub推送保护错误

**问题**：
推送时遇到GitHub推送保护错误，提示"Push cannot contain secrets"，因为代码中包含了GitHub个人访问令牌等敏感信息。

**错误信息**：
```
remote: error: GH013: Repository rule violations found for refs/heads/master.
remote: 
remote: - GITHUB PUSH PROTECTION 
remote:   ————————————————————————————————————————— 
remote:     Resolve the following violations before pushing again 
remote: 
remote:     - Push cannot contain secrets 
remote: 
remote: 
remote:      (?) Learn how to resolve a blocked push 
remote:      `https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/working-with-push-protection-from-the-command-line#resolving-a-blocked-push` 
remote: 
remote: 
remote:       —— GitHub Personal Access Token —————————————————————— 
remote:        locations: 
remote:          - commit: 113a24d1c9608cfc2caec271b39ae5566778df42 
remote:            path: create_repo.ps1:1
```

**解决方案**：

#### 方法一：移除最新提交中的密钥
1. 从代码中移除密钥
2. 运行 `git commit --amend --all` 更新原始提交
3. 使用 `git push` 推送更改

#### 方法二：移除早期提交中的密钥
1. 查看错误消息中列出的包含密钥的所有提交
2. 运行 `git log` 查看分支上的完整提交历史
3. 确定最早包含密钥的提交
4. 运行 `git rebase -i <最早提交ID>~1` 开始交互式变基
5. 在编辑器中，将最早提交的 `pick` 改为 `edit`
6. 保存并关闭编辑器开始变基
7. 从代码中移除密钥
8. 运行 `git add .` 将更改添加到暂存区
9. 运行 `git commit --amend` 提交更改
10. 运行 `git rebase --continue` 完成变基
11. 使用 `git push` 推送更改

#### 方法三：绕过推送保护（不推荐）
1. 访问GitHub返回的URL
2. 选择最能描述为什么应该允许推送的选项
3. 点击 "Allow me to push this secret"
4. 在三小时内重新尝试推送

**预防措施**：
- 使用环境变量存储敏感信息
- 使用配置文件并将其添加到 `.gitignore`
- 在上传前检查代码中是否包含敏感信息
- 使用GitHub Actions或其他CI/CD工具进行密钥检测

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
