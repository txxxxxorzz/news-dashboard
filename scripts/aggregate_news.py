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

def generate_ai_summary(platform_name, items):
    """生成 AI 热点解读 - 智能分类 + 趋势分析"""
    if not items:
        return "暂无数据"
    
    titles = [item.get('title', '') for item in items[:15] if item.get('title')]
    if not titles:
        return "暂无数据"
    
    # 关键词提取（按词频和位置）
    keywords = extract_keywords(titles)
    
    # 分类分析
    categories = categorize_topics(titles)
    
    # 生成摘要
    summary_parts = []
    
    # 1. 热点领域
    if categories:
        top_cats = list(categories.keys())[:3]
        summary_parts.append("📊 聚焦：" + "、".join(top_cats))
    
    # 2. 关键词
    if keywords:
        summary_parts.append("🔑 热词：" + "、".join(keywords[:5]))
    
    # 3. 趋势洞察
    trend = analyze_trend(titles, platform_name)
    if trend:
        summary_parts.append(trend)
    
    if summary_parts:
        return " ".join(summary_parts)
    return "🔥 热门更新中..."

def extract_keywords(titles, top_n=8):
    """提取高频关键词"""
    # 常见停用词
    stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', 
                 '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
                 '自己', '这', '那', '他', '她', '它', '们', '这个', '那个', '可以', '能', '让',
                 '但', '而', '如', '何', '为什么', '吗', '呢', '吧', '啊', '呀', '哦', '嗯'}
    
    # 简单分词（按常见词组切分）
    word_freq = {}
    for title in titles:
        # 提取可能的关键词（2-6 字）
        for i in range(len(title) - 1):
            for j in range(i + 2, min(i + 7, len(title) + 1)):
                word = title[i:j]
                # 跳过停用词和纯标点
                if word in stopwords or not word.strip() or all(c in '，。！？；：""''、' for c in word):
                    continue
                # 优先保留完整词组
                if word not in word_freq:
                    word_freq[word] = 0
                word_freq[word] += 1
    
    # 按频率排序，优先选短词（更可能是关键词）
    sorted_words = sorted(word_freq.items(), key=lambda x: (-x[1], len(x[0])))
    return [word for word, _ in sorted_words[:top_n]]

def categorize_topics(titles):
    """简单分类话题"""
    categories = {
        "社会民生": ["政策", "建议", "委员", "代表", "社保", "医疗", "教育", "住房", "就业"],
        "科技互联网": ["AI", "互联网", "科技", "手机", "App", "软件", "系统", "芯片", "5G"],
        "娱乐八卦": ["明星", "演员", "歌手", "电影", "电视剧", "综艺", "演唱会", "离婚", "恋情"],
        "国际时事": ["美国", "伊朗", "以色列", "俄罗斯", "乌克兰", "国际", "外交", "战争", "冲突"],
        "财经经济": ["股市", "基金", "房价", "经济", "金融", "银行", "投资", "理财", "消费"],
        "体育竞技": ["NBA", "足球", "篮球", "比赛", "冠军", "运动员", "奥运", "世界杯"],
        "生活健康": ["健康", "养生", "减肥", "美食", "旅游", "天气", "疫情", "疫苗"],
    }
    
    result = {}
    for title in titles:
        for cat, keywords in categories.items():
            for kw in keywords:
                if kw.lower() in title.lower():
                    result[cat] = result.get(cat, 0) + 1
                    break
    
    # 按热度排序
    return dict(sorted(result.items(), key=lambda x: -x[1]))

def analyze_trend(titles, platform_name):
    """分析趋势"""
    # 检测是否有重大事件
    urgency_words = ["突发", "重磅", "刚刚", "确认", "宣布", "正式", "首次", "历史"]
    
    urgent_count = sum(1 for t in titles if any(w in t for w in urgency_words))
    
    if urgent_count >= 2:
        return "⚡ 多条突发新闻"
    elif urgent_count == 1:
        return "⚡ 有突发动态"
    
    return None

def aggregate_to_platforms(data):
    """转换为前端需要的 platforms 格式"""
    platforms = {}
    
    # 处理知乎数据
    zhihu_items = data.get("data", {}).get("zhihu", [])
    if zhihu_items:
        platforms["zhihu"] = {
            "name": "知乎热榜",
            "icon": "📚",
            "aiSummary": generate_ai_summary("知乎", zhihu_items),
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
            "aiSummary": generate_ai_summary("微博", weibo_items),
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
    
    # 处理 B 站数据
    bilibili_items = data.get("data", {}).get("bilibili", [])
    if bilibili_items:
        platforms["bilibili"] = {
            "name": "B 站热门",
            "icon": "📺",
            "aiSummary": generate_ai_summary("B 站", bilibili_items),
            "categories": {
                "热门视频": [
                    {
                        "title": item.get("title", "")[:50],
                        "url": item.get("url", "#"),
                        "source": "B 站",
                        "time": format_time(data.get("updateTime", "")),
                        "id": f"bilibili_{i}"
                    }
                    for i, item in enumerate(bilibili_items[:20])
                ]
            }
        }
    
    # 处理抖音数据
    douyin_items = data.get("data", {}).get("douyin", [])
    if douyin_items:
        platforms["douyin"] = {
            "name": "抖音热点",
            "icon": "🎵",
            "aiSummary": generate_ai_summary("抖音", douyin_items),
            "categories": {
                "热搜": [
                    {
                        "title": item.get("title", "")[:50],
                        "url": item.get("url", "#"),
                        "source": "抖音",
                        "time": format_time(data.get("updateTime", "")),
                        "id": f"douyin_{i}"
                    }
                    for i, item in enumerate(douyin_items[:20])
                ]
            }
        }
    
    # 处理快手数据
    kuaishou_items = data.get("data", {}).get("kuaishou", [])
    if kuaishou_items:
        platforms["kuaishou"] = {
            "name": "快手热榜",
            "icon": "📹",
            "aiSummary": generate_ai_summary("快手", kuaishou_items),
            "categories": {
                "热榜": [
                    {
                        "title": item.get("title", "")[:50],
                        "url": item.get("url", "#"),
                        "source": "快手",
                        "time": format_time(data.get("updateTime", "")),
                        "id": f"kuaishou_{i}"
                    }
                    for i, item in enumerate(kuaishou_items[:20])
                ]
            }
        }
    
    # 处理小红书数据
    xiaohongshu_items = data.get("data", {}).get("xiaohongshu", [])
    if xiaohongshu_items:
        platforms["xiaohongshu"] = {
            "name": "小红书热门",
            "icon": "📕",
            "aiSummary": generate_ai_summary("小红书", xiaohongshu_items),
            "categories": {
                "热门笔记": [
                    {
                        "title": item.get("title", "")[:50],
                        "url": item.get("url", "#"),
                        "source": "小红书",
                        "time": format_time(data.get("updateTime", "")),
                        "id": f"xiaohongshu_{i}"
                    }
                    for i, item in enumerate(xiaohongshu_items[:20])
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
