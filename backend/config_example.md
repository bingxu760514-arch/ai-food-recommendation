# 豆包API配置说明

## 1. 获取豆包API密钥

1. 访问豆包开放平台：https://www.volcengine.com/product/doubao
2. 注册/登录账号
3. 创建应用并获取API密钥（API Key）

## 2. 配置环境变量

在 `backend/.env` 文件中配置：

```
DOUBAO_API_KEY=your_api_key_here
DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3
```

## 3. 配置模型名称

在 `backend/doubao_api.py` 文件中找到以下行：

```python
"model": "ep-20241222181934-kzqhd",  # 根据实际模型调整
```

将 `ep-20241222181934-kzqhd` 替换为您在豆包平台创建的实际模型ID。

## 4. 常见问题

### Q: 如果没有API密钥怎么办？
A: 系统会自动使用默认推荐理由，功能仍然可用，只是推荐理由会相对简单。

### Q: API调用失败怎么办？
A: 检查：
1. API密钥是否正确
2. 模型ID是否正确
3. API URL是否正确
4. 网络连接是否正常

### Q: 如何测试API是否配置成功？
A: 启动后端服务后，进行一次推荐，如果看到AI生成的推荐理由（而不是默认理由），说明配置成功。




