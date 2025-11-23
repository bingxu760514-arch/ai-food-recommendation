import httpx
import os
from typing import List, Dict

class DoubaoAPI:
    def __init__(self):
        self.api_key = os.getenv("DOUBAO_API_KEY")
        self.api_url = os.getenv("DOUBAO_API_URL", "https://ark.cn-beijing.volces.com/api/v3")
        
        if not self.api_key:
            raise ValueError("请在.env文件中配置DOUBAO_API_KEY。如果没有API密钥，系统将使用默认推荐理由。")
    
    async def generate_recommendation(self, restaurants: List[Dict]) -> str:
        """使用豆包API生成推荐理由"""
        try:
            # 构建推荐请求的提示词
            restaurant_info = "\n".join([
                f"- {r['name']}（{r['cuisine']}）: {r['price']}元，评分{r['rating']}，配送{r['delivery_time']}分钟"
                for r in restaurants[:5]
            ])
            
            prompt = f"""你是一个专业的外卖推荐助手。根据以下餐厅信息，为用户生成一段简洁的推荐理由（50字以内）：

{restaurant_info}

请从口味、性价比、配送速度等角度给出推荐理由。"""
            
            # 调用豆包API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "ep-20251103145219-hzndr",  # 用户配置的模型ID
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 200
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("choices", [{}])[0].get("message", {}).get("content", "推荐这些美食，希望能满足您的需求！")
                else:
                    return "根据您的筛选条件，为您推荐以下美食！"
                    
        except Exception as e:
            print(f"豆包API调用错误: {e}")
            return "根据您的筛选条件，为您推荐以下美食！"
    
    async def generate_recommendations(self, restaurants: List[Dict]) -> List[Dict]:
        """为每个餐厅生成个性化推荐理由"""
        recommendations = []
        
        for restaurant in restaurants:
            try:
                prompt = f"""你是一个专业的外卖推荐助手。为以下餐厅生成一段简洁的推荐理由（30字以内）：

餐厅：{restaurant['name']}
菜系：{restaurant['cuisine']}
价格：{restaurant['price']}元
评分：{restaurant['rating']}
配送时间：{restaurant['delivery_time']}分钟
特色：{restaurant.get('description', '')}

请给出推荐理由："""
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.api_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "ep-20251103145219-hzndr",  # 用户配置的模型ID
                            "messages": [
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 100
                        },
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        reason = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                        recommendations.append({
                            "restaurant_id": restaurant.get("id"),
                            "name": restaurant.get("name"),
                            "reason": reason
                        })
                    else:
                        recommendations.append({
                            "restaurant_id": restaurant.get("id"),
                            "name": restaurant.get("name"),
                            "reason": f"{restaurant['name']}评分高，配送快，值得一试！"
                        })
                        
            except Exception as e:
                print(f"生成推荐理由错误: {e}")
                recommendations.append({
                    "restaurant_id": restaurant.get("id"),
                    "name": restaurant.get("name"),
                    "reason": f"{restaurant['name']}评分高，配送快，值得一试！"
                })
        
        return recommendations

