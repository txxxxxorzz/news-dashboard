# 🚀 热点情报中心 - 5 分钟快速部署

## ⚡ 超简单 3 步走

### 第 1 步：创建 GitHub 仓库（2 分钟）

```
1. 访问 https://github.com/new
2. 仓库名：hot-news-dashboard
3. 选择 Public
4. 点击「Create repository」
```

### 第 2 步：上传文件（2 分钟）

**在服务器执行**：

```bash
cd /home/admin/.openclaw/workspace/web
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/hot-news-dashboard.git
git push -u origin main
```

**或网页上传**：
- 在 GitHub 仓库页点击「uploading an existing file」
- 拖拽 web/ 目录下所有文件
- 点击「Commit changes」

### 第 3 步：部署到 Vercel（1 分钟）

```
1. 访问 https://vercel.com/new
2. 点击「Continue with GitHub」
3. 找到 hot-news-dashboard 仓库
4. 点击「Import」→「Deploy」
5. 等待 1 分钟完成！
```

---

## 🎉 完成！

**你将获得**：
- ✅ 公网网址：`https://hot-news-dashboard-xxx.vercel.app`
- ✅ 飞书工作台入口
- ✅ 手机可安装 PWA

**飞书配置**：
1. 访问 https://open.feishu.cn/
2. 创建企业自建应用
3. 应用首页 URL 填你的 Vercel 地址
4. 发布并添加到工作台

---

## 📖 详细教程

- 完整部署：`web/DEPLOY_GUIDE.md`
- 飞书集成：`web/FEISHU_INTEGRATION.md`
- 功能说明：`web/README.md`

---

## 🆘 需要帮助？

**常见问题**：
- GitHub 创建失败？→ 检查网络连接
- Vercel 部署失败？→ 检查 vercel.json 格式
- 飞书打不开？→ 确保 URL 是 https:// 开头

**随时在群里问我！** 😊
