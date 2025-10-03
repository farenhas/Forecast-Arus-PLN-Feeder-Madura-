import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Forecast Arus",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%);
    }
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header */
    .main-header {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
        border: 2px solid rgba(6, 182, 212, 0.3);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(6, 182, 212, 0.3);
    }
    
    .main-title {
        font-size: 3.5em;
        font-weight: 800;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-align: center;
        letter-spacing: -2px;
    }
    
    .subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 1.1em;
        margin-top: 10px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
        border: 2px solid rgba(6, 182, 212, 0.3);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(6, 182, 212, 0.4);
        border-color: rgba(6, 182, 212, 0.6);
    }
    
    .metric-label {
        color: #06b6d4;
        font-size: 0.9em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    .metric-value {
        color: white;
        font-size: 3em;
        font-weight: 800;
        line-height: 1;
        margin: 15px 0;
    }
    
    .metric-status {
        color: #10b981;
        font-size: 0.9em;
        font-weight: 600;
    }
    
    /* GO Status Card */
    .go-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        border: 3px solid rgba(16, 185, 129, 0.5);
    }
    
    .go-value {
        color: #10b981;
        font-size: 4em;
        font-weight: 900;
    }
    
    /* Target Card */
    .target-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
        border: 3px solid rgba(59, 130, 246, 0.5);
    }
    
    .target-value {
        color: #3b82f6;
        font-size: 2.5em;
        font-weight: 800;
    }
    
    /* Recommendation List */
    .recommendation-item {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #06b6d4;
        padding: 12px 15px;
        margin: 8px 0;
        border-radius: 8px;
        color: #e2e8f0;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .recommendation-item:hover {
        background: rgba(6, 182, 212, 0.2);
        transform: translateX(5px);
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(15, 23, 42, 0.7);
        border: 2px solid rgba(6, 182, 212, 0.2);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .chart-title {
        color: #06b6d4;
        font-size: 1.5em;
        font-weight: 700;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.9);
        border: 2px solid rgba(6, 182, 212, 0.3);
        border-radius: 12px;
        color: white;
    }
    
    /* Date Input Styling */
    .stDateInput > div > div > input {
        background: rgba(15, 23, 42, 0.9);
        border: 2px solid rgba(6, 182, 212, 0.3);
        border-radius: 12px;
        color: white;
    }
    
    /* Columns Gap */
    [data-testid="column"] {
        padding: 0 10px;
    }
    
    /* Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
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

# ==================== PLOTTING FUNCTIONS ====================
def create_line_chart(data, title, color='#3b82f6', show_reference=False, ref_value=None):
    """Create beautiful line chart with Plotly"""
    fig = go.Figure()
    
    # Add main line
    fig.add_trace(go.Scatter(
        x=data['time'],
        y=data['value'],
        mode='lines+markers',
        name='Value',
        line=dict(color=color, width=3, shape='spline'),
        marker=dict(size=6, color=color, line=dict(color='white', width=1)),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)',
        hovertemplate='<b>Time:</b> %{x}<br><b>Value:</b> %{y:.1f} A<extra></extra>'
    ))
    
    # Add reference line if needed
    if show_reference and ref_value:
        fig.add_trace(go.Scatter(
            x=data['time'],
            y=[ref_value] * len(data),
            mode='lines',
            name=f'I Nom {ref_value:.0f} A',
            line=dict(color='#ef4444', width=2, dash='dash'),
            hovertemplate='<b>I Nom:</b> %{y:.0f} A<extra></extra>'
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='#06b6d4', family='Inter')),
        plot_bgcolor='rgba(15, 23, 42, 0.5)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#94a3b8', family='Inter'),
        xaxis=dict(
            title='Time',
            gridcolor='rgba(148, 163, 184, 0.1)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='Load (A)',
            gridcolor='rgba(148, 163, 184, 0.1)',
            showgrid=True,
            zeroline=False
        ),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(15, 23, 42, 0.8)',
            bordercolor='rgba(6, 182, 212, 0.3)',
            borderwidth=1
        ),
        margin=dict(l=50, r=50, t=60, b=50),
        height=350
    )
    
    return fig

# ==================== MAIN APP ====================
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">FAREN AND ICHI 4EVER</h1>
        <p class="subtitle">Current Distribution Monitoring System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters Section
    st.markdown("### Control Panel")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_penyulang = st.selectbox(
            "Select Penyulang",
            ["All", "Penyulang A", "Penyulang B", "Penyulang C", "Penyulang D"],
            key="penyulang_select"
        )
    
    with col2:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=7),
            key="start_date"
        )
    
    with col3:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            key="end_date"
        )
    
    st.markdown("---")
    
    # Main Dashboard Grid
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Beban Real Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        beban_real_data = generate_beban_real_data()
        fig_real = create_line_chart(
            beban_real_data,
            "Beban Real",
            color='#3b82f6'
        )
        st.plotly_chart(fig_real, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Current Load Card
        current_load = 132
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">BEBAN SAAT INI</div>
            <div class="metric-value">{current_load} A</div>
            <div class="metric-status">Normal Operation</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recommendations Card
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">REKOMENDASI TUJUAN MANUVER</div>
            <div class="recommendation-item">Penyulang A</div>
            <div class="recommendation-item">Penyulang B</div>
            <div class="recommendation-item">Penyulang C</div>
            <div class="recommendation-item">Penyulang D</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # GO/NO GO and Target Feeder
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card go-card">
            <div class="metric-label">GO or NO GO?</div>
            <div class="go-value pulse">GO</div>
            <div class="metric-status">Safe to Proceed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card target-card">
            <div class="metric-label">TARGET FEEDER</div>
            <div class="target-value">PENYULANG B</div>
            <div class="metric-status">Optimal Selection</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Prediction Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    prediksi_data = generate_prediksi_data()
    fig_prediksi = create_line_chart(
        prediksi_data,
        "Beban Prediksi",
        color='#06b6d4'
    )
    st.plotly_chart(fig_prediksi, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tota Penyulang Grid
    st.markdown("### Tota Penyulang Monitoring")
    
    col1, col2 = st.columns(2)
    
    penyulangs = ['A', 'B', 'C', 'D']
    colors = ['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899']
    
    for idx, penyulang in enumerate(penyulangs):
        with col1 if idx % 2 == 0 else col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            penyulang_data = generate_penyulang_data(penyulang)
            fig_penyulang = create_line_chart(
                penyulang_data,
                f"Tota Penyulang {penyulang}",
                color=colors[idx],
                show_reference=True,
                ref_value=penyulang_data['i_nom'].iloc[0]
            )
            st.plotly_chart(fig_penyulang, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 20px;">
        <p style="margin: 0; font-size: 0.9em;">© 2025 ITS - Advanced Power Distribution Monitoring</p>
        <p style="margin: 5px 0 0 0; font-size: 0.8em;">Powered by Streamlit & Plotly</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== RUN APP ====================
if __name__ == "__main__":
    main()
