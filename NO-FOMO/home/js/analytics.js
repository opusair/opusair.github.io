// NO-FOMO 网站访问统计模块
class NoFomoAnalytics {
    constructor() {
        this.storageKey = 'nofomo-analytics';
        this.initAnalytics();
    }

    // 初始化统计数据
    initAnalytics() {
        if (!localStorage.getItem(this.storageKey)) {
            const initialData = {
                totalVisits: 0,
                pageVisits: {},
                dailyVisits: {},
                lastUpdated: new Date().toISOString()
            };
            localStorage.setItem(this.storageKey, JSON.stringify(initialData));
        }
    }

    // 获取当前页面路径
    getCurrentPagePath() {
        const path = window.location.pathname;
        return path.replace('/NO-FOMO/home/', '').replace(/\/$/, '') || 'index';
    }

    // 记录页面访问
    recordVisit() {
        const data = this.getAnalyticsData();
        const pagePath = this.getCurrentPagePath();
        const today = new Date().toISOString().split('T')[0];

        // 更新总访问量
        data.totalVisits += 1;

        // 更新页面访问量
        if (!data.pageVisits[pagePath]) {
            data.pageVisits[pagePath] = 0;
        }
        data.pageVisits[pagePath] += 1;

        // 更新每日访问量
        if (!data.dailyVisits[today]) {
            data.dailyVisits[today] = {};
        }
        if (!data.dailyVisits[today][pagePath]) {
            data.dailyVisits[today][pagePath] = 0;
        }
        data.dailyVisits[today][pagePath] += 1;

        // 更新最后访问时间
        data.lastUpdated = new Date().toISOString();

        // 保存数据
        localStorage.setItem(this.storageKey, JSON.stringify(data));
        
        // 触发自定义事件，通知其他页面更新
        this.broadcastUpdate();
    }

    // 获取统计数据
    getAnalyticsData() {
        const data = localStorage.getItem(this.storageKey);
        return data ? JSON.parse(data) : null;
    }

    // 获取总页面数
    getTotalPages() {
        const data = this.getAnalyticsData();
        return data ? Object.keys(data.pageVisits).length : 0;
    }

    // 获取今日访问量
    getTodayVisits() {
        const data = this.getAnalyticsData();
        const today = new Date().toISOString().split('T')[0];
        if (!data || !data.dailyVisits[today]) return 0;
        
        return Object.values(data.dailyVisits[today]).reduce((sum, visits) => sum + visits, 0);
    }

    // 获取热门页面
    getPopularPages(limit = 5) {
        const data = this.getAnalyticsData();
        if (!data) return [];

        return Object.entries(data.pageVisits)
            .sort(([,a], [,b]) => b - a)
            .slice(0, limit)
            .map(([page, visits]) => ({ page, visits }));
    }

    // 广播更新事件
    broadcastUpdate() {
        // 使用 localStorage 事件在不同页面间同步
        const event = new CustomEvent('nofomo-analytics-update', {
            detail: this.getAnalyticsData()
        });
        window.dispatchEvent(event);
        
        // 同时触发 storage 事件
        window.dispatchEvent(new Event('storage'));
    }

    // 监听其他页面的更新
    onUpdate(callback) {
        window.addEventListener('nofomo-analytics-update', (e) => {
            callback(e.detail);
        });
        
        window.addEventListener('storage', (e) => {
            if (e.key === this.storageKey) {
                callback(this.getAnalyticsData());
            }
        });
    }

    // 格式化页面名称显示
    formatPageName(pagePath) {
        if (pagePath === 'index') return '主页';
        if (pagePath.match(/^\d{4}-\d{2}-\d{2}$/)) return `日报 ${pagePath}`;
        if (pagePath.match(/^\d{4}-\d{2}-\d{2}\/en$/)) return `英文日报 ${pagePath.replace('/en', '')}`;
        return pagePath;
    }
}

// 全局实例
window.NoFomoAnalytics = window.NoFomoAnalytics || new NoFomoAnalytics();

// 页面加载时自动记录访问
document.addEventListener('DOMContentLoaded', () => {
    window.NoFomoAnalytics.recordVisit();
}); 