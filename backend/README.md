# 后端配置说明

## 环境配置

1. 创建 `.env` 文件（复制 `.env.example`）：
```bash
cp .env.example .env
```

2. 配置豆包API密钥：
```
DOUBAO_API_KEY=your_doubao_api_key_here
DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3
```

**注意**：
- `DOUBAO_API_KEY`: 在豆包开放平台获取的API密钥
- `DOUBAO_API_URL`: 豆包API的端点URL
- 模型名称（model）在 `doubao_api.py` 中配置，请根据您的实际模型名称修改

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动

## 数据集

数据集位于 `data/restaurants.csv`，包含50家餐厅的示例数据。

您可以：
1. 直接使用示例数据
2. 替换为您自己的数据集（CSV格式，字段需包含：id, name, cuisine, price, rating, delivery_time, description）
3. 从公开数据集导入数据

## API接口

- `GET /api/restaurants` - 获取所有餐厅
- `GET /api/cuisines` - 获取所有菜系
- `POST /api/recommend` - 基于筛选条件推荐外卖




