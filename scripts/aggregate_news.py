#!/usr/bin/env python3
"""
新闻数据聚合脚本
将获取的新闻数据整理为前端需要的格式
支持 AI 智能摘要生成
"""

import json
import os
import requests
from datetime import datetime

# 阿里云百炼 API 配置
DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', '')
DASHSCOPE_API_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'

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
    """生成 AI 热点解读 - 调用阿里云百炼 API"""
    if not items:
        return "暂无数据"
    
    titles = [item.get('title', '') for item in items[:15] if item.get('title')]
    if not titles:
        return "暂无数据"
    
    # 调试：打印 API Key 状态
    if DASHSCOPE_API_KEY:
        print(f"✅ API Key 已配置（长度：{len(DASHSCOPE_API_KEY)}）")
        try:
            return call_dashscope_ai(platform_name, titles)
        except Exception as e:
            print(f"⚠ AI 调用失败：{e}，降级到规则版")
    else:
        print("⚠ 未配置 DASHSCOPE_API_KEY，使用规则版摘要")
    
    # 降级到规则版
    return generate_rule_based_summary(platform_name, titles)

def call_dashscope_ai(platform_name, titles):
    """调用阿里云百炼 API 生成摘要"""
    # 构建提示词
    titles_text = "\n".join([f"{i+1}. {t}" for i, t in enumerate(titles)])
    
    prompt = f"""你是热点新闻分析师。请根据以下{platform_name}热榜标题，生成一段 60-80 字的智能摘要。

【热榜标题】
{titles_text}

【要求】
1. 提炼 2-3 个核心话题领域
2. 指出最值得关注的 1-2 个热点
3. 语言简洁、有洞察力
4. 不要简单罗列标题
5. 输出格式：先说整体趋势，再说具体热点

【示例】
今日知乎聚焦科技与民生话题。AI 技术突破引发热议，多部门回应民生痛点成焦点。建议类问题占比显著，用户关注政策落地与实际解决方案。

【你的分析】"""

    headers = {
        'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
        'Content-Type': 'application/json',
        'X-DashScope-WorkSpace': 'standard'
    }
    
    # 阿里云百炼 API 格式（新版）
    payload = {
        'model': 'qwen-turbo',
        'input': {
            'messages': [
                {'role': 'system', 'content': '你是热点新闻分析师，擅长总结热点话题。'},
                {'role': 'user', 'content': prompt}
            ]
        },
        'parameters': {
            'max_tokens': 150,
            'temperature': 0.7
        }
    }
    
    print(f"📡 正在调用 AI API...")
    response = requests.post(DASHSCOPE_API_URL, headers=headers, json=payload, timeout=15)
    
    # 详细错误信息
    if response.status_code != 200:
        print(f"❌ API 返回错误：{response.status_code}")
        print(f"响应内容：{response.text[:200]}")
        response.raise_for_status()
    
    result = response.json()
    print(f"✅ API 调用成功")
    
    # 提取 AI 生成的内容
    content = result.get('output', {}).get('text', '').strip()
    
    # 清理输出（去掉"你的分析"等前缀）
    if '【你的分析】' in content:
        content = content.split('【你的分析】')[-1].strip()
    
    # 添加 emoji 前缀
    if content:
        return f"💡 {content}"
    
    return "🔥 热点更新中..."

def generate_rule_based_summary(platform_name, titles):
    """规则版摘要（降级方案）"""
    # 关键词提取
    keywords = extract_keywords(titles)
    
    # 分类分析
    categories = categorize_topics(titles)
    
    summary_parts = []
    
    if categories:
        top_cats = list(categories.keys())[:3]
        summary_parts.append("📊 聚焦：" + "、".join(top_cats))
    
    if keywords:
        summary_parts.append("🔑 热词：" + "、".join(keywords[:5]))
    
    if summary_parts:
        return " ".join(summary_parts)
    return "🔥 热门更新中..."

def extract_keywords(titles, top_n=8):
    """提取高频关键词（规则版）"""
    stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', 
                 '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
                 '自己', '这', '那', '他', '她', '它', '们', '这个', '那个', '可以', '能', '让',
                 '但', '而', '如', '何', '为什么', '吗', '呢', '吧', '啊', '呀', '哦', '嗯'}
    
    word_freq = {}
    for title in titles:
        for i in range(len(title) - 1):
            for j in range(i + 2, min(i + 7, len(title) + 1)):
                word = title[i:j]
                if word in stopwords or not word.strip() or all(c in '，。！？；：""''、' for c in word):
                    continue
                if word not in word_freq:
                    word_freq[word] = 0
                word_freq[word] += 1
    
    sorted_words = sorted(word_freq.items(), key=lambda x: (-x[1], len(x[0])))
    return [word for word, _ in sorted_words[:top_n]]

def categorize_topics(titles):
    """简单分类话题（规则版）"""
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
    
    return dict(sorted(result.items(), key=lambda x: -x[1]))

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
