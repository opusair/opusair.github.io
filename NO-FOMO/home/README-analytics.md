# NO-FOMO 网站访问统计系统

## 功能简介

这个统计系统为 NO-FOMO AI 日报网站提供实时访问量统计功能，包括：

- **总访问量**：网站所有页面的累计访问次数
- **今日访问**：当天的访问量统计
- **热门页面**：访问量最高的页面排行
- **多语言主页同步**：三个主页（中文、英文、根目录）数据实时同步
- **实时更新**：数据自动实时同步更新

## 技术实现

### 客户端存储
- 使用 `localStorage` 存储访问数据
- 支持跨页面数据同步
- 数据持久化保存在用户浏览器中

### 文件结构
```
NO-FOMO/home/
├── js/
│   ├── analytics.js       # 核心统计模块
│   └── stats-display.js   # 显示增强脚本
├── index.html            # 根主页（包含统计显示）
├── cn/
│   └── index.html        # 中文主页（包含统计显示）
├── en/
│   └── index.html        # 英文主页（包含统计显示）
├── 2025-06-11/
│   ├── index.html        # 日报页面（中文）
│   └── en/
│       └── index.html    # 日报页面（英文）
└── README-analytics.md   # 本说明文件
```

## 使用方法

### 1. 在新页面中添加统计
在任何新的 HTML 页面的 `<head>` 部分添加：

```html
<script src="相对路径/js/analytics.js"></script>
```

### 2. 查看统计数据
访问主页 `index.html`，在"📊 统计概览"和"🔥 热门页面"部分查看实时数据。

### 3. 自定义页面名称
在 `analytics.js` 中的 `formatPageName` 函数里添加新的页面名称映射：

```javascript
formatPageName(pagePath) {
    if (pagePath === 'index') return '主页';
    if (pagePath === 'your-new-page') return '您的新页面';
    // 添加更多页面名称映射...
    return pagePath;
}
```

## 数据说明

### 存储格式
```javascript
{
    "totalVisits": 123,           // 总访问量
    "pageVisits": {               // 每页访问量
        "index": 50,
        "2025-06-11": 30,
        "2025-06-11/en": 25
    },
    "dailyVisits": {              // 每日访问量
        "2025-06-11": {
            "index": 10,
            "2025-06-11": 8
        }
    },
    "lastUpdated": "2025-06-11T12:00:00.000Z"
}
```

### 页面路径规则
- 根主页：`index`
- 中文主页：`cn/index`
- 英文主页：`en/index`
- 中文日报：`YYYY-MM-DD`
- 英文日报：`YYYY-MM-DD/en`
- 中文日报：`YYYY-MM-DD/cn`
- 其他页面：相对于 `/NO-FOMO/home/` 的路径

## 功能特点

### 实时同步
- 多个页面/标签页之间数据自动同步
- 三个主页（根主页、中文主页、英文主页）统计数据实时同步显示
- 访问量变化实时反映在所有统计显示中

### 动画效果
- 数字更新使用平滑动画
- 统计项目更新时高亮显示
- 实时更新状态指示器

### 轻量级
- 无需服务器支持
- 纯客户端JavaScript实现
- 文件大小小，加载速度快

## 注意事项

1. **数据范围**：统计数据仅限于当前浏览器，不同设备/浏览器的数据是独立的
2. **数据持久性**：数据存储在浏览器的 localStorage 中，清除浏览器数据会重置统计
3. **隐私友好**：不收集用户个人信息，仅统计页面访问次数
4. **兼容性**：支持现代浏览器，需要 JavaScript 和 localStorage 支持

## 自定义配置

### 修改更新频率
在主页的 JavaScript 中修改定时器间隔：

```javascript
// 当前为30秒更新一次
setInterval(updateStats, 30000);

// 修改为10秒更新一次
setInterval(updateStats, 10000);
```

### 调整热门页面显示数量
在 `updatePopularPages()` 函数中修改：

```javascript
// 显示前5个热门页面
const popularPages = analytics.getPopularPages(5);

// 修改为显示前10个
const popularPages = analytics.getPopularPages(10);
```

## 扩展建议

如需更高级的统计功能，可以考虑：

1. **服务端统计**：集成 Google Analytics 或其他专业统计服务
2. **数据导出**：添加统计数据导出功能
3. **图表展示**：使用 Chart.js 等库添加图表显示
4. **访问时长统计**：记录用户在页面停留时间
5. **用户行为分析**：添加点击热力图等功能 