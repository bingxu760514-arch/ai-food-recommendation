# 项目设置指南

## 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

## 快速设置步骤

### 第一步：配置后端

1. 进入后端目录：
```bash
cd backend
```

2. 安装Python依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
   - 复制 `env.example` 为 `.env`
   - Windows: `copy env.example .env`
   - Linux/Mac: `cp env.example .env`
   
4. 编辑 `.env` 文件，填入您的豆包API密钥：
```
DOUBAO_API_KEY=您的API密钥
DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3
```

**注意**：如果没有豆包API密钥，系统仍可运行，但推荐理由将使用默认格式。

5. 启动后端服务：
```bash
python main.py
```

后端服务将在 `http://localhost:8000` 启动。

### 第二步：配置前端

1. 打开新的终端窗口，进入前端目录：
```bash
cd frontend
```

2. 安装Node.js依赖：
```bash
npm install
```

3. 启动前端开发服务器：
```bash
npm start
```

前端将在 `http://localhost:3000` 启动，浏览器会自动打开。

## 使用说明

1. **筛选餐厅**：
   - 选择菜系类型（如川菜、湘菜等）
   - 设置价格范围（最低价-最高价）
   - 选择最低评分要求
   - 选择最长配送时间
   - 输入关键词搜索

2. **查看推荐**：
   - 点击"开始推荐"按钮
   - 查看AI生成的推荐理由
   - 浏览符合条件的餐厅列表

3. **重置筛选**：
   - 点击"重置筛选"按钮清除所有筛选条件

## 故障排除

### 后端启动失败

- 检查Python版本：`python --version`（需要3.8+）
- 检查依赖是否安装完整：`pip list`
- 检查端口8000是否被占用

### 前端启动失败

- 检查Node.js版本：`node --version`（需要16+）
- 删除 `node_modules` 后重新安装：`rm -rf node_modules && npm install`
- 检查端口3000是否被占用

### API调用失败

- 检查 `.env` 文件中的API密钥是否正确
- 检查网络连接
- 查看后端控制台的错误信息
- 如果没有API密钥，系统会使用默认推荐理由

## 数据集说明

- 默认数据集：`backend/data/restaurants.csv`
- 包含50家餐厅的示例数据
- 可以替换为您自己的数据集（CSV格式）
- 必需字段：id, name, cuisine, price, rating, delivery_time, description

## 下一步

- 替换为您自己的数据集
- 自定义筛选条件
- 优化AI推荐逻辑
- 添加更多功能（如收藏、历史记录等）




