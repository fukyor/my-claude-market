# 1. 在使用github cli命令前需要先执行下面命令完成登录验证
```cmd
echo %GITHUB_PERSONAL_ACCESS_TOKEN% | gh auth login --with-token
```

```bash
echo "$GITHUB_PERSONAL_ACCESS_TOKEN" | gh auth login --with-token
```


# 2. 仓库查看（Repository viewing）
- 查找默认分支：确定默认分支
```bash
gh api repos/{owner}/{repo} --json '.default_branch' \
    --jq '.defaultBranchRef.name'
eg.
gh repo view TencentCloud/tencentcloud-sdk-go --json defaultBranchRef \
    --jq '.defaultBranchRef.name'
```

- 查看仓库描述
```bash
gh api repos/{owner}/{repo} --json description
eg.
gh repo view TencentCloud/tencentcloud-sdk-go --json description
```
- 查看仓库主要语言
```bash
gh api repos/{owner}/{repo} --json '.primaryLanguage' \
    --jq '.primaryLanguage.name'
eg.
gh repo view TencentCloud/tencentcloud-sdk-go --json primaryLanguage \
    --jq '.primaryLanguage.name'
```


## 目录/文件查看
目的：理解目录结构，查看文件内容

- 查看指定目录结构
```bash
gh api repos/{owner}/{repo}/contents/{dirpath} \
  --jq '.[] | "\(.name) \(.type)"'
eg.
gh api repos/TencentCloud/tencentcloud-sdk-go/contents/examples \
  --jq '.[] | "\(.name) \(.type)"'
```

- 查看文件内容
```bash
gh api repos/TencentCloud/tencentcloud-sdk-go/contents/examples/products.md
```
注意：文件内容在content字段，文件编码在encoding字段。通常编码都是base64，根据编码解码查看。

eg.
```bash
gh api repos/TencentCloud/tencentcloud-sdk-go/contents/products.md \
  --jq '.content' \
  | base64 -d

查看readme文件(特别重要)
gh api repos/TencentCloud/tencentcloud-sdk-go/contents/products.md \
  --jq '.content' \
  | base64 -d
```

# 3. 代码查找（Code searching）
目的：查找需要的相关代码
##  1. 按文件内容或文件路径搜索（Search by the File Contents or File Path）
    语法与限定符：
    in:file：搜索文件内容。
    in:path：搜索文件路径。
    in:file,path：搜索文件内容和路径。
    in 限定符可选，默认搜索文件内容。

eg.
```bash
在仓库中搜索文件内容包含 "NewClient" 的 Go 代码
gh search code repo:TencentCloud/tencentcloud-sdk-go NewClient in:file

在文件路径中搜索包含 "credential" 的文件
gh search code repo:TencentCloud/tencentcloud-sdk-go credential in:path

同时搜索内容或路径中包含 "profile" 的文件
gh search code repo:TencentCloud/tencentcloud-sdk-go profile in:file,path
```

## 2. 按文件位置搜索（Search by File Location）
    语法与限定符：

    path:/：匹配仓库根目录的文件。
    path:DIRECTORY：匹配指定目录或其子目录的文件。
    path:PATH/TO/DIRECTORY：匹配指定路径目录及其子目录的文件。

eg.
```bash
在仓库根目录搜索内容包含 "credential" 的文件
gh search code repo:TencentCloud/tencentcloud-sdk-go credential path:/

在 tencentcloud/common/ 目录（及其子目录）搜索 "NewClient"
gh search code repo:TencentCloud/tencentcloud-sdk-go NewClient path:tencentcloud/common

在 examples/cvm/v20170312/ 目录搜索 "request"
gh search code repo:TencentCloud/tencentcloud-sdk-go request path:examples/cvm/v20170312
```

## 3. 按文件名搜索（Search by Filename）
    语法与限定符：
    filename:FILENAME：精确匹配指定文件名。

eg.
```bash
搜索名为 "credential.go" 的文件。
gh search code repo:TencentCloud/tencentcloud-sdk-go filename:credential.go

搜索名为 "describe_instances.go" 的文件内容包含 "request" 的代码
gh search code repo:TencentCloud/tencentcloud-sdk-go request filename:describe_instances.go
```

## 4. 按文件扩展名搜索（Search by File Extension）
    语法与限定符：
    extension:EXTENSION：匹配以指定扩展名结尾的文件（不带点）。

eg.
```bash
搜索以 .go 结尾的文件内容包含 "NewClient" 的代码
gh search code repo:TencentCloud/tencentcloud-sdk-go NewClient extension:go

在 tencentcloud/common/ 目录搜索以 .go 结尾的文件内容包含 "credential" 的代码
gh search code repo:TencentCloud/tencentcloud-sdk-go credential extension:go path:tencentcloud/common

搜索所有 .go 文件中包含 "response" 的内容
gh search code repo:TencentCloud/tencentcloud-sdk-go response extension:go
```



## 注意(特别重要)
1. 注意可使用--jq附加参数对获取到的json数据进行处理，以便获得更加清晰的内容
2. 始终以master或main分支的最新提交为准
3. 注意首先查看readme文件了解代码功能和架构

## 其他注意
1. 搜索查询中不能使用以下通配符： . , : ; / \ ` ' " = * ! ? # $ & + ^ | ~ < > ( ) { } [ ] @ 。搜索将忽略这些符号。
2. 多词搜索词请用引号括起来。例如，如果您想搜索func (c *Client)函数声明，则应搜索 "func (c *Client)" 。搜索不区分大小写。
```bash
gh search code repo:TencentCloud/tencentcloud-sdk-go "func (c *Client)" extension:go
```