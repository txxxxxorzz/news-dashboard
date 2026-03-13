# 🔥 热点情报中心 - Vercel 部署超详细教程

## 📋 部署前准备

### 需要的东西
- ✅ GitHub 账号（没有就注册一个，5 分钟）
- ✅ 本项目文件（已在 `/home/admin/.openclaw/workspace/web/`）
- ✅ 5 分钟时间

---

## 🚀 方案 A：通过 GitHub 部署（推荐，最简单）

### 第 1 步：创建 GitHub 仓库

1. **访问 GitHub**
   - 打开 https://github.com
   - 登录你的账号

2. **创建新仓库**
   - 点击右上角「**+**」→「**New repository**」
   - Repository name: `hot-news-dashboard`（或你喜欢的名字）
   - 选择 **Public**（公开）
   - ✅ 勾选 "Add a README file"
   - 点击「**Create repository**」

---

### 第 2 步：上传网页文件

**方法 1：网页上传（最简单）**

1. 在刚创建的仓库页面，点击「**Add file**」→「**Upload files**」

2. 打开你本地的文件目录：
   ```
   /home/admin/.openclaw/workspace/web/
   ```

3. **拖拽以下文件到上传区域**：
   - `index.html`
   - `manifest.json`
   - `sw.js`
   - `vercel.json`
   - 整个 `news_data/` 文件夹（如果有）

4. 在下方输入提交信息：`Initial commit - 热点情报网页`

5. 点击「**Commit changes**」

**方法 2：Git 命令行（如果你熟悉 Git）**

```bash
cd /home/admin/.openclaw/workspace/web

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit - 热点情报网页"

# 关联远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/hot-news-dashboard.git

# 推送
git branch -M main
git push -u origin main
```

---

### 第 3 步：部署到 Vercel

1. **访问 Vercel**
   - 打开 https://vercel.com
   - 点击「**Sign Up**」或「**Log In**」
   - 选择「**Continue with GitHub**」授权登录

2. **导入项目**
   - 登录后点击「**Add New...**」→「**Project**」
   - 在 "Import Git Repository" 页面找到你的 `hot-news-dashboard` 仓库
   - 点击「**Import**」

3. **配置项目**
   - Project Name: `hot-news-dashboard`（可改）
   - Framework Preset: 选择「**Other**」
   - Root Directory: 保持默认（`.`）
   - Build Command: **留空**
   - Output Directory: **留空**

4. **点击「Deploy」**
   - 等待 1-2 分钟
   - 看到「🎉 Congratulations!」表示成功！

5. **获得访问地址**
   - 你会得到一个域名：`https://hot-news-dashboard-xxx.vercel.app`
   - 点击「**Visit**」打开看看！

---

### 第 4 步：配置自动更新（重要！）

现在网页是静态的，需要配置自动更新数据：

**修改 `index.html` 中的数据源 URL**：

1. 在你的 Vercel 项目页面，点击「**Settings**」→「**Environment Variables**」

2. 添加环境变量（如果需要）

3. **或者**，修改 `index.html` 第 434 行：
   ```javascript
   const DATA_URL = 'https://your-server.com/news_data/latest.json';
   ```
   改成你的服务器地址

**自动更新方案**：

在你的服务器上添加一个定时任务，每 6 小时把新数据同步到 GitHub：

```bash
# 添加到 crontab
crontab -e

# 添加这行（每 6 小时同步一次）
0 */6 * * * cd /home/admin/.openclaw/workspace/web && git add news_data/ && git commit -m "Auto update news data" && git push
```

---

## 🚀 方案 B：Vercel CLI 部署（更快速）

### 第 1 步：安装 Vercel CLI

```bash
# 安装 Node.js（如果没有）
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 Vercel CLI
npm install -g vercel
```

### 第 2 步：登录 Vercel

```bash
cd /home/admin/.openclaw/workspace/web
vercel login
```
选择「**Continue with GitHub**」

### 第 3 步：部署

```bash
vercel
```

按提示操作：
- Set up and deploy? **Y**
- Which scope? 选择你的账号
- Link to existing project? **N**
- Project name? 输入 `hot-news-dashboard`
- Directory? 按回车（默认当前目录）
- Want to modify settings? **N**

等待部署完成！

### 第 4 步：生产环境部署

```bash
vercel --prod
```

获得正式域名！

---

## 📱 飞书工作台集成

### 第 1 步：创建飞书应用

1. **访问飞书开放平台**
   - 打开 https://open.feishu.cn/
   - 登录你的飞书账号

2. **创建应用**
   - 点击「**企业自建**」→「**创建应用**」
   - 应用名称：`热点情报中心`
   - 应用图标：上传一个 🔥 图标
   - 点击「**创建**」

3. **配置应用首页**
   - 在左侧菜单找到「**应用首页**」
   - 点击「**配置**」
   - 首页类型：选择「**网页**」
   - PC 端首页 URL: `https://your-vercel-app.vercel.app`
   - 移动端首页 URL: `https://your-vercel-app.vercel.app`
   - 点击「**保存**」

4. **发布应用**
   - 点击左侧「**版本管理与发布**」
   - 点击「**创建版本**」
   - 填写版本信息
   - 点击「**提交审核**」（通常自动通过）

### 第 2 步：添加到工作台

1. **在飞书中打开工作台**
   - 打开飞书
   - 点击底部「**工作台**」

2. **添加应用**
   - 点击右上角「**+**」或「**添加应用**」
   - 找到「**热点情报中心**」
   - 点击「**添加**」

3. **完成！**
   - 现在工作台有 🔥 图标了
   - 点击直接打开热点情报页面

---

## 🎯 数据自动同步方案

### 方案 1：GitHub + Vercel 自动部署

在你的服务器上：

```bash
# 创建同步脚本
cat > /home/admin/.openclaw/workspace/sync_to_github.sh << 'EOF'
#!/bin/bash
cd /home/admin/.openclaw/workspace/web

# 更新数据
python3 ../scripts/news_fetcher.py
python3 ../scripts/aggregate_news.py

# 提交到 Git
git add news_data/
git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M')"
git push

echo "数据已同步到 GitHub"
EOF

chmod +x /home/admin/.openclaw/workspace/sync_to_github.sh

# 添加到 crontab（每 6 小时）
(crontab -l 2>/dev/null; echo "0 */6 * * * /home/admin/.openclaw/workspace/sync_to_github.sh") | crontab -
```

### 方案 2：直接部署到服务器

如果你有云服务器：

```bash
# 在服务器上
scp -r /home/admin/.openclaw/workspace/web user@your-server:/var/www/html

# Nginx 配置
server {
    listen 80;
    server_name news.your-domain.com;
    root /var/www/html;
    index index.html;
    
    location /news_data {
        add_header Cache-Control "public, max-age=60";
    }
}
```

---

## ✅ 检查清单

- [ ] GitHub 仓库已创建
- [ ] 文件已上传到 GitHub
- [ ] Vercel 已部署成功
- [ ] 能访问 `https://xxx.vercel.app`
- [ ] 飞书应用已创建
- [ ] 已添加到工作台
- [ ] 数据自动同步已配置

---

## 🆘 常见问题

**Q: Vercel 部署失败？**
A: 检查 `vercel.json` 格式，确保没有语法错误

**Q: 网页显示"暂无数据"？**
A: 确保 `news_data/latest.json` 文件存在并已推送

**Q: 飞书应用打不开？**
A: 检查 URL 是否正确，确保是 `https://` 开头

**Q: 手机看不到安装按钮？**
A: PWA 需要 HTTPS，Vercel 自动提供

---

## 🎉 完成！

部署成功后你会得到：
- ✅ 公网可访问的网址
- ✅ 飞书工作台快捷入口
- ✅ 手机可安装的 PWA
- ✅ 自动更新的数据

**网址格式**: `https://hot-news-dashboard-xxx.vercel.app`

**下一步**: 把网址发给我，我帮你测试！🚀
