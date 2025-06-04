# NO-FOMO AI 日报自动化系统

## 📖 项目简介

NO-FOMO AI 日报是一个自动化的 AI 资讯发布系统，支持每日日报的生成、管理和发布。该系统通过 GitHub Pages 提供在线访问，具有现代化的 Web 界面和完整的自动化工作流。

## 🏗️ 系统架构

### URL 结构
```
https://opusair.github.io/NO-FOMO/
├── daily/                    # 最新日报（自动重定向）
├── home/                     # 主页，显示所有日报列表
│   ├── 2025-05-29/          # 特定日期的日报
│   ├── 2025-05-28/          # 特定日期的日报
│   └── ...
└── automation/              # 自动化脚本
```

### 文件夹结构
```
NO-FOMO/
├── 2025-05-29/             # 源日报文件夹
│   ├── index.html          # 日报页面
│   ├── screenshot/         # 图片文件夹
│   └── *.json             # 数据文件
├── home/                   # 发布目录
│   ├── index.html         # 主页
│   ├── 2025-05-29/       # 已发布的日报
│   └── ...
├── daily/                 # 最新日报重定向
│   └── index.html
├── automation/            # 自动化工具
│   ├── daily_report_manager.py  # Python 主脚本
│   ├── deploy.sh              # Shell 部署脚本
│   └── README.md              # 说明文档
└── README.md              # 项目文档
```

## 🚀 快速开始

### 1. 环境要求
- Python 3.6+
- Git
- Bash/Zsh (macOS/Linux)

### 2. 初始化系统
```bash
# 进入自动化目录
cd NO-FOMO/automation

# 给脚本执行权限
chmod +x deploy.sh

# 初始化系统（首次使用）
./deploy.sh init
```

### 3. 基本使用

#### 添加新日报
```bash
# 添加今天的日报（如果存在）
./deploy.sh daily

# 添加指定日期的日报
./deploy.sh add 2025-06-01

# 检查并更新最新日报
./deploy.sh update
```

#### 查看状态
```bash
# 查看当前系统状态
./deploy.sh status

# 查看帮助信息
./deploy.sh help
```

## ⚙️ 自动化配置

### 设置定时任务
```bash
# 设置每天自动更新
./deploy.sh setup-cron
```

这将创建一个 cron 任务，每天早上 9 点自动检查并发布新日报。

### 手动 cron 配置
如果需要自定义时间，可以手动编辑 crontab：
```bash
# 编辑 crontab
crontab -e

# 添加定时任务（例如每天早上 8:30）
30 8 * * * /path/to/NO-FOMO/automation/deploy.sh daily
```

## 📝 工作流程

### 日常工作流程
1. **创建日报**: 在 `NO-FOMO/` 下创建日期文件夹（如 `2025-06-01/`）
2. **添加内容**: 在文件夹中放入 `index.html` 和 `screenshot/` 图片
3. **自动发布**: 运行 `./deploy.sh daily` 或等待定时任务执行
4. **自动更新**: 系统会自动：
   - 复制文件夹到 `home/` 目录
   - 更新主页链接
   - 更新 daily 重定向
   - 提交到 Git 并推送

### 系统自动化功能
- ✅ 自动检测新日报文件夹
- ✅ 自动复制和部署
- ✅ 自动更新主页导航
- ✅ 自动添加返回链接
- ✅ 自动统计文章数量
- ✅ 自动提取数据源
- ✅ 自动 Git 提交和推送

## 🎨 界面特性

### 主页功能
- 📊 统计概览（总日报数、总文章数、最新更新）
- 📅 日期卡片展示
- 🔍 响应式设计
- 🎯 快速导航链接

### 日报页面功能
- 📱 移动友好的响应式设计
- 🖼️ 图片自动适配
- 🏷️ 智能标签分类
- 🔗 外链跳转
- 🧭 导航面包屑

## 🔧 高级配置

### Python 脚本参数
```bash
# 使用自定义路径
python3 daily_report_manager.py --base-path /custom/path

# 同步所有文件夹
python3 daily_report_manager.py --sync-all

# 添加特定日期
python3 daily_report_manager.py --add-date 2025-06-01

# 不自动提交到 Git
python3 daily_report_manager.py --no-commit
```

### 自定义配置
如需修改默认行为，可以编辑 `daily_report_manager.py` 中的相关配置：

```python
# 修改 Git 提交信息格式
def git_commit_and_push(self, message=None):
    if message is None:
        today = date.today().strftime('%Y-%m-%d')
        message = f"自动更新日报 - {today}"  # 可自定义格式

# 修改导航链接样式
navigation_html = '''...'''  # 可自定义导航栏 HTML
```

## 📋 故障排除

### 常见问题

#### 1. Git 提交失败
```bash
# 检查 Git 状态
git status

# 手动提交
git add .
git commit -m "手动提交"
git push
```

#### 2. Python 脚本执行错误
```bash
# 检查 Python 版本
python3 --version

# 检查文件权限
ls -la automation/

# 手动运行 Python 脚本
cd NO-FOMO
python3 automation/daily_report_manager.py --help
```

#### 3. 定时任务不工作
```bash
# 查看 cron 任务
crontab -l

# 查看日志
tail -f automation/cron.log

# 测试脚本
./automation/deploy.sh daily
```

### 日志文件
- `automation/cron.log`: 定时任务执行日志
- Git 历史: 查看所有自动提交记录

## 🔄 备份和恢复

### 备份重要文件
```bash
# 备份配置
cp -r automation/ backup/automation_$(date +%Y%m%d)

# 备份 home 目录
cp -r home/ backup/home_$(date +%Y%m%d)
```

### 从备份恢复
```bash
# 恢复并重新初始化
./deploy.sh init
```

## 📞 支持与维护

### 更新系统
定期检查并更新自动化脚本以获得最新功能和修复。

### 监控
- 检查 GitHub Pages 部署状态
- 监控 cron 任务执行情况
- 定期查看日志文件

---

## 📄 许可证

本项目采用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

---

**NO-FOMO AI 日报** - 让您不错过任何重要的 AI 资讯！ 🚀 