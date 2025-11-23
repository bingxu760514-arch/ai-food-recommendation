# GitHub授权设置 - Vercel部署

## 问题：Vercel无法访问GitHub仓库

如果Vercel显示"没有授权"，需要设置GitHub仓库的访问权限。

## 解决方案

### 方案一：将仓库设置为Public（最简单）

1. **访问您的仓库**：
   https://github.com/bingxu760514-arch/ai-food-recommendation

2. **进入设置**：
   - 点击仓库页面右上角的 **Settings**（设置）

3. **更改可见性**：
   - 在左侧菜单找到 **General**（常规）
   - 滚动到页面最底部的 **Danger Zone**（危险区域）
   - 点击 **Change visibility**（更改可见性）
   - 选择 **Make public**（设为公开）
   - 按照提示确认更改

4. **完成后**：
   - 返回Vercel，刷新页面
   - 应该就能看到您的仓库了

### 方案二：配置GitHub App权限（保持Private）

如果不想公开仓库，需要配置Vercel的GitHub App权限：

1. **在Vercel中**：
   - 访问 https://vercel.com/dashboard
   - 点击右上角头像 → **Settings**
   - 选择 **Git** 或 **Integrations**
   - 找到 **GitHub** 集成

2. **配置权限**：
   - 点击 **Configure** 或 **Edit**
   - 在权限设置中：
     - **Repository access**: 选择 "All repositories" 或 "Only select repositories"
     - 如果选择 "Only select repositories"，确保勾选您的仓库
   - **Repository permissions**:
     - ✅ Contents: Read
     - ✅ Metadata: Read
     - ✅ Pull requests: Read & Write
   - 保存设置

3. **重新导入**：
   - 返回Vercel首页
   - 点击 **Add New...** → **Project**
   - 选择 **Import Git Repository**
   - 现在应该能看到您的仓库了

### 方案三：使用Vercel CLI（无需GitHub授权）

如果以上方法都不行，可以直接使用命令行部署：

```bash
# 1. 安装Vercel CLI
npm install -g vercel

# 2. 登录Vercel
vercel login

# 3. 进入前端目录
cd frontend

# 4. 部署
vercel

# 5. 按照提示完成部署
```

## 部署配置

### 前端部署设置

在Vercel导入项目时，使用以下配置：

- **Framework Preset**: Create React App
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

### 环境变量（如果需要）

如果前端需要连接后端API，在Vercel项目设置中添加环境变量：

- `REACT_APP_API_URL`: 您的后端API地址

## 注意事项

⚠️ **后端部署**：
- Vercel主要支持前端和Serverless Functions
- FastAPI后端建议使用其他平台：
  - **Railway**: https://railway.app
  - **Render**: https://render.com
  - **Fly.io**: https://fly.io
  - **Heroku**: https://heroku.com

## 快速检查清单

- [ ] GitHub仓库已设置为Public，或
- [ ] Vercel GitHub App已授权访问您的仓库
- [ ] 在Vercel中能看到您的仓库
- [ ] 配置了正确的构建设置（Root Directory: `frontend`）
- [ ] 部署成功！

