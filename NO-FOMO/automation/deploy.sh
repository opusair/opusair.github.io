#!/bin/bash

# NO-FOMO 日报自动化部署脚本

#   ./deploy.sh init        # 初始化并同步所有文件夹
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

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

cd "$BASE_DIR"

# 功能函数
function init_sync() {
    echo -e "${YELLOW}🔄 初始化并同步所有日期文件夹...${NC}"
    python3 "$PYTHON_SCRIPT" --base-path "$BASE_DIR" --sync-all
    echo -e "${GREEN}✅ 初始化完成${NC}"
}

function setup_cron() {
    echo -e "${YELLOW}⏰ 设置定时任务...${NC}"
    
    local cron_script="$SCRIPT_DIR/cron_daily_update.sh"
    cat > "$cron_script" << EOF
#!/bin/bash
# 自动日报更新脚本
cd "$BASE_DIR"
"$SCRIPT_DIR/deploy.sh" init >> "$SCRIPT_DIR/cron.log" 2>&1
EOF
    
    chmod +x "$cron_script"
    
    # 检查是否已存在cron任务
    if crontab -l 2>/dev/null | grep -q "$cron_script"; then
        echo -e "${YELLOW}⚠️  定时任务已存在${NC}"
    else
        # 添加cron任务 - 每天早上11点执行
        (crontab -l 2>/dev/null; echo "0 11 * * * $cron_script") | crontab -
        echo -e "${GREEN}✅ 已设置定时任务：每天早上11点自动更新日报${NC}"
        echo -e "${BLUE}📝 日志文件: $SCRIPT_DIR/cron.log${NC}"
    fi
}

function show_help() {
    echo -e "${BLUE}🚀 NO-FOMO 日报自动化部署工具使用说明${NC}"
    echo ""
    echo -e "${YELLOW}用法:${NC}"
    echo "  $0 init                    # 初始化并同步所有文件夹"
    echo "  $0 setup-cron             # 设置定时任务"
    echo "  $0 help                    # 显示此帮助信息"
    echo ""
    echo -e "${YELLOW}示例:${NC}"
    echo "  $0 init                    # 首次使用时初始化"
    echo "  $0 setup-cron             # 设置每日自动更新"
}

# 主逻辑
case "${1:-help}" in
    "init")
        init_sync
        ;;
    "setup-cron")
        setup_cron
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