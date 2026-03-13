#!/usr/bin/env python3
import requests
import time

url = "https://txxxxxorzz.github.io/news-dashboard/news_data/latest.json"

print("⏳ 等待 GitHub Pages 更新...")
print(f"URL: {url}\n")

for i in range(10):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GitHub Pages 已更新！")
            print(f"   更新时间：{data.get('updateTime', 'Unknown')}")
            print(f"   平台数：{len(data.get('platforms', {}))}")
            for platform, pdata in data.get('platforms', {}).items():
                count = sum(len(items) for items in pdata.get('categories', {}).values())
                print(f"   - {pdata.get('name', platform)}: {count} 条")
            break
        else:
            print(f"第 {i+1} 次尝试：HTTP {response.status_code}")
    except Exception as e:
        print(f"第 {i+1} 次尝试：{e}")
    
    time.sleep(5)
else:
    print("\n❌ 10 次尝试后仍未成功")
