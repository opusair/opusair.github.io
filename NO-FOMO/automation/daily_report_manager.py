import json
import re
import subprocess
from datetime import date
from pathlib import Path


class DailyReportManager:
    
    def __init__(self, base_path=None):
        self.base_path = Path(base_path or Path(__file__).parent.parent)
        self.home_path = self.base_path / "home"
        self.daily_path = self.base_path / "daily"
        
        self.home_path.mkdir(exist_ok=True)
        self.daily_path.mkdir(exist_ok=True)
        
        print(f"📁 工作目录: {self.base_path}")
    
    def find_date_folders(self):
        folders = []
        
        for folder in sorted(self.home_path.iterdir(), reverse=True):
            if folder.is_dir() and re.match(r'^\d{4}-\d{2}-\d{2}$', folder.name):
                if (folder / "index.html").exists():
                    folders.append({
                        'date': folder.name,
                        'path': folder,
                        'hasEnglish': (folder / "en" / "index.html").exists()
                    })
        
        print(f"📅 找到 {len(folders)} 个日期文件夹")
        return folders
    
    def add_google_analytics(self, file_path):
        GA_CODE = '''    
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-008T4WC27P"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-008T4WC27P');
    </script>
'''
        content = file_path.read_text(encoding='utf-8')
        
        if 'googletagmanager.com/gtag/js' in content:
            return
        
        content = content.replace('</head>', f'{GA_CODE}\n</head>')
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ 添加GA: {file_path}")
    
    def add_navigation(self, file_path, has_languages=False, is_chinese=True):
        content = file_path.read_text(encoding='utf-8')
        
        if '最新日报' in content or 'Latest Daily' in content:
            return
        
        depth = "../" * (3 if has_languages and not is_chinese else 2)
        
        nav_html = f'''
        <nav style="text-align: center; margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <a href="{depth}home{'/en' if not is_chinese and has_languages else ''}/" style="margin: 0 15px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; font-weight: 500;">{'🏠 返回主页' if is_chinese else '🏠 Back to Homepage'}</a>
            <a href="{depth}daily{'/en' if not is_chinese and has_languages else ''}/" style="margin: 0 15px; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; font-weight: 500;">{'📅 最新日报' if is_chinese else '📅 Latest Daily'}</a>
            <a href="https://opusair.github.io/" style="margin: 0 15px; padding: 10px 20px; background: #ff9800; color: white; text-decoration: none; border-radius: 5px; font-weight: 500;">{'👤 关于我们' if is_chinese else '👤 About Us'}</a>
        </nav>
'''
        
        content = content.replace('</header>', f'</header>\n{nav_html}')
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ 添加导航: {file_path}")
    
    def add_language_switch(self, file_path, is_chinese=True):
        content = file_path.read_text(encoding='utf-8')
        
        if 'language-switch' in content:
            return
        
        css = '''
        .language-switch {
            position: absolute;
            top: 0;
            right: 0;
            display: flex;
            gap: 10px;
        }
        .language-switch a {
            background: var(--primary-color);
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .language-switch a:hover {
            background: #0056b3;
            transform: translateY(-2px);
        }
        .language-switch a.active {
            background: var(--secondary-color);
        }'''
        
        content = content.replace('</style>', f'{css}\n    </style>')
        content = content.replace(
            'border-bottom: 1px solid var(--border-color);',
            'border-bottom: 1px solid var(--border-color);\n            position: relative;'
        )
        
        # HTML
        html = f'''            <div class="language-switch">
                <a href="{'.' if is_chinese else '../'}" class="{'active' if is_chinese else ''}">中文</a>
                <a href="{'en/' if is_chinese else '.'}" class="{'active' if not is_chinese else ''}">English</a>
            </div>\n'''
        
        content = content.replace(
            '<header class="report-header">',
            f'<header class="report-header">\n{html}'
        )
        
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ 添加语言切换: {file_path}")
    
    def update_home_page(self, file_path, folders, is_chinese=True):
        content = file_path.read_text(encoding='utf-8')
        
        # 构建报告数据
        reports = []
        for folder in folders:
            # 根据语言版本选择正确的文件路径
            if not is_chinese and folder['hasEnglish']:
                # 英文版主页，读取en子文件夹的内容
                content_path = folder['path'] / "en" / "index.html"
            else:
                # 中文版主页，读取根目录的内容
                content_path = folder['path'] / "index.html"
            
            if not content_path.exists():
                continue
                
            # 统计文章数量
            folder_content = content_path.read_text(encoding='utf-8')
            article_count = folder_content.count('class="item-card"')
            
            # 提取来源
            sources = re.findall(r'<h2 class="source-group-title">([^<]+)</h2>', folder_content)
            
            if is_chinese:
                desc = f"涵盖 {', '.join(sources[:3])} 等 {len(sources)} 个来源的最新 AI 资讯"
                title = f"AI 日报 - {folder['date']}"
            else:
                desc = f"Latest AI news from {len(sources)} sources including {', '.join(sources[:3])}"
                title = f"AI Daily Report - {folder['date']}"
            
            reports.append({
                'date': folder['date'],
                'title': title,
                'description': desc,
                'articleCount': article_count,
                'sources': sources,
                'hasLanguages': folder['hasEnglish']
            })
        
        # 替换JS数组
        js_data = json.dumps(reports, ensure_ascii=False, indent=12)
        content = re.sub(
            r'const reports = \[[\s\S]*?\];',
            f'const reports = {js_data};',
            content
        )
        
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ 更新主页: {file_path}")
    
    def update_daily_page(self, file_path, folders, is_chinese=True):
        content = file_path.read_text(encoding='utf-8')
        
        dates_info = [{'date': f['date'], 'hasLanguages': f['hasEnglish']} for f in folders]
        
        # 生成重定向脚本
        base_path = '../' if is_chinese else '../../'
        lang_path = '/en/' if not is_chinese else '/'
        no_reports_text = '暂无可用日报' if is_chinese else 'No reports available'
        
        script = f'''        const availableDates = {json.dumps(dates_info, ensure_ascii=False, indent=12)};

        function redirectToLatest() {{
            if (availableDates.length > 0) {{
                const latest = availableDates[0];
                const url = `{base_path}home/${{latest.date}}{lang_path}`;
                console.log(`Redirecting to: ${{url}}`);
                window.location.href = url;
            }} else {{
                document.getElementById('loading-text').innerHTML = '{no_reports_text}';
                document.querySelector('.spinner').style.display = 'none';
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => setTimeout(redirectToLatest, 2000));'''
        
        content = re.sub(
            r'<script>[\s\S]*?</script>',
            f'<script>\n{script}\n    </script>',
            content
        )
        
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ 更新daily页面: {file_path}")
    
    def process_folder(self, folder_info):
        folder_path = folder_info['path']
        has_english = folder_info['hasEnglish']
        
        # 中文版
        cn_index = folder_path / "index.html"
        if cn_index.exists():
            self.add_google_analytics(cn_index)
            self.add_navigation(cn_index, has_english, True)
            if has_english:
                self.add_language_switch(cn_index, True)
        
        # 英文版
        if has_english:
            en_index = folder_path / "en" / "index.html"
            if en_index.exists():
                self.add_google_analytics(en_index)
                self.add_navigation(en_index, True, False)
                self.add_language_switch(en_index, False)
    
    def sync_all(self):
        """同步所有 """
        folders = self.find_date_folders()
        
        if not folders:
            print("❌ 没找到任何文件夹，你确定路径对了？")
            return False
        
        # 处理每个日期文件夹
        for folder in folders:
            self.process_folder(folder)
        
        # 更新主页
        for path, is_chinese in [(self.home_path / "index.html", True),
                                 (self.home_path / "en" / "index.html", False)]:
            if path.exists():
                self.add_google_analytics(path)
                self.update_home_page(path, folders, is_chinese)
        
        # 更新daily页面
        for path, is_chinese in [(self.daily_path / "index.html", True),
                                 (self.daily_path / "en" / "index.html", False)]:
            if path.exists():
                self.update_daily_page(path, folders, is_chinese)
        
        print(f"✅ 同步完成: 处理了 {len(folders)} 个文件夹")
        return True
    
    def git_commit_and_push(self, message=None):
        message = message or f"自动更新日报 - {date.today()}"
        
        try:
            # 检查是否有更改
            result = subprocess.run(['git', 'status', '--porcelain'], cwd=self.base_path, 
                                  capture_output=True, text=True, check=True)
            
            if not result.stdout.strip():
                print("ℹ️  没有检测到更改，跳过Git提交")
                return True
            
            # 添加更改
            subprocess.run(['git', 'add', '.'], cwd=self.base_path, check=True)
            
            # 提交更改
            subprocess.run(['git', 'commit', '-m', message], cwd=self.base_path, check=True)
            
            # 尝试推送（如果失败也不影响主要功能）
            try:
                subprocess.run(['git', 'push'], cwd=self.base_path, check=True)
                print(f"✅ Git提交并推送成功: {message}")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Git推送失败，但本地提交成功: {e}")
                print("💡 提示: 可以稍后手动执行 'git push' 来同步到远程仓库")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git操作失败: {e}")
            return False


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--sync-all', action='store_true', help='同步所有日期文件夹')
    parser.add_argument('--no-commit', action='store_true', help='不自动提交到Git')
    
    args = parser.parse_args()
    
    if not args.sync_all:
        parser.print_help()
        print("\n❌ 你需要使用 --sync-all 参数")
        return
    
    manager = DailyReportManager()
    
    if manager.sync_all():
        if not args.no_commit:
            manager.git_commit_and_push()
    else:
        print("❌ 同步失败")


if __name__ == "__main__":
    main()
