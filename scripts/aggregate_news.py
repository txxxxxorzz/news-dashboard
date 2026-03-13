#!/usr/bin/env python3
"""
新闻数据聚合脚本
将获取的新闻数据进行整理和排序
"""

import json
import os
from datetime import datetime

# 输入输出目录
SCRIPT_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, 'web', 'news_data', 'latest.json')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'web', 'news_data', 'aggregated.json')

def load_news():
    """加载原始新闻数据"""
    if not os.path.exists(INPUT_FILE):
        print(f"输入文件不存在：{INPUT_FILE}")
        return None
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def aggregate_by_source(data):
    """按来源聚合新闻"""
    aggregated = {
        "updateTime": data.get("updateTime", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "categories": []
    }
    
    # 处理每个来源的数据
    sources = data.get("data", {})
    
    # 知乎热榜
    if sources.get("zhihu"):
        aggregated["categories"].append({
            "name": "知乎热榜",
            "icon": "📚",
            "color": "#0084ff",
            "items": sources["zhihu"][:15]  # 取前 15 条
        })
    
    # 微博热搜
    if sources.get("weibo"):
        aggregated["categories"].append({
            "name": "微博热搜",
            "icon": "🔥",
            "color": "#e6162d",
            "items": sources["weibo"][:15]
        })
    
    # GitHub Trending
    if sources.get("github"):
        aggregated["categories"].append({
            "name": "GitHub 趋势",
            "icon": "💻",
            "color": "#24292e",
            "items": sources["github"][:15]
        })
    
    # 科技新闻
    if sources.get("news"):
        aggregated["categories"].append({
            "name": "科技新闻",
            "icon": "📰",
            "color": "#10b981",
            "items": sources["news"][:15]
        })
    
    return aggregated

def save_aggregated(data):
    """保存聚合后的数据"""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"聚合数据已保存到：{OUTPUT_FILE}")

def main():
    print(f"开始聚合新闻数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 加载原始数据
    raw_data = load_news()
    if not raw_data:
        print("无法加载新闻数据，跳过聚合")
        return
    
    # 聚合
    aggregated = aggregate_by_source(raw_data)
    
    # 保存
    save_aggregated(aggregated)
    
    # 统计
    total = sum(len(cat["items"]) for cat in aggregated["categories"])
    print(f"聚合完成，共 {len(aggregated['categories'])} 个分类，{total} 条新闻")

if __name__ == '__main__':
    main()
