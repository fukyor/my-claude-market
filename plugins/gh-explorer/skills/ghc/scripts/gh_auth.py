#!/usr/bin/env python3
"""
GitHub CLI 认证脚本

跨平台认证脚本，用于通过环境变量中的 Personal Access Token 登录 GitHub CLI。
解决 Windows cmd 和 bash 命令差异问题。

使用方法:
    python gh_auth.py

环境变量:
    GITHUB_PERSONAL_ACCESS_TOKEN - GitHub Personal Access Token

功能:
    1. 检查是否已认证，避免重复登录
    2. 从环境变量读取 token
    3. 通过 stdin 传递 token 给 gh auth login
"""

import os
import sys
import subprocess


def check_auth_status():
    """检查 GitHub CLI 是否已认证"""
    try:
        result = subprocess.run(
            ['gh', 'auth', 'status'],
            capture_output=True,
            text=True,
            timeout=10
        )
        # gh auth status 返回 0 表示已认证
        return result.returncode == 0
    except Exception as e:
        print(f"检查认证状态时出错: {e}", file=sys.stderr)
        return False


def authenticate():
    """使用环境变量中的 token 进行认证"""
    # 读取环境变量
    token = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')

    if not token:
        print("错误: 未找到环境变量 GITHUB_PERSONAL_ACCESS_TOKEN", file=sys.stderr)
        print("请设置环境变量后重试", file=sys.stderr)
        return False

    try:
        # 通过 stdin 传递 token
        result = subprocess.run(
            ['gh', 'auth', 'login', '--with-token'],
            input=token,
            text=True,
            capture_output=True,
            timeout=30
        )

        if result.returncode == 0:
            print("✓ GitHub CLI 认证成功")
            return True
        else:
            print(f"认证失败: {result.stderr}", file=sys.stderr)
            return False

    except FileNotFoundError:
        print("错误: 未找到 gh 命令，请先安装 GitHub CLI", file=sys.stderr)
        print("访问 https://cli.github.com/ 下载安装", file=sys.stderr)
        return False
    except Exception as e:
        print(f"认证过程中出错: {e}", file=sys.stderr)
        return False


def main():
    """主函数"""
    print("检查 GitHub CLI 认证状态...")

    # 先检查是否已认证
    if check_auth_status():
        print("✓ 已认证，无需重新登录")
        return 0

    print("未认证，开始认证流程...")

    # 执行认证
    if authenticate():
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
