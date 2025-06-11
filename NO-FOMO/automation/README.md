# NO-FOMO 日报自动化管理工具使用说明

## 简介

`daily_report_manager.py` 是一个自动化管理工具，用于：
- 同步和管理 NO-FOMO 日报网站的所有页面
- 自动添加统计脚本到所有页面
- 管理导航链接和语言切换功能
- 更新主页和daily页面的日期列表

## 功能特点

### 🔄 智能检测，避免重复
- 每次运行时会检查页面是否已包含相应功能
- 不会重复插入统计脚本、导航栏或语言切换
- 安全地多次运行，不会破坏现有页面

### 📊 统计脚本管理
- 自动为所有日报页面添加访问统计脚本
- 为主页添加完整的统计和显示脚本
- 根据页面位置自动计算正确的脚本路径

### 🌐 多语言支持
- 自动检测和处理中英文双语页面
- 为支持多语言的页面添加语言切换功能
- 生成对应语言的导航链接

## 使用方法

### 基本语法
```bash
python daily_report_manager.py [选项]
```

### 选项说明

#### `--sync-all`
同步所有内容，包括：
- 统计脚本
- 导航链接
- 语言切换功能
- 主页日期列表更新
- Daily页面重定向更新

```bash
# 完整同步所有功能
python daily_report_manager.py --sync-all

# 同步但不提交到Git
python daily_report_manager.py --sync-all --no-commit
```

#### `--sync-analytics`
仅同步统计脚本，适用于：
- 新添加的统计功能
- 统计脚本更新后的批量部署
- 快速为所有页面添加统计功能

```bash
# 仅同步统计脚本
python daily_report_manager.py --sync-analytics

# 同步统计脚本但不提交到Git
python daily_report_manager.py --sync-analytics --no-commit
```

#### `--base-path`
指定工作目录（可选）
```bash
python daily_report_manager.py --sync-all --base-path /path/to/NO-FOMO
```

#### `--no-commit`
执行操作但不自动提交到Git
```bash
python daily_report_manager.py --sync-all --no-commit
```

## 工作原理

### 文件夹检测
脚本会自动扫描 `home/` 目录下的所有日期文件夹（格式：YYYY-MM-DD），并检测：
- 是否包含 `index.html`（单语言版本）
- 是否包含 `cn/index.html` 和 `en/index.html`（多语言版本）

### 统计脚本添加
根据页面位置自动计算脚本路径：
- 主页：`js/analytics.js`
- 中文/英文主页：`../js/analytics.js`
- 日报页面：`../js/analytics.js` 或 `../../js/analytics.js`

### 安全检查
在添加任何功能前，都会先检查：
- 统计脚本：检查是否包含 `analytics.js`、`NoFomoAnalytics` 等关键词
- 导航栏：检查是否包含导航相关的HTML结构
- 语言切换：检查是否包含 `language-switch` 类

## 常见使用场景

### 1. 首次部署统计功能
```bash
python daily_report_manager.py --sync-analytics
```

### 2. 新增日报后完整同步
```bash
python daily_report_manager.py --sync-all
```

### 3. 更新统计脚本后重新部署
```bash
python daily_report_manager.py --sync-analytics --no-commit
# 检查结果后手动提交
```

### 4. 维护模式（仅测试，不提交）
```bash
python daily_report_manager.py --sync-all --no-commit
```

## 输出示例

### 成功运行示例
```
📁 工作目录: /path/to/NO-FOMO
📅 发现home日期文件夹: ['2025-06-11', '2025-06-10', '2025-06-09']
ℹ️  home/2025-06-11/cn/index.html 已存在统计脚本，跳过添加
✅ 已为 home/2025-06-11/en/index.html 添加统计脚本
📊 统计脚本同步完成: 处理了 3 个文件夹 + 主页
✅ 已提交到Git: 同步统计脚本到所有页面
```

### 检测到重复时的输出
```
ℹ️  home/index.html 已存在统计脚本，跳过添加
ℹ️  home/2025-06-11/index.html 已存在导航链接，跳过添加
ℹ️  home/2025-06-11/index.html 已存在语言切换，跳过添加
```

## 注意事项

1. **运行前确保在正确的目录**：脚本会自动检测当前目录结构
2. **Git仓库状态**：默认会自动提交更改，使用 `--no-commit` 选项来跳过
3. **备份重要文件**：首次运行建议先备份关键文件
4. **检查输出日志**：注意查看哪些文件被修改，哪些被跳过

## 故障排除

### 问题：脚本路径错误
确保在正确的目录运行脚本，或使用 `--base-path` 指定正确路径。

### 问题：Git提交失败
使用 `--no-commit` 选项，手动检查更改后再提交。

### 问题：统计脚本重复插入
脚本已内置检测机制，如果仍有问题，请检查页面中的关键词是否正确。 