"""
MZ세대의 팝업스토어 및 문화 공간 소비 트렌드 지도
실행 방법:
    pip install streamlit plotly folium streamlit-folium pandas numpy
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
from datetime import datetime

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MZ세대 팝업스토어 트렌드 지도",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 전역 CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

    .main { background: #0f0f14; }
    .block-container { padding: 1.5rem 2rem 3rem 2rem; }

    /* 헤더 */
    .hero-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,180,50,0.2);
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute; top: -50%; right: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(255,180,50,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2rem; font-weight: 700;
        color: #ffffff; margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
    }
    .hero-sub {
        font-size: 1rem; color: rgba(255,255,255,0.6);
        margin: 0; font-weight: 300;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,180,50,0.15);
        border: 1px solid rgba(255,180,50,0.4);
        color: #ffb432; font-size: 0.75rem; font-weight: 500;
        padding: 0.25rem 0.8rem; border-radius: 20px;
        margin-bottom: 1rem; letter-spacing: 0.05em;
    }

    /* 메트릭 카드 */
    .metric-card {
        background: #1a1a2e;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem; font-weight: 700;
        color: #ffb432; line-height: 1;
        margin-bottom: 0.3rem;
    }
    .metric-label {
        font-size: 0.78rem; color: rgba(255,255,255,0.5);
        font-weight: 400;
    }
    .metric-delta {
        font-size: 0.8rem; color: #4ade80; margin-top: 0.2rem;
    }

    /* 섹션 타이틀 */
    .section-title {
        font-size: 1.1rem; font-weight: 600;
        color: #ffffff; margin: 0 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ffb432;
        display: inline-block;
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: #13131f;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    [data-testid="stSidebar"] .block-container { padding: 1rem; }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: rgba(255,255,255,0.5);
        font-size: 0.88rem;
    }
    .stTabs [aria-selected="true"] {
        background: #ffb432 !important;
        color: #000 !important;
        font-weight: 600;
    }

    /* 태그 칩 */
    .tag-chip {
        display: inline-block;
        background: rgba(255,180,50,0.1);
        border: 1px solid rgba(255,180,50,0.3);
        color: #ffb432;
        font-size: 0.72rem; padding: 0.2rem 0.6rem;
        border-radius: 20px; margin: 2px;
    }

    /* 정보 카드 */
    .info-card {
        background: #1a1a2e;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .info-card-title {
        font-size: 0.95rem; font-weight: 600; color: #fff;
        margin-bottom: 0.3rem;
    }
    .info-card-sub {
        font-size: 0.8rem; color: rgba(255,255,255,0.45);
    }

    /* 플롯 배경 */
    .js-plotly-plot { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 데이터 정의
# ─────────────────────────────────────────────

@st.cache_data
def load_popup_data():
    data = [
        # 서울 성수동
        {"name": "Nike Air Max Pop-up", "district": "성수동", "gu": "성동구", "lat": 37.5445, "lng": 127.0557,
         "category": "패션·스포츠", "brand": "Nike", "period": "2024-03", "visitors": 12400,
         "instagram_tags": 28000, "satisfaction": 4.6, "age_mz_ratio": 88,
         "price_range": "무료", "keywords": ["한정판", "포토스팟", "리셀"], "open_days": 14},
        {"name": "무신사 스탠다드 팝업", "district": "성수동", "gu": "성동구", "lat": 37.5438, "lng": 127.0561,
         "category": "패션·스포츠", "brand": "무신사", "period": "2024-04", "visitors": 19200,
         "instagram_tags": 41000, "satisfaction": 4.5, "age_mz_ratio": 92,
         "price_range": "무료", "keywords": ["스트릿", "데일리룩", "할인"], "open_days": 21},
        {"name": "카카오프렌즈 팝업", "district": "성수동", "gu": "성동구", "lat": 37.5441, "lng": 127.0548,
         "category": "캐릭터·IP", "brand": "카카오", "period": "2024-05", "visitors": 22000,
         "instagram_tags": 55000, "satisfaction": 4.7, "age_mz_ratio": 85,
         "price_range": "무료", "keywords": ["캐릭터", "굿즈", "포토부스"], "open_days": 30},
        {"name": "젠틀몬스터 하우스 도산", "district": "성수동", "gu": "성동구", "lat": 37.5452, "lng": 127.0553,
         "category": "라이프스타일·뷰티", "brand": "젠틀몬스터", "period": "2024-02", "visitors": 9800,
         "instagram_tags": 32000, "satisfaction": 4.8, "age_mz_ratio": 91,
         "price_range": "무료", "keywords": ["아트", "인스타그래머블", "명품"], "open_days": 21},

        # 홍대
        {"name": "애플 뮤직 × 아이브 팝업", "district": "홍대", "gu": "마포구", "lat": 37.5563, "lng": 126.9243,
         "category": "음악·엔터", "brand": "Apple Music", "period": "2024-03", "visitors": 31000,
         "instagram_tags": 78000, "satisfaction": 4.7, "age_mz_ratio": 95,
         "price_range": "무료", "keywords": ["K-pop", "아이돌", "한정굿즈"], "open_days": 7},
        {"name": "올리브영 뷰티 페스타", "district": "홍대", "gu": "마포구", "lat": 37.5551, "lng": 126.9238,
         "category": "라이프스타일·뷰티", "brand": "올리브영", "period": "2024-06", "visitors": 25600,
         "instagram_tags": 49000, "satisfaction": 4.4, "age_mz_ratio": 89,
         "price_range": "무료", "keywords": ["뷰티", "샘플", "체험"], "open_days": 10},
        {"name": "버버리 팝업스토어", "district": "홍대", "gu": "마포구", "lat": 37.5568, "lng": 126.9255,
         "category": "패션·스포츠", "brand": "Burberry", "period": "2024-01", "visitors": 7600,
         "instagram_tags": 22000, "satisfaction": 4.5, "age_mz_ratio": 78,
         "price_range": "유료(₩50,000+)", "keywords": ["럭셔리", "한정판", "영국"], "open_days": 14},

        # 강남 / 도산공원
        {"name": "구찌 가든 팝업", "district": "도산공원", "gu": "강남구", "lat": 37.5248, "lng": 127.0336,
         "category": "패션·스포츠", "brand": "Gucci", "period": "2024-05", "visitors": 14500,
         "instagram_tags": 61000, "satisfaction": 4.9, "age_mz_ratio": 82,
         "price_range": "무료", "keywords": ["럭셔리", "아트", "플래그십"], "open_days": 21},
        {"name": "디올 뷰티 팝업", "district": "도산공원", "gu": "강남구", "lat": 37.5245, "lng": 127.0329,
         "category": "라이프스타일·뷰티", "brand": "Dior", "period": "2024-04", "visitors": 11200,
         "instagram_tags": 47000, "satisfaction": 4.8, "age_mz_ratio": 80,
         "price_range": "무료", "keywords": ["뷰티", "향수", "프랑스"], "open_days": 14},
        {"name": "네이버 웹툰 팝업전", "district": "강남역", "gu": "강남구", "lat": 37.4979, "lng": 127.0277,
         "category": "캐릭터·IP", "brand": "네이버웹툰", "period": "2024-07", "visitors": 18700,
         "instagram_tags": 38000, "satisfaction": 4.5, "age_mz_ratio": 90,
         "price_range": "무료", "keywords": ["웹툰", "캐릭터", "굿즈"], "open_days": 21},

        # 여의도 / 더현대
        {"name": "더현대 서울 MZ 팝업존", "district": "여의도", "gu": "영등포구", "lat": 37.5219, "lng": 126.9240,
         "category": "F&B·식음료", "brand": "현대백화점", "period": "2024-06", "visitors": 42000,
         "instagram_tags": 88000, "satisfaction": 4.6, "age_mz_ratio": 87,
         "price_range": "무료", "keywords": ["백화점", "F&B", "트렌드"], "open_days": 30},
        {"name": "포켓몬 팝업스토어", "district": "여의도", "gu": "영등포구", "lat": 37.5215, "lng": 126.9235,
         "category": "캐릭터·IP", "brand": "포켓몬", "period": "2024-08", "visitors": 38500,
         "instagram_tags": 95000, "satisfaction": 4.8, "age_mz_ratio": 88,
         "price_range": "무료", "keywords": ["캐릭터", "IP", "한정판"], "open_days": 21},

        # 이태원 / 한남
        {"name": "르세라핌 팬미팅 팝업", "district": "한남동", "gu": "용산구", "lat": 37.5340, "lng": 126.9978,
         "category": "음악·엔터", "brand": "르세라핌", "period": "2024-02", "visitors": 29000,
         "instagram_tags": 112000, "satisfaction": 4.9, "age_mz_ratio": 96,
         "price_range": "유료(₩30,000)", "keywords": ["K-pop", "팬덤", "굿즈"], "open_days": 7},
        {"name": "파타고니아 팝업", "district": "한남동", "gu": "용산구", "lat": 37.5335, "lng": 126.9985,
         "category": "패션·스포츠", "brand": "Patagonia", "period": "2024-09", "visitors": 6800,
         "instagram_tags": 15000, "satisfaction": 4.4, "age_mz_ratio": 82,
         "price_range": "무료", "keywords": ["지속가능", "아웃도어", "친환경"], "open_days": 14},

        # 인사동 / 북촌
        {"name": "삼성 갤럭시 AI 체험관", "district": "인사동", "gu": "종로구", "lat": 37.5741, "lng": 126.9838,
         "category": "테크·전자", "brand": "Samsung", "period": "2024-07", "visitors": 24300,
         "instagram_tags": 42000, "satisfaction": 4.5, "age_mz_ratio": 85,
         "price_range": "무료", "keywords": ["AI", "갤럭시", "테크"], "open_days": 30},
        {"name": "LG 올레드 아트 팝업", "district": "인사동", "gu": "종로구", "lat": 37.5736, "lng": 126.9843,
         "category": "테크·전자", "brand": "LG", "period": "2024-08", "visitors": 11400,
         "instagram_tags": 22000, "satisfaction": 4.3, "age_mz_ratio": 77,
         "price_range": "무료", "keywords": ["TV", "아트", "인테리어"], "open_days": 21},

        # 잠실
        {"name": "롤스로이스 아트 팝업", "district": "잠실", "gu": "송파구", "lat": 37.5133, "lng": 127.1028,
         "category": "패션·스포츠", "brand": "Rolls-Royce", "period": "2024-10", "visitors": 5600,
         "instagram_tags": 18000, "satisfaction": 4.7, "age_mz_ratio": 70,
         "price_range": "무료", "keywords": ["럭셔리", "슈퍼카", "아트"], "open_days": 10},
        {"name": "하이브 아티스트 팝업", "district": "잠실", "gu": "송파구", "lat": 37.5128, "lng": 127.1022,
         "category": "음악·엔터", "brand": "HYBE", "period": "2024-11", "visitors": 45000,
         "instagram_tags": 135000, "satisfaction": 4.9, "age_mz_ratio": 97,
         "price_range": "유료(₩25,000)", "keywords": ["K-pop", "BTS", "아미"], "open_days": 14},

        # 명동
        {"name": "코카콜라 Y2K 팝업", "district": "명동", "gu": "중구", "lat": 37.5633, "lng": 126.9845,
         "category": "F&B·식음료", "brand": "Coca-Cola", "period": "2024-05", "visitors": 16800,
         "instagram_tags": 31000, "satisfaction": 4.2, "age_mz_ratio": 86,
         "price_range": "무료", "keywords": ["Y2K", "레트로", "체험"], "open_days": 21},
        {"name": "스타벅스 더 리저브 팝업", "district": "명동", "gu": "중구", "lat": 37.5638, "lng": 126.9852,
         "category": "F&B·식음료", "brand": "Starbucks", "period": "2024-09", "visitors": 21500,
         "instagram_tags": 44000, "satisfaction": 4.4, "age_mz_ratio": 84,
         "price_range": "유료(₩15,000+)", "keywords": ["커피", "굿즈", "시즌"], "open_days": 30},
    ]
    return pd.DataFrame(data)


@st.cache_data
def load_monthly_trend():
    months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    return pd.DataFrame({
        "월": months,
        "팝업스토어 수": [18, 22, 31, 28, 35, 42, 38, 44, 40, 33, 29, 25],
        "방문자수(만명)": [24, 31, 48, 42, 56, 71, 65, 79, 68, 55, 48, 42],
        "인스타태그(만)": [38, 55, 82, 74, 98, 124, 112, 138, 118, 92, 78, 65],
    })


@st.cache_data
def load_district_stats():
    return pd.DataFrame({
        "지역": ["성수동", "홍대", "강남/도산", "여의도", "한남동", "인사동", "잠실", "명동"],
        "팝업수": [24, 19, 22, 15, 12, 10, 8, 11],
        "평균방문자": [15850, 21400, 12500, 40250, 17900, 17850, 25300, 19150],
        "MZ비율평균": [89, 87, 81, 88, 89, 81, 84, 85],
        "평균인스타태그": [39000, 49667, 42000, 91500, 63500, 32000, 76500, 37500],
    })


# ─────────────────────────────────────────────
# 데이터 로드
# ─────────────────────────────────────────────
df = load_popup_data()
monthly = load_monthly_trend()
district_stats = load_district_stats()

# 카테고리 색상 매핑
CATEGORY_COLORS = {
    "패션·스포츠":      "#ff6b6b",
    "라이프스타일·뷰티": "#ffd93d",
    "음악·엔터":        "#6bcb77",
    "캐릭터·IP":        "#4d96ff",
    "F&B·식음료":       "#ff922b",
    "테크·전자":         "#cc5de8",
}

PLOTLY_THEME = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor":  "rgba(26,26,46,0.8)",
    "font_color":    "#ffffff",
    "gridcolor":     "rgba(255,255,255,0.08)",
}

# ─────────────────────────────────────────────
# 사이드바 필터
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 필터 설정")

    selected_categories = st.multiselect(
        "카테고리",
        options=list(CATEGORY_COLORS.keys()),
        default=list(CATEGORY_COLORS.keys()),
    )

    selected_districts = st.multiselect(
        "지역 (구)",
        options=sorted(df["district"].unique()),
        default=sorted(df["district"].unique()),
    )

    min_visitors = st.slider(
        "최소 방문자 수",
        min_value=0, max_value=50000, value=0, step=1000,
        format="%d명"
    )

    mz_ratio_min = st.slider(
        "MZ 비율 최소",
        min_value=60, max_value=100, value=70, step=1,
        format="%d%%"
    )

    price_filter = st.multiselect(
        "입장료",
        options=df["price_range"].unique().tolist(),
        default=df["price_range"].unique().tolist(),
    )

    st.markdown("---")
    st.markdown("#### 📊 지도 설정")
    map_style = st.selectbox(
        "지도 스타일",
        ["CartoDB dark_matter", "CartoDB positron", "OpenStreetMap"],
        index=0,
    )
    marker_size = st.select_slider(
        "마커 크기 기준",
        options=["방문자 수", "인스타 태그 수", "MZ 비율"],
        value="방문자 수"
    )

# ─────────────────────────────────────────────
# 데이터 필터링
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
# 헤더
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">📍 서울시 팝업스토어 트렌드 대시보드 2024</div>
    <h1 class="hero-title">🗺️ MZ세대의 팝업스토어 &amp; 문화 공간<br>소비 트렌드 지도</h1>
    <p class="hero-sub">서울 주요 상권의 팝업스토어 데이터를 분석하고, MZ세대 소비 트렌드를 시각화합니다</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI 메트릭
# ─────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
kpi_data = [
    (col1, f"{len(filtered_df)}개", "팝업스토어", "↑12% YoY"),
    (col2, f"{filtered_df['visitors'].sum():,}명", "총 방문자", "↑34% YoY"),
    (col3, f"{int(filtered_df['age_mz_ratio'].mean())}%", "평균 MZ 비율", "↑8%p"),
    (col4, f"{filtered_df['satisfaction'].mean():.1f}점", "평균 만족도", "★ 4.6/5.0"),
    (col5, f"{int(filtered_df['instagram_tags'].sum()/10000)}만", "인스타 태그", "↑61% YoY"),
]
for col, val, label, delta in kpi_data:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-delta">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 탭 구성
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ 인터랙티브 지도", "📊 트렌드 분석", "📍 지역별 분석", "🏆 팝업스토어 랭킹"])

# ════════════════════════════════════════════
# TAB 1 — 지도
# ════════════════════════════════════════════
with tab1:
    col_map, col_info = st.columns([2, 1])

    with col_map:
        st.markdown('<p class="section-title">서울 팝업스토어 분포 지도</p>', unsafe_allow_html=True)

        # Folium 지도 생성
        tile_map = {
            "CartoDB dark_matter": "CartoDB dark_matter",
            "CartoDB positron": "CartoDB positron",
            "OpenStreetMap": "OpenStreetMap",
        }
        m = folium.Map(
            location=[37.5350, 126.9950],
            zoom_start=12,
            tiles=tile_map[map_style],
        )

        # 범례 HTML
        legend_html = """
        <div style="position:fixed; bottom:30px; left:30px; z-index:9999;
                    background:rgba(15,15,20,0.92); padding:12px 16px;
                    border-radius:10px; border:1px solid rgba(255,255,255,0.1);
                    font-family: sans-serif; font-size:12px; color:#fff;">
            <b style="font-size:13px;">카테고리</b><br><br>
        """
        for cat, color in CATEGORY_COLORS.items():
            legend_html += f'<span style="color:{color};">●</span> {cat}<br>'
        legend_html += "</div>"
        m.get_root().html.add_child(folium.Element(legend_html))

        # 마커 크기 기준 컬럼
        size_col_map = {"방문자 수": "visitors", "인스타 태그 수": "instagram_tags", "MZ 비율": "age_mz_ratio"}
        size_col = size_col_map[marker_size]
        size_max = filtered_df[size_col].max() if len(filtered_df) > 0 else 1

        for _, row in filtered_df.iterrows():
            color = CATEGORY_COLORS.get(row["category"], "#ffffff")
            radius = 8 + (row[size_col] / size_max) * 22

            keywords_html = " ".join([f'<span style="background:rgba(255,180,50,0.2);color:#ffb432;padding:2px 7px;border-radius:12px;font-size:11px;">{kw}</span>' for kw in row["keywords"]])

            popup_html = f"""
            <div style="font-family:sans-serif;min-width:220px;background:#1a1a2e;color:#fff;
                        border-radius:10px;overflow:hidden;padding:14px;">
                <div style="font-size:14px;font-weight:700;margin-bottom:4px;">{row['name']}</div>
                <div style="font-size:12px;color:#ffb432;margin-bottom:8px;">{row['district']} · {row['category']}</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;margin-bottom:10px;">
                    <div>👥 방문자: <b>{row['visitors']:,}명</b></div>
                    <div>⭐ 만족도: <b>{row['satisfaction']}</b></div>
                    <div>📸 인스타: <b>{row['instagram_tags']:,}</b></div>
                    <div>🧑 MZ비율: <b>{row['age_mz_ratio']}%</b></div>
                    <div>💰 입장료: <b>{row['price_range']}</b></div>
                    <div>📅 기간: <b>{row['open_days']}일</b></div>
                </div>
                <div style="margin-top:6px;">{keywords_html}</div>
            </div>
            """

            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.75,
                weight=2,
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=f"📍 {row['name']} ({row['visitors']:,}명)",
            ).add_to(m)

        # 히트맵 레이어 (방문자 기반)
        try:
            from folium.plugins import HeatMap
            heat_data = [[row["lat"], row["lng"], row["visitors"] / 1000] for _, row in filtered_df.iterrows()]
            HeatMap(heat_data, radius=35, blur=25, min_opacity=0.3).add_to(m)
        except Exception:
            pass

        st_folium(m, width=None, height=520, returned_objects=[])

    with col_info:
        st.markdown('<p class="section-title">선택된 팝업 정보</p>', unsafe_allow_html=True)
        st.markdown(f"**현재 {len(filtered_df)}개** 팝업스토어 표시 중")
        st.markdown("---")

        # 카테고리별 분포
        cat_counts = filtered_df["category"].value_counts()
        for cat, cnt in cat_counts.items():
            color = CATEGORY_COLORS.get(cat, "#aaa")
            pct = int(cnt / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;font-size:13px;color:#fff;margin-bottom:3px;">
                    <span><span style="color:{color};">●</span> {cat}</span>
                    <span>{cnt}개 ({pct}%)</span>
                </div>
                <div style="background:rgba(255,255,255,0.08);border-radius:4px;height:6px;">
                    <div style="background:{color};width:{pct}%;height:100%;border-radius:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**🔥 HOT 키워드**")
        all_keywords = []
        for kws in filtered_df["keywords"]:
            all_keywords.extend(kws)
        from collections import Counter
        kw_counts = Counter(all_keywords).most_common(10)
        kw_html = "".join([f'<span class="tag-chip">{kw} ({cnt})</span>' for kw, cnt in kw_counts])
        st.markdown(f'<div style="margin-top:8px;">{kw_html}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 2 — 트렌드 분석
# ════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title">2024 연간 트렌드</p>', unsafe_allow_html=True)

    # 월별 복합 차트
    fig_trend = make_subplots(
        rows=1, cols=1,
        specs=[[{"secondary_y": True}]],
    )
    fig_trend.add_trace(
        go.Bar(
            x=monthly["월"], y=monthly["팝업스토어 수"],
            name="팝업스토어 수", marker_color="rgba(255,180,50,0.7)",
            yaxis="y"
        )
    )
    fig_trend.add_trace(
        go.Scatter(
            x=monthly["월"], y=monthly["방문자수(만명)"],
            name="방문자수(만명)", line=dict(color="#6bcb77", width=2.5),
            mode="lines+markers", marker=dict(size=7),
            yaxis="y2"
        )
    )
    fig_trend.add_trace(
        go.Scatter(
            x=monthly["월"], y=monthly["인스타태그(만)"],
            name="인스타태그(만)", line=dict(color="#4d96ff", width=2, dash="dot"),
            mode="lines+markers", marker=dict(size=6),
            yaxis="y2"
        )
    )
    fig_trend.update_layout(
        **PLOTLY_THEME,
        height=380, margin=dict(l=10, r=10, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", font=dict(color="#fff")),
        yaxis=dict(title="팝업 수", gridcolor=PLOTLY_THEME["gridcolor"], color="#fff"),
        yaxis2=dict(title="만 명 / 만 건", overlaying="y", side="right", color="#fff",
                    gridcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#fff"),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="section-title">카테고리별 방문자 & 만족도</p>', unsafe_allow_html=True)
        cat_agg = filtered_df.groupby("category").agg(
            visitors=("visitors", "sum"),
            satisfaction=("satisfaction", "mean"),
            count=("name", "count"),
        ).reset_index()

        fig_bubble = px.scatter(
            cat_agg,
            x="satisfaction", y="visitors",
            size="count", color="category",
            color_discrete_map=CATEGORY_COLORS,
            text="category",
            size_max=50,
            labels={"satisfaction": "평균 만족도", "visitors": "총 방문자", "category": "카테고리"},
        )
        fig_bubble.update_traces(textposition="top center", textfont=dict(color="#fff", size=11))
        fig_bubble.update_layout(
            **PLOTLY_THEME, height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            xaxis=dict(gridcolor=PLOTLY_THEME["gridcolor"], color="#fff"),
            yaxis=dict(gridcolor=PLOTLY_THEME["gridcolor"], color="#fff"),
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-title">입장료 유형 & MZ 비율 분포</p>', unsafe_allow_html=True)

        fig_sub = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "pie"}, {"type": "box"}]],
            subplot_titles=["입장료 구성", "MZ 비율 분포"],
        )
        price_counts = filtered_df["price_range"].value_counts()
        fig_sub.add_trace(
            go.Pie(
                labels=price_counts.index,
                values=price_counts.values,
                hole=0.5,
                marker=dict(colors=["#ffb432", "#ff6b6b", "#4d96ff"]),
                textfont=dict(color="#fff"),
            ), row=1, col=1
        )
        for cat in filtered_df["category"].unique():
            sub_df = filtered_df[filtered_df["category"] == cat]
            fig_sub.add_trace(
                go.Box(
                    y=sub_df["age_mz_ratio"],
                    name=cat[:4],
                    marker_color=CATEGORY_COLORS.get(cat, "#aaa"),
                    showlegend=False,
                ), row=1, col=2
            )
        fig_sub.update_layout(
            **PLOTLY_THEME, height=340,
            margin=dict(l=10, r=10, t=30, b=10),
            font=dict(color="#fff"),
        )
        fig_sub.update_xaxes(color="#fff", gridcolor="rgba(0,0,0,0)")
        fig_sub.update_yaxes(color="#fff", gridcolor=PLOTLY_THEME["gridcolor"])
        st.plotly_chart(fig_sub, use_container_width=True)

    # 운영기간 vs 방문자 상관관계
    st.markdown('<p class="section-title">운영 기간 vs 총 방문자 상관관계</p>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        filtered_df,
        x="open_days", y="visitors",
        color="category",
        size="instagram_tags",
        color_discrete_map=CATEGORY_COLORS,
        hover_data={"name": True, "district": True, "satisfaction": True},
        labels={"open_days": "운영 기간 (일)", "visitors": "방문자 수", "instagram_tags": "인스타 태그"},
        trendline="ols",
    )
    fig_scatter.update_layout(
        **PLOTLY_THEME, height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#fff")),
        xaxis=dict(gridcolor=PLOTLY_THEME["gridcolor"], color="#fff"),
        yaxis=dict(gridcolor=PLOTLY_THEME["gridcolor"], color="#fff"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ════════════════════════════════════════════
# TAB 3 — 지역별 분석
# ════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-title">지역별 팝업스토어 현황 비교</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(
            district_stats.sort_values("팝업수", ascending=True),
            x="팝업수", y="지역",
            orientation="h",
            color="팝업수",
            color_continuous_scale=[[0, "#1a1a4e"], [0.5, "#ffb432"], [1, "#ff6b6b"]],
            labels={"팝업수": "팝업스토어 수", "지역": ""},
        )
        fig_bar.update_layout(
            **PLOTLY_THEME, height=350,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor=PLOTLY_THEME["gridcolor"], color="#fff"),
            yaxis=dict(color="#fff"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_radar = go.Figure()
        for i, row in district_stats.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[
                    row["팝업수"] / district_stats["팝업수"].max() * 100,
                    row["평균방문자"] / district_stats["평균방문자"].max() * 100,
                    row["MZ비율평균"],
                    row["평균인스타태그"] / district_stats["평균인스타태그"].max() * 100,
                ],
                theta=["팝업 수", "평균 방문자", "MZ 비율", "인스타 태그"],
                fill="toself",
                name=row["지역"],
                opacity=0.6,
            ))
        fig_radar.update_layout(
            **PLOTLY_THEME, height=350,
            polar=dict(
                bgcolor="rgba(26,26,46,0.8)",
                radialaxis=dict(visible=True, color="#888", gridcolor="rgba(255,255,255,0.1)"),
                angularaxis=dict(color="#fff"),
            ),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#fff", size=11)),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # 지역별 상세 테이블
    st.markdown('<p class="section-title">지역별 상세 지표</p>', unsafe_allow_html=True)
    display_district = district_stats.copy()
    display_district["평균방문자"] = display_district["평균방문자"].apply(lambda x: f"{x:,}명")
    display_district["MZ비율평균"] = display_district["MZ비율평균"].apply(lambda x: f"{x}%")
    display_district["평균인스타태그"] = display_district["평균인스타태그"].apply(lambda x: f"{x:,}")
    st.dataframe(
        display_district.rename(columns={
            "지역": "📍 지역", "팝업수": "팝업 수", "평균방문자": "평균 방문자",
            "MZ비율평균": "MZ 비율", "평균인스타태그": "평균 인스타 태그"
        }),
        use_container_width=True,
        hide_index=True,
    )

    # Treemap
    st.markdown('<p class="section-title">지역 × 카테고리 트리맵</p>', unsafe_allow_html=True)
    fig_tree = px.treemap(
        filtered_df,
        path=["district", "category", "name"],
        values="visitors",
        color="satisfaction",
        color_continuous_scale=[[0, "#1a1a4e"], [0.5, "#ffb432"], [1, "#ff6b6b"]],
        hover_data={"instagram_tags": True, "age_mz_ratio": True},
    )
    fig_tree.update_layout(
        **PLOTLY_THEME, height=420,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    fig_tree.update_traces(textfont=dict(size=12))
    st.plotly_chart(fig_tree, use_container_width=True)

# ════════════════════════════════════════════
# TAB 4 — 랭킹
# ════════════════════════════════════════════
with tab4:
    col_r1, col_r2 = st.columns([2, 1])

    with col_r1:
        sort_by = st.selectbox(
            "정렬 기준",
            ["visitors", "instagram_tags", "satisfaction", "age_mz_ratio"],
            format_func=lambda x: {
                "visitors": "👥 방문자 수",
                "instagram_tags": "📸 인스타 태그 수",
                "satisfaction": "⭐ 만족도",
                "age_mz_ratio": "🧑 MZ 비율",
            }[x]
        )

        ranked = filtered_df.sort_values(sort_by, ascending=False).reset_index(drop=True)
        ranked.index += 1

        st.markdown('<p class="section-title">팝업스토어 종합 랭킹</p>', unsafe_allow_html=True)

        for i, row in ranked.head(15).iterrows():
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"**{i}위**")
            color = CATEGORY_COLORS.get(row["category"], "#aaa")
            kw_chips = " ".join([f'<span style="background:rgba(255,180,50,0.12);color:#ffb432;padding:1px 7px;border-radius:12px;font-size:11px;">{k}</span>' for k in row["keywords"]])

            st.markdown(f"""
            <div class="info-card" style="border-left:3px solid {color};">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div class="info-card-title">{medal} {row['name']}</div>
                        <div class="info-card-sub">📍 {row['district']} &nbsp;|&nbsp; <span style="color:{color};">{row['category']}</span> &nbsp;|&nbsp; {row['period']}</div>
                        <div style="margin-top:6px;">{kw_chips}</div>
                    </div>
                    <div style="text-align:right;min-width:130px;">
                        <div style="color:#ffb432;font-size:1.1rem;font-weight:700;">{row[sort_by]:,}{'%' if sort_by=='age_mz_ratio' else ''}</div>
                        <div style="font-size:11px;color:rgba(255,255,255,0.4);">{{'visitors':'방문자','instagram_tags':'인스타태그','satisfaction':'만족도','age_mz_ratio':'MZ비율'}}['{sort_by}']</div>
                        <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:4px;">⭐{row['satisfaction']} &nbsp; 💰{row['price_range']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_r2:
        st.markdown('<p class="section-title">핵심 인사이트</p>', unsafe_allow_html=True)
        insights = [
            ("🔥 가장 핫한 지역", "여의도 더현대", "평균 41,250명 방문"),
            ("📸 인스타 최강", "하이브 아티스트 팝업", "135,000 태그"),
            ("⭐ 최고 만족도", "구찌 가든 / 르세라핌", "4.9점"),
            ("🧑 MZ 집결지", "홍대 K-pop 팝업", "95~97% MZ 비율"),
            ("🎯 최다 카테고리", "패션·스포츠", f"{(df['category']=='패션·스포츠').sum()}개"),
            ("💡 무료 입장 비율", "무료 팝업", f"{(df['price_range']=='무료').sum() / len(df) * 100:.0f}%"),
        ]
        for title, name, desc in insights:
            st.markdown(f"""
            <div class="info-card">
                <div style="font-size:0.78rem;color:#ffb432;font-weight:600;margin-bottom:3px;">{title}</div>
                <div class="info-card-title">{name}</div>
                <div class="info-card-sub">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        # 워드클라우드 대체 — 키워드 빈도 수평 바
        st.markdown("---")
        st.markdown('<p class="section-title">키워드 빈도</p>', unsafe_allow_html=True)
        from collections import Counter
        all_kw = []
        for kws in filtered_df["keywords"]:
            all_kw.extend(kws)
        kw_df = pd.DataFrame(Counter(all_kw).most_common(12), columns=["keyword", "count"])
        fig_kw = px.bar(
            kw_df.sort_values("count"),
            x="count", y="keyword", orientation="h",
            color="count",
            color_continuous_scale=[[0, "#1a1a4e"], [1, "#ffb432"]],
        )
        fig_kw.update_layout(
            **PLOTLY_THEME, height=320,
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor=PLOTLY_THEME["gridcolor"], color="#fff"),
            yaxis=dict(color="#fff"),
        )
        st.plotly_chart(fig_kw, use_container_width=True)

# ─────────────────────────────────────────────
# 푸터
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:rgba(255,255,255,0.25);font-size:0.78rem;padding:1rem 0 2rem;">
    MZ세대 팝업스토어 & 문화 공간 소비 트렌드 지도 | 데이터: 2024 서울 주요 상권 현황
</div>
""", unsafe_allow_html=True)
