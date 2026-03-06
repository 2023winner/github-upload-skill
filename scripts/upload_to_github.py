#!/usr/bin/env python3
"""
通用GitHub上传脚本
从Trea IDE上传文件到GitHub仓库
"""

import requests
import base64
import argparse
import os

# 读取文件内容
def read_file(file_path):
    """
    读取文件内容并转换为base64编码
    """
    with open(file_path, 'rb') as f:
        content = f.read()
    return base64.b64encode(content).decode('utf-8')

# 创建仓库
def create_repository(token, repo_name, description=""):
    """
    创建GitHub仓库
    """
    url = f"https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": description,
        "private": False
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    print(f"创建仓库响应: {response.status_code}")
    if response.status_code == 201:
        print(f"仓库创建成功: {response.json()['html_url']}")
    else:
        print(f"仓库创建失败: {response.json()}")
    return response.status_code == 201

# 上传文件
def upload_file(token, owner, repo, branch, file_path, remote_path, commit_message):
    """
    上传文件到GitHub仓库
    """
    # 读取文件内容
    content = read_file(file_path)
    
    # 构建API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{remote_path}"
    
    # 请求头
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 请求数据
    data = {
        "message": commit_message,
        "content": content,
        "branch": branch
    }
    
    # 发送请求
    response = requests.put(url, headers=headers, json=data, verify=False)
    print(f"上传文件响应: {response.status_code}")
    if response.status_code in [201, 200]:
        print(f"文件上传成功: {response.json()['content']['html_url']}")
    else:
        print(f"文件上传失败: {response.json()}")
    return response.status_code in [201, 200]

# 上传目录
def upload_directory(token, owner, repo, branch, directory, commit_message):
    """
    上传目录中的所有文件到GitHub仓库
    """
    for root, dirs, files in os.walk(directory):
        # 跳过.git目录和其他不需要上传的目录
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'evals']]
        
        for file in files:
            # 跳过配置文件和临时文件
            if file == 'config.py' or file.endswith('.pyc') or file.endswith('~'):
                continue
            
            local_path = os.path.join(root, file)
            # 计算相对路径作为远程路径
            remote_path = os.path.relpath(local_path, directory).replace('\\', '/')
            
            print(f"正在上传: {local_path} -> {remote_path}")
            upload_file(token, owner, repo, branch, local_path, remote_path, commit_message)

# 主函数
def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="从Trea IDE上传文件到GitHub仓库")
    parser.add_argument("--token", help="GitHub个人访问令牌，默认从config.py读取")
    parser.add_argument("--owner", help="GitHub用户名，默认从config.py读取")
    parser.add_argument("--repo", required=True, help="仓库名称")
    parser.add_argument("--branch", default="main", help="分支名称，默认main")
    parser.add_argument("--file", help="要上传的文件路径")
    parser.add_argument("--directory", help="要上传的目录路径")
    parser.add_argument("--remote-path", help="文件在GitHub中的路径，默认与本地文件名相同")
    parser.add_argument("--commit-message", default="从Trea IDE上传文件", help="提交信息")
    parser.add_argument("--create-repo", action="store_true", help="是否创建新仓库")
    parser.add_argument("--repo-description", default="从Trea IDE上传的项目", help="仓库描述")
    
    args = parser.parse_args()
    
    # 尝试从配置文件读取
    try:
        # 尝试从上级目录导入config
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import config
        if not args.token:
            args.token = config.GITHUB_TOKEN
        if not args.owner:
            args.owner = config.GITHUB_OWNER
    except ImportError:
        # 如果配置文件不存在，检查必要参数
        if not args.token or not args.owner:
            print("错误: 请提供GitHub个人访问令牌和用户名，或创建config.py配置文件")
            return
    
    # 如果需要创建仓库
    if args.create_repo:
        create_repository(args.token, args.repo, args.repo_description)
    
    # 上传文件或目录
    if args.file:
        # 检查文件是否存在
        if not os.path.exists(args.file):
            print(f"错误: 文件 {args.file} 不存在")
            return
        # 确定远程路径
        remote_path = args.remote_path if args.remote_path else os.path.basename(args.file)
        # 上传文件
        upload_file(
            args.token,
            args.owner,
            args.repo,
            args.branch,
            args.file,
            remote_path,
            args.commit_message
        )
    elif args.directory:
        # 检查目录是否存在
        if not os.path.exists(args.directory):
            print(f"错误: 目录 {args.directory} 不存在")
            return
        # 上传目录
        upload_directory(
            args.token,
            args.owner,
            args.repo,
            args.branch,
            args.directory,
            args.commit_message
        )
    else:
        print("错误: 请提供 --file 或 --directory 参数")
        return

if __name__ == "__main__":
    main()
