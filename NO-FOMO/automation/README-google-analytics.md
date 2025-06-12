# Google Analytics 设置指南

本项目已集成Google Analytics 4 (GA4)，提供专业的网站访问统计功能。

## 📊 功能特性

- ✅ **跨用户统计** - 真正的全站访问量统计
- ✅ **实时数据** - 实时访问者监控
- ✅ **详细报告** - 页面浏览量、访问时长、用户行为等
- ✅ **移动友好** - 自动适配移动设备
- ✅ **无需维护** - Google自动处理数据存储和分析

## 🚀 快速设置

### 1. 创建Google Analytics账户

1. 访问 [Google Analytics](https://analytics.google.com/)
2. 使用Google账户登录
3. 点击"开始衡量"
4. 创建账户和资源

### 2. 获取衡量ID

1. 在GA4控制台中，转到"管理" > "数据流"
2. 选择你的网络数据流
3. 复制"衡量ID"（格式：G-XXXXXXXXXX）

### 3. 配置网站

**方法一：手动替换（推荐）**

在所有HTML文件中找到并替换：
```html
<!-- 将这个占位符 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'GA_MEASUREMENT_ID');
</script>

<!-- 替换为你的实际ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
</script>
```

**方法二：使用自动化脚本**

```bash
# 批量替换所有文件中的GA_MEASUREMENT_ID
cd NO-FOMO/automation
find ../home -name "*.html" -exec sed -i 's/GA_MEASUREMENT_ID/G-XXXXXXXXXX/g' {} \;
```

### 4. 验证安装

1. 部署网站到生产环境
2. 在GA4控制台中查看"实时"报告
3. 访问你的网站，确认能看到实时访问者

## 📈 查看统计数据

### 在Google Analytics控制台中：

1. **实时报告** - 查看当前在线用户
2. **受众群体** - 了解访问者特征
3. **获客** - 查看流量来源
4. **行为** - 分析页面浏览情况
5. **转化** - 设置和跟踪目标

### 常用指标：

- **页面浏览量** - 总访问次数
- **用户数** - 独立访问者数量
- **会话数** - 访问会话总数
- **平均会话时长** - 用户停留时间
- **跳出率** - 单页访问比例

## 🔧 管理命令

```bash
# 为所有页面添加Google Analytics
python3 daily_report_manager.py --sync-ga

# 同步所有内容（包括GA）
python3 daily_report_manager.py --sync-all

# 不自动提交Git
python3 daily_report_manager.py --sync-ga --no-commit
```

## 🔒 隐私保护

Google Analytics默认配置已符合GDPR要求：
- 自动匿名化IP地址
- 不收集个人身份信息
- 数据保留期限可配置

## ❓ 常见问题

**Q: 为什么看不到数据？**
A: 新设置的GA4通常需要24-48小时才能显示历史数据，但实时数据会立即显示。

**Q: 如何过滤自己的访问？**
A: 在GA4中设置IP过滤器，或使用Google Analytics Debugger扩展。

**Q: 数据准确性如何？**
A: Google Analytics是行业标准，准确性高于95%。

**Q: 需要添加隐私政策吗？**
A: 建议添加，特别是面向欧盟用户的网站。

## 📚 进阶功能

### 自定义事件跟踪

```javascript
// 跟踪日报下载
gtag('event', 'download', {
    'event_category': 'engagement',
    'event_label': '2025-06-11'
});

// 跟踪外链点击
gtag('event', 'click', {
    'event_category': 'outbound',
    'event_label': 'github'
});
```

### 电子商务跟踪

如果将来需要跟踪转化：

```javascript
gtag('event', 'purchase', {
    'transaction_id': '12345',
    'value': 25.25,
    'currency': 'USD'
});
```

## 🛠 故障排除

1. **检查控制台错误** - 打开浏览器开发者工具
2. **验证GA代码** - 确保ID格式正确（G-开头）
3. **检查网络连接** - 确保能访问google-analytics.com
4. **使用GA调试扩展** - Chrome扩展可显示详细调试信息

---

💡 **提示**: Google Analytics提供免费且强大的分析功能，建议充分利用其报告和洞察功能来优化网站内容。 