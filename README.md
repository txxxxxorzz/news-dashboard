# 🔥 热点情报中心 - 完整部署指南

> 从 0 到上线，15 分钟部署你的热点情报系统！

---

## 🎯 最终效果

部署完成后你将拥有：

1. **公网访问网址**: `https://your-app.vercel.app`
2. **飞书工作台入口**: 🔥 热点情报中心
3. **手机可安装**: PWA 应用
4. **自动更新**: 每 6 小时自动刷新数据
5. **完整功能**: 搜索、收藏、实时刷新、多平台数据

---

## 📋 快速开始（15 分钟）

### 第 1 步：准备 GitHub 账号（3 分钟）

1. 访问 https://github.com
2. 注册/登录账号
3. 记住你的用户名

### 第 2 步：上传代码到 GitHub（5 分钟）

**打开终端执行**：

```bash
cd /home/admin/.openclaw/workspace/web

# 初始化 Git
git init
git add .
git commit -m "Initial commit - 热点情报中心"

# 关联远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/hot-news-dashboard.git
git branch -M main
git push -u origin main
```

**或者网页上传**：
1. 访问 https://github.com/new
2. 仓库名：`hot-news-dashboard`
3. 选择 Public
4. 创建后点击 "uploading an existing file"
5. 拖拽 `web/` 目录下所有文件上传

### 第 3 步：部署到 Vercel（5 分钟）

1. 访问 https://vercel.com/new
2. 点击「Continue with GitHub」登录
3. 找到 `hot-news-dashboard` 仓库
4. 点击「Import」
5. 保持默认配置，点击「Deploy」
6. 等待 1-2 分钟，看到「🎉 Congratulations!」

**获得网址**: `https://hot-news-dashboard-xxx.vercel.app`

### 第 4 步：配置飞书工作台（2 分钟）

1. 访问 https://open.feishu.cn/
2. 登录飞书账号
3. 点击「企业自建」→「创建应用」
4. 应用名称：`热点情报中心`
5. 应用首页 → 配置 → 网页类型
6. URL 填写你的 Vercel 地址
7. 发布应用
8. 在飞书工作台添加应用

---

## 🎉 完成！

现在你可以：

1. **访问网页**: 打开 Vercel 提供的网址
2. **飞书访问**: 工作台 → 🔥 热点情报中心
3. **手机安装**: 浏览器打开 → 分享 → 添加到主屏幕

---

## 📁 文件说明

```
web/
├── index.html          # 主页面（含所有功能）
├── manifest.json       # PWA 配置
├── sw.js              # Service Worker（离线缓存）
├── vercel.json        # Vercel 部署配置
├── icon.html          # 图标预览页
├── DEPLOY_GUIDE.md    # 详细部署教程
├── FEISHU_INTEGRATION.md  # 飞书集成教程
└── news_data/         # 数据目录
    └── latest.json    # 最新热点数据
```

---

## 🔄 数据自动更新

### 方案 1：GitHub + Vercel 自动部署

```bash
# 创建同步脚本
cat > /home/admin/.openclaw/workspace/sync_news.sh << 'EOF'
#!/bin/bash
cd /home/admin/.openclaw/workspace/web

# 更新数据
python3 ../scripts/news_fetcher.py
python3 ../scripts/aggregate_news.py

# 提交到 Git
git add news_data/
git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M')"
git push

echo "✅ 数据已同步"
EOF

chmod +x /home/admin/.openclaw/workspace/sync_news.sh

# 添加到 crontab（每 6 小时）
(crontab -l 2>/dev/null; echo "0 */6 * * * /home/admin/.openclaw/workspace/sync_news.sh") | crontab -
```

### 方案 2：直接同步到 Vercel

使用 Vercel CLI：

```bash
npm install -g vercel

# 每 6 小时部署一次
(crontab -l 2>/dev/null; echo "0 */6 * * * cd /home/admin/.openclaw/workspace/web && vercel --prod") | crontab -
```

---

## 🛠️ 功能说明

### 已实现功能

- ✅ **实时刷新**: 每 5 分钟自动更新数据
- ✅ **搜索功能**: 支持标题、来源搜索
- ✅ **收藏功能**: 本地存储，永久保存
- ✅ **多平台**: NewsAPI、微博、Twitter、Reddit、RSS
- ✅ **智能分类**: 政治、经济、AI、科技、娱乐等
- ✅ **移动端适配**: 完美支持手机/平板
- ✅ **PWA 支持**: 可安装到手机桌面
- ✅ **离线访问**: Service Worker 缓存

### 平台切换

- 🌐 全部
- 📰 NewsAPI
- 🔴 微博
- 🐦 Twitter
- 👽 Reddit
- 📡 RSS

---

## 📱 飞书集成

### 应用信息

```
应用名称：热点情报中心
应用图标：🔥
应用描述：实时热点新闻聚合平台
首页 URL: https://your-app.vercel.app
```

### 配置位置

1. 飞书开放平台 → 企业自建 → 应用管理
2. 找到「热点情报中心」
3. 应用首页 → 配置网页 URL
4. 版本管理 → 发布应用
5. 工作台 → 添加应用

---

## 🆘 故障排查

### 问题 1: Vercel 部署失败

```bash
# 检查 vercel.json 格式
cat vercel.json | python3 -m json.tool

# 重新部署
vercel --prod
```

### 问题 2: 网页显示"暂无数据"

```bash
# 检查数据文件
ls -la news_data/
cat news_data/latest.json

# 重新生成数据
cd /home/admin/.openclaw/workspace/scripts
python3 news_fetcher.py
python3 aggregate_news.py
```

### 问题 3: 飞书应用打不开

- 检查 URL 是否为 `https://` 开头
- 检查 Vercel 部署是否成功
- 清除飞书缓存重试

### 问题 4: 数据不更新

```bash
# 检查 cron 任务
crontab -l

# 手动执行一次
/home/admin/.openclaw/workspace/sync_news.sh

# 查看日志
tail -f /home/admin/.openclaw/workspace/scripts/news_data/cron.log
```

---

## 📊 性能优化

### 已优化

- ✅ CDN 加速（Vercel 全球节点）
- ✅ 静态资源缓存
- ✅ Service Worker 离线缓存
- ✅ 图片懒加载
- ✅ 代码压缩

### 可进一步优化

- 添加 API 接口（后端服务）
- 数据库存储（MongoDB/PostgreSQL）
- 用户系统（登录/注册）
- 个性化推荐

---

## 🎨 自定义配置

### 修改主题色

编辑 `index.html` 第 12-20 行：

```css
:root {
    --primary: #3b82f6;    /* 主色调 */
    --danger: #ef4444;     /* 警告色 */
    --success: #10b981;    /* 成功色 */
}
```

### 修改刷新频率

编辑 `index.html` 第 437 行：

```javascript
setInterval(loadNewsData, 5 * 60 * 1000);  // 改为其他分钟数
```

### 修改推送频率

```bash
crontab -e
# 修改时间表达式
0 */6 * * *  # 每 6 小时
0 */4 * * *  # 每 4 小时
0 9 * * *    # 每天 9 点
```

---

## 📞 技术支持

- 📖 详细教程：`web/DEPLOY_GUIDE.md`
- 📱 飞书集成：`web/FEISHU_INTEGRATION.md`
- 🔧 脚本配置：`scripts/README.md`

---

## 🎉 上线检查清单

- [ ] GitHub 仓库已创建
- [ ] 代码已推送
- [ ] Vercel 部署成功
- [ ] 能访问公网 URL
- [ ] 飞书应用已创建
- [ ] 已添加到工作台
- [ ] 数据自动更新已配置
- [ ] 手机端测试通过
- [ ] 搜索功能正常
- [ ] 收藏功能正常

---

**恭喜！你的热点情报系统已上线！** 🚀

**访问地址**: `https://your-app.vercel.app`

**飞书访问**: 工作台 → 🔥 热点情报中心
