#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试图片生成功能"""
from recommendation import RecommendationEngine

def test_image_generation():
    engine = RecommendationEngine()
    
    # 测试1: 烧烤相关
    test_restaurant1 = {
        'name': '韩式烤肉',
        'signature_dish': '韩式烤肉、石锅拌饭、泡菜汤'
    }
    result1 = engine._add_dish_images(test_restaurant1)
    print("=" * 50)
    print("测试1: 韩式烤肉")
    print(f"招牌菜: {test_restaurant1['signature_dish']}")
    print(f"image1: {result1.get('image1')}")
    print(f"image2: {result1.get('image2')}")
    
    # 测试2: 火锅相关
    test_restaurant2 = {
        'name': '海底捞火锅',
        'signature_dish': '毛肚、虾滑、牛肉片'
    }
    result2 = engine._add_dish_images(test_restaurant2)
    print("=" * 50)
    print("测试2: 海底捞火锅")
    print(f"招牌菜: {test_restaurant2['signature_dish']}")
    print(f"image1: {result2.get('image1')}")
    print(f"image2: {result2.get('image2')}")
    
    # 测试3: 单个招牌菜
    test_restaurant3 = {
        'name': '测试餐厅',
        'signature_dish': '拉面'
    }
    result3 = engine._add_dish_images(test_restaurant3)
    print("=" * 50)
    print("测试3: 单个招牌菜")
    print(f"招牌菜: {test_restaurant3['signature_dish']}")
    print(f"image1: {result3.get('image1')}")
    print(f"image2: {result3.get('image2')}")

if __name__ == '__main__':
    test_image_generation()

