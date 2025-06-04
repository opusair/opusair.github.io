#!/bin/bash

# NO-FOMO 日报自动化部署脚本
# 使用方法：
#   ./deploy.sh init        # 初始化并同步所有文件夹
#   ./deploy.sh daily       # 添加今天的日报（如果存在）
#   ./deploy.sh add 2025-06-01  # 添加指定日期的日报
#   ./deploy.sh update      # 检查并更新最新日报
#   ./deploy.sh setup-cron  # 设置定时任务

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$SCRIPT_DIR/daily_report_manager.py"

echo -e "${BLUE}📡 NO-FOMO 日报自动化部署工具${NC}"
echo -e "${BLUE}🏠 工作目录: $BASE_DIR${NC}"

# 检查Python脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}❌ Python脚本不存在: $PYTHON_SCRIPT${NC}"
    exit 1
fi

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

# 检查Git环境
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git 未安装${NC}"
    exit 1
fi

# 切换到基础目录
cd "$BASE_DIR"

# 功能函数
function init_sync() {
    echo -e "${YELLOW}🔄 初始化并同步所有日期文件夹...${NC}"
    python3 "$PYTHON_SCRIPT" --base-path "$BASE_DIR" --sync-all
    echo -e "${GREEN}✅ 初始化完成${NC}"
}

function daily_update() {
    echo -e "${YELLOW}📅 检查今日日报...${NC}"
    TODAY=$(date +%Y-%m-%d)
    if [ -d "$BASE_DIR/$TODAY" ]; then
        echo -e "${BLUE}📰 发现今日日报: $TODAY${NC}"
        python3 "$PYTHON_SCRIPT" --base-path "$BASE_DIR" --add-date "$TODAY"
    else
        echo -e "${YELLOW}⚠️  今日日报文件夹不存在: $TODAY${NC}"
        # 检查是否有其他新日期
        python3 "$PYTHON_SCRIPT" --base-path "$BASE_DIR"
    fi
}

function add_date() {
    local date_to_add="$1"
    if [ -z "$date_to_add" ]; then
        echo -e "${RED}❌ 请指定要添加的日期，格式: YYYY-MM-DD${NC}"
        exit 1
    fi
    
    # 验证日期格式
    if [[ ! "$date_to_add" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo -e "${RED}❌ 日期格式错误，应为: YYYY-MM-DD${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}➕ 添加日期: $date_to_add${NC}"
    python3 "$PYTHON_SCRIPT" --base-path "$BASE_DIR" --add-date "$date_to_add"
}

function update_latest() {
    echo -e "${YELLOW}🔍 检查并更新最新日报...${NC}"
    python3 "$PYTHON_SCRIPT" --base-path "$BASE_DIR"
}

function setup_cron() {
    echo -e "${YELLOW}⏰ 设置定时任务...${NC}"
    
    # 创建crontab脚本
    local cron_script="$SCRIPT_DIR/cron_daily_update.sh"
    cat > "$cron_script" << EOF
#!/bin/bash
# 自动日报更新脚本
cd "$BASE_DIR"
"$SCRIPT_DIR/deploy.sh" daily >> "$SCRIPT_DIR/cron.log" 2>&1
EOF
    
    chmod +x "$cron_script"
    
    # 检查是否已存在cron任务
    if crontab -l 2>/dev/null | grep -q "$cron_script"; then
        echo -e "${YELLOW}⚠️  定时任务已存在${NC}"
    else
        # 添加cron任务 - 每天早上9点执行
        (crontab -l 2>/dev/null; echo "0 9 * * * $cron_script") | crontab -
        echo -e "${GREEN}✅ 已设置定时任务：每天早上9点自动更新日报${NC}"
        echo -e "${BLUE}📝 日志文件: $SCRIPT_DIR/cron.log${NC}"
    fi
}

function show_status() {
    echo -e "${BLUE}📊 当前状态:${NC}"
    
    # 检查源文件夹
    echo -e "${YELLOW}📁 源文件夹:${NC}"
    find "$BASE_DIR" -maxdepth 1 -type d -name "20*-*-*" | sort -r | head -5 | while read -r dir; do
        local dirname=$(basename "$dir")
        if [ -f "$dir/index.html" ]; then
            echo -e "  ✅ $dirname"
        else
            echo -e "  ❌ $dirname (缺少index.html)"
        fi
    done
    
    # 检查home文件夹
    echo -e "${YELLOW}🏠 Home文件夹:${NC}"
    if [ -d "$BASE_DIR/home" ]; then
        find "$BASE_DIR/home" -maxdepth 1 -type d -name "20*-*-*" | sort -r | head -5 | while read -r dir; do
            local dirname=$(basename "$dir")
            echo -e "  ✅ $dirname"
        done
    else
        echo -e "  ❌ home目录不存在"
    fi
    
    # 检查Git状态
    echo -e "${YELLOW}📋 Git状态:${NC}"
    if git status --porcelain | grep -q .; then
        echo -e "  ⚠️  有未提交的更改"
        git status --short
    else
        echo -e "  ✅ 工作目录干净"
    fi
}

function show_help() {
    echo -e "${BLUE}🚀 NO-FOMO 日报自动化部署工具使用说明${NC}"
    echo ""
    echo -e "${YELLOW}用法:${NC}"
    echo "  $0 init                    # 初始化并同步所有文件夹"
    echo "  $0 daily                   # 添加今天的日报（如果存在）"
    echo "  $0 add YYYY-MM-DD         # 添加指定日期的日报"
    echo "  $0 update                  # 检查并更新最新日报"
    echo "  $0 setup-cron             # 设置定时任务"
    echo "  $0 status                  # 显示当前状态"
    echo "  $0 help                    # 显示此帮助信息"
    echo ""
    echo -e "${YELLOW}示例:${NC}"
    echo "  $0 init                    # 首次使用时初始化"
    echo "  $0 add 2025-06-01         # 添加6月1日的日报"
    echo "  $0 daily                   # 每日更新"
}

# 主逻辑
case "${1:-help}" in
    "init")
        init_sync
        ;;
    "daily")
        daily_update
        ;;
    "add")
        add_date "$2"
        ;;
    "update")
        update_latest
        ;;
    "setup-cron")
        setup_cron
        ;;
    "status")
        show_status
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        echo -e "${RED}❌ 未知命令: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo -e "${GREEN}🎉 操作完成！${NC}" 