#!/usr/bin/env python3
import requests
import time

url = "https://api.github.com/repos/txxxxxorzz/news-dashboard/actions/runs"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "News-Dashboard"
}

print("📊 检查最新的 Workflow 运行状态...\n")

response = requests.get(url, headers=headers, timeout=10)
data = response.json()

runs = data.get('workflow_runs', [])[:3]

for run in runs:
    status = run.get('status', 'unknown')
    conclusion = run.get('conclusion', '-')
    name = run.get('name', 'Unknown')
    run_number = run.get('run_number', '?')
    created_at = run.get('created_at', '?')
    run_id = run.get('id', '')
    
    # 状态图标
    if status == 'completed':
        icon = '✅' if conclusion == 'success' else '❌'
    elif status == 'in_progress':
        icon = '🔄 运行中...'
    elif status == 'queued':
        icon = '⏳ 排队中...'
    else:
        icon = '⚪'
    
    print(f"{icon} Run #{run_number}")
    print(f"   名称：{name}")
    print(f"   状态：{status}")
    if conclusion != '-':
        print(f"   结果：{conclusion}")
    print(f"   时间：{created_at}")
    print(f"   链接：https://github.com/txxxxxorzz/news-dashboard/actions/runs/{run_id}")
    print()
