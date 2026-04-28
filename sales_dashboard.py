# sales_dashboard.py
# pip install streamlit pandas plotly numpy
# streamlit run sales_dashboard.py

import os
import requests
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@400;600;700&family=Cabinet+Grotesk:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, .stApp {
    background: #07090f !important;
    color: #e8edf8 !important;
    font-family: 'Cabinet Grotesk', sans-serif !important;
}

.block-container { padding: 1.5rem 2.5rem !important; max-width: 1500px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1017 !important;
    border-right: 1px solid rgba(255,255,255,0.055) !important;
}
section[data-testid="stSidebar"] > div { padding: 1.5rem 1rem !important; }
section[data-testid="stSidebar"] * { font-family: 'Cabinet Grotesk', sans-serif !important; }

/* Selectbox / widgets */
.stSelectbox label, .stSlider label, .stMultiselect label, .stDateInput label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #4d5a78 !important;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiselect"] > div > div {
    background: #131822 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e8edf8 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1017 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.055) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #4d5a78 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: rgba(0,230,118,0.1) !important;
    color: #00e676 !important;
}

/* Buttons */
.stButton > button {
    background: #0d1017 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e8edf8 !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
}
.stButton > button:hover {
    border-color: rgba(0,230,118,0.35) !important;
    color: #00e676 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.055) !important;
    overflow: hidden !important;
    background: #0d1017 !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: #0d1017 !important;
    border: 1px solid rgba(255,255,255,0.055) !important;
    border-radius: 14px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Clash Display', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    letter-spacing: -1px !important;
    color: #e8edf8 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #4d5a78 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #00e676 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; display: none !important; }

/* Cards */
.dash-card {
    background: #0d1017;
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
}
.hero-banner {
    background: linear-gradient(135deg, rgba(0,230,118,0.07) 0%, rgba(41,121,255,0.05) 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero-banner::after {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 250px; height: 250px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,230,118,0.08) 0%, transparent 70%);
}
.hero-title {
    font-family: 'Clash Display', sans-serif;
    font-size: 2.4rem; font-weight: 700;
    letter-spacing: -1.5px;
    background: linear-gradient(to right, #e8edf8, #4d5a78);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0;
}
.hero-accent { color: #00e676 !important; -webkit-text-fill-color: #00e676 !important; }
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; letter-spacing: 2.5px;
    color: #4d5a78; text-transform: uppercase;
    margin-top: 0.4rem;
}
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; letter-spacing: 2px;
    color: #4d5a78; text-transform: uppercase;
    margin-bottom: 0.6rem;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Product Card Animations */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes floatProduct {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

@keyframes glowBorder {
    0% { box-shadow: 0 0 0 rgba(0,230,118,0); }
    50% { box-shadow: 0 0 15px rgba(0,230,118,0.3); }
    100% { box-shadow: 0 0 0 rgba(0,230,118,0); }
}

.product-card {
    animation: slideInUp 0.8s ease-out forwards;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 12px 24px rgba(0,230,118,0.15) !important;
    border-color: rgba(0,230,118,0.4) !important;
}

.product-icon {
    font-size: 2.5rem;
    animation: floatProduct 3s ease-in-out infinite;
    display: inline-block;
    margin-bottom: 0.5rem;
}

.product-revenue {
    animation: pulse 2s ease-in-out infinite;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHART THEME
# ─────────────────────────────────────────────
PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono", color="#4d5a78", size=10),
    margin=dict(t=20, b=30, l=10, r=10),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#4d5a78", size=10),
        orientation="h",
        yanchor="bottom", y=1.02, xanchor="right", x=1
    ),
    hoverlabel=dict(
        bgcolor="#0d1017",
        bordercolor="rgba(255,255,255,0.08)",
        font=dict(family="JetBrains Mono", color="#e8edf8", size=11),
    ),
)
ACCENT = ["#00e676","#2979ff","#ffb300","#ff4560","#aa00ff","#00e5ff","#f472b6","#34d399"]

GRID_STYLE = dict(
    xaxis=dict(showgrid=False, linecolor="rgba(255,255,255,0.06)", tickfont=dict(size=9)),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(0,0,0,0)", tickfont=dict(size=9)),
)

@st.cache_data
def fetch_youtube_video_url(query: str, api_key: str) -> str | None:
    if not api_key:
        return None

    endpoint = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": api_key,
    }

    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        if not items:
            return None
        video_id = items[0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    except Exception:
        return None


# ─────────────────────────────────────────────
#  DATA GENERATION
# ─────────────────────────────────────────────
@st.cache_data
def generate_sales_data(seed: int = 42) -> dict:
    rng = np.random.default_rng(seed)

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    regions = ["North America","Europe","Asia Pacific","Latin America","MEA"]
    categories = ["Electronics","Apparel","Software","Hardware","Services"]
    products = ["ProMax X1","Vertex S9","Pulse Mini","Aero Tab","NexBand",
                "CoreDesk","SkyEar","FlexWear","DataBox","ConnectHub"]
    reps = ["Alex Morgan","Jamie Chen","Taylor Brown","Morgan Lee",
            "Casey Williams","Sam Patel","Jordan Kim","Drew Nguyen"]

    # Monthly revenue (2023 & 2024)
    base_2023 = np.array([260,280,330,310,370,400,380,430,410,470,440,500])
    noise_2023 = rng.integers(-20, 20, 12)
    rev_2023 = (base_2023 + noise_2023).tolist()
    growth = rng.uniform(1.12, 1.28, 12)
    rev_2024 = [int(r * g) for r, g in zip(rev_2023, growth)]

    # Region data
    region_data = pd.DataFrame({
        "Region": regions,
        "Revenue_2024": [1540, 1120, 980, 620, 360],
        "Revenue_2023": [1280,  940, 820, 540, 300],
        "Target":       [1640, 1380, 1290, 1070, 840],
        "Units_2024":   [38500, 28000, 24500, 15500,  9000],
    })
    region_data["Achievement"] = (region_data["Revenue_2024"] / region_data["Target"] * 100).round(1)

    # Category mix
    cat_data = pd.DataFrame({
        "Category": categories,
        "Revenue":  [1832, 1062, 869,  675, 386],
        "Units":    [22400,38700,12800,16500,34000],
        "Margin":   [34, 42, 68, 29, 55],
    })

    # Product table
    prod_data = pd.DataFrame({
        "Product":  products,
        "Revenue":  [1240, 980, 760, 620, 440, 380, 310, 260, 180, 120],
        "Units":    [18400,14100,21000,8700,32900,9800,12400,18700,6200,8900],
        "Margin_Pct":[34,28,45,31,52,39,44,48,27,56],
        "MoM_Pct":  [22,14,1,-6,31,8,-11,19,-3,7],
        "Category": ["Electronics","Electronics","Apparel","Hardware",
                     "Services","Hardware","Software","Apparel","Software","Services"],
    })
    
    # Product icons mapping by category
    category_icons = {
        "Electronics": "📱",
        "Apparel": "👕",
        "Software": "💻",
        "Hardware": "⚙️",
        "Services": "🎯"
    }
    prod_data["Icon"] = prod_data["Category"].map(category_icons)

    # Sales reps
    rep_data = pd.DataFrame({
        "Rep":    reps,
        "Region": ["North America","North America","Europe","Europe",
                   "Asia Pacific","Asia Pacific","Latin America","MEA"],
        "Revenue":  [rng.integers(280,450) for _ in reps],
        "Deals":    [rng.integers(28,65) for _ in reps],
        "Win_Rate": [rng.integers(45,80) for _ in reps],
        "Quota_Pct":[rng.integers(70,120) for _ in reps],
    })

    # Daily data (last 90 days)
    dates = [datetime(2024,10,1) + timedelta(days=i) for i in range(90)]
    daily_rev = [rng.integers(120,280) for _ in dates]
    daily_units = [rng.integers(300,900) for _ in dates]
    daily_df = pd.DataFrame({"Date": dates, "Revenue": daily_rev, "Units": daily_units})

    # Funnel
    funnel = pd.DataFrame({
        "Stage":  ["Leads","Qualified","Proposal","Negotiation","Closed Won"],
        "Count":  [5400, 3100, 1760, 980, 512],
        "Value":  [21600,12400,8800, 4900, 2560],
    })

    return {
        "months":      months,
        "rev_2023":    rev_2023,
        "rev_2024":    rev_2024,
        "region":      region_data,
        "category":    cat_data,
        "products":    prod_data,
        "reps":        rep_data,
        "daily":       daily_df,
        "funnel":      funnel,
    }


data = generate_sales_data()


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding-bottom:1.2rem;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1rem;">
        <div style="width:36px;height:36px;background:#00e676;border-radius:9px;display:flex;align-items:center;justify-content:center;">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#07090f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 16l4-4 4 4 4-4"/></svg>
        </div>
        <div style="font-family:'Clash Display',sans-serif;font-weight:700;font-size:1rem;color:#e8edf8;line-height:1.2;">
            Sales<span style="color:#00e676;">IQ</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Display Options</div>', unsafe_allow_html=True)

    year_compare = st.toggle("Show 2023 Comparison", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Period</div>', unsafe_allow_html=True)
    period = st.selectbox("Time Range", ["Full Year", "H1 (Jan-Jun)", "H2 (Jul-Dec)", "Q4"])

    period_slice = {
        "Full Year":    slice(0, 12),
        "H1 (Jan-Jun)": slice(0, 6),
        "H2 (Jul-Dec)": slice(6, 12),
        "Q4":           slice(9, 12),
    }[period]

    months_sliced = data["months"][period_slice]
    rev_24 = data["rev_2024"][period_slice]
    rev_23 = data["rev_2023"][period_slice]

    st.markdown("""
    <br>
    <div style="background:rgba(0,230,118,0.06);border:1px solid rgba(0,230,118,0.14);
                border-radius:10px;padding:0.7rem 1rem;font-family:'JetBrains Mono',monospace;
                font-size:0.65rem;color:#00e676;">
        <span style="display:inline-block;width:7px;height:7px;background:#00e676;
                     border-radius:50%;margin-right:6px;animation:pulse 1.5s infinite;"></span>
        Sample Data Mode
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
st.markdown(f"""
<div class="hero-banner">
    <p class="hero-sub">Sales Intelligence Platform</p>
    <h1 class="hero-title">Sales <span class="hero-accent">Dashboard</span></h1>
    <p style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;letter-spacing:2px;
              color:#4d5a78;margin-top:0.5rem;">{period.upper()} &bull; {now_str}</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  KPI STRIP
# ─────────────────────────────────────────────
total_rev_24 = sum(rev_24)
total_rev_23 = sum(rev_23)
rev_growth   = ((total_rev_24 - total_rev_23) / total_rev_23) * 100
total_units  = data["products"]["Units"].sum()
avg_margin   = data["products"]["Margin_Pct"].mean()
total_deals  = data["reps"]["Deals"].sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue",   f"${total_rev_24:,}K",     f"+{rev_growth:.1f}% vs 2023")
k2.metric("Units Sold",       f"{total_units:,}",        "+11.2% vs 2023")
k3.metric("Avg Gross Margin", f"{avg_margin:.1f}%",      "+3.4pp vs 2023")
k4.metric("Deals Closed",     f"{total_deals}",          "+18 vs 2023")

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TOP PRODUCTS SHOWCASE
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">🚀 Top 5 Products Performance</div>', unsafe_allow_html=True)

top5_products = data["products"].nlargest(5, "Revenue")[["Product", "Revenue", "Units", "Margin_Pct", "Category", "MoM_Pct", "Icon"]].copy()

pc1, pc2, pc3, pc4, pc5 = st.columns(5, gap="small")
product_cols = [pc1, pc2, pc3, pc4, pc5]

for idx, (col, (_, prod)) in enumerate(zip(product_cols, top5_products.iterrows())):
    mom_color = "#00e676" if prod["MoM_Pct"] >= 0 else "#ff4560"
    mom_sign = "+" if prod["MoM_Pct"] >= 0 else ""
    gradient_color = '0,230,118' if idx % 2 == 0 else '41,121,255'
    
    with col:
        st.markdown(f"""
        <div class="product-card" style="background: linear-gradient(135deg, rgba({gradient_color},0.08) 0%, rgba(255,179,0,0.04) 100%);
                    border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1.2rem 1rem;
                    text-align: center;">
            <div class="product-icon">
                {prod['Icon']}
            </div>
            <div style="font-family: 'Clash Display', sans-serif; font-size: 0.9rem; font-weight: 700; color: #e8edf8; margin-bottom: 0.5rem;">
                {prod['Product']}
            </div>
            <div style="font-size: 0.65rem; color: #4d5a78; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.8rem;">
                {prod['Category']}
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 0.8rem;">
                <div class="product-revenue" style="font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: #00e676; font-weight: 700; margin-bottom: 0.3rem;">
                    ${prod['Revenue']}K
                </div>
                <div style="font-size: 0.65rem; color: #4d5a78; margin-bottom: 0.4rem;">Revenue</div>
                <div style="display: flex; justify-content: space-around; font-size: 0.7rem; color: #4d5a78;">
                    <span>{int(prod['Units']/1000)}K Units</span>
                    <span>{int(prod['Margin_Pct'])}% Margin</span>
                </div>
                <div style="margin-top: 0.6rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: {mom_color}; font-weight: 700;">
                    MoM: {mom_sign}{prod['MoM_Pct']}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="section-label">Animated Product Videos</div>', unsafe_allow_html=True)

api_key = st.secrets.get("YOUTUBE_API_KEY", os.getenv("YOUTUBE_API_KEY"))
if not api_key:
    st.warning("Set YOUTUBE_API_KEY in Streamlit secrets or environment variables to enable live YouTube video previews.")

video_queries = [
    ("Mobile Product Launch", "mobile product launch demo"),
    ("Wearable Product Tour", "wearable product tour demo"),
    ("SaaS Product Demo", "saas product demo"),
]

video_urls = []
for title, query in video_queries:
    url = fetch_youtube_video_url(query, api_key)
    if url is None:
        url = "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
    video_urls.append((title, url))

v1, v2, v3 = st.columns(3, gap="large")
for col, (title, url) in zip((v1, v2, v3), video_urls):
    with col:
        st.markdown(f'<div style="font-family:\'JetBrains Mono\', monospace; color:#4d5a78; font-size:0.72rem; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:0.6rem;">{title}</div>', unsafe_allow_html=True)
        st.video(url)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
t1, t2, t3, t4, t5 = st.tabs(["REVENUE TRENDS","REGION ANALYSIS","PRODUCT MIX","SALES TEAM","PIPELINE"])


# ── TAB 1: REVENUE TRENDS ────────────────────
with t1:
    st.markdown("<br>", unsafe_allow_html=True)

    # Main line chart
    fig_line = go.Figure()
    if year_compare:
        fig_line.add_trace(go.Scatter(
            x=months_sliced, y=rev_23, name="2023",
            line=dict(color="#2979ff", width=2, dash="dot"),
            mode="lines+markers", marker=dict(size=5),
            fill="tozeroy", fillcolor="rgba(41,121,255,0.05)",
        ))
    fig_line.add_trace(go.Scatter(
        x=months_sliced, y=rev_24, name="2024",
        line=dict(color="#00e676", width=2.5),
        mode="lines+markers", marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(0,230,118,0.08)",
    ))
    fig_line.update_layout(
        **PLOTLY_BASE, height=300,
        title=None,
        xaxis=dict(showgrid=False, linecolor="rgba(255,255,255,0.06)", tickfont=dict(size=9)),
        yaxis=dict(tickprefix="$", ticksuffix="K",
                   gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(0,0,0,0)",
                   tickfont=dict(size=9)),
    )
    st.markdown('<div class="section-label">Monthly Revenue Trend</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_line, use_container_width=True)

    # Row: bar chart + waterfall
    c1, c2 = st.columns([1.2, 1], gap="large")

    with c1:
        st.markdown('<div class="section-label">Monthly Delta vs Prior Year</div>', unsafe_allow_html=True)
        deltas = [a - b for a, b in zip(rev_24, rev_23)]
        colors_bar = ["#00e676" if d >= 0 else "#ff4560" for d in deltas]
        fig_bar_delta = go.Figure(go.Bar(
            x=months_sliced, y=deltas,
            marker_color=colors_bar,
            marker_line_width=0,
        ))
        fig_bar_delta.update_layout(**PLOTLY_BASE, height=240,
            xaxis=dict(showgrid=False, linecolor="rgba(255,255,255,0.06)", tickfont=dict(size=9)),
            yaxis=dict(tickprefix="$", ticksuffix="K",
                       gridcolor="rgba(255,255,255,0.04)",
                       linecolor="rgba(0,0,0,0)", tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_bar_delta, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">Daily Revenue (Last 90 Days)</div>', unsafe_allow_html=True)
        fig_area = go.Figure(go.Scatter(
            x=data["daily"]["Date"],
            y=data["daily"]["Revenue"].rolling(7).mean(),
            fill="tozeroy",
            fillcolor="rgba(0,229,255,0.08)",
            line=dict(color="#00e5ff", width=1.5),
            name="7-day avg",
        ))
        fig_area.update_layout(**PLOTLY_BASE, height=240,
            xaxis=dict(showgrid=False, linecolor="rgba(255,255,255,0.06)", tickfont=dict(size=9)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(0,0,0,0)",
                       ticksuffix="K", tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_area, use_container_width=True)


# ── TAB 2: REGION ANALYSIS ───────────────────
with t2:
    st.markdown("<br>", unsafe_allow_html=True)
    rdf = data["region"]

    c1, c2 = st.columns([1.3, 1], gap="large")

    with c1:
        st.markdown('<div class="section-label">Revenue by Region — 2024 vs 2023</div>', unsafe_allow_html=True)
        fig_reg = go.Figure()
        fig_reg.add_trace(go.Bar(
            y=rdf["Region"], x=rdf["Revenue_2023"],
            name="2023", orientation="h",
            marker_color="rgba(41,121,255,0.45)",
            marker_line_width=0,
        ))
        fig_reg.add_trace(go.Bar(
            y=rdf["Region"], x=rdf["Revenue_2024"],
            name="2024", orientation="h",
            marker_color="#00e676",
            marker_line_width=0,
        ))
        fig_reg.update_layout(
            **PLOTLY_BASE, height=300, barmode="group",
            xaxis=dict(showgrid=False, tickprefix="$", ticksuffix="K", tickfont=dict(size=9)),
            yaxis=dict(showgrid=False, tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">Target Achievement</div>', unsafe_allow_html=True)
        fig_ach = go.Figure(go.Bar(
            x=rdf["Achievement"],
            y=rdf["Region"],
            orientation="h",
            marker=dict(
                color=rdf["Achievement"],
                colorscale=[[0,"#ff4560"],[0.5,"#ffb300"],[1,"#00e676"]],
                cmin=40, cmax=100,
                line_width=0,
            ),
            text=[f"{v}%" for v in rdf["Achievement"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=9, color="#4d5a78"),
        ))
        fig_ach.add_vline(x=100, line_dash="dot", line_color="rgba(255,255,255,0.15)", line_width=1)
        fig_ach.update_layout(
            **PLOTLY_BASE, height=300,
            xaxis=dict(showgrid=False, ticksuffix="%", range=[0,115], tickfont=dict(size=9)),
            yaxis=dict(showgrid=False, tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_ach, use_container_width=True)

    # Map-like treemap
    st.markdown('<div class="section-label">Revenue Treemap by Region</div>', unsafe_allow_html=True)
    fig_tree = px.treemap(
        rdf, path=["Region"], values="Revenue_2024",
        color="Achievement",
        color_continuous_scale=["#ff4560","#ffb300","#00e676"],
        range_color=[40, 100],
    )
    fig_tree.update_traces(
        textfont=dict(family="Clash Display", color="white", size=14),
        texttemplate="<b>%{label}</b><br>$%{value}K",
        hovertemplate="<b>%{label}</b><br>Revenue: $%{value}K<extra></extra>",
    )
    fig_tree.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono", color="#4d5a78", size=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#4d5a78", size=10),
            orientation="h",
            yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        hoverlabel=dict(
            bgcolor="#0d1017",
            bordercolor="rgba(255,255,255,0.08)",
            font=dict(family="JetBrains Mono", color="#e8edf8", size=11),
        ),
        height=260,
        coloraxis_showscale=False,
        margin=dict(t=0, b=0, l=0, r=0),
    )
    st.plotly_chart(fig_tree, use_container_width=True)

    # Region table
    with st.expander("Region Detail Table"):
        display = rdf.copy()
        display["Revenue_2024"] = display["Revenue_2024"].apply(lambda x: f"${x:,}K")
        display["Revenue_2023"] = display["Revenue_2023"].apply(lambda x: f"${x:,}K")
        display["Target"]       = display["Target"].apply(lambda x: f"${x:,}K")
        display["Achievement"]  = display["Achievement"].apply(lambda x: f"{x}%")
        st.dataframe(display, use_container_width=True, hide_index=True)


# ── TAB 3: PRODUCT MIX ───────────────────────
with t3:
    st.markdown("<br>", unsafe_allow_html=True)
    pdf = data["products"].copy()
    cdf = data["category"].copy()

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown('<div class="section-label">Revenue by Category</div>', unsafe_allow_html=True)
        fig_donut = go.Figure(go.Pie(
            labels=cdf["Category"], values=cdf["Revenue"],
            hole=0.65,
            marker=dict(colors=ACCENT[:5], line=dict(color="#07090f", width=3)),
            textfont=dict(family="JetBrains Mono", size=10, color="#4d5a78"),
            hovertemplate="<b>%{label}</b><br>$%{value}K<br>%{percent}<extra></extra>",
        ))
        fig_donut.update_layout(**PLOTLY_BASE, height=300)
        st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">Margin by Category</div>', unsafe_allow_html=True)
        fig_margin = go.Figure(go.Bar(
            x=cdf["Category"], y=cdf["Margin"],
            marker=dict(
                color=cdf["Margin"],
                colorscale=[[0,"rgba(255,69,96,0.7)"],[0.5,"rgba(255,179,0,0.8)"],[1,"rgba(0,230,118,0.85)"]],
                cmin=25, cmax=70, line_width=0,
            ),
            text=[f"{v}%" for v in cdf["Margin"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=10, color="#4d5a78"),
        ))
        fig_margin.add_hline(y=40, line_dash="dot", line_color="rgba(255,255,255,0.12)", line_width=1)
        fig_margin.update_layout(
            **PLOTLY_BASE, height=300,
            xaxis=dict(showgrid=False, tickfont=dict(size=9)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)", ticksuffix="%",
                       linecolor="rgba(0,0,0,0)", tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_margin, use_container_width=True)

    # Bubble: Revenue vs Margin vs Units
    st.markdown('<div class="section-label">Revenue vs Margin vs Units (Bubble Size)</div>', unsafe_allow_html=True)
    fig_bubble = px.scatter(
        pdf,
        x="Revenue", y="Margin_Pct",
        size="Units", color="Category",
        hover_name="Product",
        color_discrete_sequence=ACCENT,
        size_max=50,
        labels={"Revenue":"Revenue ($K)", "Margin_Pct":"Gross Margin (%)"},
    )
    fig_bubble.update_traces(
        marker=dict(line=dict(width=1, color="rgba(0,0,0,0.3)")),
        hovertemplate="<b>%{hovertext}</b><br>Revenue: $%{x}K<br>Margin: %{y}%<extra></extra>",
    )
    fig_bubble.update_layout(
        **PLOTLY_BASE, height=280,
        xaxis=dict(showgrid=False, tickprefix="$", ticksuffix="K", tickfont=dict(size=9)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", ticksuffix="%",
                   linecolor="rgba(0,0,0,0)", tickfont=dict(size=9)),
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

    # Product Rankings
    st.markdown('<div class="section-label">Product Rankings & Performance</div>', unsafe_allow_html=True)
    
    # Create product ranking tabs
    rank_col1, rank_col2 = st.columns(2, gap="large")
    
    with rank_col1:
        # Top Products by Revenue
        top_revenue = pdf.nlargest(7, "Revenue")[["Product", "Revenue"]].reset_index(drop=True)
        fig_rank_rev = go.Figure(go.Bar(
            y=top_revenue["Product"],
            x=top_revenue["Revenue"],
            orientation="h",
            marker=dict(
                color=top_revenue["Revenue"],
                colorscale=["#ff4560", "#ffb300", "#00e676"],
                cmin=top_revenue["Revenue"].min(),
                cmax=top_revenue["Revenue"].max(),
                line_width=0
            ),
            text=[f"${v}K" for v in top_revenue["Revenue"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=9, color="#4d5a78"),
        ))
        fig_rank_rev.update_layout(
            **PLOTLY_BASE, height=280,
            xaxis=dict(showgrid=False, tickprefix="$", ticksuffix="K", tickfont=dict(size=9)),
            yaxis=dict(showgrid=False, tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_rank_rev, use_container_width=True)
    
    with rank_col2:
        # Top Products by Margin
        top_margin = pdf.nlargest(7, "Margin_Pct")[["Product", "Margin_Pct"]].reset_index(drop=True)
        fig_rank_margin = go.Figure(go.Bar(
            y=top_margin["Product"],
            x=top_margin["Margin_Pct"],
            orientation="h",
            marker=dict(
                color=top_margin["Margin_Pct"],
                colorscale=[[0,"#ff4560"],[0.5,"#ffb300"],[1,"#00e676"]],
                cmin=20, cmax=70,
                line_width=0
            ),
            text=[f"{int(v)}%" for v in top_margin["Margin_Pct"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=9, color="#4d5a78"),
        ))
        fig_rank_margin.update_layout(
            **PLOTLY_BASE, height=280,
            xaxis=dict(showgrid=False, ticksuffix="%", tickfont=dict(size=9)),
            yaxis=dict(showgrid=False, tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_rank_margin, use_container_width=True)

    # Product table
    st.markdown('<div class="section-label">Product Leaderboard</div>', unsafe_allow_html=True)
    pt = pdf.copy()
    pt["Revenue"] = pt["Revenue"].apply(lambda x: f"${x:,}K")
    pt["Units"]   = pt["Units"].apply(lambda x: f"{x:,}")
    pt["MoM"]     = pt["MoM_Pct"].apply(lambda x: f"+{x}%" if x >= 0 else f"{x}%")
    pt["Margin"]  = pt["Margin_Pct"].apply(lambda x: f"{x}%")
    
    display_pt = pt[["Product","Category","Revenue","Units","Margin","MoM"]].copy()
    styled_df = display_pt.style.map(
        lambda v: "color: #00e676" if "+" in str(v) and "%" in str(v) else
                  "color: #ff4560" if "-" in str(v) and "%" in str(v) else "",
        subset=["MoM"]
    )
    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=300)


# ── TAB 4: SALES TEAM ────────────────────────
with t4:
    st.markdown("<br>", unsafe_allow_html=True)
    reps = data["reps"].copy()

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown('<div class="section-label">Rep Revenue Performance</div>', unsafe_allow_html=True)
        fig_rep = go.Figure(go.Bar(
            x=reps["Rep"], y=reps["Revenue"],
            marker=dict(
                color=reps["Quota_Pct"],
                colorscale=[[0,"#ff4560"],[0.7,"#ffb300"],[1,"#00e676"]],
                cmin=60, cmax=120, line_width=0,
            ),
            text=[f"${v}K" for v in reps["Revenue"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=9, color="#4d5a78"),
        ))
        fig_rep.update_layout(
            **PLOTLY_BASE, height=280,
            xaxis=dict(showgrid=False, tickfont=dict(size=9), tickangle=-20),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickprefix="$",
                       ticksuffix="K", linecolor="rgba(0,0,0,0)", tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_rep, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">Win Rate vs Quota Achievement</div>', unsafe_allow_html=True)
        fig_scatter_rep = px.scatter(
            reps, x="Win_Rate", y="Quota_Pct",
            color="Region", size="Deals", hover_name="Rep",
            color_discrete_sequence=ACCENT,
            labels={"Win_Rate":"Win Rate (%)","Quota_Pct":"Quota Achieved (%)"},
            size_max=22,
        )
        fig_scatter_rep.add_hline(y=100, line_dash="dot", line_color="rgba(0,230,118,0.25)")
        fig_scatter_rep.update_layout(
            **PLOTLY_BASE, height=280,
            xaxis=dict(showgrid=False, ticksuffix="%", tickfont=dict(size=9)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)", ticksuffix="%",
                       linecolor="rgba(0,0,0,0)", tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_scatter_rep, use_container_width=True)

    # Radar: team performance
    st.markdown('<div class="section-label">Team Performance Radar</div>', unsafe_allow_html=True)
    radar_cats = ["Revenue", "Deals", "Win Rate", "Quota", "Avg Deal Size"]
    fig_radar = go.Figure()
    for i, (_, row) in enumerate(reps.iterrows()):
        norm = [
            row["Revenue"] / reps["Revenue"].max() * 100,
            row["Deals"] / reps["Deals"].max() * 100,
            row["Win_Rate"],
            min(row["Quota_Pct"], 100),
            (row["Revenue"] / row["Deals"]) / (reps["Revenue"] / reps["Deals"]).max() * 100,
        ]
        fig_radar.add_trace(go.Scatterpolar(
            r=norm + [norm[0]],
            theta=radar_cats + [radar_cats[0]],
            name=row["Rep"].split()[0],
            line=dict(color=ACCENT[i % len(ACCENT)], width=1.5),
            fill="toself",
            fillcolor=f"rgba({int(ACCENT[i%len(ACCENT)][1:3],16)},{int(ACCENT[i%len(ACCENT)][3:5],16)},{int(ACCENT[i%len(ACCENT)][5:7],16)},0.04)",
        ))
    fig_radar.update_layout(
        **PLOTLY_BASE, height=320,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,100], gridcolor="rgba(255,255,255,0.06)",
                            tickfont=dict(size=8), color="#4d5a78"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", color="#4d5a78",
                             tickfont=dict(size=9)),
        ),
    )
    st.plotly_chart(fig_radar, use_container_width=True)


# ── TAB 5: PIPELINE ──────────────────────────
with t5:
    st.markdown("<br>", unsafe_allow_html=True)
    fdf = data["funnel"]

    c1, c2 = st.columns([1.2, 1], gap="large")

    with c1:
        st.markdown('<div class="section-label">Sales Funnel</div>', unsafe_allow_html=True)
        fig_funnel = go.Figure(go.Funnel(
            y=fdf["Stage"],
            x=fdf["Count"],
            textinfo="value+percent total",
            marker=dict(
                color=ACCENT[:5],
                line=dict(width=1, color="#07090f"),
            ),
            connector=dict(line=dict(color="rgba(255,255,255,0.04)", width=1)),
            textfont=dict(family="JetBrains Mono", size=10, color="#e8edf8"),
        ))
        fig_funnel.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="JetBrains Mono", color="#4d5a78", size=10),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color="#4d5a78", size=10),
                orientation="h",
                yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            hoverlabel=dict(
                bgcolor="#0d1017",
                bordercolor="rgba(255,255,255,0.08)",
                font=dict(family="JetBrains Mono", color="#e8edf8", size=11),
            ),
            height=320,
            margin=dict(t=10,b=10,l=60,r=10)
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">Pipeline Value by Stage ($K)</div>', unsafe_allow_html=True)
        fig_pipe = go.Figure(go.Bar(
            x=fdf["Stage"], y=fdf["Value"],
            marker=dict(color=ACCENT[:5], line_width=0),
            text=[f"${v:,}K" for v in fdf["Value"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=9, color="#4d5a78"),
        ))
        fig_pipe.update_layout(
            **PLOTLY_BASE, height=320,
            xaxis=dict(showgrid=False, tickfont=dict(size=9)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickprefix="$",
                       ticksuffix="K", linecolor="rgba(0,0,0,0)", tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_pipe, use_container_width=True)

    # Funnel conversion rates
    st.markdown('<div class="section-label">Stage Conversion Rates</div>', unsafe_allow_html=True)
    for i in range(len(fdf)-1):
        rate = fdf["Count"].iloc[i+1] / fdf["Count"].iloc[i] * 100
        from_s, to_s = fdf["Stage"].iloc[i], fdf["Stage"].iloc[i+1]
        color = "#00e676" if rate >= 50 else "#ffb300" if rate >= 40 else "#ff4560"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
            <div style="font-size:0.8rem;color:#e8edf8;width:200px;white-space:nowrap;">{from_s} → {to_s}</div>
            <div style="flex:1;height:6px;background:rgba(255,255,255,0.05);border-radius:3px;overflow:hidden;">
                <div style="height:100%;width:{rate}%;background:{color};border-radius:3px;"></div>
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:{color};width:50px;text-align:right;">{rate:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    overall = fdf["Count"].iloc[-1] / fdf["Count"].iloc[0] * 100
    st.markdown(f"""
    <div style="background:rgba(0,230,118,0.06);border:1px solid rgba(0,230,118,0.14);
                border-radius:10px;padding:0.75rem 1rem;margin-top:0.5rem;
                font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#00e676;">
        Overall Lead-to-Close Rate: <b>{overall:.1f}%</b>
        &bull; Avg Deal Size: <b>${int(fdf["Value"].iloc[-1] / fdf["Count"].iloc[-1]):,}K</b>
    </div>
    """, unsafe_allow_html=True)
