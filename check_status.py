#!/usr/bin/env python3
import requests

url = "https://api.github.com/repos/txxxxxorzz/news-dashboard/actions/runs"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "News-Dashboard"
}

response = requests.get(url, headers=headers, timeout=10)
data = response.json()

print("\n📊 最新 Workflow 运行状态:\n")

for run in data.get('workflow_runs', [])[:2]:
    status = run.get('status', 'unknown')
    conclusion = run.get('conclusion', '-')
    run_number = run.get('run_number', '?')
    run_id = run.get('id', '')
    created_at = run.get('created_at', '?')
    
    if status == 'completed':
        icon = '✅' if conclusion == 'success' else '❌'
    elif status == 'in_progress':
        icon = '🔄'
    else:
        icon = '⏳'
    
    print(f"{icon} Run #{run_number} - {status} ({conclusion})")
    print(f"   时间：{created_at}")
    print(f"   链接：https://github.com/txxxxxorzz/news-dashboard/actions/runs/{run_id}\n")
