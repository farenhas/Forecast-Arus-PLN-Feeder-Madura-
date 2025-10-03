import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Current Distribution Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #0f1829 50%, #1e2a4a 75%, #0a0e27 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header */
    .main-header {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.15) 50%, rgba(139, 92, 246, 0.15) 100%);
        border: 2px solid rgba(6, 182, 212, 0.4);
        border-radius: 24px;
        padding: 40px 30px;
        margin-bottom: 35px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(6, 182, 212, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .main-title {
        font-size: 3.2em;
        font-weight: 900;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-align: center;
        letter-spacing: -2px;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 40px rgba(6, 182, 212, 0.3);
    }
    
    .subtitle {
        color: #cbd5e1;
        text-align: center;
        font-size: 1.15em;
        margin-top: 12px;
        font-weight: 500;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
    }
    
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 12px;
        color: #10b981;
        font-size: 0.75em;
        font-weight: 600;
        margin-left: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Control Panel */
    .control-panel {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(6, 182, 212, 0.25);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    .control-title {
        color: #06b6d4;
        font-size: 1.1em;
        font-weight: 700;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        border: 2px solid rgba(6, 182, 212, 0.3);
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 16px 48px rgba(6, 182, 212, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border-color: rgba(6, 182, 212, 0.6);
    }
    
    .metric-icon {
        font-size: 2.5em;
        margin-bottom: 10px;
        opacity: 0.8;
    }
    
    .metric-label {
        color: #06b6d4;
        font-size: 0.85em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
        opacity: 0.9;
    }
    
    .metric-value {
        color: white;
        font-size: 2.8em;
        font-weight: 900;
        line-height: 1;
        margin: 15px 0;
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 0 2px 10px rgba(6, 182, 212, 0.3);
    }
    
    .metric-status {
        color: #10b981;
        font-size: 0.9em;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .metric-subtext {
        color: #94a3b8;
        font-size: 0.8em;
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Operational Status Card */
    .status-operational {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.15) 100%);
        border: 3px solid rgba(16, 185, 129, 0.5);
        position: relative;
    }
    
    .status-operational::after {
        content: '';
        position: absolute;
        top: 20px;
        right: 20px;
        width: 12px;
        height: 12px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.8);
        animation: pulse-dot 2s ease-in-out infinite;
    }
    
    @keyframes pulse-dot {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.7; }
    }
    
    .status-value {
        color: #10b981;
        font-size: 3.5em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 30px rgba(16, 185, 129, 0.5);
    }
    
    /* Warning Status Card */
    .status-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.15) 100%);
        border: 3px solid rgba(245, 158, 11, 0.5);
    }
    
    .warning-value {
        color: #f59e0b;
    }
    
    /* Target Card */
    .target-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
        border: 3px solid rgba(59, 130, 246, 0.5);
    }
    
    .target-value {
        color: #3b82f6;
        font-size: 2.2em;
        font-weight: 900;
        letter-spacing: 1px;
        text-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Recommendation List */
    .recommendations-container {
        max-height: 280px;
        overflow-y: auto;
        padding-right: 5px;
    }
    
    .recommendations-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .recommendations-container::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
    }
    
    .recommendations-container::-webkit-scrollbar-thumb {
        background: rgba(6, 182, 212, 0.5);
        border-radius: 10px;
    }
    
    .recommendation-item {
        background: linear-gradient(90deg, rgba(6, 182, 212, 0.1) 0%, rgba(15, 23, 42, 0.6) 100%);
        border-left: 4px solid #06b6d4;
        padding: 14px 18px;
        margin: 10px 0;
        border-radius: 10px;
        color: #e2e8f0;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-item::before {
        content: '→';
        position: absolute;
        right: 18px;
        opacity: 0;
        transition: all 0.3s ease;
        color: #06b6d4;
        font-weight: bold;
    }
    
    .recommendation-item:hover {
        background: linear-gradient(90deg, rgba(6, 182, 212, 0.25) 0%, rgba(15, 23, 42, 0.8) 100%);
        transform: translateX(8px);
        border-left-color: #3b82f6;
        box-shadow: 0 4px 16px rgba(6, 182, 212, 0.3);
    }
    
    .recommendation-item:hover::before {
        opacity: 1;
        right: 12px;
    }
    
    .recommendation-badge {
        display: inline-block;
        padding: 2px 8px;
        background: rgba(16, 185, 129, 0.2);
        border-radius: 6px;
        font-size: 0.75em;
        color: #10b981;
        margin-left: 8px;
        font-weight: 700;
    }
    
    /* Chart Container */
    .chart-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.85) 100%);
        border: 2px solid rgba(6, 182, 212, 0.25);
        border-radius: 20px;
        padding: 25px;
        margin: 18px 0;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        border-color: rgba(6, 182, 212, 0.4);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }
    
    .chart-title {
        color: #06b6d4;
        font-size: 1.4em;
        font-weight: 800;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        letter-spacing: 0.5px;
    }
    
    .chart-icon {
        font-size: 1.2em;
    }
    
    /* Section Headers */
    .section-header {
        color: #cbd5e1;
        font-size: 1.6em;
        font-weight: 800;
        margin: 35px 0 20px 0;
        padding-left: 15px;
        border-left: 4px solid #06b6d4;
        letter-spacing: 0.5px;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.95);
        border: 2px solid rgba(6, 182, 212, 0.3);
        border-radius: 12px;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(6, 182, 212, 0.5);
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.2);
    }
    
    /* Date Input Styling */
    .stDateInput > div > div > input {
        background: rgba(15, 23, 42, 0.95);
        border: 2px solid rgba(6, 182, 212, 0.3);
        border-radius: 12px;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stDateInput > div > div > input:hover {
        border-color: rgba(6, 182, 212, 0.5);
    }
    
    /* Columns Gap */
    [data-testid="column"] {
        padding: 0 12px;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .stat-item {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .stat-value {
        color: #06b6d4;
        font-size: 1.5em;
        font-weight: 800;
        margin-top: 5px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Loading Animation */
    .loading-pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.5), transparent);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA GENERATION ====================
@st.cache_data
def generate_beban_real_data(periods=45):
    """Generate realistic load data"""
    time_points = list(range(1, periods + 1))
    base_load = 140
    noise = np.random.normal(0, 8, periods)
    trend = np.where(np.array(time_points) > 30, 50, 0)
    values = base_load + noise + trend + np.sin(np.array(time_points) * 0.3) * 10
    
    return pd.DataFrame({
        'time': time_points,
        'value': values
    })

@st.cache_data
def generate_prediksi_data(periods=45):
    """Generate prediction data"""
    time_points = list(range(1, periods + 1))
    base_load = 150
    noise = np.random.normal(0, 6, periods)
    trend = np.where(np.array(time_points) > 30, 40, 0)
    values = base_load + noise + trend + np.sin(np.array(time_points) * 0.3) * 8
    
    return pd.DataFrame({
        'time': time_points,
        'value': values
    })

@st.cache_data
def generate_penyulang_data(penyulang_name, periods=46):
    """Generate feeder data"""
    time_points = list(range(1, periods + 1))
    offsets = {'A': 0, 'B': 5, 'C': -5, 'D': 10}
    offset = offsets.get(penyulang_name, 0)
    
    base_load = 180 + offset
    noise = np.random.normal(0, 5, periods)
    seasonal = np.sin(np.array(time_points) * 0.2) * 15
    values = base_load + noise + seasonal
    
    i_nom = 200 + offset
    
    return pd.DataFrame({
        'time': time_points,
        'value': values,
        'i_nom': [i_nom] * periods
    })

def calculate_statistics(data):
    """Calculate statistical metrics"""
    return {
        'avg': np.mean(data['value']),
        'max': np.max(data['value']),
        'min': np.min(data['value']),
        'current': data['value'].iloc[-1]
    }

# ==================== PLOTTING FUNCTIONS ====================
def create_line_chart(data, title, color='#3b82f6', show_reference=False, ref_value=None):
    """Create beautiful line chart with Plotly"""
    fig = go.Figure()
    
    # Add main line with gradient fill
    fig.add_trace(go.Scatter(
        x=data['time'],
        y=data['value'],
        mode='lines+markers',
        name='Current Load',
        line=dict(color=color, width=3.5, shape='spline'),
        marker=dict(size=7, color=color, line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.15)',
        hovertemplate='<b>Time Period:</b> %{x}<br><b>Load:</b> %{y:.2f} A<br><extra></extra>'
    ))
    
    # Add reference line if needed
    if show_reference and ref_value:
        fig.add_trace(go.Scatter(
            x=data['time'],
            y=[ref_value] * len(data),
            mode='lines',
            name=f'Nominal Current ({ref_value:.0f} A)',
            line=dict(color='#ef4444', width=2.5, dash='dash'),
            hovertemplate='<b>I Nominal:</b> %{y:.0f} A<extra></extra>'
        ))
        
        # Add warning zone
        fig.add_trace(go.Scatter(
            x=data['time'],
            y=[ref_value * 0.9] * len(data),
            mode='lines',
            name='Warning Threshold (90%)',
            line=dict(color='#f59e0b', width=1.5, dash='dot'),
            hovertemplate='<b>Warning Level:</b> %{y:.0f} A<extra></extra>'
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=22, color='#06b6d4', family='Inter', weight=800)
        ),
        plot_bgcolor='rgba(15, 23, 42, 0.3)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#cbd5e1', family='Inter'),
        xaxis=dict(
            title='Time Period',
            gridcolor='rgba(148, 163, 184, 0.12)',
            showgrid=True,
            zeroline=False,
            linecolor='rgba(148, 163, 184, 0.3)'
        ),
        yaxis=dict(
            title='Load Current (Ampere)',
            gridcolor='rgba(148, 163, 184, 0.12)',
            showgrid=True,
            zeroline=False,
            linecolor='rgba(148, 163, 184, 0.3)'
        ),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(15, 23, 42, 0.9)',
            bordercolor='rgba(6, 182, 212, 0.4)',
            borderwidth=2,
            font=dict(size=11)
        ),
        margin=dict(l=60, r=40, t=70, b=60),
        height=380
    )
    
    return fig

# ==================== MAIN APP ====================
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">⚡ CURRENT DISTRIBUTION MONITOR</h1>
        <p class="subtitle">Real-Time Power Distribution Management System<span class="status-badge">● ONLINE</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Control Panel
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown('<div class="control-title">📊 Control Panel & Filters</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_penyulang = st.selectbox(
            "🔌 Select Feeder",
            ["All Feeders", "Penyulang A", "Penyulang B", "Penyulang C", "Penyulang D"],
            key="penyulang_select"
        )
    
    with col2:
        start_date = st.date_input(
            "📅 Start Date",
            value=datetime.now() - timedelta(days=7),
            key="start_date"
        )
    
    with col3:
        end_date = st.date_input(
            "📅 End Date",
            value=datetime.now(),
            key="end_date"
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Main Dashboard Grid
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Beban Real Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><span class="chart-icon">📈</span>Real-Time Load Current</div>', unsafe_allow_html=True)
        
        beban_real_data = generate_beban_real_data()
        stats_real = calculate_statistics(beban_real_data)
        
        # Stats Row
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Current</div>
                <div class="stat-value">{stats_real['current']:.1f}A</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Average</div>
                <div class="stat-value">{stats_real['avg']:.1f}A</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Peak</div>
                <div class="stat-value">{stats_real['max']:.1f}A</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Minimum</div>
                <div class="stat-value">{stats_real['min']:.1f}A</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        fig_real = create_line_chart(
            beban_real_data,
            "",
            color='#3b82f6'
        )
        st.plotly_chart(fig_real, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Current Load Card
        current_load = 132
        load_percentage = (current_load / 200) * 100
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⚡</div>
            <div class="metric-label">Current Load</div>
            <div class="metric-value">{current_load}<span style="font-size: 0.5em; color: #94a3b8;"> A</span></div>
            <div class="metric-status">● Normal Operation</div>
            <div class="metric-subtext">{load_percentage:.1f}% of Nominal Capacity</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recommendations Card
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-label">Recommended Feeders</div>
            <div class="recommendations-container">
                <div class="recommendation-item">Penyulang A<span class="recommendation-badge">Optimal</span></div>
                <div class="recommendation-item">Penyulang B<span class="recommendation-badge">Available</span></div>
                <div class="recommendation-item">Penyulang C<span class="recommendation-badge">Available</span></div>
                <div class="recommendation-item">Penyulang D<span class="recommendation-badge">Backup</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Operational Status and Target Feeder
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card status-operational">
            <div class="metric-icon">✓</div>
            <div class="metric-label">Operational Status</div>
            <div class="status-value">APPROVED</div>
            <div class="metric-status">Safe to Proceed with Maneuver</div>
            <div class="metric-subtext">All parameters within safe limits</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card target-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-label">Recommended Target</div>
            <div class="target-value">PENYULANG B</div>
            <div class="metric-status">Optimal Selection Based on Analysis</div>
            <div class="metric-subtext">Lowest load utilization (72%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Prediction Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><span class="chart-icon">🔮</span>Load Forecast Analysis</div>', unsafe_allow_html=True)
    
    prediksi_data = generate_prediksi_data()
    stats_prediksi = calculate_statistics(prediksi_data)
    
    # Prediction Stats
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-item">
            <div class="stat-label">Predicted Peak</div>
            <div class="stat-value">{stats_prediksi['max']:.1f}A</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Expected Average</div>
            <div class="stat-value">{stats_prediksi['avg']:.1f}A</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Forecast Accuracy</div>
            <div class="stat-value">94.2%</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Confidence Level</div>
            <div class="stat-value">High</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_prediksi = create_line_chart(
        prediksi_data,
        "",
        color='#06b6d4'
    )
    st.plotly_chart(fig_prediksi, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Feeder Monitoring Section
    st.markdown('<div class="section-header">🔌 Individual Feeder Monitoring</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    penyulangs = ['A', 'B', 'C', 'D']
    colors = ['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899']
    icons = ['⚡', '🔋', '💡', '⚙️']
    
    for idx, penyulang in enumerate(penyulangs):
        with col1 if idx % 2 == 0 else col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            penyulang_data = generate_penyulang_data(penyulang)
            stats_penyulang = calculate_statistics(penyulang_data)
            i_nom = penyulang_data['i_nom'].iloc[0]
            utilization = (stats_penyulang['current'] / i_nom) * 100
            
            # Status badge
            status_color = '#10b981' if utilization < 80 else '#f59e0b' if utilization < 90 else '#ef4444'
            status_text = 'Normal' if utilization < 80 else 'Warning' if utilization < 90 else 'Critical'
            
            st.markdown(f"""
            <div class="chart-title">
                <span class="chart-icon">{icons[idx]}</span>
                Feeder {penyulang}
                <span style="margin-left: auto; font-size: 0.6em; color: {status_color}; background: rgba({int(status_color[1:3], 16)}, {int(status_color[3:5], 16)}, {int(status_color[5:7], 16)}, 0.2); padding: 4px 12px; border-radius: 8px;">● {status_text}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Mini stats
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px;">
                <div class="stat-item">
                    <div class="stat-label">Current</div>
                    <div class="stat-value" style="font-size: 1.2em;">{stats_penyulang['current']:.1f}A</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Nominal</div>
                    <div class="stat-value" style="font-size: 1.2em;">{i_nom:.0f}A</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Utilization</div>
                    <div class="stat-value" style="font-size: 1.2em; color: {status_color};">{utilization:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            fig_penyulang = create_line_chart(
                penyulang_data,
                "",
                color=colors[idx],
                show_reference=True,
                ref_value=i_nom
            )
            st.plotly_chart(fig_penyulang, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # System Overview Card
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 System Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🌐</div>
            <div class="metric-label">Total Feeders</div>
            <div class="metric-value" style="font-size: 2.5em;">4</div>
            <div class="metric-status">All Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">⚡</div>
            <div class="metric-label">System Load</div>
            <div class="metric-value" style="font-size: 2.5em;">685A</div>
            <div class="metric-status">85.6% Capacity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">📈</div>
            <div class="metric-label">Efficiency</div>
            <div class="metric-value" style="font-size: 2.5em;">96.8%</div>
            <div class="metric-status">Excellent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🛡️</div>
            <div class="metric-label">System Health</div>
            <div class="metric-value" style="font-size: 2.5em; color: #10b981;">A+</div>
            <div class="metric-status">Optimal</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 30px; background: rgba(15, 23, 42, 0.5); border-radius: 16px; border: 1px solid rgba(6, 182, 212, 0.2);">
        <p style="margin: 0; font-size: 1em; font-weight: 600; color: #94a3b8;">⚡ Advanced Power Distribution Monitoring System</p>
        <p style="margin: 8px 0 0 0; font-size: 0.85em;">Developed with ❤️ by ITS Engineering Team • Powered by Streamlit & Plotly</p>
        <p style="margin: 8px 0 0 0; font-size: 0.75em; color: #64748b;">© 2025 Institut Teknologi Sepuluh Nopember • Real-Time Monitoring Dashboard v2.0</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== RUN APP ====================
if __name__ == "__main__":
    main()
