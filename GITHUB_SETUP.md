# GitHub上传指南

## 本地仓库已准备完成 ✅

项目已经初始化并提交到本地Git仓库。

## 上传到GitHub的步骤

### 方法一：使用GitHub网页创建仓库（推荐）

1. **登录GitHub**，访问 https://github.com/new

2. **创建新仓库**：
   - Repository name: `ai-food-recommendation` (或您喜欢的名称)
   - Description: `AI外卖推荐助手 - 基于豆包API的智能推荐系统`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
   - 点击 "Create repository"

3. **连接并推送代码**：
   在项目目录下运行以下命令（将 `YOUR_USERNAME` 替换为您的GitHub用户名）：

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/ai-food-recommendation.git

# 推送代码
git branch -M main
git push -u origin main
```

### 方法二：使用GitHub CLI（如果已安装）

```bash
# 创建仓库并推送
gh repo create ai-food-recommendation --public --source=. --remote=origin --push
```

## 重要提示

⚠️ **安全提醒**：
- `.env` 文件已添加到 `.gitignore`，不会被上传
- 但请确保在GitHub上不要公开您的API密钥
- 如果 `.env` 文件已经被提交，请运行：
  ```bash
  git rm --cached backend/.env
  git commit -m "Remove .env file"
  ```

## 后续更新

以后更新代码时，使用以下命令：

```bash
git add .
git commit -m "更新说明"
git push
```

