---
name: github-repo-explorer
description: 通过 GitHub CLI 远程查询代码仓库信息。适用场景：(1) 浏览远程仓库的目录结构；(2) 查看远程仓库的文件内容；(3) 在远程仓库中搜索代码；(4) 获取仓库元数据（默认分支、描述、主要语言）；(5) 读取仓库 README 了解项目。
---

# GitHub Repo Explorer

通过 GitHub CLI (`gh`) 远程查询和探索 GitHub 代码仓库，无需克隆到本地。

## 工作流程

### 步骤 1: 认证

在使用任何 GitHub CLI 命令前，必须先完成认证。

运行认证脚本：

```bash
python scripts/gh_auth.py
```

该脚本会：
1. 检查是否已认证，避免重复登录
2. 从环境变量 `GITHUB_PERSONAL_ACCESS_TOKEN` 读取 token
3. 通过 stdin 安全地传递 token 给 `gh auth login`

**环境变量设置：**

Windows (cmd):
```cmd
set GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here
```

Linux/Mac (bash):
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here
```

### 步骤 2: 获取仓库概览

在开始探索前，先了解仓库的基本信息。

**查找默认分支：**

```bash
gh repo view owner/repo --json defaultBranchRef --jq '.defaultBranchRef.name'
```

示例：
```bash
gh repo view TencentCloud/tencentcloud-sdk-go --json defaultBranchRef --jq '.defaultBranchRef.name'
```

**查看仓库描述：**

```bash
gh repo view owner/repo --json description
```

**查看主要编程语言：**

```bash
gh repo view owner/repo --json primaryLanguage --jq '.primaryLanguage.name'
```

### 步骤 3: 读取 README（重要）

在深入探索前，**务必先阅读 README** 了解项目结构和功能。

```bash
gh api repos/owner/repo/contents/README.md --jq '.content' | base64 -d
```

示例：
```bash
gh api repos/TencentCloud/tencentcloud-sdk-go/contents/README.md --jq '.content' | base64 -d
```

### 步骤 4: 根据目标选择操作

根据用户的具体需求，选择以下操作之一：

## 操作 A: 浏览目录结构

查看指定目录下的文件和子目录列表。

**命令格式：**

```bash
gh api repos/owner/repo/contents/dirpath --jq '.[] | "\(.name) \(.type)"'
```

**示例：**

```bash
# 查看根目录
gh api repos/TencentCloud/tencentcloud-sdk-go/contents/ --jq '.[] | "\(.name) \(.type)"'

# 查看 examples 目录
gh api repos/TencentCloud/tencentcloud-sdk-go/contents/examples --jq '.[] | "\(.name) \(.type)"'

# 查看嵌套目录
gh api repos/owner/repo/contents/src/utils --jq '.[] | "\(.name) \(.type)"'
```

**输出格式：**
- 每行显示：`文件名 类型`
- 类型为 `file` 或 `dir`

## 操作 B: 查看文件内容

读取远程仓库中的文件内容。

**命令格式：**

```bash
gh api repos/owner/repo/contents/filepath --jq '.content' | base64 -d
```

**重要说明：**
- 文件内容在 `content` 字段中
- 编码格式在 `encoding` 字段中（通常是 base64）
- 需要根据编码格式解码查看

**示例：**

```bash
# 查看 products.md 文件
gh api repos/TencentCloud/tencentcloud-sdk-go/contents/products.md --jq '.content' | base64 -d

# 查看配置文件
gh api repos/owner/repo/contents/config.json --jq '.content' | base64 -d

# 查看源代码文件
gh api repos/owner/repo/contents/src/main.py --jq '.content' | base64 -d
```

## 操作 C: 搜索代码

在远程仓库中搜索特定代码、文件名或路径。

**基础搜索：**

```bash
# 搜索文件内容
gh search code repo:owner/repo keyword

# 搜索文件路径
gh search code repo:owner/repo keyword in:path

# 搜索文件内容和路径
gh search code repo:owner/repo keyword in:file,path
```

**高级搜索技巧：**

由于搜索语法较为复杂，建议阅读详细的搜索语法参考文档：

```
references/search-syntax.md
```

该文档包含：
- 按文件内容/路径搜索（`in:file`, `in:path`）
- 按文件位置搜索（`path:/`, `path:directory`）
- 按文件名搜索（`filename:`）
- 按扩展名搜索（`extension:`）
- 组合限定符使用
- 特殊字符限制和引号规则

**常用搜索示例：**

```bash
# 搜索特定函数
gh search code repo:owner/repo "function name" extension:py

# 在特定目录搜索
gh search code repo:owner/repo keyword path:src/utils

# 搜索特定文件名
gh search code repo:owner/repo filename:config.json

# 搜索特定扩展名
gh search code repo:owner/repo keyword extension:go
```

## 最佳实践

1. **始终先认证** - 运行 `python scripts/gh_auth.py` 确保已登录
2. **先读 README** - 了解项目结构和约定
3. **使用 --jq 处理输出** - 获得更清晰、可读的结果
4. **以默认分支为准** - 通常是 main 或 master 分支
5. **组合搜索限定符** - 使用多个限定符精确定位代码
6. **注意特殊字符** - 搜索时避免使用通配符，多词用引号

## 故障排除

**认证失败：**
- 检查环境变量 `GITHUB_PERSONAL_ACCESS_TOKEN` 是否设置
- 确认 token 有效且具有 repo 权限
- 确保已安装 GitHub CLI (`gh`)

**文件内容乱码：**
- 确认使用 `base64 -d` 解码
- 检查 `encoding` 字段确认编码格式

**搜索无结果：**
- 检查仓库名称是否正确（`owner/repo` 格式）
- 尝试简化搜索关键词
- 参考 `references/search-syntax.md` 调整搜索语法
