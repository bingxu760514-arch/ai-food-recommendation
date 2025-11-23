# AI外卖推荐助手

基于豆包API的智能外卖推荐系统，通过聊天对话的方式，根据用户的位置和需求智能推荐合适的外卖餐厅。

## 功能特点

- 💬 聊天式交互，自然对话推荐
- 🌍 自动获取用户IP地址和地理位置
- 🤖 豆包API智能理解用户需求
- 📊 基于公开数据集
- 💻 Web界面，简洁易用

## 技术栈

- 前端：React + TypeScript
- 后端：Python FastAPI
- AI：豆包API
- 数据：CSV数据集

## 快速开始

### 1. 配置后端

1. 进入后端目录：
```bash
cd backend
```

2. 创建环境变量文件（复制示例文件）：
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

3. 编辑 `.env` 文件，配置豆包API密钥：
```
DOUBAO_API_KEY=your_doubao_api_key_here
DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3
```

**注意**：如果没有豆包API密钥，系统仍可使用默认推荐理由运行。配置说明详见 `backend/config_example.md`

4. 安装依赖并启动后端：
```bash
pip install -r requirements.txt
python main.py
```

后端将在 `http://localhost:8000` 启动

### 2. 配置前端

1. 打开新的终端，进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动前端开发服务器：
```bash
npm start
```

前端将在 `http://localhost:3000` 启动

## 功能说明

### 聊天式推荐功能

- **自然对话**：像和朋友聊天一样，用自然语言描述你的需求
- **智能理解**：AI自动理解你的需求（菜系、价格、口味、配送时间等）
- **位置感知**：自动获取你的IP地址，推荐适合你所在城市的餐厅
- **多轮对话**：支持多轮对话，可以细化需求或询问更多信息
- **餐厅展示**：推荐结果以卡片形式展示，包含价格、评分、配送时间等信息

### 使用示例

- "我想吃点辣的"
- "推荐一些价格在50元以下的餐厅"
- "我想吃川菜，30分钟内能送到的"
- "有什么评分高的日式料理吗？"

## 数据集

- 数据集位于 `backend/data/restaurants.csv`
- 包含50家餐厅的示例数据
- 可以替换为您自己的数据集（CSV格式）

