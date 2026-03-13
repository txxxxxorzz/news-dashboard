# 热点情报中心 - 部署教程

## 📦 项目结构

```
web/
├── index.html          # 主页面（包含所有功能）
├── manifest.json       # PWA 配置
├── sw.js              # Service Worker（离线缓存）
├── package.json       # NPM 配置（可选）
└── news_data/
    └── latest.json    # 数据文件（自动更新）
```

---

## 🚀 方案 A：Vercel 部署（推荐）

### 第 1 步：准备 GitHub 账号

1. 访问 https://github.com
2. 登录或注册账号
3. 创建新仓库，例如：`news-dashboard`

### 第 2 步：上传代码到 GitHub

**方法 1：使用 Git 命令**

```bash
# 进入 web 目录
cd /home/admin/.openclaw/workspace/web

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit - 热点情报中心"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/news-dashboard.git

# 推送到 GitHub
git push -u origin main
```

**方法 2：GitHub 网页上传**

1. 打开你的 GitHub 仓库
2. 点击 "Add file" → "Upload files"
3. 把 `web/` 目录下的文件拖进去
4. 点击 "Commit changes"

### 第 3 步：部署到 Vercel

1. **访问 Vercel**
   - 打开 https://vercel.com
   - 点击 "Continue with GitHub" 登录

2. **导入项目**
   - 点击 "Add New..." → "Project"
   - 找到你的 `news-dashboard` 仓库
   - 点击 "Import"

3. **配置部署**
   - Framework Preset: 选择 "Other"
   - Build Command: 留空（静态网站无需构建）
   - Output Directory: 留空（默认根目录）
   - 点击 "Deploy"

4. **等待部署完成**
   - 大约 1-2 分钟
   - 看到绿色对勾表示成功

5. **获取访问地址**
   - 部署成功后会显示域名，如：
     ```
     https://news-dashboard-xxx.vercel.app
     ```
   - 点击 "Visit" 预览

### 第 4 步：配置自动更新（重要！）

**让 Vercel 自动同步 GitHub 更新：**

1. 在 Vercel 项目页面 → Settings → Git
2. 确保 "Production Branch" 是 `main`
3. 开启 "Auto Expose GitHub Deployments"

**配置自动推送数据：**

修改抓取脚本，在抓取后自动更新 Vercel：

```bash
# 在 scripts/news_fetcher.py 最后添加：
import subprocess

def trigger_vercel_build():
    """触发 Vercel 重新部署"""
    # 方法 1: 通过 GitHub Actions
    # 创建一个空提交来触发部署
    subprocess.run([
        'git', '-C', '/home/admin/.openclaw/workspace/web',
        'commit', '--allow-empty', '-m', 'Auto update news data'
    ])
    subprocess.run([
        'git', '-C', '/home/admin/.openclaw/workspace/web',
        'push'
    ])

# 在 main() 函数最后调用
trigger_vercel_build()
```

### 第 5 步：自定义域名（可选）

1. 在 Vercel 项目 → Settings → Domains
2. 输入你的域名，如：`news.your-domain.com`
3. 按提示配置 DNS

---

## 📱 方案 B：Netlify 部署（备选）

### 步骤

1. 访问 https://netlify.com
2. 登录 GitHub 账号
3. 点击 "Add new site" → "Import from Git"
4. 选择你的仓库
5. 配置：
   - Build command: 留空
   - Publish directory: 留空
6. 点击 "Deploy site"

---

## 🔗 飞书工作台集成

### 第 1 步：创建飞书自建应用

1. **打开飞书开放平台**
   - 访问 https://open.feishu.cn/app
   - 用飞书登录

2. **创建应用**
   - 点击 "创建应用"
   - 选择 "自建应用"
   - 填写：
     - 应用名称：热点情报中心
     - 图标：上传一个 🔥 图标
   - 点击 "创建"

3. **获取凭证**
   - 在应用管理页面，记录：
     - App ID
     - App Secret

### 第 2 步：配置应用

1. **添加网页链接**
   - 在应用管理 → 应用配置
   - 点击 "添加网页"
   - 填写：
     - 页面名称：热点榜单
     - 页面链接：你的 Vercel 地址（如 `https://news-dashboard-xxx.vercel.app`）
   - 保存

2. **配置权限**
   - 权限管理 → 添加权限
   - 搜索并添加：
     - `user:readonly` - 读取用户信息
   - 提交审核（通常自动通过）

3. **发布应用**
   - 版本管理与发布 → 创建版本
   - 填写版本号：1.0.0
   - 提交发布

### 第 3 步：添加到工作台

1. **在飞书中添加**
   - 打开飞书 → 工作台
   - 点击右上角 "..." → "添加应用"
   - 找到 "热点情报中心"
   - 点击添加

2. **或者分享给用户**
   - 在应用管理 → 版本管理与发布
   - 点击 "发布范围"
   - 添加成员或群组

---

## 📊 数据自动更新配置

### 修改 Cron 任务

编辑 crontab，在抓取后自动推送到 GitHub：

```bash
crontab -e
```

添加或修改为：

```bash
# 每 6 小时抓取 + 推送
0 */6 * * * cd /home/admin/.openclaw/workspace/scripts && source .env && python3 news_fetcher.py && python3 aggregate_news.py && python3 push_feishu.py && /home/admin/.openclaw/workspace/scripts/auto_deploy.sh >> news_data/cron.log 2>&1
```

### 创建自动部署脚本

创建 `/home/admin/.openclaw/workspace/scripts/auto_deploy.sh`：

```bash
#!/bin/bash
# 自动部署脚本

cd /home/admin/.openclaw/workspace/web

# 检查是否有更新
git status

# 如果有更新，提交并推送
if ! git diff --quiet; then
    git add news_data/latest.json
    git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M')"
    git push origin main
    echo "✅ 已推送到 GitHub，Vercel 将自动部署"
else
    echo "ℹ️  无更新"
fi
```

赋予执行权限：

```bash
chmod +x /home/admin/.openclaw/workspace/scripts/auto_deploy.sh
```

---

## ✅ 验证部署

### 1. 访问网页

打开 Vercel 提供的域名，应该看到：
- ✅ 热点榜单正常显示
- ✅ 平台切换正常
- ✅ 搜索功能可用
- ✅ 收藏功能可用

### 2. 测试 PWA

**手机访问：**
- iOS Safari: 点击分享 → 添加到主屏幕
- Android Chrome: 点击右上角 → 安装应用

### 3. 测试自动更新

等待下次抓取时间（00:00, 06:00, 12:00, 18:00），检查：
- 飞书群是否收到推送
- 网页数据是否更新
- Vercel 是否自动重新部署

---

## 🛠️ 常见问题

### Q1: Vercel 部署失败？

**检查：**
- GitHub 仓库是否公开（或 Vercel 有权限）
- 文件是否在根目录
- 查看 Vercel 部署日志

### Q2: 数据不更新？

**检查：**
- Cron 任务是否正常：`crontab -l`
- 查看日志：`tail -f news_data/cron.log`
- Git 推送是否成功

### Q3: 飞书应用打不开？

**检查：**
- 应用链接是否正确
- 是否需要翻墙访问 Vercel
- 考虑使用国内 CDN 或服务器

---

## 📞 需要帮助？

遇到问题随时在群里问我！

---

**最后更新**: 2026-03-12
