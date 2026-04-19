#!/usr/bin/env python3
"""
Pet Cell Dashboard - Streamlit应用
集成增强版销售仪表板功能
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random

# 页面配置
st.set_page_config(
    page_title="Pet Cell 销售仪表板",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 主容器 */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* 标题样式 */
    .dashboard-title {
        color: #4361ee;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* 卡片样式 */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border-top: 4px solid #4361ee;
        transition: all 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }
    
    .metric-icon {
        font-size: 2.5rem;
        color: #4361ee;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #212529;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #6c757d;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    .metric-change {
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .metric-change.positive {
        color: #28a745;
    }
    
    .metric-change.negative {
        color: #dc3545;
    }
    
    /* 图表容器 */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    /* 漏斗阶段 */
    .funnel-stage {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 10px;
        background: linear-gradient(90deg, rgba(67, 97, 238, 0.1), rgba(58, 12, 163, 0.05));
    }
    
    .stage-number {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #4361ee;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
    }
    
    .stage-content {
        flex: 1;
    }
    
    .stage-title {
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .stage-count {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4361ee;
    }
    
    /* 排行榜 */
    .leaderboard-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.75rem;
        transition: all 0.3s;
    }
    
    .leaderboard-item:hover {
        background: rgba(67, 97, 238, 0.05);
    }
    
    .rank {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
    }
    
    .rank-1 { background: gold; color: #333; }
    .rank-2 { background: silver; color: #333; }
    .rank-3 { background: #cd7f32; color: white; }
    .rank-other { background: #e9ecef; color: #6c757d; }
    
    /* 时间线 */
    .timeline-item {
        position: relative;
        margin-bottom: 1.5rem;
        padding-left: 2rem;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0.5rem;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #4361ee;
        border: 3px solid white;
        box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
    }
    
    .timeline-time {
        font-size: 0.85rem;
        color: #6c757d;
        margin-bottom: 0.25rem;
    }
    
    .timeline-content {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.05);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(45deg, #4361ee, #3a0ca3);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(67, 97, 238, 0.3);
    }
    
    /* 侧边栏样式 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4361ee 0%, #3a0ca3 100%);
        color: white;
    }
    
    /* 响应式调整 */
    @media (max-width: 768px) {
        .metric-value {
            font-size: 1.8rem;
        }
        
        .dashboard-title {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = {
        'monthly_revenue': [65000, 82000, 78000, 95000, 110000, 125000, 
                           98000, 112000, 136000, 142000, 158000, 175000],
        'funnel_stages': [
            {'stage': '潜在客户', 'count': 156, 'percentage': 100},
            {'stage': '初步咨询', 'count': 89, 'percentage': 57},
            {'stage': '方案评估', 'count': 64, 'percentage': 41},
            {'stage': '签订合同', 'count': 48, 'percentage': 31},
            {'stage': '完成治疗', 'count': 42, 'percentage': 27}
        ],
        'leaderboard': [
            {'name': '张经理', 'score': 245800, 'rank': 1},
            {'name': '李专员', 'score': 198500, 'rank': 2},
            {'name': '王顾问', 'score': 176300, 'rank': 3},
            {'name': '赵主管', 'score': 152400, 'rank': 4},
            {'name': '刘顾问', 'score': 138900, 'rank': 5}
        ],
        'recent_activities': [
            {'time': '刚刚', 'content': '张经理 成功签约新患者 #PT20240048，合同金额 ¥38,500'},
            {'time': '5分钟前', 'content': '李专员 完成患者 #PT20240032 的第二次治疗'},
            {'time': '15分钟前', 'content': '新潜在客户 王先生 提交咨询，宠物类型：犬，疾病：关节炎'},
            {'time': '30分钟前', 'content': '赵主管 完成月度销售报告，本月目标完成率 92%'},
            {'time': '1小时前', 'content': '患者 #PT20240025 疗效评估完成，改善率 85%'}
        ],
        'disease_distribution': {
            '关节炎': 35,
            '皮肤病': 25,
            '消化系统疾病': 20,
            '神经系统疾病': 12,
            '其他': 8
        }
    }

# 模拟数据更新函数
def update_sales_data():
    """模拟实时数据更新"""
    data = st.session_state.sales_data
    
    # 随机更新一些数据
    revenue_change = random.randint(-2000, 5000)
    current_revenue = 1234567 + revenue_change
    data['current_revenue'] = max(1000000, current_revenue)
    
    # 更新漏斗数据（轻微变化）
    for stage in data['funnel_stages']:
        change = random.randint(-2, 3)
        stage['count'] = max(0, stage['count'] + change)
    
    # 更新排行榜（轻微变化）
    for person in data['leaderboard']:
        change = random.randint(-5000, 10000)
        person['score'] = max(100000, person['score'] + change)
    
    # 重新排序排行榜
    data['leaderboard'].sort(key=lambda x: x['score'], reverse=True)
    for i, person in enumerate(data['leaderboard']):
        person['rank'] = i + 1
    
    # 添加新的活动
    activities = [
        f"新签约患者 #PT{random.randint(20240000, 20249999)}，合同金额 ¥{random.randint(20000, 50000)}",
        f"患者 #PT{random.randint(20240000, 20249999)} 完成第{random.randint(1, 3)}次治疗",
        f"新潜在客户咨询，宠物类型：{random.choice(['犬', '猫'])}, 疾病：{random.choice(['关节炎', '皮肤病', '消化系统疾病'])}",
        f"疗效评估完成，改善率 {random.randint(70, 95)}%",
        f"销售报告生成，目标完成率 {random.randint(85, 105)}%"
    ]
    
    new_activity = {
        'time': '刚刚',
        'content': random.choice(activities)
    }
    
    # 更新时间
    for activity in data['recent_activities']:
        if activity['time'] == '刚刚':
            activity['time'] = '1分钟前'
        elif activity['time'] == '1分钟前':
            activity['time'] = '5分钟前'
        elif activity['time'] == '5分钟前':
            activity['time'] = '15分钟前'
        elif activity['time'] == '15分钟前':
            activity['time'] = '30分钟前'
        elif activity['time'] == '30分钟前':
            activity['time'] = '1小时前'
        elif activity['time'] == '1小时前':
            activity['time'] = '2小时前'
    
    # 移除最旧的活动，添加新的
    if len(data['recent_activities']) >= 6:
        data['recent_activities'].pop()
    data['recent_activities'].insert(0, new_activity)

# 侧边栏导航
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: white; margin-bottom: 0.5rem;">🐾 Pet Cell</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">干细胞治疗销售管理系统</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 导航菜单
    page = st.radio(
        "导航菜单",
        ["销售仪表板", "患者管理", "销售漏斗", "业绩分析", "团队管理", "销售报告", "系统设置"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # 用户信息
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(45deg, #fff, #e0e0e0); 
             display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: #4361ee; font-weight: bold; font-size: 1.5rem;">
            王
        </div>
        <p style="color: white; font-weight: bold; margin-bottom: 0.25rem;">王经理</p>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">销售总监</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 系统状态
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-top: 1rem;">
        <div style="width: 10px; height: 10px; border-radius: 50%; background: #28a745;"></div>
        <span style="color: rgba(255,255,255,0.9);">系统在线</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 版本信息
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8rem; padding-top: 1rem;">
        <p>销售版本 2.0.0</p>
        <p>© 2024 Pet Cell研究中心</p>
    </div>
    """, unsafe_allow_html=True)

# 主内容区域
if page == "销售仪表板":
    # 标题区域
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1 class="dashboard-title">销售仪表板</h1>', unsafe_allow_html=True)
        st.markdown('<p class="dashboard-subtitle">实时跟踪销售业绩与患者转化</p>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 刷新数据", use_container_width=True):
            update_sales_data()
            st.rerun()
    
    # 关键指标卡片
    st.markdown("### 📊 关键指标")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-value">¥ 1,234,567</div>
            <div class="metric-label">本月销售额</div>
            <div class="metric-change positive">📈 12.5% 较上月</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-value">48</div>
            <div class="metric-label">本月新增患者</div>
            <div class="metric-change positive">📈 8.2% 较上月</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">📈</div>
            <div class="metric-value">68.5%</div>
            <div class="metric-label">转化率</div>
            <div class="metric-change positive">📈 3.1% 较上月</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">⏱️</div>
            <div class="metric-value">2.4</div>
            <div class="metric-label">平均响应时间(天)</div>
            <div class="metric-change negative">📉 0.3 较上月</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 销售漏斗和排行榜
    st.markdown("### 🎯 销售漏斗分析")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 销售漏斗各阶段")
        
        # 显示漏斗阶段
        for stage in st.session_state.sales_data['funnel_stages']:
            st.markdown(f"""
            <div class="funnel-stage">
                <div class="stage-number">{stage['stage'][0]}</div>
                <div class="stage-content">
                    <div class="stage-title">{stage['stage']}</div>
                    <div class="stage-count">{stage['count']}</div>
                    <div style="height: 8px; background: #e9ecef; border-radius: 4px; margin-top: 0.5rem;">
                        <div style="width: {stage['percentage']}%; height: 100%; background: linear-gradient(90deg, #4361ee, #3a0ca3); border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🏆 本月销售之星")
        
        # 显示排行榜
        for person in st.session_state.sales_data['leaderboard'][:5]:
            rank_class = f"rank-{person['rank']}" if person['rank'] <= 3 else "rank-other"
            st.markdown(f"""
            <div class="leaderboard-item">
                <div class="rank {rank_class}">{person['rank']}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">{person['name']}</div>
                    <div style="font-weight: 700; color: #4361ee; font-size: 1.2rem;">¥ {person['score']:,}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 图表区域
    st.markdown("### 📈 数据可视化")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 月度销售趋势")
        
        # 创建销售趋势图
        months = ['1月', '2月', '3月', '4月', '5月', '6月', 
                 '7月', '8月', '9月', '10月', '11月', '12月']
        revenue = st.session_state.sales_data['monthly_revenue']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=revenue,
            mode='lines+markers',
            name='销售额',
            line=dict(color='#4361ee', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(67, 97, 238, 0.1)'
        ))
        
        fig.update_layout(
            height=300,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(
                gridcolor='#e9ecef',
                showline=True,
                linecolor='#e9ecef'
            ),
            yaxis=dict(
                gridcolor='#e9ecef',
                showline=True,
                linecolor='#e9ecef',
                tickprefix='¥ '
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 疾病类型分布")
        
        # 创建疾病分布饼图
        diseases = list(st.session_state.sales_data['disease_distribution'].keys())
        counts = list(st.session_state.sales_data['disease_distribution'].values())
        
        colors = ['#4361ee', '#3a0ca3', '#4cc9f0', '#f72585', '#7209b7']
        
        fig = go.Figure(data=[go.Pie(
            labels=diseases,
            values=counts,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            height=300,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 实时动态和目标进度
    st.markdown("### ⚡ 实时动态")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 最新活动")
        
        # 显示时间线
        for activity in st.session_state.sales_data['recent_activities'][:5]:
            st.markdown(f"""
            <div class="timeline-item">
                <div class="timeline-time">{activity['time']}</div>
                <div class="timeline-content">{activity['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🎯 月度目标进度")
        
        # 目标进度
        goal_percentage = 78
        completed = 936000
        remaining = 264000
        days_left = 12
        
        # 创建环形进度图
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=goal_percentage,
            number={'suffix': '%'},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#4361ee"},
                'steps': [
                    {'range': [0, 100], 'color': "#e9ecef"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 目标详情
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="margin-bottom: 0.5rem;">
                <span style="color: #6c757d;">已完成:</span>
                <span style="font-weight: bold; margin-left: 0.5rem;">¥ {completed:,}</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span style="color: #6c757d;">剩余:</span>
                <span style="font-weight: bold; margin-left: 0.5rem;">¥ {remaining:,}</span>
            </div>
            <div style="margin-bottom: 1rem;">
                <span style="color: #6c757d;">剩余天数:</span>
                <span style="font-weight: bold; margin-left: 0.5rem;">{days_left} 天</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("查看详细目标", use_container_width=True):
            st.info("目标详情功能开发中...")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "患者管理":
    st.title("患者管理")
    st.info("患者管理功能开发中...")
    
    # 这里可以集成原有的患者管理功能
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input("搜索患者...")
    with col2:
        st.button("新增患者")
    
    # 显示患者表格
    st.dataframe(pd.DataFrame({
        '患者ID': ['PT001', 'PT002', 'PT003', 'PT004'],
        '物种': ['犬', '猫', '犬', '猫'],
        '品种': ['金毛', '波斯猫', '哈士奇', '暹罗猫'],
        '年龄': ['3岁', '2岁', '5岁', '1岁'],
        '疾病类型': ['关节炎', '皮肤病', '消化系统疾病', '神经系统疾病'],
        '最近治疗': ['2024-01-15', '2024-01-10', '2024-01-05', '2024-01-02']
    }))

elif page == "销售漏斗":
    st.title("销售漏斗分析")
    st.info("销售漏斗分析功能开发中...")
    
    # 这里可以添加更详细的漏斗分析

elif page == "业绩分析":
    st.title("业绩分析")
    st.info("业绩分析功能开发中...")
    
    # 这里可以添加更详细的业绩分析图表

elif page == "团队管理":
    st.title("团队管理")
    st.info("团队管理功能开发中...")
    
    # 这里可以添加团队管理功能

elif page == "销售报告":
    st.title("销售报告")
    st.info("销售报告功能开发中...")
    
    # 这里可以添加报告生成和导出功能

elif page == "系统设置":
    st.title("系统设置")
    st.info("系统设置功能开发中...")
    
    # 这里可以添加系统设置选项

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem; padding: 1rem 0;">
    <p>Pet Cell 销售管理系统 | 版本 2.0.0 | 数据最后更新: {}</p>
    <p>如有问题，请联系技术支持: support@petcell.com</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# 自动刷新（可选）
if st.checkbox("启用自动刷新（每30秒）"):
    st.write("⏳ 数据将自动刷新...")
    st.rerun()
