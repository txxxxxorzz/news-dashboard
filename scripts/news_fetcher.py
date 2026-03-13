#!/usr/bin/env python3
"""
新闻数据获取脚本
从多个免费 API 获取热点新闻数据
"""

import requests
import json
import os
from datetime import datetime

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'web', 'news_data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_zhihu_hot():
    """获取知乎热榜"""
    try:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        items = []
        for item in data.get('data', []):
            target = item.get('target', {})
            items.append({
                "title": target.get('title', ''),
                "url": target.get('url', '').replace('api.', 'www.'),
                "hot": target.get('excerpt', '')[:100] if target.get('excerpt') else '',
                "source": "知乎"
            })
        print(f"✓ 知乎热榜：{len(items)} 条")
        return items
    except Exception as e:
        print(f"✗ 知乎获取失败：{e}")
        return []

def fetch_weibo_hot():
    """获取微博热搜"""
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        items = []
        realtime_list = data.get('data', {}).get('realtime', [])
        for item in realtime_list[:20]:
            word = item.get('word', '')
            if word:  # 跳过广告
                items.append({
                    "title": word,
                    "url": f"https://s.weibo.com/weibo?q={word}",
                    "hot": item.get('num', 0),
                    "source": "微博"
                })
        print(f"✓ 微博热搜：{len(items)} 条")
        return items
    except Exception as e:
        print(f"✗ 微博获取失败：{e}")
        return []

def fetch_github_trending():
    """获取 GitHub Trending - 使用 GitHub API"""
    try:
        # 使用 GitHub Search API 获取 trending repos
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "stars:>1000 pushed:>=2024-01-01",
            "sort": "stars",
            "order": "desc",
            "per_page": 15
        }
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "News-Dashboard"
        }
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        items = []
        for repo in data.get('items', []):
            items.append({
                "title": f"{repo['owner']['login']}/{repo['name']}",
                "url": repo['html_url'],
                "hot": repo.get('description', 'No description') or 'No description',
                "source": "GitHub"
            })
        print(f"✓ GitHub Trending: {len(items)} 条")
        return items
    except Exception as e:
        print(f"✗ GitHub 获取失败：{e}")
        return []

def fetch_news_api():
    """使用 NewsAPI 获取科技新闻（需要 API Key）"""
    api_key = os.environ.get('NEWS_API_KEY', '')
    if not api_key:
        print("⚠ 未配置 NEWS_API_KEY，跳过科技新闻")
        return []
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": "technology",
            "language": "zh",
            "apiKey": api_key,
            "pageSize": 20
        }
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'ok':
            print(f"✗ NewsAPI 错误：{data.get('message', 'Unknown error')}")
            return []
        
        items = []
        for article in data.get('articles', []):
            items.append({
                "title": article.get('title', ''),
                "url": article.get('url', ''),
                "hot": article.get('description', '')[:100] if article.get('description') else '',
                "source": article.get('source', {}).get('name', 'News')
            })
        print(f"✓ 科技新闻：{len(items)} 条")
        return items
    except Exception as e:
        print(f"✗ NewsAPI 获取失败：{e}")
        return []

def main():
    print(f"\n🚀 开始获取新闻数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_news = {
        "zhihu": fetch_zhihu_hot(),
        "weibo": fetch_weibo_hot(),
        "github": fetch_github_trending(),
        "news": fetch_news_api()
    }
    
    # 添加元数据
    result = {
        "updateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "sources": {
            "zhihu": len(all_news["zhihu"]),
            "weibo": len(all_news["weibo"]),
            "github": len(all_news["github"]),
            "news": len(all_news["news"])
        },
        "data": all_news
    }
    
    # 保存到文件
    output_file = os.path.join(OUTPUT_DIR, 'latest.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    total = sum(len(v) for v in all_news.values())
    print(f"\n✓ 新闻数据已保存到：{output_file}")
    print(f"✓ 总计：{total} 条新闻\n")

if __name__ == '__main__':
    main()
