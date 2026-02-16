# GitHub 代码搜索语法参考

本文档详细说明如何使用 `gh search code` 命令的各种搜索限定符和语法。

## 1. 按文件内容或文件路径搜索

### 语法与限定符

- `in:file` - 搜索文件内容
- `in:path` - 搜索文件路径
- `in:file,path` - 搜索文件内容和路径
- `in` 限定符可选，默认搜索文件内容

### 示例

```bash
# 在仓库中搜索文件内容包含 "NewClient" 的 Go 代码
gh search code repo:TencentCloud/tencentcloud-sdk-go NewClient in:file

# 在文件路径中搜索包含 "credential" 的文件
gh search code repo:TencentCloud/tencentcloud-sdk-go credential in:path

# 同时搜索内容或路径中包含 "profile" 的文件
gh search code repo:TencentCloud/tencentcloud-sdk-go profile in:file,path
```

## 2. 按文件位置搜索

### 语法与限定符

- `path:/` - 匹配仓库根目录的文件
- `path:DIRECTORY` - 匹配指定目录或其子目录的文件
- `path:PATH/TO/DIRECTORY` - 匹配指定路径目录及其子目录的文件

### 示例

```bash
# 在仓库根目录搜索内容包含 "credential" 的文件
gh search code repo:TencentCloud/tencentcloud-sdk-go credential path:/

# 在 tencentcloud/common/ 目录（及其子目录）搜索 "NewClient"
gh search code repo:TencentCloud/tencentcloud-sdk-go NewClient path:tencentcloud/common

# 在 examples/cvm/v20170312/ 目录搜索 "request"
gh search code repo:TencentCloud/tencentcloud-sdk-go request path:examples/cvm/v20170312
```

## 3. 按文件名搜索

### 语法与限定符

- `filename:FILENAME` - 精确匹配指定文件名

### 示例

```bash
# 搜索名为 "credential.go" 的文件
gh search code repo:TencentCloud/tencentcloud-sdk-go filename:credential.go

# 搜索名为 "describe_instances.go" 的文件内容包含 "request" 的代码
gh search code repo:TencentCloud/tencentcloud-sdk-go request filename:describe_instances.go
```

## 4. 按文件扩展名搜索

### 语法与限定符

- `extension:EXTENSION` - 匹配以指定扩展名结尾的文件（不带点）

### 示例

```bash
# 搜索以 .go 结尾的文件内容包含 "NewClient" 的代码
gh search code repo:TencentCloud/tencentcloud-sdk-go NewClient extension:go

# 在 tencentcloud/common/ 目录搜索以 .go 结尾的文件内容包含 "credential" 的代码
gh search code repo:TencentCloud/tencentcloud-sdk-go credential extension:go path:tencentcloud/common

# 搜索所有 .go 文件中包含 "response" 的内容
gh search code repo:TencentCloud/tencentcloud-sdk-go response extension:go
```

## 5. 组合限定符

可以组合多个限定符来精确定位代码：

```bash
# 在特定目录的特定扩展名文件中搜索特定内容
gh search code repo:owner/repo keyword extension:py path:src/utils

# 在特定文件名中搜索特定内容
gh search code repo:owner/repo "function name" filename:main.py

# 在根目录的特定扩展名文件中搜索
gh search code repo:owner/repo config extension:json path:/
```

## 重要注意事项

### 特殊字符限制

搜索查询中**不能使用**以下通配符：

```
. , : ; / \ ` ' " = * ! ? # $ & + ^ | ~ < > ( ) { } [ ] @
```

搜索将忽略这些符号。

### 多词搜索

多词搜索词请用**引号**括起来。例如：

```bash
# 搜索函数声明 func (c *Client)
gh search code repo:TencentCloud/tencentcloud-sdk-go "func (c *Client)" extension:go
```

### 大小写

搜索**不区分大小写**。

## 使用建议

1. 使用 `--jq` 参数处理 JSON 输出，获得更清晰的结果
2. 始终以 master 或 main 分支的最新提交为准
3. 先查看 README 文件了解代码功能和架构
4. 组合使用多个限定符可以更精确地定位代码
