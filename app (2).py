"""
MZ Generation Pop-up Store & Cultural Space Consumption Trend Map — Seoul 2024
Run:
    pip install streamlit plotly folium streamlit-folium pandas numpy scipy
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from collections import Counter

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MZ Pop-up Store Trend Map | Seoul 2024",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background: #0f0f14; }
    .block-container { padding: 1.5rem 2rem 3rem 2rem; }

    .hero-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px; padding: 2.5rem 3rem; margin-bottom: 2rem;
        border: 1px solid rgba(255,180,50,0.2); position: relative; overflow: hidden;
    }
    .hero-header::before {
        content: ''; position: absolute; top: -50%; right: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(255,180,50,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title { font-size: 2rem; font-weight: 700; color: #fff; margin: 0 0 0.4rem 0; letter-spacing: -0.02em; }
    .hero-sub   { font-size: 1rem; color: rgba(255,255,255,0.6); margin: 0; font-weight: 300; }
    .hero-badge {
        display: inline-block;
        background: rgba(255,180,50,0.15); border: 1px solid rgba(255,180,50,0.4);
        color: #ffb432; font-size: 0.75rem; font-weight: 500;
        padding: 0.25rem 0.8rem; border-radius: 20px; margin-bottom: 1rem; letter-spacing: 0.05em;
    }
    .metric-card {
        background: #1a1a2e; border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px; padding: 1.2rem 1.5rem; text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #ffb432; line-height: 1; margin-bottom: 0.3rem; }
    .metric-label { font-size: 0.78rem; color: rgba(255,255,255,0.5); font-weight: 400; }
    .metric-delta { font-size: 0.8rem; color: #4ade80; margin-top: 0.2rem; }

    .section-title {
        font-size: 1.1rem; font-weight: 600; color: #fff; margin: 0 0 1rem 0;
        padding-bottom: 0.5rem; border-bottom: 2px solid #ffb432; display: inline-block;
    }
    [data-testid="stSidebar"] { background: #13131f; border-right: 1px solid rgba(255,255,255,0.06); }
    [data-testid="stSidebar"] .block-container { padding: 1rem; }

    .stTabs [data-baseweb="tab-list"] { background: #1a1a2e; border-radius: 10px; padding: 4px; gap: 4px; }
    .stTabs [data-baseweb="tab"]      { border-radius: 8px; color: rgba(255,255,255,0.5); font-size: 0.88rem; }
    .stTabs [aria-selected="true"]    { background: #ffb432 !important; color: #000 !important; font-weight: 600; }

    .tag-chip {
        display: inline-block; background: rgba(255,180,50,0.1); border: 1px solid rgba(255,180,50,0.3);
        color: #ffb432; font-size: 0.72rem; padding: 0.2rem 0.6rem; border-radius: 20px; margin: 2px;
    }
    .info-card {
        background: #1a1a2e; border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.8rem;
    }
    .info-card-title { font-size: 0.95rem; font-weight: 600; color: #fff; margin-bottom: 0.3rem; }
    .info-card-sub   { font-size: 0.8rem; color: rgba(255,255,255,0.45); }
    .js-plotly-plot  { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME HELPER  (fixes the ValueError)
# ─────────────────────────────────────────────
def apply_theme(fig, height=380):
    """Apply consistent dark theme to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,26,46,0.8)",
        font=dict(color="#ffffff", family="Inter, sans-serif"),
        height=height,
        margin=dict(l=10, r=10, t=20, b=20),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)", color="#ffffff", zerolinecolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", color="#ffffff", zerolinecolor="rgba(255,255,255,0.1)")
    return fig

GRID = "rgba(255,255,255,0.08)"

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_popup_data():
    data = [
        # Seongsu-dong
        {"name": "Nike Air Max Pop-up",        "district": "Seongsu-dong", "gu": "Seongdong-gu", "lat": 37.5445, "lng": 127.0557,
         "category": "Fashion & Sports",  "brand": "Nike",          "period": "2024-03", "visitors": 12400,
         "instagram_tags": 28000, "satisfaction": 4.6, "age_mz_ratio": 88, "price_range": "Free",
         "keywords": ["Limited Ed.", "Photo Spot", "Resell"], "open_days": 14},
        {"name": "Musinsa Standard Pop-up",    "district": "Seongsu-dong", "gu": "Seongdong-gu", "lat": 37.5438, "lng": 127.0561,
         "category": "Fashion & Sports",  "brand": "Musinsa",       "period": "2024-04", "visitors": 19200,
         "instagram_tags": 41000, "satisfaction": 4.5, "age_mz_ratio": 92, "price_range": "Free",
         "keywords": ["Streetwear", "Daily Look", "Discount"], "open_days": 21},
        {"name": "Kakao Friends Pop-up",       "district": "Seongsu-dong", "gu": "Seongdong-gu", "lat": 37.5441, "lng": 127.0548,
         "category": "Character & IP",    "brand": "Kakao",         "period": "2024-05", "visitors": 22000,
         "instagram_tags": 55000, "satisfaction": 4.7, "age_mz_ratio": 85, "price_range": "Free",
         "keywords": ["Character", "Goods", "Photo Booth"], "open_days": 30},
        {"name": "Gentle Monster House Dosan", "district": "Seongsu-dong", "gu": "Seongdong-gu", "lat": 37.5452, "lng": 127.0553,
         "category": "Lifestyle & Beauty", "brand": "Gentle Monster","period": "2024-02", "visitors": 9800,
         "instagram_tags": 32000, "satisfaction": 4.8, "age_mz_ratio": 91, "price_range": "Free",
         "keywords": ["Art", "Instagrammable", "Luxury"], "open_days": 21},
        # Hongdae
        {"name": "Apple Music × IVE Pop-up",  "district": "Hongdae",      "gu": "Mapo-gu",      "lat": 37.5563, "lng": 126.9243,
         "category": "Music & Entertainment","brand": "Apple Music",  "period": "2024-03", "visitors": 31000,
         "instagram_tags": 78000, "satisfaction": 4.7, "age_mz_ratio": 95, "price_range": "Free",
         "keywords": ["K-pop", "Idol", "Limited Goods"], "open_days": 7},
        {"name": "Olive Young Beauty Festa",   "district": "Hongdae",      "gu": "Mapo-gu",      "lat": 37.5551, "lng": 126.9238,
         "category": "Lifestyle & Beauty", "brand": "Olive Young",   "period": "2024-06", "visitors": 25600,
         "instagram_tags": 49000, "satisfaction": 4.4, "age_mz_ratio": 89, "price_range": "Free",
         "keywords": ["Beauty", "Samples", "Experience"], "open_days": 10},
        {"name": "Burberry Pop-up Store",      "district": "Hongdae",      "gu": "Mapo-gu",      "lat": 37.5568, "lng": 126.9255,
         "category": "Fashion & Sports",  "brand": "Burberry",      "period": "2024-01", "visitors": 7600,
         "instagram_tags": 22000, "satisfaction": 4.5, "age_mz_ratio": 78, "price_range": "Paid (₩50,000+)",
         "keywords": ["Luxury", "Limited Ed.", "British"], "open_days": 14},
        # Gangnam / Dosan
        {"name": "Gucci Garden Pop-up",        "district": "Dosan Park",   "gu": "Gangnam-gu",   "lat": 37.5248, "lng": 127.0336,
         "category": "Fashion & Sports",  "brand": "Gucci",         "period": "2024-05", "visitors": 14500,
         "instagram_tags": 61000, "satisfaction": 4.9, "age_mz_ratio": 82, "price_range": "Free",
         "keywords": ["Luxury", "Art", "Flagship"], "open_days": 21},
        {"name": "Dior Beauty Pop-up",         "district": "Dosan Park",   "gu": "Gangnam-gu",   "lat": 37.5245, "lng": 127.0329,
         "category": "Lifestyle & Beauty", "brand": "Dior",          "period": "2024-04", "visitors": 11200,
         "instagram_tags": 47000, "satisfaction": 4.8, "age_mz_ratio": 80, "price_range": "Free",
         "keywords": ["Beauty", "Perfume", "French"], "open_days": 14},
        {"name": "Naver Webtoon Pop-up",       "district": "Gangnam Station","gu": "Gangnam-gu",  "lat": 37.4979, "lng": 127.0277,
         "category": "Character & IP",    "brand": "Naver Webtoon", "period": "2024-07", "visitors": 18700,
         "instagram_tags": 38000, "satisfaction": 4.5, "age_mz_ratio": 90, "price_range": "Free",
         "keywords": ["Webtoon", "Character", "Goods"], "open_days": 21},
        # Yeouido / The Hyundai
        {"name": "The Hyundai MZ Pop-up Zone", "district": "Yeouido",      "gu": "Yeongdeungpo-gu","lat": 37.5219,"lng": 126.9240,
         "category": "F&B",                "brand": "Hyundai Dept.", "period": "2024-06", "visitors": 42000,
         "instagram_tags": 88000, "satisfaction": 4.6, "age_mz_ratio": 87, "price_range": "Free",
         "keywords": ["Department", "F&B", "Trend"], "open_days": 30},
        {"name": "Pokémon Pop-up Store",       "district": "Yeouido",      "gu": "Yeongdeungpo-gu","lat": 37.5215,"lng": 126.9235,
         "category": "Character & IP",    "brand": "Pokémon",       "period": "2024-08", "visitors": 38500,
         "instagram_tags": 95000, "satisfaction": 4.8, "age_mz_ratio": 88, "price_range": "Free",
         "keywords": ["Character", "IP", "Limited Ed."], "open_days": 21},
        # Hannam-dong
        {"name": "LE SSERAFIM Fan Pop-up",     "district": "Hannam-dong",  "gu": "Yongsan-gu",   "lat": 37.5340, "lng": 126.9978,
         "category": "Music & Entertainment","brand": "LE SSERAFIM", "period": "2024-02", "visitors": 29000,
         "instagram_tags": 112000, "satisfaction": 4.9, "age_mz_ratio": 96, "price_range": "Paid (₩30,000)",
         "keywords": ["K-pop", "Fandom", "Goods"], "open_days": 7},
        {"name": "Patagonia Pop-up",           "district": "Hannam-dong",  "gu": "Yongsan-gu",   "lat": 37.5335, "lng": 126.9985,
         "category": "Fashion & Sports",  "brand": "Patagonia",     "period": "2024-09", "visitors": 6800,
         "instagram_tags": 15000, "satisfaction": 4.4, "age_mz_ratio": 82, "price_range": "Free",
         "keywords": ["Sustainable", "Outdoor", "Eco"], "open_days": 14},
        # Insadong
        {"name": "Samsung Galaxy AI Experience","district": "Insadong",     "gu": "Jongno-gu",    "lat": 37.5741, "lng": 126.9838,
         "category": "Tech & Electronics", "brand": "Samsung",       "period": "2024-07", "visitors": 24300,
         "instagram_tags": 42000, "satisfaction": 4.5, "age_mz_ratio": 85, "price_range": "Free",
         "keywords": ["AI", "Galaxy", "Tech"], "open_days": 30},
        {"name": "LG OLED Art Pop-up",         "district": "Insadong",     "gu": "Jongno-gu",    "lat": 37.5736, "lng": 126.9843,
         "category": "Tech & Electronics", "brand": "LG",            "period": "2024-08", "visitors": 11400,
         "instagram_tags": 22000, "satisfaction": 4.3, "age_mz_ratio": 77, "price_range": "Free",
         "keywords": ["Display", "Art", "Interior"], "open_days": 21},
        # Jamsil
        {"name": "Rolls-Royce Art Pop-up",     "district": "Jamsil",       "gu": "Songpa-gu",    "lat": 37.5133, "lng": 127.1028,
         "category": "Fashion & Sports",  "brand": "Rolls-Royce",   "period": "2024-10", "visitors": 5600,
         "instagram_tags": 18000, "satisfaction": 4.7, "age_mz_ratio": 70, "price_range": "Free",
         "keywords": ["Luxury", "Supercar", "Art"], "open_days": 10},
        {"name": "HYBE Artist Pop-up",         "district": "Jamsil",       "gu": "Songpa-gu",    "lat": 37.5128, "lng": 127.1022,
         "category": "Music & Entertainment","brand": "HYBE",        "period": "2024-11", "visitors": 45000,
         "instagram_tags": 135000, "satisfaction": 4.9, "age_mz_ratio": 97, "price_range": "Paid (₩25,000)",
         "keywords": ["K-pop", "BTS", "ARMY"], "open_days": 14},
        # Myeongdong
        {"name": "Coca-Cola Y2K Pop-up",       "district": "Myeongdong",   "gu": "Jung-gu",      "lat": 37.5633, "lng": 126.9845,
         "category": "F&B",                "brand": "Coca-Cola",     "period": "2024-05", "visitors": 16800,
         "instagram_tags": 31000, "satisfaction": 4.2, "age_mz_ratio": 86, "price_range": "Free",
         "keywords": ["Y2K", "Retro", "Experience"], "open_days": 21},
        {"name": "Starbucks The Reserve Pop-up","district": "Myeongdong",   "gu": "Jung-gu",      "lat": 37.5638, "lng": 126.9852,
         "category": "F&B",                "brand": "Starbucks",     "period": "2024-09", "visitors": 21500,
         "instagram_tags": 44000, "satisfaction": 4.4, "age_mz_ratio": 84, "price_range": "Paid (₩15,000+)",
         "keywords": ["Coffee", "Goods", "Seasonal"], "open_days": 30},
    ]
    return pd.DataFrame(data)


@st.cache_data
def load_monthly_trend():
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return pd.DataFrame({
        "Month": months,
        "Pop-up Stores": [18,22,31,28,35,42,38,44,40,33,29,25],
        "Visitors (10k)": [24,31,48,42,56,71,65,79,68,55,48,42],
        "Instagram Tags (10k)": [38,55,82,74,98,124,112,138,118,92,78,65],
    })


@st.cache_data
def load_district_stats():
    return pd.DataFrame({
        "District":         ["Seongsu-dong","Hongdae","Gangnam/Dosan","Yeouido","Hannam-dong","Insadong","Jamsil","Myeongdong"],
        "Pop-ups":          [24, 19, 22, 15, 12, 10, 8, 11],
        "Avg Visitors":     [15850, 21400, 12500, 40250, 17900, 17850, 25300, 19150],
        "MZ Ratio (%)":     [89, 87, 81, 88, 89, 81, 84, 85],
        "Avg Insta Tags":   [39000, 49667, 42000, 91500, 63500, 32000, 76500, 37500],
    })


# ── Load ──
df            = load_popup_data()
monthly       = load_monthly_trend()
district_stats = load_district_stats()

CATEGORY_COLORS = {
    "Fashion & Sports":      "#ff6b6b",
    "Lifestyle & Beauty":    "#ffd93d",
    "Music & Entertainment": "#6bcb77",
    "Character & IP":        "#4d96ff",
    "F&B":                   "#ff922b",
    "Tech & Electronics":    "#cc5de8",
}

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filters")

    selected_categories = st.multiselect(
        "Category",
        options=list(CATEGORY_COLORS.keys()),
        default=list(CATEGORY_COLORS.keys()),
    )
    selected_districts = st.multiselect(
        "District",
        options=sorted(df["district"].unique()),
        default=sorted(df["district"].unique()),
    )
    min_visitors = st.slider("Min. Visitors", 0, 50000, 0, 1000, format="%d")
    mz_ratio_min = st.slider("Min. MZ Ratio (%)", 60, 100, 70, 1)
    price_filter = st.multiselect(
        "Entry Fee",
        options=df["price_range"].unique().tolist(),
        default=df["price_range"].unique().tolist(),
    )

    st.markdown("---")
    st.markdown("#### 🗺️ Map Settings")
    map_style   = st.selectbox("Map Style", ["CartoDB dark_matter","CartoDB positron","OpenStreetMap"])
    marker_size = st.select_slider("Marker Size By", ["Visitors","Instagram Tags","MZ Ratio"], value="Visitors")

# ─────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────
mask = (
    df["category"].isin(selected_categories) &
    df["district"].isin(selected_districts) &
    (df["visitors"] >= min_visitors) &
    (df["age_mz_ratio"] >= mz_ratio_min) &
    df["price_range"].isin(price_filter)
)
filtered_df = df[mask].copy()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">📍 Seoul Pop-up Store Trend Dashboard · 2024</div>
    <h1 class="hero-title">🗺️ MZ Generation Pop-up Store &amp; Cultural Space<br>Consumption Trend Map</h1>
    <p class="hero-sub">Analysing pop-up store data across Seoul's key commercial districts to visualise MZ generation consumption trends</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
kpi_list = [
    (c1, f"{len(filtered_df)}", "Pop-up Stores", "↑12% YoY"),
    (c2, f"{filtered_df['visitors'].sum():,}", "Total Visitors", "↑34% YoY"),
    (c3, f"{int(filtered_df['age_mz_ratio'].mean())}%", "Avg MZ Ratio", "↑8%p"),
    (c4, f"{filtered_df['satisfaction'].mean():.1f}", "Avg Satisfaction", "★ out of 5.0"),
    (c5, f"{int(filtered_df['instagram_tags'].sum()/10000)}万", "Instagram Tags", "↑61% YoY"),
]
for col, val, label, delta in kpi_list:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-delta">{delta}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Interactive Map",
    "📊 Trend Analysis",
    "📍 District Analysis",
    "🏆 Rankings",
])

# ════════════════════════════════════════════
# TAB 1 — MAP
# ════════════════════════════════════════════
with tab1:
    col_map, col_info = st.columns([2, 1])

    with col_map:
        st.markdown('<p class="section-title">Seoul Pop-up Store Distribution Map</p>', unsafe_allow_html=True)

        m = folium.Map(location=[37.5350, 126.9950], zoom_start=12, tiles=map_style)

        # Legend
        legend_html = """
        <div style="position:fixed;bottom:30px;left:30px;z-index:9999;
                    background:rgba(15,15,20,0.92);padding:12px 16px;
                    border-radius:10px;border:1px solid rgba(255,255,255,0.1);
                    font-family:sans-serif;font-size:12px;color:#fff;">
            <b style="font-size:13px;">Category</b><br><br>
        """
        for cat, clr in CATEGORY_COLORS.items():
            legend_html += f'<span style="color:{clr};">●</span> {cat}<br>'
        legend_html += "</div>"
        m.get_root().html.add_child(folium.Element(legend_html))

        size_col_map = {"Visitors": "visitors", "Instagram Tags": "instagram_tags", "MZ Ratio": "age_mz_ratio"}
        size_col = size_col_map[marker_size]
        size_max = filtered_df[size_col].max() if len(filtered_df) > 0 else 1

        for _, row in filtered_df.iterrows():
            clr    = CATEGORY_COLORS.get(row["category"], "#ffffff")
            radius = 8 + (row[size_col] / size_max) * 22
            kw_html = " ".join([
                f'<span style="background:rgba(255,180,50,0.2);color:#ffb432;padding:2px 7px;border-radius:12px;font-size:11px;">{kw}</span>'
                for kw in row["keywords"]
            ])
            popup_html = f"""
            <div style="font-family:sans-serif;min-width:230px;background:#1a1a2e;color:#fff;border-radius:10px;padding:14px;">
                <div style="font-size:14px;font-weight:700;margin-bottom:4px;">{row['name']}</div>
                <div style="font-size:12px;color:#ffb432;margin-bottom:8px;">{row['district']} · {row['category']}</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;margin-bottom:10px;">
                    <div>👥 Visitors: <b>{row['visitors']:,}</b></div>
                    <div>⭐ Rating: <b>{row['satisfaction']}</b></div>
                    <div>📸 Insta: <b>{row['instagram_tags']:,}</b></div>
                    <div>🧑 MZ: <b>{row['age_mz_ratio']}%</b></div>
                    <div>💰 Entry: <b>{row['price_range']}</b></div>
                    <div>📅 Days: <b>{row['open_days']}</b></div>
                </div>
                <div>{kw_html}</div>
            </div>"""
            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=radius, color=clr, fill=True,
                fill_color=clr, fill_opacity=0.75, weight=2,
                popup=folium.Popup(popup_html, max_width=290),
                tooltip=f"📍 {row['name']} ({row['visitors']:,} visitors)",
            ).add_to(m)

        try:
            from folium.plugins import HeatMap
            heat_data = [[r["lat"], r["lng"], r["visitors"]/1000] for _, r in filtered_df.iterrows()]
            HeatMap(heat_data, radius=35, blur=25, min_opacity=0.3).add_to(m)
        except Exception:
            pass

        st_folium(m, width=None, height=520, returned_objects=[])

    with col_info:
        st.markdown('<p class="section-title">Store Info</p>', unsafe_allow_html=True)
        st.markdown(f"**{len(filtered_df)} pop-up stores** currently shown")
        st.markdown("---")

        cat_counts = filtered_df["category"].value_counts()
        for cat, cnt in cat_counts.items():
            clr = CATEGORY_COLORS.get(cat, "#aaa")
            pct = int(cnt / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;font-size:13px;color:#fff;margin-bottom:3px;">
                    <span><span style="color:{clr};">●</span> {cat}</span>
                    <span>{cnt} ({pct}%)</span>
                </div>
                <div style="background:rgba(255,255,255,0.08);border-radius:4px;height:6px;">
                    <div style="background:{clr};width:{pct}%;height:100%;border-radius:4px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**🔥 Hot Keywords**")
        all_kw = []
        for kws in filtered_df["keywords"]:
            all_kw.extend(kws)
        kw_counts = Counter(all_kw).most_common(10)
        kw_html   = "".join([f'<span class="tag-chip">{kw} ({c})</span>' for kw, c in kw_counts])
        st.markdown(f'<div style="margin-top:8px;">{kw_html}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 2 — TRENDS
# ════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title">2024 Annual Trend Overview</p>', unsafe_allow_html=True)

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(go.Bar(
        x=monthly["Month"], y=monthly["Pop-up Stores"],
        name="Pop-up Stores", marker_color="rgba(255,180,50,0.7)",
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Visitors (10k)"],
        name="Visitors (10k)", line=dict(color="#6bcb77", width=2.5),
        mode="lines+markers", marker=dict(size=7),
    ), secondary_y=True)
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Instagram Tags (10k)"],
        name="Insta Tags (10k)", line=dict(color="#4d96ff", width=2, dash="dot"),
        mode="lines+markers", marker=dict(size=6),
    ), secondary_y=True)

    apply_theme(fig_trend, height=380)
    fig_trend.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)"),
        yaxis2=dict(title="Visitors / Tags (10k)", color="#fff",
                    gridcolor="rgba(0,0,0,0)", overlaying="y", side="right"),
    )
    fig_trend.update_yaxes(title_text="No. of Pop-ups", secondary_y=False)
    st.plotly_chart(fig_trend, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="section-title">Visitors vs Satisfaction by Category</p>', unsafe_allow_html=True)
        cat_agg = filtered_df.groupby("category").agg(
            visitors=("visitors","sum"),
            satisfaction=("satisfaction","mean"),
            count=("name","count"),
        ).reset_index()
        fig_bubble = px.scatter(
            cat_agg, x="satisfaction", y="visitors",
            size="count", color="category",
            color_discrete_map=CATEGORY_COLORS, text="category", size_max=50,
            labels={"satisfaction":"Avg Rating","visitors":"Total Visitors","category":"Category"},
        )
        fig_bubble.update_traces(textposition="top center", textfont=dict(size=11))
        apply_theme(fig_bubble, height=340)
        fig_bubble.update_layout(showlegend=False, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-title">Entry Fee Mix & MZ Ratio Distribution</p>', unsafe_allow_html=True)
        fig_sub = make_subplots(
            rows=1, cols=2, specs=[[{"type":"pie"},{"type":"box"}]],
            subplot_titles=["Entry Fee Mix","MZ Ratio by Category"],
        )
        price_counts = filtered_df["price_range"].value_counts()
        fig_sub.add_trace(go.Pie(
            labels=price_counts.index, values=price_counts.values,
            hole=0.5, marker=dict(colors=["#ffb432","#ff6b6b","#4d96ff"]),
            textfont=dict(color="#fff"),
        ), row=1, col=1)
        for cat in filtered_df["category"].unique():
            sub = filtered_df[filtered_df["category"]==cat]
            fig_sub.add_trace(go.Box(
                y=sub["age_mz_ratio"], name=cat[:6],
                marker_color=CATEGORY_COLORS.get(cat,"#aaa"), showlegend=False,
            ), row=1, col=2)
        apply_theme(fig_sub, height=340)
        fig_sub.update_layout(margin=dict(l=10,r=10,t=30,b=10))
        st.plotly_chart(fig_sub, use_container_width=True)

    st.markdown('<p class="section-title">Operating Duration vs Total Visitors</p>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        filtered_df, x="open_days", y="visitors",
        color="category", size="instagram_tags",
        color_discrete_map=CATEGORY_COLORS,
        hover_data={"name":True,"district":True,"satisfaction":True},
        labels={"open_days":"Operating Days","visitors":"Total Visitors","instagram_tags":"Insta Tags"},
        trendline="ols",
    )
    apply_theme(fig_scatter, height=350)
    fig_scatter.update_layout(
        margin=dict(l=10,r=10,t=10,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ════════════════════════════════════════════
# TAB 3 — DISTRICT ANALYSIS
# ════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-title">District-Level Comparison</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(
            district_stats.sort_values("Pop-ups", ascending=True),
            x="Pop-ups", y="District", orientation="h",
            color="Pop-ups",
            color_continuous_scale=[[0,"#1a1a4e"],[0.5,"#ffb432"],[1,"#ff6b6b"]],
            labels={"Pop-ups":"Number of Pop-ups","District":""},
        )
        apply_theme(fig_bar, height=350)
        fig_bar.update_layout(coloraxis_showscale=False, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_radar = go.Figure()
        for _, row in district_stats.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[
                    row["Pop-ups"]       / district_stats["Pop-ups"].max() * 100,
                    row["Avg Visitors"]  / district_stats["Avg Visitors"].max() * 100,
                    row["MZ Ratio (%)"],
                    row["Avg Insta Tags"]/ district_stats["Avg Insta Tags"].max() * 100,
                ],
                theta=["Pop-up Count","Avg Visitors","MZ Ratio","Insta Tags"],
                fill="toself", name=row["District"], opacity=0.6,
            ))
        apply_theme(fig_radar, height=350)
        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(26,26,46,0.8)",
                radialaxis=dict(visible=True, color="#888", gridcolor="rgba(255,255,255,0.1)"),
                angularaxis=dict(color="#fff"),
            ),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
            margin=dict(l=20,r=20,t=20,b=20),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown('<p class="section-title">District Detail Table</p>', unsafe_allow_html=True)
    display_d = district_stats.copy()
    display_d["Avg Visitors"]  = display_d["Avg Visitors"].apply(lambda x: f"{x:,}")
    display_d["MZ Ratio (%)"]  = display_d["MZ Ratio (%)"].apply(lambda x: f"{x}%")
    display_d["Avg Insta Tags"]= display_d["Avg Insta Tags"].apply(lambda x: f"{x:,}")
    st.dataframe(display_d.rename(columns={
        "District":"📍 District","Pop-ups":"Pop-ups","Avg Visitors":"Avg Visitors",
        "MZ Ratio (%)":"MZ Ratio","Avg Insta Tags":"Avg Insta Tags",
    }), use_container_width=True, hide_index=True)

    st.markdown('<p class="section-title">District × Category Treemap</p>', unsafe_allow_html=True)
    if len(filtered_df) > 0:
        fig_tree = px.treemap(
            filtered_df, path=["district","category","name"], values="visitors",
            color="satisfaction",
            color_continuous_scale=[[0,"#1a1a4e"],[0.5,"#ffb432"],[1,"#ff6b6b"]],
            hover_data={"instagram_tags":True,"age_mz_ratio":True},
        )
        apply_theme(fig_tree, height=420)
        fig_tree.update_layout(margin=dict(l=0,r=0,t=10,b=0))
        fig_tree.update_traces(textfont=dict(size=12))
        st.plotly_chart(fig_tree, use_container_width=True)
    else:
        st.info("No data to display — adjust filters.")

# ════════════════════════════════════════════
# TAB 4 — RANKINGS
# ════════════════════════════════════════════
with tab4:
    col_r1, col_r2 = st.columns([2, 1])

    with col_r1:
        sort_by = st.selectbox(
            "Sort by",
            ["visitors","instagram_tags","satisfaction","age_mz_ratio"],
            format_func=lambda x: {
                "visitors":       "👥 Total Visitors",
                "instagram_tags": "📸 Instagram Tags",
                "satisfaction":   "⭐ Satisfaction Score",
                "age_mz_ratio":   "🧑 MZ Ratio (%)",
            }[x],
        )
        ranked = filtered_df.sort_values(sort_by, ascending=False).reset_index(drop=True)
        ranked.index += 1

        st.markdown('<p class="section-title">Pop-up Store Overall Ranking</p>', unsafe_allow_html=True)

        sort_label = {"visitors":"Visitors","instagram_tags":"Insta Tags",
                      "satisfaction":"Rating","age_mz_ratio":"MZ Ratio"}

        for i, row in ranked.head(15).iterrows():
            medal = {1:"🥇",2:"🥈",3:"🥉"}.get(i, f"#{i}")
            clr   = CATEGORY_COLORS.get(row["category"],"#aaa")
            kw_chips = " ".join([
                f'<span style="background:rgba(255,180,50,0.12);color:#ffb432;padding:1px 7px;border-radius:12px;font-size:11px;">{k}</span>'
                for k in row["keywords"]
            ])
            suffix = "%" if sort_by == "age_mz_ratio" else ""
            val_str = f"{row[sort_by]:,}{suffix}" if isinstance(row[sort_by], (int,float)) and sort_by != "satisfaction" else f"{row[sort_by]}{suffix}"

            st.markdown(f"""
            <div class="info-card" style="border-left:3px solid {clr};">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div class="info-card-title">{medal} {row['name']}</div>
                        <div class="info-card-sub">📍 {row['district']} &nbsp;|&nbsp; <span style="color:{clr};">{row['category']}</span> &nbsp;|&nbsp; {row['period']}</div>
                        <div style="margin-top:6px;">{kw_chips}</div>
                    </div>
                    <div style="text-align:right;min-width:130px;">
                        <div style="color:#ffb432;font-size:1.1rem;font-weight:700;">{val_str}</div>
                        <div style="font-size:11px;color:rgba(255,255,255,0.4);">{sort_label[sort_by]}</div>
                        <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:4px;">⭐{row['satisfaction']} &nbsp; 💰 {row['price_range']}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col_r2:
        st.markdown('<p class="section-title">Key Insights</p>', unsafe_allow_html=True)
        free_pct = int((df["price_range"]=="Free").sum() / len(df) * 100)
        insights = [
            ("🔥 Hottest District",   "Yeouido (The Hyundai)",    "Avg 41,250 visitors"),
            ("📸 Instagram King",      "HYBE Artist Pop-up",       "135,000 tags"),
            ("⭐ Top Satisfaction",    "Gucci Garden / LE SSERAFIM","4.9 / 5.0"),
            ("🧑 MZ Concentration",   "Hongdae K-pop Pop-ups",    "95–97% MZ ratio"),
            ("🎯 Top Category",        "Fashion & Sports",         f"{(df['category']=='Fashion & Sports').sum()} stores"),
            ("💡 Free Entry Rate",     "Free admission",           f"{free_pct}% of all pop-ups"),
        ]
        for title, name, desc in insights:
            st.markdown(f"""
            <div class="info-card">
                <div style="font-size:0.78rem;color:#ffb432;font-weight:600;margin-bottom:3px;">{title}</div>
                <div class="info-card-title">{name}</div>
                <div class="info-card-sub">{desc}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<p class="section-title">Keyword Frequency</p>', unsafe_allow_html=True)
        all_kw2 = []
        for kws in filtered_df["keywords"]:
            all_kw2.extend(kws)
        kw_df2 = pd.DataFrame(Counter(all_kw2).most_common(12), columns=["keyword","count"])
        if len(kw_df2) > 0:
            fig_kw = px.bar(
                kw_df2.sort_values("count"),
                x="count", y="keyword", orientation="h",
                color="count",
                color_continuous_scale=[[0,"#1a1a4e"],[1,"#ffb432"]],
                labels={"count":"Frequency","keyword":""},
            )
            apply_theme(fig_kw, height=320)
            fig_kw.update_layout(coloraxis_showscale=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_kw, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:rgba(255,255,255,0.25);font-size:0.78rem;padding:1rem 0 2rem;">
    MZ Generation Pop-up Store &amp; Cultural Space Consumption Trend Map &nbsp;|&nbsp; Data: Seoul Key Commercial Districts 2024
</div>
""", unsafe_allow_html=True)
