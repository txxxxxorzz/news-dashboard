#!/usr/bin/env python3
"""
测试阿里云百炼 API 是否可用
"""

import os
import requests

DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', '')

if not DASHSCOPE_API_KEY:
    print("❌ 未配置 DASHSCOPE_API_KEY 环境变量")
    exit(1)

print(f"✅ API Key 已配置（长度：{len(DASHSCOPE_API_KEY)}）")
print(f"API Key 前缀：{DASHSCOPE_API_KEY[:10]}...")

url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'

headers = {
    'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
    'Content-Type': 'application/json',
    'X-DashScope-WorkSpace': 'standard'
}

payload = {
    'model': 'qwen-turbo',
    'input': {
        'messages': [
            {'role': 'system', 'content': '你是一个助手。'},
            {'role': 'user', 'content': '你好，请用一句话介绍你自己。'}
        ]
    },
    'parameters': {
        'max_tokens': 50,
        'temperature': 0.7
    }
}

print(f"\n📡 正在测试 API...")
try:
    response = requests.post(url, headers=headers, json=payload, timeout=15)
    print(f"HTTP 状态码：{response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        content = result.get('output', {}).get('text', '')
        print(f"✅ API 调用成功！")
        print(f"AI 回复：{content}")
    else:
        print(f"❌ API 调用失败")
        print(f"错误信息：{response.text[:300]}")
except Exception as e:
    print(f"❌ 异常：{e}")
