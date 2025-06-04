#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NO-FOMO 日报自动化管理脚本
功能：
1. 复制最新日期文件夹到home目录
2. 更新主页的日期列表
3. 更新daily页面的重定向
4. 自动提交到Git
"""

import os
import sys
import shutil
import json
import re
from datetime import datetime, date
from pathlib import Path
import subprocess

class DailyReportManager:
    def __init__(self, base_path=None):
        """初始化管理器"""
        if base_path is None:
            # 默认为当前脚本所在目录的上级目录
            self.base_path = Path(__file__).parent.parent
        else:
            self.base_path = Path(base_path)
        
        self.home_path = self.base_path / "home"
        self.daily_path = self.base_path / "daily"
        self.automation_path = self.base_path / "automation"
        
        # 确保目录存在
        self.home_path.mkdir(exist_ok=True)
        self.daily_path.mkdir(exist_ok=True)
        self.automation_path.mkdir(exist_ok=True)
        
        print(f"📁 工作目录: {self.base_path}")

    def find_source_folders(self):
        """查找所有源日期文件夹"""
        date_folders = []
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        for item in self.base_path.iterdir():
            if item.is_dir() and date_pattern.match(item.name):
                # 检查是否包含index.html
                if (item / "index.html").exists():
                    date_folders.append(item.name)
        
        # 按日期排序（最新的在前）
        date_folders.sort(reverse=True)
        print(f"📅 发现日期文件夹: {date_folders}")
        return date_folders

    def copy_date_folder(self, source_date, target_date=None):
        """复制日期文件夹到home目录"""
        if target_date is None:
            target_date = source_date
        
        source_path = self.base_path / source_date
        target_path = self.home_path / target_date
        
        if not source_path.exists():
            print(f"❌ 源文件夹不存在: {source_path}")
            return False
        
        if target_path.exists():
            print(f"⚠️  目标文件夹已存在，将覆盖: {target_path}")
            shutil.rmtree(target_path)
        
        try:
            shutil.copytree(source_path, target_path)
            print(f"✅ 成功复制 {source_date} -> home/{target_date}")
            
            # 修改目标文件夹中的index.html，添加导航链接
            self.add_navigation_to_index(target_path / "index.html")
            return True
        except Exception as e:
            print(f"❌ 复制失败: {e}")
            return False

    def add_navigation_to_index(self, index_path):
        """为日报页面添加导航链接"""
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 在header后添加导航栏
            navigation_html = '''
        <nav style="text-align: center; margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <a href="../../home/" style="margin: 0 15px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; font-weight: 500;">🏠 返回主页</a>
            <a href="../../daily/" style="margin: 0 15px; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; font-weight: 500;">📅 最新日报</a>
        </nav>
'''
            
            # 在report-header后插入导航
            content = content.replace(
                '</header>',
                '</header>\n' + navigation_html
            )
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已为 {index_path} 添加导航链接")
        except Exception as e:
            print(f"⚠️  添加导航链接失败: {e}")

    def count_articles_in_folder(self, folder_path):
        """统计文件夹中的文章数量"""
        try:
            with open(folder_path / "index.html", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统计item-card数量
            article_count = content.count('class="item-card"')
            return article_count
        except:
            return 0

    def extract_sources_from_folder(self, folder_path):
        """从文件夹中提取数据源"""
        try:
            with open(folder_path / "index.html", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取source-group-title
            sources = re.findall(r'<h2 class="source-group-title">([^<]+)</h2>', content)
            return sources
        except:
            return []

    def update_home_page(self, available_dates):
        """更新主页的日期列表"""
        home_index = self.home_path / "index.html"
        
        if not home_index.exists():
            print(f"❌ 主页文件不存在: {home_index}")
            return False
        
        try:
            with open(home_index, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 构建新的reports数组
            reports_data = []
            for date_str in available_dates:
                folder_path = self.home_path / date_str
                if folder_path.exists():
                    article_count = self.count_articles_in_folder(folder_path)
                    sources = self.extract_sources_from_folder(folder_path)
                    
                    # 生成描述
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%Y年%m月%d日')
                    
                    description = f"涵盖 {', '.join(sources[:3])} 等来源的最新 AI 资讯和技术突破"
                    if len(sources) > 3:
                        description += f"等 {len(sources)} 个来源"
                    
                    reports_data.append({
                        'date': date_str,
                        'title': f'AI 日报 - {formatted_date}',
                        'description': description,
                        'articleCount': article_count,
                        'sources': sources
                    })
            
            # 替换JavaScript中的reports数组
            reports_js = json.dumps(reports_data, ensure_ascii=False, indent=12)
            pattern = r'const reports = \[[\s\S]*?\];'
            replacement = f'const reports = {reports_js};'
            
            content = re.sub(pattern, replacement, content)
            
            with open(home_index, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新主页，包含 {len(reports_data)} 个日报")
            return True
        except Exception as e:
            print(f"❌ 更新主页失败: {e}")
            return False

    def update_daily_page(self, available_dates):
        """更新daily页面的重定向"""
        daily_index = self.daily_path / "index.html"
        
        if not daily_index.exists():
            print(f"❌ Daily页面文件不存在: {daily_index}")
            return False
        
        try:
            with open(daily_index, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新availableDates数组
            dates_js = json.dumps(available_dates, ensure_ascii=False, indent=12)
            pattern = r'const availableDates = \[[\s\S]*?\];'
            replacement = f'const availableDates = {dates_js};'
            
            content = re.sub(pattern, replacement, content)
            
            with open(daily_index, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新daily页面，最新日期: {available_dates[0] if available_dates else 'None'}")
            return True
        except Exception as e:
            print(f"❌ 更新daily页面失败: {e}")
            return False

    def git_commit_and_push(self, message=None):
        """提交更改到Git"""
        if message is None:
            today = date.today().strftime('%Y-%m-%d')
            message = f"自动更新日报 - {today}"
        
        try:
            # 切换到base_path目录
            os.chdir(self.base_path)
            
            # Git操作
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', message], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            print(f"✅ 已提交到Git: {message}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git操作失败: {e}")
            return False
        except Exception as e:
            print(f"❌ Git操作出错: {e}")
            return False

    def sync_all_dates(self):
        """同步所有日期文件夹到home目录"""
        source_dates = self.find_source_folders()
        
        if not source_dates:
            print("❌ 没有找到任何日期文件夹")
            return False
        
        success_count = 0
        for date_str in source_dates:
            if self.copy_date_folder(date_str):
                success_count += 1
        
        print(f"📊 同步完成: {success_count}/{len(source_dates)} 个文件夹")
        
        # 更新页面
        self.update_home_page(source_dates)
        self.update_daily_page(source_dates)
        
        return success_count > 0

    def add_new_date(self, source_date, auto_commit=True):
        """添加新的日期文件夹"""
        print(f"🚀 开始处理新日期: {source_date}")
        
        # 复制文件夹
        if not self.copy_date_folder(source_date):
            return False
        
        # 获取更新后的日期列表
        available_dates = self.find_available_home_dates()
        
        # 更新页面
        self.update_home_page(available_dates)
        self.update_daily_page(available_dates)
        
        # 自动提交
        if auto_commit:
            commit_message = f"添加新日报 - {source_date}"
            self.git_commit_and_push(commit_message)
        
        print(f"🎉 成功添加新日报: {source_date}")
        return True

    def find_available_home_dates(self):
        """查找home目录中可用的日期"""
        date_folders = []
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        for item in self.home_path.iterdir():
            if item.is_dir() and date_pattern.match(item.name):
                if (item / "index.html").exists():
                    date_folders.append(item.name)
        
        date_folders.sort(reverse=True)
        return date_folders

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='NO-FOMO 日报自动化管理工具')
    parser.add_argument('--base-path', help='基础路径', default=None)
    parser.add_argument('--sync-all', action='store_true', help='同步所有日期文件夹')
    parser.add_argument('--add-date', help='添加特定日期的文件夹')
    parser.add_argument('--no-commit', action='store_true', help='不自动提交到Git')
    
    args = parser.parse_args()
    
    # 创建管理器
    manager = DailyReportManager(args.base_path)
    
    if args.sync_all:
        print("🔄 开始同步所有日期文件夹...")
        if manager.sync_all_dates():
            if not args.no_commit:
                manager.git_commit_and_push("同步所有日报文件夹")
        else:
            sys.exit(1)
    
    elif args.add_date:
        print(f"➕ 添加新日期: {args.add_date}")
        if not manager.add_new_date(args.add_date, not args.no_commit):
            sys.exit(1)
    
    else:
        # 默认行为：查找最新的源文件夹并添加
        source_dates = manager.find_source_folders()
        if source_dates:
            latest_date = source_dates[0]
            available_dates = manager.find_available_home_dates()
            
            if not available_dates or latest_date not in available_dates:
                print(f"🆕 发现新日期: {latest_date}")
                if not manager.add_new_date(latest_date, not args.no_commit):
                    sys.exit(1)
            else:
                print(f"✅ 最新日期 {latest_date} 已存在，无需更新")
        else:
            print("❌ 没有找到任何源日期文件夹")
            sys.exit(1)

if __name__ == "__main__":
    main() 