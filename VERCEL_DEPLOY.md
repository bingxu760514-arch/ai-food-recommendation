# Vercel部署指南

## GitHub仓库授权设置

### 方法一：通过Vercel网站授权（推荐）

1. **访问Vercel**：https://vercel.com
2. **登录/注册**账号
3. **导入项目**：
   - 点击 "Add New..." → "Project"
   - 选择 "Import Git Repository"
   - 如果看不到您的仓库，点击 "Configure GitHub App" 或 "Adjust GitHub App Permissions"
4. **授权GitHub访问**：
   - 在GitHub授权页面，确保勾选以下权限：
     - ✅ Repository access: 选择 "All repositories" 或 "Only select repositories"（选择您的仓库）
     - ✅ Repository permissions:
       - Contents: Read
       - Metadata: Read
       - Pull requests: Read & Write（如果需要）
5. **完成授权**后，返回Vercel导入您的项目

### 方法二：检查GitHub仓库设置

1. **访问您的仓库**：https://github.com/bingxu760514-arch/ai-food-recommendation
2. **进入Settings** → **Actions** → **General**
3. **Workflow permissions**：
   - 选择 "Read and write permissions"
   - 勾选 "Allow GitHub Actions to create and approve pull requests"
4. **保存设置**

### 方法三：使用GitHub Personal Access Token

如果Vercel无法直接连接，可以使用Personal Access Token：

1. **创建Token**：
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 点击 "Generate new token (classic)"
   - 权限选择：`repo`（完整仓库访问）
   - 生成并复制Token

2. **在Vercel中使用Token**：
   - Vercel → Settings → Git → 添加GitHub集成
   - 使用Token进行连接

## Vercel部署配置

### 前端部署（React）

1. **Root Directory**: `frontend`
2. **Build Command**: `npm run build`
3. **Output Directory**: `build`
4. **Install Command**: `npm install`

### 后端部署（FastAPI）

Vercel主要支持前端部署。对于后端，建议：

1. **使用Vercel Serverless Functions**（需要调整代码结构）
2. **或使用其他平台**：
   - Railway
   - Render
   - Fly.io
   - Heroku

## 快速部署步骤

1. 确保GitHub仓库是Public或已授权Vercel访问
2. 在Vercel导入项目
3. 配置构建设置（Root Directory: `frontend`）
4. 添加环境变量（如果需要）
5. 部署！

