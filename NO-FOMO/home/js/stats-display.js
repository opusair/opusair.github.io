// 统计显示增强脚本
class StatsDisplay {
    constructor() {
        this.animationDuration = 1000; // 动画持续时间
        this.isAnimating = false;
    }

    // 数字动画效果
    animateNumber(element, startValue, endValue, duration = this.animationDuration) {
        if (this.isAnimating) return;
        
        this.isAnimating = true;
        const start = performance.now();
        const change = endValue - startValue;

        const animate = (currentTime) => {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            
            // 使用缓动函数
            const easeOutCubic = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.floor(startValue + (change * easeOutCubic));
            
            element.textContent = currentValue.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                this.isAnimating = false;
                element.textContent = endValue.toLocaleString();
            }
        };

        requestAnimationFrame(animate);
    }

    // 更新统计项目并添加动画
    updateStatItem(elementId, newValue) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const currentValue = parseInt(element.textContent.replace(/,/g, '')) || 0;
        
        if (currentValue !== newValue) {
            this.animateNumber(element, currentValue, newValue);
            
            // 添加更新高亮效果
            element.parentElement.classList.add('stat-updated');
            setTimeout(() => {
                element.parentElement.classList.remove('stat-updated');
            }, 2000);
        }
    }

    // 添加实时更新指示器
    addUpdateIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'stats-indicator';
        indicator.innerHTML = `
            <div class="update-dot"></div>
            <span>实时统计</span>
        `;
        indicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(40, 167, 69, 0.3);
        `;

        const style = document.createElement('style');
        style.textContent = `
            .update-dot {
                width: 8px;
                height: 8px;
                background: white;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .stat-updated {
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
                transform: scale(1.02);
                transition: all 0.3s ease;
            }
            
            .popular-page-item.new-visit {
                animation: newVisit 0.5s ease;
            }
            
            @keyframes newVisit {
                0% { background: #4caf50; color: white; }
                100% { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); color: inherit; }
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(indicator);
    }

    // 显示更新通知
    showUpdateNotification(message) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: #007bff;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 1000;
            box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // 滑入动画
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // 3秒后移除
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // 初始化
    init() {
        this.addUpdateIndicator();
        
        // 监听页面可见性变化
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.showUpdateNotification('📊 统计数据已更新');
            }
        });
    }
}

// 全局实例
window.StatsDisplay = window.StatsDisplay || new StatsDisplay();

// 页面加载后初始化
document.addEventListener('DOMContentLoaded', () => {
    window.StatsDisplay.init();
}); 