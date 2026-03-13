#!/usr/bin/env python3
import requests
import base64

# 获取 workflow run 的日志
job_id = "66900750856"
url = f"https://api.github.com/repos/txxxxxorzz/news-dashboard/actions/jobs/{job_id}/logs"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "News-Dashboard"
}

response = requests.get(url, headers=headers, timeout=10, stream=True)

if response.status_code == 200:
    # 日志是纯文本，直接打印
    log_text = response.text
    print("\n📜 Workflow 日志:\n")
    print("=" * 60)
    
    # 只显示最后 50 行
    lines = log_text.split('\n')
    for line in lines[-50:]:
        print(line)
    print("=" * 60)
else:
    print(f"无法获取日志：HTTP {response.status_code}")
    print(response.text)
