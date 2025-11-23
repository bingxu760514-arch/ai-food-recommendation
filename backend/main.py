from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import os
from dotenv import load_dotenv
from doubao_api import DoubaoAPI
from recommendation import RecommendationEngine
import httpx

load_dotenv()

app = FastAPI(title="AI外卖推荐助手")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化推荐引擎
recommendation_engine = RecommendationEngine()

class FilterRequest(BaseModel):
    cuisine: Optional[str] = None  # 菜系
    min_price: Optional[float] = None  # 最低价格
    max_price: Optional[float] = None  # 最高价格
    min_rating: Optional[float] = None  # 最低评分
    max_delivery_time: Optional[int] = None  # 最长配送时间（分钟）
    keyword: Optional[str] = None  # 关键词搜索

class ChatRequest(BaseModel):
    message: str  # 用户消息
    conversation_history: Optional[List[dict]] = []  # 对话历史

@app.get("/")
async def root():
    return {"message": "AI外卖推荐助手 API"}

@app.get("/api/restaurants")
async def get_restaurants():
    """获取所有餐厅列表"""
    restaurants = recommendation_engine.get_all_restaurants()
    return {"data": restaurants}

@app.get("/api/cuisines")
async def get_cuisines():
    """获取所有菜系列表"""
    cuisines = recommendation_engine.get_all_cuisines()
    return {"data": cuisines}

def get_client_ip(request: Request) -> str:
    """获取客户端IP地址"""
    # 优先从X-Forwarded-For获取（代理服务器）
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    # 从X-Real-IP获取
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    # 直接从客户端获取
    if request.client:
        return request.client.host
    return "unknown"

async def get_location_from_ip(ip: str) -> dict:
    """根据IP地址获取地理位置信息（使用免费API）"""
    # 如果是本地IP，跳过API调用
    if ip in ["127.0.0.1", "localhost", "::1", "unknown"] or ip.startswith("192.168.") or ip.startswith("10."):
        return {
            "city": "北京",  # 默认城市
            "region": "北京",
            "country": "中国"
        }
    
    try:
        # 使用ipapi.co免费API（无需密钥）
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://ipapi.co/{ip}/json/",
                timeout=5.0
            )
            if response.status_code == 200:
                data = response.json()
                # 检查是否有错误
                if "error" in data:
                    raise Exception(data.get("reason", "API返回错误"))
                return {
                    "city": data.get("city", "未知"),
                    "region": data.get("region", "未知"),
                    "country": data.get("country_name", "未知")
                }
    except Exception as e:
        print(f"获取IP地理位置失败 ({ip}): {e}")
    
    # 如果获取失败，返回默认值
    return {
        "city": "北京",  # 默认城市
        "region": "北京",
        "country": "中国"
    }

@app.post("/api/chat")
async def chat(request: ChatRequest, http_request: Request):
    """聊天接口，根据用户消息和IP地址推荐餐厅"""
    try:
        # 获取用户IP地址
        try:
            client_ip = get_client_ip(http_request)
            # 获取地理位置信息
            location = await get_location_from_ip(client_ip)
            location_str = f"{location['city']}市" if location['city'] != "未知" else "您所在的城市"
        except Exception as e:
            print(f"获取位置信息失败: {e}")
            location_str = "您所在的城市"  # 使用默认值
        
        # 获取所有餐厅数据
        try:
            all_restaurants = recommendation_engine.get_all_restaurants()
        except Exception as e:
            print(f"获取餐厅数据失败: {e}")
            raise HTTPException(status_code=500, detail="获取餐厅数据失败")
        
        # 使用豆包API理解用户需求并推荐
        try:
            response_data = await recommendation_engine.chat_recommend(
                user_message=request.message,
                conversation_history=request.conversation_history or [],
                location=location_str,
                restaurants=all_restaurants
            )
            return response_data
        except Exception as e:
            print(f"聊天推荐失败: {e}")
            import traceback
            traceback.print_exc()
            # 返回友好的错误消息
            return {
                "message": f"抱歉，处理您的请求时出现错误：{str(e)}。请稍后重试。",
                "restaurants": [],
                "type": "error"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"聊天接口异常: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@app.post("/api/recommend")
async def recommend(request: FilterRequest):
    """基于筛选条件推荐外卖"""
    try:
        results = recommendation_engine.filter_restaurants(
            cuisine=request.cuisine,
            min_price=request.min_price,
            max_price=request.max_price,
            min_rating=request.min_rating,
            max_delivery_time=request.max_delivery_time,
            keyword=request.keyword
        )
        
        # 使用豆包API生成推荐理由
        if results:
            recommendations = await recommendation_engine.generate_recommendations(results[:5])
        else:
            recommendations = []
            
        return {
            "data": results,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




