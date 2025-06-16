#!/usr/bin/env python3
"""
简化版 Analytics 数据更新脚本
在没有GA API访问权限时，基于合理估算生成统计数据
"""

import json
import os
from datetime import datetime

STATS_FILE = "analytics-stats.json"

def load_existing_stats():
    """加载现有的统计数据"""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "lastUpdated": None,
        "totalVisits": 0,
        "todayVisits": 0,
        "yesterdayVisits": 0,
        "last7DaysVisits": 0,
        "last30DaysVisits": 0,
        "popularPages": [],
        "trafficSources": {},
        "deviceStats": {},
        "countryStats": {}
    }

def generate_realistic_stats():
    """维护现有统计数据，不自动增加"""
    existing_stats = load_existing_stats()
    
    # 获取当前时间
    now = datetime.utcnow()
    
    # 如果是第一次运行，初始化基础数据
    if existing_stats["totalVisits"] == 0:
        # 初始化基础数据（只在第一次运行时）
        base_total = 1000
        today_visits = 25
    else:
        # 保持现有数据不变
        base_total = existing_stats["totalVisits"]
        
        # 检查是否是新的一天
        last_updated = existing_stats.get("lastUpdated")
        if last_updated:
            last_date = datetime.fromisoformat(last_updated.replace('Z', '+00:00')).date()
            current_date = now.date()
            
            if current_date > last_date:
                # 新的一天，重置今日访问量为0
                today_visits = 0
            else:
                # 同一天，保持现有今日访问量
                today_visits = existing_stats["todayVisits"]
        else:
            today_visits = existing_stats.get("todayVisits", 0)
    
    # 构建统计数据
    stats = {
        "lastUpdated": now.isoformat() + "Z",
        "totalVisits": base_total,
        "todayVisits": today_visits,
        "yesterdayVisits": existing_stats.get("yesterdayVisits", 20),
        "last7DaysVisits": existing_stats.get("last7DaysVisits", 200),
        "last30DaysVisits": existing_stats.get("last30DaysVisits", 800),
        "popularPages": existing_stats.get("popularPages", [
            {
                "path": "/NO-FOMO/home/",
                "title": "NO-FOMO AI 日报 - 主页",
                "views": 150
            },
            {
                "path": "/NO-FOMO/daily/",
                "title": "最新日报",
                "views": 100
            },
            {
                "path": "/NO-FOMO/home/2025-06-11/",
                "title": "AI 日报 - 2025-06-11",
                "views": 55
            }
        ]),
        "trafficSources": existing_stats.get("trafficSources", {
            "direct": 40,
            "search": 30,
            "social": 20,
            "referral": 10
        }),
        "deviceStats": existing_stats.get("deviceStats", {
            "desktop": 50,
            "mobile": 40,
            "tablet": 10
        }),
        "countryStats": existing_stats.get("countryStats", {
            "CN": 55,
            "US": 20,
            "JP": 10,
            "KR": 8,
            "other": 7
        })
    }
    
    return stats

def update_stats_file(stats):
    """更新统计文件"""
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"✅ 统计数据已更新: {STATS_FILE}")
        return True
    except Exception as e:
        print(f"❌ 更新统计文件时出错: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始更新 NO-FOMO AI 日报统计数据...")
    
    try:
        # 生成统计数据
        stats = generate_realistic_stats()
        
        # 更新统计文件
        if update_stats_file(stats):
            print("📊 统计数据更新成功!")
            print(f"   📈 总访问量: {stats['totalVisits']:,}")
            print(f"   📅 今日访问: {stats['todayVisits']:,}")
            print(f"   🕐 更新时间: {stats['lastUpdated']}")
            print(f"   🔥 热门页面: {len(stats['popularPages'])} 个")
        else:
            print("❌ 统计数据更新失败")
            return False
            
    except Exception as e:
        print(f"❌ 执行过程中出错: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1) 