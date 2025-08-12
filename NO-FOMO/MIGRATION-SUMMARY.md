# 清理过时引用并修复所有页面（推荐）
python automation/daily_report_manager.py --clean-fix

# 同步所有日期文件夹（不清理）
python daily_report_manager.py --sync-all

# 仅同步Google Analytics
python automation/daily_report_manager.py --sync-ga