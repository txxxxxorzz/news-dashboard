#!/usr/bin/env python3
"""
新闻数据聚合脚本
将获取的新闻数据整理为前端需要的格式
"""

import json
import os
from datetime import datetime

# 输入输出目录
SCRIPT_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, 'web', 'news_data', 'latest.json')
# 输出两份：web/news_data/ 和 根目录 news_data/（GitHub Pages 访问）
OUTPUT_FILE_WEB = os.path.join(SCRIPT_DIR, 'web', 'news_data', 'latest.json')
OUTPUT_FILE_ROOT = os.path.join(SCRIPT_DIR, 'news_data', 'latest.json')

def load_news():
    """加载原始新闻数据"""
    if not os.path.exists(INPUT_FILE):
        print(f"输入文件不存在：{INPUT_FILE}")
        return None
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_time(time_str):
    """格式化时间为相对时间"""
    try:
        dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        diff = (now - dt).total_seconds()
        
        if diff < 60:
            return '刚刚'
        elif diff < 3600:
            return f'{int(diff / 60)}分钟前'
        elif diff < 86400:
            return f'{int(diff / 3600)}小时前'
        else:
            return f'{int(diff / 86400)}天前'
    except:
        return time_str

def aggregate_to_platforms(data):
    """转换为前端需要的 platforms 格式"""
    platforms = {}
    
    # 处理知乎数据
    zhihu_items = data.get("data", {}).get("zhihu", [])
    if zhihu_items:
        platforms["zhihu"] = {
            "name": "知乎热榜",
            "icon": "📚",
            "categories": {
                "热榜": [
                    {
                        "title": item.get("title", "")[:50],
                        "url": item.get("url", "#"),
                        "source": "知乎",
                        "time": format_time(data.get("updateTime", "")),
                        "id": f"zhihu_{i}"
                    }
                    for i, item in enumerate(zhihu_items[:20])
                ]
            }
        }
    
    # 处理微博数据
    weibo_items = data.get("data", {}).get("weibo", [])
    if weibo_items:
        platforms["weibo"] = {
            "name": "微博热搜",
            "icon": "🔴",
            "categories": {
                "热搜": [
                    {
                        "title": item.get("title", "")[:50],
                        "url": item.get("url", "#"),
                        "source": "微博",
                        "time": format_time(data.get("updateTime", "")),
                        "id": f"weibo_{i}"
                    }
                    for i, item in enumerate(weibo_items[:20])
                ]
            }
        }
    
    # 处理 GitHub 数据
    github_items = data.get("data", {}).get("github", [])
    if github_items:
        platforms["github"] = {
            "name": "GitHub 趋势",
            "icon": "💻",
            "categories": {
                "Trending": [
                    {
                        "title": item.get("title", "")[:50],
                        "url": item.get("url", "#"),
                        "source": "GitHub",
                        "time": format_time(data.get("updateTime", "")),
                        "id": f"github_{i}"
                    }
                    for i, item in enumerate(github_items[:20])
                ]
            }
        }
    
    # 处理 NewsAPI 数据
    news_items = data.get("data", {}).get("news", [])
    if news_items:
        platforms["newsapi"] = {
            "name": "NewsAPI",
            "icon": "📰",
            "categories": {
                "科技新闻": [
                    {
                        "title": item.get("title", "")[:50],
                        "url": item.get("url", "#"),
                        "source": item.get("source", "News"),
                        "time": format_time(data.get("updateTime", "")),
                        "id": f"news_{i}"
                    }
                    for i, item in enumerate(news_items[:20])
                ]
            }
        }
    
    # 如果没有数据，添加示例数据
    if not platforms:
        platforms = {
            "github": {
                "name": "GitHub 趋势",
                "icon": "💻",
                "categories": {
                    "Trending": [
                        {
                            "title": "codecrafters-io/build-your-own-x",
                            "url": "https://github.com/codecrafters-io/build-your-own-x",
                            "source": "GitHub",
                            "time": "刚刚",
                            "id": "github_0"
                        },
                        {
                            "title": "sindresorhus/awesome",
                            "url": "https://github.com/sindresorhus/awesome",
                            "source": "GitHub",
                            "time": "刚刚",
                            "id": "github_1"
                        }
                    ]
                }
            }
        }
    
    result = {
        "updateTime": data.get("updateTime", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "platforms": platforms
    }
    
    return result

def save_aggregated(data):
    """保存聚合后的数据到两个位置"""
    # 保存到 web/news_data/
    os.makedirs(os.path.dirname(OUTPUT_FILE_WEB), exist_ok=True)
    with open(OUTPUT_FILE_WEB, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ 聚合数据已保存到：{OUTPUT_FILE_WEB}")
    
    # 保存到根目录 news_data/（GitHub Pages 访问）
    os.makedirs(os.path.dirname(OUTPUT_FILE_ROOT), exist_ok=True)
    with open(OUTPUT_FILE_ROOT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ 聚合数据已保存到：{OUTPUT_FILE_ROOT}")

def main():
    print(f"\n🔄 开始聚合新闻数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 加载原始数据
    raw_data = load_news()
    if not raw_data:
        print("✗ 无法加载新闻数据，生成示例数据")
        raw_data = {
            "updateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "data": {"zhihu": [], "weibo": [], "github": [], "news": []}
        }
    
    # 聚合
    aggregated = aggregate_to_platforms(raw_data)
    
    # 保存
    save_aggregated(aggregated)
    
    # 统计
    total = sum(
        len(items) 
        for platform in aggregated["platforms"].values() 
        for items in platform["categories"].values()
    )
    print(f"✓ 聚合完成，共 {len(aggregated['platforms'])} 个平台，{total} 条新闻\n")

if __name__ == '__main__':
    main()
