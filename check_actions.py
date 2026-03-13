#!/usr/bin/env python3
import requests

# GitHub API - 获取最近的 workflow runs
url = "https://api.github.com/repos/txxxxxorzz/news-dashboard/actions/runs"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "News-Dashboard"
}

response = requests.get(url, headers=headers, timeout=10)
data = response.json()

print(f"\n📊 最近的 Workflow 运行记录:\n")

for run in data.get('workflow_runs', [])[:5]:
    status = run.get('status', 'unknown')
    conclusion = run.get('conclusion', '-')
    name = run.get('name', 'Unknown')
    run_number = run.get('run_number', '?')
    created_at = run.get('created_at', '?')
    
    # 状态图标
    if status == 'completed':
        icon = '✅' if conclusion == 'success' else '❌'
    elif status == 'in_progress':
        icon = '🔄'
    elif status == 'queued':
        icon = '⏳'
    else:
        icon = '⚪'
    
    print(f"{icon} Run #{run_number}")
    print(f"   名称：{name}")
    print(f"   状态：{status} ({conclusion})")
    print(f"   时间：{created_at}")
    print(f"   链接：https://github.com/txxxxxorzz/news-dashboard/actions/runs/{run.get('id', '')}")
    print()
