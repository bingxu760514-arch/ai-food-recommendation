import pandas as pd
import os
from typing import List, Dict, Optional
import httpx
import re
from doubao_api import DoubaoAPI

class RecommendationEngine:
    def __init__(self):
        # 加载数据集
        data_path = os.path.join(os.path.dirname(__file__), "data", "restaurants.csv")
        if os.path.exists(data_path):
            self.df = pd.read_csv(data_path, encoding='utf-8-sig')
        else:
            # 如果没有数据集，使用示例数据
            self.df = self._create_sample_data()
            # 确保数据目录存在
            os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
            self.df.to_csv(data_path, index=False, encoding='utf-8-sig')
        
        # 延迟初始化豆包API，避免配置错误时立即失败
        self.doubao_api = None
    
    def _create_sample_data(self) -> pd.DataFrame:
        """创建示例数据集"""
        data = {
            "id": range(1, 51),
            "name": [
                "川味小厨", "湘味轩", "粤式茶餐厅", "东北饺子王", "新疆大盘鸡",
                "重庆小面", "兰州拉面", "沙县小吃", "黄焖鸡米饭", "麻辣香锅",
                "日式拉面屋", "韩式烤肉", "泰式料理", "意式披萨", "法式西餐",
                "麦当劳", "肯德基", "必胜客", "星巴克", "一点点",
                "海底捞火锅", "小龙坎", "大龙燚", "呷哺呷哺", "小肥羊",
                "老乡鸡", "真功夫", "永和大王", "李先生", "和合谷",
                "西贝莜面村", "外婆家", "绿茶餐厅", "南京大牌档", "眉州东坡",
                "全聚德", "便宜坊", "东来顺", "护国寺小吃", "庆丰包子铺",
                "杨国福麻辣烫", "张亮麻辣烫", "小杨生煎", "阿香米线", "味千拉面",
                "吉野家", "食其家", "丸龟制面", "萨莉亚", "达美乐披萨"
            ],
            "cuisine": [
                "川菜", "湘菜", "粤菜", "东北菜", "新疆菜",
                "川菜", "面食", "快餐", "快餐", "川菜",
                "日式", "韩式", "泰式", "意式", "法式",
                "快餐", "快餐", "快餐", "饮品", "饮品",
                "火锅", "火锅", "火锅", "火锅", "火锅",
                "快餐", "快餐", "快餐", "快餐", "快餐",
                "西北菜", "杭帮菜", "江浙菜", "江浙菜", "川菜",
                "京菜", "京菜", "京菜", "京菜", "京菜",
                "麻辣烫", "麻辣烫", "江浙菜", "快餐", "日式",
                "日式", "日式", "日式", "意式", "意式"
            ],
            "price": [
                45, 52, 68, 38, 55, 25, 22, 20, 28, 58,
                48, 85, 72, 65, 120, 35, 38, 55, 40, 25,
                95, 88, 92, 75, 85, 35, 32, 28, 25, 30,
                75, 65, 58, 72, 68, 150, 85, 120, 35, 25,
                32, 28, 25, 22, 45, 38, 35, 42, 48, 62
            ],
            "rating": [
                4.5, 4.6, 4.7, 4.4, 4.5, 4.3, 4.2, 4.0, 4.1, 4.6,
                4.4, 4.5, 4.6, 4.5, 4.8, 4.2, 4.3, 4.4, 4.5, 4.3,
                4.7, 4.6, 4.7, 4.5, 4.6, 4.3, 4.2, 4.1, 4.0, 4.2,
                4.6, 4.5, 4.4, 4.7, 4.6, 4.8, 4.5, 4.7, 4.2, 4.1,
                4.3, 4.2, 4.4, 4.1, 4.3, 4.2, 4.1, 4.3, 4.4, 4.5
            ],
            "delivery_time": [
                35, 40, 45, 30, 50, 25, 28, 20, 30, 40,
                35, 45, 50, 40, 60, 30, 35, 45, 25, 20,
                50, 55, 60, 45, 50, 30, 28, 25, 25, 30,
                45, 40, 35, 50, 45, 60, 40, 55, 30, 25,
                30, 28, 25, 30, 35, 32, 30, 35, 38, 45
            ],
            "description": [
                "正宗川味，麻辣鲜香", "湖南风味，香辣下饭", "广式茶点，精致美味", "东北风味，分量十足", "新疆特色，大盘实惠",
                "重庆小面，麻辣过瘾", "兰州拉面，汤鲜味美", "沙县小吃，经济实惠", "黄焖鸡米饭，嫩滑香浓", "麻辣香锅，食材丰富",
                "日式拉面，汤底浓郁", "韩式烤肉，肉质鲜嫩", "泰式料理，酸甜开胃", "意式披萨，芝士拉丝", "法式西餐，精致浪漫",
                "快餐连锁，方便快捷", "炸鸡汉堡，经典美味", "披萨意面，多种选择", "咖啡饮品，提神醒脑", "奶茶果茶，香甜可口",
                "火锅连锁，服务贴心", "重庆火锅，麻辣鲜香", "四川火锅，地道正宗", "台式火锅，清淡健康", "内蒙古火锅，羊肉鲜嫩",
                "中式快餐，营养搭配", "蒸菜快餐，健康美味", "台式快餐，米饭配菜", "牛肉面，汤鲜肉烂", "日式快餐，精致美味",
                "西北风味，面食丰富", "杭帮菜，清淡精致", "江浙菜，甜咸适中", "南京风味，鸭血粉丝", "川菜连锁，菜品丰富",
                "北京烤鸭，皮脆肉嫩", "焖炉烤鸭，别有风味", "涮羊肉，肉质鲜嫩", "北京小吃，种类丰富", "包子铺，馅料多样",
                "麻辣烫，自选食材", "麻辣烫连锁，口味统一", "生煎包，皮薄馅大", "米线，汤鲜味美", "日式拉面，汤底浓郁",
                "日式快餐，牛肉饭", "日式快餐，多种套餐", "日式面食，乌冬面", "意式快餐，经济实惠", "披萨连锁，外送快速"
            ],
            "signature_dish": [
                "麻婆豆腐、水煮鱼、宫保鸡丁", "剁椒鱼头、口味虾、小炒肉", "虾饺、烧卖、叉烧包", "猪肉大葱饺子、锅包肉、地三鲜", "大盘鸡、羊肉串、手抓饭",
                "重庆小面、豌杂面、红油抄手", "牛肉拉面、羊肉拉面、凉拌牛肉", "扁肉、拌面、蒸饺", "黄焖鸡米饭、黄焖排骨", "麻辣香锅、干锅牛蛙",
                "豚骨拉面、味增拉面、日式炸鸡", "韩式烤肉、石锅拌饭、泡菜汤", "冬阴功汤、泰式咖喱、芒果糯米饭", "玛格丽特披萨、意大利面、提拉米苏", "牛排、鹅肝、法式蜗牛",
                "巨无霸、薯条、麦乐鸡", "原味鸡、香辣鸡腿堡、蛋挞", "超级至尊披萨、意式肉酱面", "拿铁、美式咖啡、星冰乐", "珍珠奶茶、四季春茶、波霸奶茶",
                "毛肚、虾滑、牛肉片", "麻辣牛肉、鸭肠、脑花", "嫩牛肉、黄喉、毛肚", "肥牛、蔬菜拼盘、虾滑", "羊肉片、羊蝎子、手切羊肉",
                "鸡汤、蒸蛋、小菜", "蒸蛋、蒸排骨、蒸鸡", "卤肉饭、豆浆、油条", "牛肉面、小菜", "日式套餐、味增汤",
                "莜面、羊肉串、凉皮", "西湖醋鱼、东坡肉、龙井虾仁", "糖醋里脊、白切鸡、小笼包", "鸭血粉丝汤、盐水鸭、小笼包", "东坡肉、麻婆豆腐、宫保鸡丁",
                "北京烤鸭、鸭架汤、京酱肉丝", "焖炉烤鸭、炸酱面", "涮羊肉、芝麻烧饼", "豆汁、焦圈、驴打滚", "猪肉大葱包子、三鲜包子",
                "麻辣烫、自选配菜", "麻辣烫、自选配菜", "生煎包、小笼包", "过桥米线、酸辣米线", "味千拉面、日式炸鸡",
                "牛肉饭、照烧鸡排饭", "牛丼饭、咖喱饭", "乌冬面、天妇罗", "意式肉酱面、披萨", "经典披萨、意式香肠披萨"
            ],
            "reviews": [
                "味道正宗，麻辣鲜香！|分量很足，性价比高|服务态度好，配送快",
                "湘菜很正宗，辣得过瘾|菜品新鲜，味道好|价格合理，值得推荐",
                "茶点很精致，味道正宗|环境不错，适合聚餐|价格稍贵但值得",
                "饺子皮薄馅大，很好吃|分量真的很足|性价比超高",
                "大盘鸡分量足，味道好|羊肉串很香|配送时间稍长但值得等",
                "小面很正宗，麻辣过瘾|价格便宜，性价比高|配送快，包装好",
                "拉面劲道，汤很鲜|价格实惠|配送及时",
                "价格便宜，味道不错|配送很快|适合工作餐",
                "鸡肉嫩滑，米饭香|价格实惠|配送准时",
                "食材新鲜，味道好|可以自选配菜|分量足",
                "拉面汤底浓郁，很正宗|环境干净|价格适中",
                "肉质新鲜，烤得很好|配菜丰富|价格稍贵但值得",
                "泰式风味正宗|酸甜开胃|配送时间稍长",
                "披萨芝士拉丝，很好吃|意面正宗|价格合理",
                "菜品精致，味道好|环境优雅|价格较高但值得",
                "经典快餐，味道稳定|配送快|价格适中",
                "炸鸡外酥里嫩|配送准时|性价比不错",
                "披萨种类多|味道不错|配送及时",
                "咖啡香浓|服务好|配送快",
                "奶茶好喝，甜度可选|价格便宜|配送快",
                "服务很好，食材新鲜|配送包装好|价格稍贵",
                "重庆火锅很正宗|麻辣过瘾|配送时间稍长",
                "四川火锅地道|食材新鲜|味道好",
                "台式火锅清淡|适合不吃辣的人|价格合理",
                "羊肉很新鲜|汤底好|配送及时",
                "营养搭配好|味道不错|价格实惠",
                "蒸菜健康|味道清淡|配送快",
                "台式快餐正宗|价格便宜|配送及时",
                "牛肉面汤鲜|价格实惠|配送快",
                "日式快餐精致|味道好|价格适中",
                "西北风味正宗|面食好吃|价格合理",
                "杭帮菜清淡|味道精致|环境好",
                "江浙菜正宗|甜咸适中|价格合理",
                "南京风味正宗|鸭血粉丝好吃|配送时间稍长",
                "川菜连锁，味道稳定|菜品丰富|价格适中",
                "烤鸭皮脆肉嫩|正宗北京味|价格较高但值得",
                "焖炉烤鸭别有风味|价格合理|配送及时",
                "涮羊肉肉质好|汤底鲜|价格稍贵",
                "北京小吃种类多|味道正宗|价格实惠",
                "包子皮薄馅大|价格便宜|配送快",
                "可以自选配菜|味道好|价格实惠",
                "麻辣烫口味统一|价格便宜|配送快",
                "生煎包皮薄馅大|价格实惠|配送及时",
                "米线汤鲜|价格便宜|配送快",
                "拉面汤底浓郁|味道好|价格适中",
                "牛肉饭好吃|价格合理|配送及时",
                "套餐种类多|味道不错|价格实惠",
                "乌冬面劲道|价格适中|配送快",
                "意式快餐经济实惠|味道好|价格便宜",
                "披萨外送快|味道好|价格合理"
            ]
        }
        return pd.DataFrame(data)
    
    def get_all_restaurants(self) -> List[Dict]:
        """获取所有餐厅"""
        return self.df.to_dict(orient="records")
    
    def get_all_cuisines(self) -> List[str]:
        """获取所有菜系"""
        return sorted(self.df["cuisine"].unique().tolist())
    
    def filter_restaurants(
        self,
        cuisine: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        max_delivery_time: Optional[int] = None,
        keyword: Optional[str] = None
    ) -> List[Dict]:
        """根据筛选条件过滤餐厅"""
        filtered_df = self.df.copy()
        
        if cuisine:
            filtered_df = filtered_df[filtered_df["cuisine"] == cuisine]
        
        if min_price is not None:
            filtered_df = filtered_df[filtered_df["price"] >= min_price]
        
        if max_price is not None:
            filtered_df = filtered_df[filtered_df["price"] <= max_price]
        
        if min_rating is not None:
            filtered_df = filtered_df[filtered_df["rating"] >= min_rating]
        
        if max_delivery_time is not None:
            filtered_df = filtered_df[filtered_df["delivery_time"] <= max_delivery_time]
        
        if keyword:
            keyword_lower = keyword.lower()
            filtered_df = filtered_df[
                filtered_df["name"].str.contains(keyword_lower, case=False, na=False) |
                filtered_df["description"].str.contains(keyword_lower, case=False, na=False)
            ]
        
        # 按评分和价格排序
        filtered_df = filtered_df.sort_values(["rating", "price"], ascending=[False, True])
        
        return filtered_df.to_dict(orient="records")
    
    async def generate_recommendations(self, restaurants: List[Dict]) -> List[Dict]:
        """使用豆包API生成推荐理由"""
        if self.doubao_api is None:
            try:
                self.doubao_api = DoubaoAPI()
            except Exception as e:
                print(f"豆包API初始化失败: {e}，将使用默认推荐理由")
                return self._generate_default_recommendations(restaurants)
        
        try:
            return await self.doubao_api.generate_recommendations(restaurants)
        except Exception as e:
            print(f"豆包API调用失败: {e}，将使用默认推荐理由")
            return self._generate_default_recommendations(restaurants)
    
    def _generate_default_recommendations(self, restaurants: List[Dict]) -> List[Dict]:
        """生成默认推荐理由（当API不可用时）"""
        return [
            {
                "restaurant_id": r.get("id"),
                "name": r.get("name"),
                "reason": f"{r['name']}评分{r['rating']}分，价格¥{r['price']}，配送{r['delivery_time']}分钟，值得一试！"
            }
            for r in restaurants
        ]
    
    async def chat_recommend(
        self,
        user_message: str,
        conversation_history: List[dict],
        location: str,
        restaurants: List[Dict]
    ) -> dict:
        """基于聊天对话推荐餐厅"""
        # 初始化豆包API
        if self.doubao_api is None:
            try:
                self.doubao_api = DoubaoAPI()
            except Exception as e:
                print(f"豆包API初始化失败: {e}")
                return {
                    "message": "抱歉，AI服务暂时不可用，请稍后重试。",
                    "restaurants": [],
                    "type": "error"
                }
        
        try:
            # 构建餐厅信息摘要（包含所有餐厅，特别是烧烤相关的）
            # 如果用户提到烧烤，优先包含所有包含"烤"字的餐厅
            user_message_lower = user_message.lower()
            if '烧烤' in user_message_lower or '烤肉' in user_message_lower:
                # 先筛选出包含"烤"的餐厅
                bbq_restaurants = [r for r in restaurants if '烤' in r['name'] or '烤' in r.get('description', '') or '烤' in r.get('signature_dish', '')]
                other_restaurants = [r for r in restaurants if r not in bbq_restaurants]
                # 优先展示烧烤相关的餐厅
                restaurants_to_show = bbq_restaurants[:20] + other_restaurants[:10]
            else:
                restaurants_to_show = restaurants[:30]
            
            restaurant_summary = "\n".join([
                f"{i+1}. {r['name']}（{r['cuisine']}）- ¥{r['price']}，评分{r['rating']}，配送{r['delivery_time']}分钟 - {r['description']} - 招牌菜：{r.get('signature_dish', '无')}"
                for i, r in enumerate(restaurants_to_show)
            ])
            
            # 构建系统提示词
            system_prompt = f"""你是一个专业的外卖推荐助手，位于{location}。你的任务是理解用户的需求，并从以下餐厅列表中推荐合适的餐厅。

可用餐厅列表：
{restaurant_summary}

重要提示：
1. 必须严格匹配用户的需求。如果用户说"烧烤"，只能推荐包含"烤"字的餐厅（如韩式烤肉、烤鸭等）
2. 如果用户提到价格范围（如"人均100左右"），必须推荐价格在范围内的餐厅
3. 优先推荐完全匹配的餐厅，如果没有完全匹配的，再考虑相似类型
4. **只推荐1家最符合需求的餐厅**（最重要的一条！）

请根据用户的对话内容，理解他们的需求（如菜系、价格、口味、配送时间等），然后：
1. 用自然、友好的语言回复用户
2. **只推荐1家最符合需求的餐厅**（必须严格匹配用户需求）
3. 说明推荐理由

回复格式要求：
- 第一段：理解用户需求并友好回复
- 第二段：推荐餐厅（必须在回复中明确提到餐厅名称，格式：餐厅名（菜系）- 价格 - 评分 - 配送时间 - 推荐理由）
- 保持对话自然流畅，像朋友聊天一样

如果用户的需求不明确，可以询问更多细节。"""
            
            # 构建消息历史
            messages = [{"role": "system", "content": system_prompt}]
            
            # 添加对话历史（最近5轮）
            for msg in conversation_history[-10:]:  # 保留最近10条消息
                messages.append(msg)
            
            # 添加当前用户消息
            messages.append({"role": "user", "content": user_message})
            
            # 调用豆包API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.doubao_api.api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.doubao_api.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "ep-20251103145219-hzndr",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 1000
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    if not ai_message:
                        ai_message = "抱歉，AI暂时无法生成回复，请稍后重试。"
                    
                    # 从AI回复中提取餐厅名称，匹配实际餐厅数据
                    recommended_restaurants = self._extract_restaurants_from_message(ai_message, restaurants)
                    
                    # 只返回1家餐厅
                    if recommended_restaurants:
                        # 根据招牌菜生成或匹配图片
                        restaurant = recommended_restaurants[0]
                        restaurant = self._add_dish_images(restaurant)
                        recommended_restaurants = [restaurant]
                    
                    return {
                        "message": ai_message,
                        "restaurants": recommended_restaurants,
                        "type": "recommendation"
                    }
                else:
                    error_detail = f"API返回错误: {response.status_code}"
                    try:
                        error_body = response.json()
                        error_detail = error_body.get("error", {}).get("message", error_detail)
                    except:
                        error_detail = f"API返回错误: {response.status_code} - {response.text[:200]}"
                    
                    print(f"豆包API调用失败: {error_detail}")
                    
                    # 即使API失败，也尝试基于关键词推荐
                    fallback_restaurants = self._fallback_recommend(user_message, restaurants)
                    
                    # 只返回1家餐厅
                    if fallback_restaurants:
                        restaurant = fallback_restaurants[0]
                        restaurant = self._add_dish_images(restaurant)
                        fallback_restaurants = [restaurant]
                    
                    return {
                        "message": f"根据您的需求，我为您推荐以下餐厅：",
                        "restaurants": fallback_restaurants,
                        "type": "recommendation"
                    }
                    
        except Exception as e:
            print(f"聊天推荐错误: {e}")
            import traceback
            traceback.print_exc()
            
            # 尝试备用推荐
            try:
                fallback_restaurants = self._fallback_recommend(user_message, restaurants)
                
                # 只返回1家餐厅
                if fallback_restaurants:
                    restaurant = fallback_restaurants[0]
                    restaurant = self._add_dish_images(restaurant)
                    fallback_restaurants = [restaurant]
                
                return {
                    "message": f"根据您的需求「{user_message}」，我为您推荐以下餐厅：",
                    "restaurants": fallback_restaurants,
                    "type": "recommendation"
                }
            except:
                return {
                    "message": f"抱歉，处理您的请求时出现错误：{str(e)}。请稍后重试。",
                    "restaurants": [],
                    "type": "error"
                }
    
    def _extract_restaurants_from_message(self, message: str, restaurants: List[Dict]) -> List[Dict]:
        """从AI回复中提取餐厅信息"""
        recommended = []
        message_lower = message.lower()
        
        # 尝试匹配餐厅名称（精确匹配）
        for restaurant in restaurants:
            if restaurant['name'] in message:
                if restaurant not in recommended:
                    recommended.append(restaurant)
                if len(recommended) >= 1:  # 只返回1个
                    break
        
        # 如果匹配到的餐厅少于3个，尝试从关键词匹配
        if len(recommended) < 3:
            # 检查是否提到烧烤
            if '烧烤' in message_lower or '烤肉' in message_lower:
                # 优先匹配包含"烤"字的餐厅
                bbq_restaurants = [r for r in restaurants if '烤' in r['name'] or '烤' in r.get('description', '') or '烤' in r.get('signature_dish', '')]
                for restaurant in bbq_restaurants:
                    if restaurant not in recommended:
                        recommended.append(restaurant)
                        if len(recommended) >= 5:
                            break
            
            # 提取价格范围
            import re
            price_pattern = r'(\d+)\s*[元块]|人均\s*(\d+)|(\d+)\s*左右'
            price_matches = re.findall(price_pattern, message)
            if price_matches:
                prices = [int(p) for match in price_matches for p in match if p]
                if prices:
                    target_price = prices[0]
                    min_price = max(0, target_price - 20)
                    max_price = target_price + 20
                    # 按价格筛选
                    price_filtered = [r for r in restaurants if min_price <= r['price'] <= max_price and r not in recommended]
                    for restaurant in price_filtered:
                        if restaurant not in recommended:
                            recommended.append(restaurant)
                            if len(recommended) >= 5:
                                break
        
        # 如果还是没有匹配到，返回评分最高的1个
        if not recommended:
            recommended = sorted(restaurants, key=lambda x: x['rating'], reverse=True)[:1]
        
        return recommended
    
    def _fallback_recommend(self, user_message: str, restaurants: List[Dict]) -> List[Dict]:
        """当API失败时的备用推荐方法"""
        # 简单的关键词匹配
        message_lower = user_message.lower()
        
        # 提取价格范围
        import re
        price_pattern = r'(\d+)\s*[元块]|人均\s*(\d+)|(\d+)\s*左右'
        price_matches = re.findall(price_pattern, user_message)
        min_price = None
        max_price = None
        if price_matches:
            prices = [int(p) for match in price_matches for p in match if p]
            if prices:
                target_price = prices[0]
                min_price = max(0, target_price - 20)  # 允许±20的浮动
                max_price = target_price + 20
        
        # 菜系关键词（更精确的匹配）
        cuisine_keywords = {
            '烧烤': ['烧烤', '烤肉', '烤串', '烤'],
            '川菜': ['川菜', '川', '辣', '麻', '火锅'],
            '湘菜': ['湘菜', '湘', '湖南'],
            '粤菜': ['粤菜', '粤', '广东', '广式'],
            '日式': ['日式', '日', '拉面', '寿司'],
            '韩式': ['韩式', '韩', '烤肉'],
            '快餐': ['快餐', '快', '便当', '盒饭'],
            '面食': ['面食', '面', '馄饨', '饺子', '包子'],
            '火锅': ['火锅'],
            '京菜': ['京菜', '北京', '烤鸭']
        }
        
        matched_cuisines = []
        matched_keywords = []
        
        # 优先匹配精确关键词
        for keyword, cuisines in cuisine_keywords.items():
            if keyword in message_lower:
                matched_keywords.append(keyword)
                if keyword == '烧烤':
                    # 烧烤匹配韩式烤肉、烤鸭等
                    matched_cuisines.extend(['韩式', '京菜'])
                else:
                    matched_cuisines.extend(cuisines)
        
        # 如果没有精确匹配，尝试部分匹配
        if not matched_cuisines:
            for cuisine, keywords in cuisine_keywords.items():
                if any(keyword in message_lower for keyword in keywords):
                    matched_cuisines.append(cuisine)
        
        # 筛选餐厅
        filtered = restaurants
        
        # 按菜系筛选
        if matched_cuisines:
            filtered = [r for r in restaurants if r['cuisine'] in matched_cuisines]
        
        # 按名称和描述筛选（包含"烤"字）
        if '烧烤' in message_lower or '烤肉' in message_lower:
            filtered = [r for r in filtered if '烤' in r['name'] or '烤' in r.get('description', '') or '烤' in r.get('signature_dish', '')]
        
        # 按价格筛选
        if min_price is not None and max_price is not None:
            filtered = [r for r in filtered if min_price <= r['price'] <= max_price]
        
        # 按评分排序，返回前1个
        recommended = sorted(filtered, key=lambda x: x['rating'], reverse=True)[:1]
        
        # 如果还是没有，返回评分最高的1个
        if not recommended:
            recommended = sorted(restaurants, key=lambda x: x['rating'], reverse=True)[:1]
        
        return recommended
    
    def _add_dish_images(self, restaurant: Dict) -> Dict:
        """根据招牌菜动态生成或匹配图片URL"""
        signature_dish = restaurant.get('signature_dish', '')
        
        # 优先根据招牌菜匹配图片
        dish_keywords = self._extract_dish_keywords(signature_dish)
        
        # 根据招牌菜关键词匹配图片（覆盖原有图片）
        if dish_keywords:
            if len(dish_keywords) >= 2:
                # 有两个或更多招牌菜，分别匹配图片
                restaurant['image1'] = self._get_food_image_url(dish_keywords[0], 0)
                restaurant['image2'] = self._get_food_image_url(dish_keywords[1], 0)
            else:
                # 只有一个招牌菜，使用不同角度的图片
                restaurant['image1'] = self._get_food_image_url(dish_keywords[0], 0)
                restaurant['image2'] = self._get_food_image_url(dish_keywords[0], 1)
        else:
            # 如果没有招牌菜信息，使用默认图片
            if not restaurant.get('image1'):
                restaurant['image1'] = self._get_food_image_url('food', 0)
            if not restaurant.get('image2'):
                restaurant['image2'] = self._get_food_image_url('food', 1)
        
        return restaurant
    
    def _extract_dish_keywords(self, signature_dish: str) -> List[str]:
        """从招牌菜字符串中提取关键词"""
        if not signature_dish:
            return ['food']
        
        # 移除标点符号，按逗号、顿号、空格分割
        dishes = re.split(r'[、，,\s]+', signature_dish)
        # 过滤空字符串，取前2个
        keywords = [d.strip() for d in dishes if d.strip()][:2]
        return keywords if keywords else ['food']
    
    def _get_food_image_url(self, keyword: str, offset: int = 0) -> str:
        """根据关键词获取美食图片URL（使用Unsplash Source API）"""
        # 使用Unsplash Source API根据关键词动态获取图片
        # 格式: https://source.unsplash.com/400x300/?keyword
        
        keyword_lower = keyword.lower()
        
        # 关键词映射到英文搜索词（用于Unsplash搜索）
        keyword_mapping = {
            # 火锅相关
            '火锅': 'hotpot',
            '毛肚': 'hotpot',
            '虾滑': 'hotpot',
            '牛肉片': 'hotpot',
            '海底捞': 'hotpot',
            '小龙坎': 'hotpot',
            '大龙燚': 'hotpot',
            '呷哺呷哺': 'hotpot',
            '小肥羊': 'hotpot',
            '麻辣牛肉': 'hotpot',
            '鸭肠': 'hotpot',
            '脑花': 'hotpot',
            '黄喉': 'hotpot',
            '肥牛': 'hotpot',
            '蔬菜拼盘': 'hotpot',
            '羊肉片': 'hotpot',
            '羊蝎子': 'hotpot',
            '手切羊肉': 'hotpot',
            
            # 烧烤相关
            '烧烤': 'barbecue',
            '烤肉': 'barbecue',
            '烤串': 'barbecue',
            '韩式烤肉': 'korean-barbecue',
            '羊肉串': 'barbecue',
            '烤': 'barbecue',
            '石锅拌饭': 'korean-food',
            '泡菜汤': 'korean-food',
            
            # 烤鸭相关
            '烤鸭': 'peking-duck',
            '北京烤鸭': 'peking-duck',
            '焖炉烤鸭': 'peking-duck',
            '鸭架汤': 'peking-duck',
            '京酱肉丝': 'chinese-food',
            
            # 川菜
            '麻婆豆腐': 'mapo-tofu',
            '水煮鱼': 'sichuan-fish',
            '宫保鸡丁': 'kung-pao-chicken',
            '麻辣香锅': 'spicy-hot-pot',
            '麻辣烫': 'spicy-soup',
            '干锅牛蛙': 'spicy-food',
            
            # 面食
            '拉面': 'ramen',
            '牛肉拉面': 'beef-noodles',
            '羊肉拉面': 'lamb-noodles',
            '重庆小面': 'chongqing-noodles',
            '豌杂面': 'noodles',
            '红油抄手': 'wonton',
            '米线': 'rice-noodles',
            '过桥米线': 'rice-noodles',
            '酸辣米线': 'spicy-noodles',
            '凉拌牛肉': 'beef',
            
            # 饺子包子
            '饺子': 'dumplings',
            '包子': 'steamed-buns',
            '小笼包': 'xiaolongbao',
            '生煎包': 'pan-fried-buns',
            '扁肉': 'wonton',
            '拌面': 'noodles',
            '蒸饺': 'dumplings',
            
            # 西餐
            '披萨': 'pizza',
            '牛排': 'steak',
            '意面': 'pasta',
            '意大利面': 'pasta',
            '提拉米苏': 'tiramisu',
            '玛格丽特披萨': 'pizza',
            '意式肉酱面': 'pasta',
            '意式香肠披萨': 'pizza',
            
            # 日式
            '日式': 'japanese-food',
            '寿司': 'sushi',
            '乌冬面': 'udon',
            '豚骨拉面': 'ramen',
            '味增拉面': 'ramen',
            '日式炸鸡': 'japanese-fried-chicken',
            '天妇罗': 'tempura',
            '牛肉饭': 'beef-rice',
            '照烧鸡排饭': 'teriyaki-chicken',
            '牛丼饭': 'gyudon',
            '咖喱饭': 'curry-rice',
            '日式套餐': 'japanese-bento',
            '味增汤': 'miso-soup',
            
            # 粤菜
            '虾饺': 'shrimp-dumplings',
            '烧卖': 'shumai',
            '叉烧包': 'char-siu-bao',
            '茶点': 'dim-sum',
            
            # 其他
            '黄焖鸡': 'braised-chicken',
            '黄焖排骨': 'braised-pork',
            '大盘鸡': 'xinjiang-chicken',
            '手抓饭': 'pilaf',
            '剁椒鱼头': 'fish-head',
            '口味虾': 'spicy-shrimp',
            '小炒肉': 'stir-fried-pork',
            '锅包肉': 'sweet-sour-pork',
            '地三鲜': 'three-delicacies',
            '西湖醋鱼': 'west-lake-fish',
            '东坡肉': 'dongpo-pork',
            '龙井虾仁': 'shrimp',
            '糖醋里脊': 'sweet-sour-pork',
            '白切鸡': 'white-cut-chicken',
            '鸭血粉丝汤': 'duck-blood-soup',
            '盐水鸭': 'salted-duck',
            '豆汁': 'beijing-food',
            '焦圈': 'beijing-food',
            '驴打滚': 'beijing-snack',
            '卤肉饭': 'braised-pork-rice',
            '豆浆': 'soy-milk',
            '油条': 'youtiao',
            '莜面': 'noodles',
            '凉皮': 'liangpi',
            '鸡汤': 'chicken-soup',
            '蒸蛋': 'steamed-egg',
            '小菜': 'side-dish',
            '蒸排骨': 'steamed-ribs',
            '蒸鸡': 'steamed-chicken',
        }
        
        # 查找匹配的英文关键词
        search_keyword = 'food'  # 默认关键词
        
        # 先尝试完全匹配
        if keyword_lower in keyword_mapping:
            search_keyword = keyword_mapping[keyword_lower]
        else:
            # 尝试部分匹配
            for chinese_keyword, english_keyword in keyword_mapping.items():
                if chinese_keyword in keyword_lower or keyword_lower in chinese_keyword:
                    search_keyword = english_keyword
                    break
        
        # 使用Unsplash Source API（随机但相关）
        # 添加随机参数确保每次获取不同图片
        import random
        random_seed = random.randint(1, 1000) + offset * 100
        
        return f"https://source.unsplash.com/400x300/?{search_keyword}&sig={random_seed}"

