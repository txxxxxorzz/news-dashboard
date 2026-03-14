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
    """获取知乎热榜 - 使用公开 API"""
    try:
        # 使用第三方聚合 API（无需登录）
        url = "https://api.zhihu.com/topstory/hot-lists/total?limit=20"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 401:
            # 如果 API 需要认证，尝试备用方案
            return fetch_zhihu_backup()
        
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
        print(f"⚠ 知乎获取失败：{e}")
        return fetch_zhihu_backup()

def fetch_zhihu_backup():
    """知乎备用方案 - 使用 RSS 或模拟数据"""
    try:
        # 尝试使用 RSS
        url = "https://www.zhihu.com/rss"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.ok:
            # 解析 RSS（简化处理）
            print("✓ 知乎 RSS 获取成功")
            return []
    except:
        pass
    
    print("⚠ 知乎使用备用数据")
    return []

def fetch_weibo_hot():
    """获取微博热搜"""
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://weibo.com/"
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 403:
            print("⚠ 微博 API 受限，使用备用方案")
            return fetch_weibo_backup()
        
        response.raise_for_status()
        data = response.json()
        
        items = []
        realtime_list = data.get('data', {}).get('realtime', [])
        for item in realtime_list[:20]:
            word = item.get('word', '')
            if word and not item.get('is_ad'):  # 跳过广告
                items.append({
                    "title": word,
                    "url": f"https://s.weibo.com/weibo?q={word}",
                    "hot": item.get('num', 0),
                    "source": "微博"
                })
        print(f"✓ 微博热搜：{len(items)} 条")
        return items
    except Exception as e:
        print(f"⚠ 微博获取失败：{e}")
        return fetch_weibo_backup()

def fetch_weibo_backup():
    """微博备用方案"""
    print("⚠ 微博使用备用数据")
    return []

def fetch_github_trending():
    """获取 GitHub Trending - 使用 GitHub API"""
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "stars:>1000 pushed:>=2024-01-01",
            "sort": "stars",
            "order": "desc",
            "per_page": 20
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
        print(f"⚠ GitHub 获取失败：{e}")
        return []

def fetch_news_api():
    """使用 NewsAPI 获取科技新闻"""
    api_key = os.environ.get('NEWS_API_KEY', '')
    if not api_key:
        print("⚠ 未配置 NEWS_API_KEY，跳过科技新闻")
        return []
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": "technology",
            "language": "en",  # 改为英文，中文源较少
            "apiKey": api_key,
            "pageSize": 20
        }
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'ok':
            error_msg = data.get('message', 'Unknown error')
            print(f"⚠ NewsAPI 错误：{error_msg}")
            return []
        
        items = []
        for article in data.get('articles', []):
            items.append({
                "title": article.get('title', '')[:100],
                "url": article.get('url', '#'),
                "hot": article.get('description', '')[:100] if article.get('description') else '',
                "source": article.get('source', {}).get('name', 'News')
            })
        print(f"✓ 科技新闻：{len(items)} 条")
        return items
    except Exception as e:
        print(f"⚠ NewsAPI 获取失败：{e}")
        return []

def fetch_bilibili_hot():
    """获取 B 站热门"""
    try:
        # 使用第三方 API
        url = "https://api.pearktrue.cn/api/bilibili"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = []
        for item in data.get('data', [])[:20]:
            items.append({
                "title": item.get('title', '')[:80],
                "url": item.get('url', '#'),
                "hot": f"🔥 {item.get('hot', 0)}",
                "source": "B 站"
            })
        print(f"✓ B 站热门：{len(items)} 条")
        return items
    except Exception as e:
        print(f"⚠ B 站获取失败：{e}")
        # 备用方案：返回空数据
        return []

def fetch_douyin_hot():
    """获取抖音热点"""
    try:
        # 使用公开的抖音热点 API
        url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        items = []
        for item in data.get('data', {}).get('word_list', [])[:20]:
            items.append({
                "title": item.get('word', '')[:60],
                "url": f"https://www.douyin.com/hot/{item.get('sentence_id', '')}",
                "hot": f"🔥 {item.get('hot_value', 0)}",
                "source": "抖音"
            })
        print(f"✓ 抖音热点：{len(items)} 条")
        return items
    except Exception as e:
        print(f"⚠ 抖音获取失败：{e}")
        # 备用方案
        return fetch_douyin_backup()

def fetch_douyin_backup():
    """抖音备用方案 - 使用第三方 API"""
    try:
        # 尝试多个备用 API（按稳定性排序）
        urls = [
            "https://api.qqsuu.cn/api/dm-douyin",
            "https://api.vvhan.com/api/hotlist/douyin",
            "https://api.pearktrue.cn/api/douyin",
            "https://api.wapi.cn/api/douyin-hot"
        ]
        for url in urls:
            try:
                response = requests.get(url, timeout=8)
                if response.status_code != 200:
                    continue
                data = response.json()
                
                items = []
                # 不同 API 返回格式不同
                word_list = data.get('data', []) or data.get('result', []) or data.get('list', [])
                for item in word_list[:20]:
                    title = item.get('Word', '') or item.get('word', '') or item.get('title', '') or item.get('name', '')
                    if title:
                        items.append({
                            "title": title[:60],
                            "url": f"https://www.douyin.com/hot/{item.get('SentenceId', item.get('id', ''))}",
                            "hot": f"🔥 {item.get('HotValue', item.get('hot', item.get('num', 0)))}",
                            "source": "抖音"
                        })
                if items:
                    print(f"✓ 抖音热点（备用 API）: {len(items)} 条")
                    return items
            except:
                continue
        
        print("⚠ 抖音所有备用 API 均不可用")
        return []
    except Exception as e:
        print(f"⚠ 抖音备用失败：{e}")
        return []

def fetch_xiaohongshu_hot():
    """获取小红书热门 - 使用第三方 API"""
    try:
        # 按稳定性排序
        urls = [
            "https://api.qqsuu.cn/api/dm-xhs",
            "https://api.pearktrue.cn/api/xiaohongshu",
            "https://api.vvhan.com/api/hotlist/xiaohongshu"
        ]
        for url in urls:
            try:
                response = requests.get(url, timeout=8)
                if response.status_code != 200:
                    continue
                data = response.json()
                
                items = []
                word_list = data.get('data', []) or data.get('result', [])
                for item in word_list[:20]:
                    title = item.get('title', '') or item.get('word', '') or item.get('name', '')
                    if title:
                        items.append({
                            "title": title[:60],
                            "url": item.get('url', f"https://www.xiaohongshu.com/search/result?keyword={title}"),
                            "hot": f"🔥 {item.get('num', item.get('hot', 0))}",
                            "source": "小红书"
                        })
                if items:
                    print(f"✓ 小红书热门：{len(items)} 条")
                    return items
            except:
                continue
        
        print("⚠ 小红书暂无可用数据源")
        return []
    except Exception as e:
        print(f"⚠ 小红书获取失败：{e}")
        return []

def fetch_kuaishou_hot():
    """获取快手热榜 - 使用第三方 API"""
    try:
        # 按稳定性排序
        urls = [
            "https://api.qqsuu.cn/api/dm-kuaishou",
            "https://api.pearktrue.cn/api/kuaishou",
            "https://api.vvhan.com/api/hotlist/kuaishou"
        ]
        for url in urls:
            try:
                response = requests.get(url, timeout=8)
                if response.status_code != 200:
                    continue
                data = response.json()
                
                items = []
                word_list = data.get('data', []) or data.get('result', [])
                for item in word_list[:20]:
                    title = item.get('title', '') or item.get('word', '') or item.get('name', '')
                    if title:
                        items.append({
                            "title": title[:60],
                            "url": item.get('url', f"https://www.kuaishou.com/search/video?searchKey={title}"),
                            "hot": f"🔥 {item.get('num', item.get('hot', 0))}",
                            "source": "快手"
                        })
                if items:
                    print(f"✓ 快手热榜：{len(items)} 条")
                    return items
            except:
                continue
        
        print("⚠ 快手暂无可用数据源")
        return []
    except Exception as e:
        print(f"⚠ 快手获取失败：{e}")
        return []

def main():
    print(f"\n🚀 开始获取新闻数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_news = {
        "zhihu": fetch_zhihu_hot(),
        "weibo": fetch_weibo_hot(),
        "bilibili": fetch_bilibili_hot(),
        "douyin": fetch_douyin_hot(),
        "kuaishou": fetch_kuaishou_hot(),
        "xiaohongshu": fetch_xiaohongshu_hot(),
        "github": fetch_github_trending(),
        "news": fetch_news_api()
    }
    
    # 添加元数据
    result = {
        "updateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "sources": {
            "zhihu": len(all_news["zhihu"]),
            "weibo": len(all_news["weibo"]),
            "bilibili": len(all_news["bilibili"]),
            "douyin": len(all_news["douyin"]),
            "kuaishou": len(all_news["kuaishou"]),
            "xiaohongshu": len(all_news["xiaohongshu"]),
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
