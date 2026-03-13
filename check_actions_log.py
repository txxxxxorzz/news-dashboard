#!/usr/bin/env python3
import requests

# 获取最近的 workflow run 的日志
run_id = "23034911936"  # 最近的一次运行
url = f"https://api.github.com/repos/txxxxxorzz/news-dashboard/actions/runs/{run_id}/jobs"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "News-Dashboard"
}

response = requests.get(url, headers=headers, timeout=10)
data = response.json()

print(f"\n📋 Workflow Run #{run_id} 详情:\n")

for job in data.get('jobs', []):
    job_name = job.get('name', 'Unknown')
    status = job.get('status', 'unknown')
    conclusion = job.get('conclusion', '-')
    started_at = job.get('started_at', '?')
    completed_at = job.get('completed_at', '?')
    
    print(f"任务：{job_name}")
    print(f"状态：{status}")
    print(f"结论：{conclusion}")
    print(f"开始：{started_at}")
    print(f"完成：{completed_at}")
    print(f"日志：https://github.com/txxxxxorzz/news-dashboard/actions/runs/{run_id}/job/{job.get('id', '')}")
    print()
