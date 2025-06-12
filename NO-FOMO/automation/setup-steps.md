# 🚀 Google Analytics 设置步骤

## 当前步骤：设置数据流

### 填写表单
1. **Stream name**: `NO-FOMO AI Daily Report`
2. **Website URL**: `https://opusair.github.io/NO-FOMO/home/` ✅
3. **Enhanced measurement**: 保持勾选 ✅

### 点击 "Create stream" 按钮

## 下一步：获取衡量ID

创建数据流后，您将看到：

### 1. 数据流详情页面
- 会显示您的 **衡量ID**（格式：`G-XXXXXXXXXX`）
- 复制这个ID，稍后需要用到

### 2. 实施跟踪代码
您会看到类似这样的代码：
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**不用手动添加这些代码！** 我们的自动化脚本会处理。

## 第三步：配置网站

拿到衡量ID后，运行以下命令：

```bash
# 进入项目目录
cd /Users/foreverwaterrr/Documents/code/mcp/opusair.github\ 2.io/NO-FOMO/automation

# 批量替换所有文件中的占位符
find ../home -name "*.html" -exec sed -i '' 's/GA_MEASUREMENT_ID/G-您的实际ID/g' {} \;

# 例如，如果您的ID是 G-ABC123XYZ
find ../home -name "*.html" -exec sed -i '' 's/GA_MEASUREMENT_ID/G-ABC123XYZ/g' {} \;
```

## 第四步：验证设置

1. **提交代码到GitHub**：
   ```bash
   git add .
   git commit -m "添加Google Analytics跟踪"
   git push
   ```

2. **等待部署**（GitHub Pages通常需要几分钟）

3. **验证统计**：
   - 访问您的网站：https://opusair.github.io/NO-FOMO/home/
   - 在GA控制台的"实时"报告中查看是否有访问数据

## 🎯 预期效果

设置完成后，您将能够看到：
- 📊 实时访问者数量
- 📈 页面浏览量统计
- 🌍 访问者地理分布
- 📱 设备类型分析
- 🔗 热门页面排行

## ❓ 需要帮助？

如果在设置过程中遇到问题，请告诉我：
1. 您的衡量ID
2. 遇到的具体错误信息
3. 当前所在的设置步骤 