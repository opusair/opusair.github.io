import os
import sys
import json
import re
from datetime import date
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
        
        self.home_path.mkdir(exist_ok=True)
        self.daily_path.mkdir(exist_ok=True)
        
        print(f"📁 工作目录: {self.base_path}")

    def has_language_folders(self, date_folder_path):
        """检查日期文件夹是否包含en子文件夹（支持英文版本）"""
        en_exists = (date_folder_path / "en" / "index.html").exists()
        return en_exists

    def find_home_folders(self):
        """查找home目录下的所有日期文件夹"""
        date_folders = []
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        for item in self.home_path.iterdir():
            if item.is_dir() and date_pattern.match(item.name):
                # 检查是否包含主index.html（默认中文版）
                has_main_index = (item / "index.html").exists()
                has_en_version = self.has_language_folders(item)
                
                if has_main_index:
                    date_folders.append({
                        'date': item.name,
                        'path': item,
                        'hasEnglish': has_en_version
                    })
        
        # 按日期排序（最新的在前）
        date_folders.sort(key=lambda x: x['date'], reverse=True)
        
        date_list = [folder['date'] for folder in date_folders]
        print(f"📅 发现home日期文件夹: {date_list}")
        return date_folders

    def add_language_switch_to_report(self, index_path, is_chinese=True, has_languages=True):
        """为日报页面添加语言切换功能"""
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经存在语言切换
            if 'language-switch' in content:
                print(f"ℹ️  {index_path} 已存在语言切换，跳过添加")
                return
            
            if not has_languages:
                print(f"ℹ️  {index_path} 不支持多语言，跳过添加语言切换")
                return
            
            # 添加语言切换CSS样式
            language_switch_css = '''
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
            transition: background-color 0.3s ease, transform 0.2s ease;
            border: 2px solid transparent;
            font-size: 0.9em;
        }

        .language-switch a:hover {
            background: #0056b3;
            transform: translateY(-2px);
        }

        .language-switch a.active {
            background: var(--secondary-color);
            border-color: var(--border-color);
        }

        @media (max-width: 768px) {
            .language-switch {
                position: static;
                justify-content: center;
                margin-bottom: 20px;
            }
        }'''
            
            # 添加CSS到style标签中
            content = content.replace('</style>', language_switch_css + '\n    </style>')
            
            # 修改report-header样式为relative定位
            content = content.replace(
                'border-bottom: 1px solid var(--border-color);',
                'border-bottom: 1px solid var(--border-color);\n            position: relative;'
            )
            
            # 添加语言切换HTML
            if is_chinese:
                language_switch_html = '''            <div class="language-switch">
                <a href="./" class="active">中文</a>
                <a href="en/">English</a>
            </div>
'''
            else:
                language_switch_html = '''            <div class="language-switch">
                <a href="../">中文</a>
                <a href="./" class="active">English</a>
            </div>
'''
            
            # 在report-header开始标签后插入语言切换
            content = content.replace(
                '<header class="report-header">',
                '<header class="report-header">\n' + language_switch_html
            )
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已为 {index_path} 添加语言切换功能")
        except Exception as e:
            print(f"⚠️  添加语言切换失败: {e}")

    def clean_obsolete_references(self, index_path):
        """清理过时的引用（如analytics.js）"""
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 删除对analytics.js的引用
            content = re.sub(r'<script src="[^"]*analytics\.js"><\/script>\s*', '', content)
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已清理 {index_path} 的过时引用")
        except Exception as e:
            print(f"⚠️  清理过时引用失败: {e}")

    def configure_ga_measurement_id(self, index_path, measurement_id="G-008T4WC27P"):
        """配置Google Analytics测量ID"""
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换GA_MEASUREMENT_ID占位符
            content = content.replace('GA_MEASUREMENT_ID', measurement_id)
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已配置 {index_path} 的GA测量ID: {measurement_id}")
        except Exception as e:
            print(f"⚠️  配置GA测量ID失败: {e}")

    def add_google_analytics(self, index_path, has_languages=False):
        """为页面添加Google Analytics（如果不存在的话）"""
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经存在Google Analytics
            if 'googletagmanager.com/gtag/js' in content or 'gtag(' in content:
                print(f"ℹ️  {index_path} 已存在Google Analytics，跳过添加")
                return
            
            # Google Analytics代码
            ga_code = '''    
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-008T4WC27P"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-008T4WC27P');
    </script>
'''
            
            # 在</head>标签前插入
            if '</head>' in content:
                content = content.replace('</head>', f'{ga_code}\n</head>')
            else:
                print(f"⚠️  {index_path} 未找到</head>标签")
                return
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已为 {index_path} 添加Google Analytics")
        except Exception as e:
            print(f"⚠️  添加Google Analytics失败: {e}")

    def add_navigation_to_index(self, index_path, has_languages=False, is_chinese=True):
        """为日报页面添加导航链接（如果不存在的话）"""
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经存在导航栏（更精确的检测）
            # 检查是否存在包含主页、最新日报、关于我们的nav标签
            nav_indicators = [
                '<nav style="text-align: center',  # 导航栏的开始标签
                'background: #f8f9fa',              # 导航栏的背景色
                'Latest Daily' if not is_chinese else '最新日报',  # 最新日报按钮
                'About Us' if not is_chinese else '关于我们'       # 关于我们按钮
            ]
            
            if all(indicator in content for indicator in nav_indicators):
                print(f"ℹ️  {index_path} 已存在导航链接，跳过添加")
                return
            
            # 根据是否有语言版本调整链接路径
            if has_languages:
                # 对于cn/en子文件夹中的文件，需要额外的../
                if is_chinese:
                    home_link = "../../home/"
                    daily_link = "../../daily/"
                else:
                    home_link = "../../../home/en/"
                    daily_link = "../../../daily/en/"
            else:
                # 对于直接在日期文件夹中的文件
                home_link = "../../home/"
                daily_link = "../../daily/"
            
            # 根据语言生成按钮文本
            if is_chinese:
                home_text = "🏠 返回主页"
                daily_text = "📅 最新日报"
                about_text = "👤 关于我们"
            else:
                home_text = "🏠 Back to Homepage"
                daily_text = "📅 Latest Daily"
                about_text = "👤 About Us"
            
            # 在header后添加导航栏
            navigation_html = f'''
        <nav style="text-align: center; margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <a href="{home_link}" style="margin: 0 15px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; font-weight: 500;">{home_text}</a>
            <a href="{daily_link}" style="margin: 0 15px; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; font-weight: 500;">{daily_text}</a>
            <a href="https://opusair.github.io/" style="margin: 0 15px; padding: 10px 20px; background: #ff9800; color: white; text-decoration: none; border-radius: 5px; font-weight: 500;">{about_text}</a>
        </nav>
'''
            
            # 在report-header后插入导航
            content = content.replace(
                '</header>',
                '</header>\n' + navigation_html
            )
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            lang_desc = "中文" if is_chinese else "英文"
            print(f"✅ 已为 {index_path} 添加{lang_desc}导航链接")
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

    def update_home_pages(self, available_folders):
        """更新所有主页（默认主页、英文版）"""
        success = True
        
        # 更新默认主页（中文版）
        success &= self._update_home_page(
            self.home_path / "index.html", 
            available_folders, 
            is_chinese=True
        )
        
        # 更新英文版主页
        en_home = self.home_path / "en" / "index.html"
        if en_home.exists():
            success &= self._update_home_page(en_home, available_folders, is_chinese=False)
        
        return success

    def _update_home_page(self, home_index_path, available_folders, is_chinese=True):
        """更新单个主页的日期列表"""
        if not home_index_path.exists():
            print(f"❌ 主页文件不存在: {home_index_path}")
            return False
        
        try:
            with open(home_index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 构建新的reports数组
            reports_data = []
            for folder_info in available_folders:
                date_str = folder_info['date']
                folder_path = folder_info['path']
                has_english = folder_info['hasEnglish']
                
                # 主文件夹包含中文版本信息
                if (folder_path / "index.html").exists():
                    info_path = folder_path
                else:
                    continue
                
                article_count = self.count_articles_in_folder(info_path)
                sources = self.extract_sources_from_folder(info_path)
                
                # 根据语言生成描述
                if is_chinese:
                    description = f"涵盖 {', '.join(sources[:3])} 等来源的最新 AI 资讯和技术突破"
                    if len(sources) > 3:
                        description += f"等 {len(sources)} 个来源"
                    title = f'AI 日报 - {date_str}'
                else:
                    description = f"Covering the latest AI news and breakthroughs from {len(sources)} sources including {', '.join(sources[:3])}"
                    if len(sources) > 3:
                        description += ", and more"
                    title = f'AI Daily Report - {date_str}'
                
                reports_data.append({
                    'date': date_str,
                    'title': title,
                    'description': description,
                    'articleCount': article_count,
                    'sources': sources,
                    'hasLanguages': has_english
                })
            
            # 替换JavaScript中的reports数组
            reports_js = json.dumps(reports_data, ensure_ascii=False, indent=12)
            pattern = r'const reports = \[[\s\S]*?\];'
            replacement = f'const reports = {reports_js};'
            
            content = re.sub(pattern, replacement, content)
            
            with open(home_index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            lang_desc = "中文" if is_chinese else "英文"
            print(f"✅ 已更新{lang_desc}主页，包含 {len(reports_data)} 个日报")
            return True
        except Exception as e:
            print(f"❌ 更新主页失败: {e}")
            return False

    def update_daily_pages(self, available_folders):
        """更新所有daily页面的重定向，支持多语言检测"""
        success = True
        
        # 更新默认daily页面（使用语言检测）
        success &= self._update_daily_page(
            self.daily_path / "index.html", 
            available_folders, 
            is_chinese=True, 
            use_detection=True
        )
        
        # 更新英文版daily页面
        en_daily = self.daily_path / "en" / "index.html"
        if en_daily.exists():
            success &= self._update_daily_page(en_daily, available_folders, is_chinese=False)
        
        return success

    def _update_daily_page(self, daily_index_path, available_folders, is_chinese=True, use_detection=False):
        """更新单个daily页面的重定向"""
        if not daily_index_path.exists():
            print(f"❌ Daily页面文件不存在: {daily_index_path}")
            return False
        
        try:
            with open(daily_index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 构建可用日期列表
            dates_with_info = []
            for folder_info in available_folders:
                dates_with_info.append({
                    'date': folder_info['date'],
                    'hasLanguages': folder_info['hasEnglish']
                })
            
            if use_detection:
                # 默认daily页面使用语言检测
                new_script = '''        // 可用的日报日期列表（按时间倒序排列）
        const availableDates = ''' + json.dumps(dates_with_info, ensure_ascii=False, indent=12) + ''';

        function detectUserLanguage() {
            // 检测用户语言偏好
            const browserLang = navigator.language || navigator.userLanguage;
            const isChineseBrowser = browserLang.toLowerCase().includes('zh');
            
            // 检查URL参数
            const urlParams = new URLSearchParams(window.location.search);
            const langParam = urlParams.get('lang');
            
            if (langParam === 'en') return 'en';
            if (langParam === 'zh' || langParam === 'cn') return 'zh';
            
            // 默认根据浏览器语言判断，现在默认是中文版（无cn路径）
            return isChineseBrowser ? 'zh' : 'zh'; // 默认中文
        }

        function redirectToLatest() {
            if (availableDates.length > 0) {
                const latestReport = availableDates[0];
                const userLang = detectUserLanguage();
                
                let redirectUrl;
                if (latestReport.hasLanguages && userLang === 'en') {
                    // 如果支持多语言且用户偏好英文，跳转到英文版
                    redirectUrl = `../home/${latestReport.date}/en/`;
                } else {
                    // 默认跳转到中文版（无cn路径）
                    redirectUrl = `../home/${latestReport.date}/`;
                }
                
                console.log(`Redirecting to: ${redirectUrl}`);
                window.location.href = redirectUrl;
            } else {
                // 如果没有可用日报，显示错误信息
                document.getElementById('loading-text').innerHTML = '暂无可用日报';
                document.querySelector('.spinner').style.display = 'none';
            }
        }

        // 页面加载后延迟2秒重定向
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(redirectToLatest, 2000);
        });'''
            else:
                # 语言特定的daily页面直接跳转到对应语言版本
                lang_code = 'en' if not is_chinese else 'zh'
                
                # 根据语言生成注释和错误信息
                if is_chinese:
                    date_list_comment = '// 可用的日报日期列表（按时间倒序排列）'
                    force_redirect_comment = f'// 强制跳转到中文版本（无cn路径）'
                    default_redirect_comment = '// 跳转到默认版本'
                    no_reports_comment = '// 如果没有可用日报，显示错误信息'
                    delay_comment = '// 页面加载后延迟2秒重定向'
                    no_reports_text = '暂无可用日报'
                else:
                    date_list_comment = '// Available daily report dates (in reverse chronological order)'
                    force_redirect_comment = f'// Force redirect to EN version'
                    default_redirect_comment = '// Redirect to default version'
                    no_reports_comment = '// If no reports available, show error message'
                    delay_comment = '// Redirect after 2 seconds delay when page loads'
                    no_reports_text = 'No reports available'
                
                new_script = f'''        {date_list_comment}
        const availableDates = ''' + json.dumps(dates_with_info, ensure_ascii=False, indent=12) + f''';

        function redirectToLatest() {{
            if (availableDates.length > 0) {{
                const latestReport = availableDates[0];
                let redirectUrl;
                
                if (latestReport.hasLanguages && "{lang_code}" === "en") {{
                    {force_redirect_comment}
                    redirectUrl = `../../home/${{latestReport.date}}/en/`;
                }} else {{
                    {default_redirect_comment}
                    redirectUrl = `../../home/${{latestReport.date}}/`;
                }}
                
                console.log(`Redirecting to: ${{redirectUrl}}`);
                window.location.href = redirectUrl;
            }} else {{
                {no_reports_comment}
                document.getElementById('loading-text').innerHTML = '{no_reports_text}';
                document.querySelector('.spinner').style.display = 'none';
            }}
        }}

        {delay_comment}
        document.addEventListener('DOMContentLoaded', function() {{
            setTimeout(redirectToLatest, 2000);
        }});'''
            
            # 替换整个script标签内容
            pattern = r'<script>[\s\S]*?</script>'
            replacement = f'<script>\n{new_script}\n    </script>'
            
            content = re.sub(pattern, replacement, content)
            
            with open(daily_index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            lang_desc = "中文" if is_chinese else "英文"
            latest_date = available_folders[0]['date'] if available_folders else 'None'
            if use_detection:
                print(f"✅ 已更新默认daily页面，支持多语言检测，最新日期: {latest_date}")
            else:
                print(f"✅ 已更新{lang_desc}daily页面，最新日期: {latest_date}")
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

    def sync_google_analytics(self):
        """仅同步Google Analytics到所有页面"""
        available_folders = self.find_home_folders()
        
        if not available_folders:
            print("❌ home目录下没有找到任何日期文件夹")
            return False
        
        # 为每个文件夹添加Google Analytics（如果没有的话）
        for folder_info in available_folders:
            folder_path = folder_info['path']
            has_english = folder_info['hasEnglish']
            
            # 处理主版本（中文）
            main_index = folder_path / "index.html"
            if main_index.exists():
                self.add_google_analytics(main_index, has_languages=has_english)
            
            # 处理英文版本（如果存在）
            if has_english:
                en_index = folder_path / "en" / "index.html"
                if en_index.exists():
                    self.add_google_analytics(en_index, has_languages=True)
        
        # 为主页添加Google Analytics
        home_pages = [
            self.home_path / "index.html",
            self.home_path / "en" / "index.html"
        ]
        
        for home_page in home_pages:
            if home_page.exists():
                self.add_google_analytics(home_page)
        
        print(f"📊 Google Analytics同步完成: 处理了 {len(available_folders)} 个文件夹 + 主页")
        return True

    def clean_and_fix_all_pages(self):
        """清理并修复所有页面"""
        available_folders = self.find_home_folders()
        
        if not available_folders:
            print("❌ home目录下没有找到任何日期文件夹")
            return False
        
        processed_count = 0
        
        # 处理每个日期文件夹
        for folder_info in available_folders:
            folder_path = folder_info['path']
            has_english = folder_info['hasEnglish']
            
            # 处理主版本（中文）
            main_index = folder_path / "index.html"
            if main_index.exists():
                self.clean_obsolete_references(main_index)
                self.configure_ga_measurement_id(main_index)
                self.add_google_analytics(main_index, has_languages=has_english)
                self.add_navigation_to_index(main_index, has_languages=has_english, is_chinese=True)
                if has_english:
                    self.add_language_switch_to_report(main_index, is_chinese=True, has_languages=True)
                processed_count += 1
            
            # 处理英文版本（如果存在）
            if has_english:
                en_index = folder_path / "en" / "index.html"
                if en_index.exists():
                    self.clean_obsolete_references(en_index)
                    self.configure_ga_measurement_id(en_index)
                    self.add_google_analytics(en_index, has_languages=True)
                    self.add_navigation_to_index(en_index, has_languages=True, is_chinese=False)
                    self.add_language_switch_to_report(en_index, is_chinese=False, has_languages=True)
                    processed_count += 1
        
        # 处理主页
        home_pages = [
            (self.home_path / "index.html", True),
            (self.home_path / "en" / "index.html", False)
        ]
        
        for home_page, is_chinese in home_pages:
            if home_page.exists():
                self.clean_obsolete_references(home_page)
                self.configure_ga_measurement_id(home_page)
                self.add_google_analytics(home_page)
                processed_count += 1
        
        print(f"🧹 清理和修复完成: 处理了 {processed_count} 个页面")
        
        # 更新页面数据
        self.update_home_pages(available_folders)
        self.update_daily_pages(available_folders)
        
        return True

    def sync_all_dates(self):
        """同步home目录下的所有日期文件夹（不清理）"""
        available_folders = self.find_home_folders()
        
        if not available_folders:
            print("❌ home目录下没有找到任何日期文件夹")
            return False
        
        # 为每个文件夹添加Google Analytics、导航和语言切换（如果没有的话）
        for folder_info in available_folders:
            folder_path = folder_info['path']
            has_english = folder_info['hasEnglish']
            
            # 处理主版本（中文）
            main_index = folder_path / "index.html"
            if main_index.exists():
                self.add_google_analytics(main_index, has_languages=has_english)
                self.add_navigation_to_index(main_index, has_languages=has_english, is_chinese=True)
                if has_english:
                    self.add_language_switch_to_report(main_index, is_chinese=True, has_languages=True)
            
            # 处理英文版本（如果存在）
            if has_english:
                en_index = folder_path / "en" / "index.html"
                if en_index.exists():
                    self.add_google_analytics(en_index, has_languages=True)
                    self.add_navigation_to_index(en_index, has_languages=True, is_chinese=False)
                    self.add_language_switch_to_report(en_index, is_chinese=False, has_languages=True)
        
        print(f"📊 同步完成: 处理了 {len(available_folders)} 个文件夹")
        
        # 更新页面
        self.update_home_pages(available_folders)
        self.update_daily_pages(available_folders)
        
        return True

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='NO-FOMO 日报自动化管理工具')
    parser.add_argument('--base-path', help='基础路径', default=None)
    parser.add_argument('--sync-all', action='store_true', help='同步所有日期文件夹')
    parser.add_argument('--sync-ga', action='store_true', help='仅同步Google Analytics')
    parser.add_argument('--clean-fix', action='store_true', help='清理过时引用并修复所有页面')
    parser.add_argument('--no-commit', action='store_true', help='不自动提交到Git')
    
    args = parser.parse_args()
    
    manager = DailyReportManager(args.base_path)
    
    if args.clean_fix:
        print("🧹 开始清理过时引用并修复所有页面...")
        if manager.clean_and_fix_all_pages():
            if not args.no_commit:
                manager.git_commit_and_push("清理过时引用，删除Mock数据，修复所有页面")
        else:
            sys.exit(1)
    elif args.sync_all:
        print("🔄 开始同步home目录下的所有日期文件夹...")
        if manager.sync_all_dates():
            if not args.no_commit:
                manager.git_commit_and_push("同步所有日报文件夹，添加Google Analytics")
        else:
            sys.exit(1)
    elif args.sync_ga:
        print("📊 开始同步Google Analytics到所有页面...")
        if manager.sync_google_analytics():
            if not args.no_commit:
                manager.git_commit_and_push("添加Google Analytics到所有页面")
        else:
            sys.exit(1)
    else:
        print("❌ 请使用 --sync-all、--sync-ga 或 --clean-fix 参数")
        print("  --clean-fix: 清理过时引用并修复所有页面")
        print("  --sync-all: 同步所有日期文件夹")
        print("  --sync-ga: 仅同步Google Analytics")
        sys.exit(1)

if __name__ == "__main__":
    main() 