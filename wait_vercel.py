#!/usr/bin/env python3
import requests
import time

url = "https://news-dashboard-three-mu.vercel.app/"

print("⏳ 等待 Vercel 部署完成...\n")

for i in range(15):
    try:
        response = requests.get(url, timeout=10)
        content = response.text
        
        # 检查是否包含"最后更新："和实际时间（不是"--"）
        if '最后更新：--' not in content and '最后更新：' in content:
            print(f"✅ Vercel 部署完成！页面已更新！")
            print(f"   URL: {url}")
            break
        else:
            print(f"第 {i+1} 次检查：页面还在加载旧缓存...")
    except Exception as e:
        print(f"第 {i+1} 次检查：{e}")
    
    time.sleep(10)
else:
    print("\n⚠️ 15 次检查后仍未更新，可能需要手动刷新浏览器缓存")
    print(f"   请尝试：Ctrl + F5 (Windows) 或 Cmd + Shift + R (Mac)")
