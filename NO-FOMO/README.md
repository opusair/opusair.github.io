# NO-FOMO AI 日报 🤖

> Never miss out on AI breakthroughs again! 不再错过任何AI突破！

## 🔗 快速访问

- 🌐 [查看最新日报](https://opusair.github.io/NO-FOMO/daily/)
- 📅 [浏览历史日报](https://opusair.github.io/NO-FOMO/home/)
- 🌍 [English Version](https://opusair.github.io/NO-FOMO/home/en/)
- 📊 [最新日报 (2025-09-09)](https://opusair.github.io/NO-FOMO/home/2025-09-09/)

## 📂 项目结构

```
NO-FOMO/
├── home/                      # 日报主页和历史归档
│   ├── index.html            # 中文主页
│   ├── en/                   # 英文版本
│   │   └── index.html        
│   └── YYYY-MM-DD/           # 按日期组织的日报
│       ├── index.html        # 中文日报
│       ├── en/               # 英文日报
│       │   ├── index.html
│       │   └── YYYYMMDD_en.json
│       └── screenshot/       # 文章截图
│           ├── github/       # GitHub项目截图
│           ├── twitter/      # Twitter推文截图
│           └── wechat/       # 微信文章截图
├── daily/                    # 最新日报重定向页面
│   ├── index.html           # 中文重定向
│   └── en/                  # 英文重定向
│       └── index.html
└── automation/              # 自动化脚本
    ├── daily_report_manager.py  # 核心管理脚本
    └── config.json             # 配置文件
```

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Git

### 安装

克隆仓库：
```bash
git clone https://github.com/opusair/opusair.github.io.git
cd opusair.github.io/NO-FOMO
```


### 使用方法

#### 同步所有日报文件夹

更新所有日期文件夹的导航、语言切换和分析代码：

```bash
python automation/daily_report_manager.py --sync-all
```

#### 仅同步不提交

如果只想同步文件但不自动提交到Git：

```bash
python automation/daily_report_manager.py --sync-all --no-commit
```

### 使用示例

```bash
# 完整同步并自动提交
python automation/daily_report_manager.py --sync-all

# 只同步不提交（适合手动检查后再提交）
python automation/daily_report_manager.py --sync-all --no-commit

# 查看帮助信息
python automation/daily_report_manager.py --help
```

### 主要功能

1. **自动添加Google Analytics**
   - 自动检测并添加GA追踪代码到所有HTML页面

2. **智能导航栏**
   - 自动为每个页面添加返回主页、查看最新日报等导航链接
   - 根据页面位置自动调整路径深度

3. **语言切换功能**
   - 为支持双语的日报自动添加中英文切换按钮
   - 智能检测当前语言并高亮对应按钮

4. **主页更新**
   - 自动扫描所有日报文件夹
   - 提取文章数量和来源信息
   - 生成日报列表并按日期排序

5. **重定向页面**
   - 自动跳转到最新的日报
   - 支持中英文不同路径

## 📊 数据格式

### 日报数据

每个日报包含以下信息：

- **日期**：YYYY-MM-DD格式
- **标题**：AI日报标题
- **描述**：包含来源数量和类型
- **文章数量**：该日收录的文章总数
- **来源列表**：GitHub、Twitter、微信等

### 访问统计

系统自动收集访问数据（`analytics-stats.json`）：

- **访问量统计**：总访问量、今日/昨日/最近7天/30天访问量
- **热门页面**：最受欢迎的日报和页面
- **流量来源**：直接访问、搜索引擎、社交媒体、引荐
- **设备分布**：桌面端、移动端、平板电脑
- **地域分布**：访客国家/地区统计
---

<p align="center">
  Made with ❤️ by OpusAir Team<br>
  让AI资讯触手可及 | Making AI News Accessible
</p>