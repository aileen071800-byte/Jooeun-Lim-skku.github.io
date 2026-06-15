import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

st.set_page_config(
    page_title="Seoul Pop-up Trend Map 2024-2026",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #04060d !important;
    color: #f0eee8 !important;
}
[data-testid="stAppViewContainer"] { background-color: #04060d !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 2rem 2rem 4rem !important; max-width: 100% !important; }

/* Sidebar */
[data-testid="stSidebar"] { background-color: #080c18 !important; border-right: 1px solid rgba(255,255,255,0.07) !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] span, [data-testid="stSidebar"] div { color: #f0eee8 !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: #0d1221 !important; border: 1px solid rgba(255,255,255,0.1) !important;
    color: #f0eee8 !important; border-radius: 20px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: rgba(0,229,204,0.15) !important; color: #00e5cc !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #080c18; border-bottom: 1px solid rgba(255,255,255,0.07); gap: 0; }
.stTabs [data-baseweb="tab"] {
    color: #6b7280 !important; font-family: 'DM Mono', monospace !important;
    font-size: 12px !important; letter-spacing: 0.08em !important;
    padding: 12px 20px !important; background: transparent !important;
}
.stTabs [aria-selected="true"] { color: #00e5cc !important; border-bottom: 2px solid #00e5cc !important; }
.stTabs [data-baseweb="tab-panel"] { background: #04060d; padding: 24px 0 0 !important; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #04060d 0%, #0a0e1a 100%);
    padding: 60px 48px 48px; margin: -2rem -2rem 32px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    position: relative; overflow: hidden;
}
.hero::before {
    content: '';position: absolute; inset: 0;
    background: radial-gradient(ellipse 60% 60% at 10% 30%, rgba(255,107,157,0.08) 0%, transparent 60%),
                radial-gradient(ellipse 40% 50% at 90% 70%, rgba(0,229,204,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.hero-label {
    font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.22em;
    text-transform: uppercase; color: #00e5cc; margin-bottom: 16px;
    display: flex; align-items: center; gap: 12px;
}
.hero-label::before { content:''; width:28px; height:1px; background:#00e5cc; display:inline-block; }
.hero-title {
    font-family: 'Syne', sans-serif; font-size: clamp(36px, 6vw, 80px);
    font-weight: 800; line-height: 0.93; letter-spacing: -0.04em; margin-bottom: 20px;
}
.hero-title .t1 { color: #f0eee8; display: block; }
.hero-title .t2 {
    display: block;
    background: linear-gradient(90deg, #ff6b9d, #a78bfa, #00e5cc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { color: #6b7280; font-size: 14px; line-height: 1.9; max-width: 560px; margin-bottom: 32px; }
.hero-sub b { color: #f0eee8; }
.year-pills { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 28px; }
.ypill {
    font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.14em;
    text-transform: uppercase; padding: 4px 12px; border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1); color: #6b7280;
}
.ypill.y2024 { border-color: #ffd166; color: #ffd166; }
.ypill.y2025 { border-color: #ff9a3c; color: #ff9a3c; }
.ypill.y2026 { border-color: #ff6b9d; color: #ff6b9d; }
.stat-row { display: flex; gap: 36px; flex-wrap: wrap; }
.stat { border-left: 2px solid #ff6b9d; padding-left: 14px; }
.stat:nth-child(2) { border-color: #00e5cc; }
.stat:nth-child(3) { border-color: #ffd166; }
.stat:nth-child(4) { border-color: #a78bfa; }
.stat-n { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #ff6b9d; line-height: 1; }
.stat:nth-child(2) .stat-n { color: #00e5cc; }
.stat:nth-child(3) .stat-n { color: #ffd166; }
.stat:nth-child(4) .stat-n { color: #a78bfa; }
.stat-l { font-size: 10px; color: #6b7280; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 3px; }

/* District header */
.dist-hdr { margin: 40px 0 8px; display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; }
.dist-num {
    font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.18em;
    text-transform: uppercase; padding: 3px 10px; border-radius: 20px; border: 1px solid currentColor;
}
.dist-name { font-family: 'Syne', sans-serif; font-size: clamp(22px, 3.5vw, 36px); font-weight: 800; letter-spacing: -0.03em; }
.dist-sub { font-family: 'DM Mono', monospace; font-size: 11px; color: #6b7280; }
.dist-desc { color: #6b7280; font-size: 13px; line-height: 1.9; max-width: 620px; margin: 8px 0 20px; }

/* Pop-up card */
.pcard {
    background: #0d1221; border: 1px solid rgba(255,255,255,0.07);
    border-radius: 2px; margin-bottom: 14px; overflow: hidden;
}
.pcard-bar { height: 3px; }
.pcard-inner { padding: 18px 20px 20px; }
.pcard-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; gap: 8px; }
.pcard-cat {
    font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.13em;
    text-transform: uppercase; padding: 2px 8px; border-radius: 10px; flex-shrink: 0;
}
.cat-fashion  { background: rgba(255,107,157,0.15); color: #ff6b9d; }
.cat-beauty   { background: rgba(167,139,250,0.15); color: #a78bfa; }
.cat-fb       { background: rgba(255,154,60,0.15);  color: #ff9a3c; }
.cat-ip       { background: rgba(255,209,102,0.15); color: #ffd166; }
.cat-art      { background: rgba(74,222,128,0.15);  color: #4ade80; }
.cat-lifestyle{ background: rgba(96,165,250,0.15);  color: #60a5fa; }
.pcard-right { display: flex; flex-direction: column; align-items: flex-end; gap: 3px; }
.pcard-yr {
    font-family: 'DM Mono', monospace; font-size: 9px;
    border: 1px solid rgba(255,255,255,0.15); padding: 2px 6px; border-radius: 6px; color: #6b7280;
}
.yr2024 { border-color: #ffd166 !important; color: #ffd166 !important; }
.yr2025 { border-color: #ff9a3c !important; color: #ff9a3c !important; }
.yr2026 { border-color: #ff6b9d !important; color: #ff6b9d !important; }
.pcard-hot { font-family: 'DM Mono', monospace; font-size: 9px; color: #ff6b9d; }
.pcard-name { font-size: 14px; font-weight: 600; color: #f0eee8; margin-bottom: 3px; line-height: 1.35; }
.pcard-brand { font-family: 'DM Mono', monospace; font-size: 11px; color: #6b7280; margin-bottom: 10px; }
.pcard-desc { font-size: 12px; color: #6b7280; line-height: 1.75; margin-bottom: 12px; }
.pcard-meta { font-family: 'DM Mono', monospace; font-size: 11px; color: #6b7280; margin-bottom: 10px; line-height: 1.9; }
.pcard-tags { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 12px; }
.ctag {
    font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 2px 7px; border: 1px solid rgba(255,255,255,0.1);
    color: #6b7280; border-radius: 10px;
}
.pcard-why {
    background: rgba(255,107,157,0.06); border-left: 2px solid #ff6b9d;
    padding: 10px 14px; font-size: 11px; color: rgba(240,238,232,0.55);
    line-height: 1.75; font-style: italic; border-radius: 0 2px 2px 0;
}

/* Trend card */
.tcard { background: #0d1221; border: 1px solid rgba(255,255,255,0.07); padding: 24px; margin-bottom: 14px; }
.tcard-num { font-family: 'Syne', sans-serif; font-size: 40px; font-weight: 800; line-height: 1; margin-bottom: 10px; }
.tcard-title { font-size: 13px; font-weight: 600; color: #f0eee8; margin-bottom: 7px; }
.tcard-desc { font-size: 11px; color: #6b7280; line-height: 1.8; }

/* Divider */
.ndiv { height: 1px; background: linear-gradient(90deg, transparent, #ff6b9d, #00e5cc, transparent); margin: 28px 0; }

/* Section labels */
.slabel { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.22em; text-transform: uppercase; color: #00e5cc; margin-bottom: 6px; }
.stitle { font-family: 'Syne', sans-serif; font-size: clamp(22px, 3vw, 34px); font-weight: 800; letter-spacing: -0.03em; margin-bottom: 14px; }

/* Result count */
.rcount { font-family: 'DM Mono', monospace; font-size: 11px; color: #6b7280; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
POPUPS = [
    # ── SEONGSU 2026 ──
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="Pokémon Ditto Playground", brand="Pokémon Mega Festa 2026",
         desc="Enter a pink, squishy world where Ditto has copied everything — slides, plush toys, and décor. Part of Pokémon's 30th Anniversary.",
         loc="Seongsui-ro 7ga-gil 9, Seongsu", date="May 1 – Jun 21, 2026", adm="Free", goods="Limited Ditto merch",
         tags=["Pokémon","30th Anniversary","Free","Photo Zone"],
         why="One of three simultaneous Pokémon events in Seongsu — Pokémon Mega Festa 2026 is unprecedented in scale.",
         img="Pokemon Ditto Metamon playground popup Seongsu Seoul 2026"),
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="🏆 Major",
         name="Pokémon 30th Birthday Party Pop-up", brand="Pokémon Mega Festa × Olive Young N Seongsu",
         desc="Birthday-party themed pop-up: cake, ribbon & balloon photo zones, coloring corner, and exclusive Birthday Edition merch.",
         loc="Olive Young N Seongsu, 1F", date="May 1 – Jun 21, 2026", adm="Free", goods="Birthday Edition limited goods",
         tags=["Pokémon","Birthday","30th","Limited Ed."],
         why="Olive Young's collab leverages Pokémon mania to drive flagship traffic — a perfect channel partnership model.",
         img="Pokemon birthday party popup Olive Young Seongsu Seoul"),
    dict(d="seongsu", cat="Beauty", yr=2026, hot="",
         name="Olive Young × Pokémon Pikachu Picnic", brand="Olive Young N Seongsu",
         desc="K-Beauty meets Pokémon — 1F Trend Fountain becomes a Pikachu & Minibu picnic with photo spots and themed beauty bundles.",
         loc="Olive Young N Seongsu, 1F", date="May 1 – May 31, 2026", adm="Free", goods="Collab beauty bundles",
         tags=["K-Beauty","Pokémon","Collab","Seasonal"],
         why="Shows how a beauty retailer can use IP licensing to create destination-worthy experiences."),
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="SEVENTEEN MINITEEN Flagship Pop-up", brand="SEVENTEEN × Pledis Entertainment",
         desc="Two-story flagship: Floor 1 is a themed café with ice cream & drinks, Floor 2 is a full character merchandise floor.",
         loc="Seongsu-dong (2-story)", date="May 23 – Jun 2, 2026", adm="Free", goods="Character merch + café menu",
         tags=["K-Pop","SEVENTEEN","Café","Flagship"],
         why="Two-floor café + shop format maximises dwell time — a growing blueprint for K-pop pop-ups.",
         img="SEVENTEEN MINITEEN popup store Seoul Seongsu cafe merch"),
    dict(d="seongsu", cat="Fashion", yr=2026, hot="",
         name="Lacoste 'Polo Factory' Pop-up", brand="Lacoste",
         desc="French heritage brand celebrates 90+ years of the polo shirt through an immersive walk-through of construction, fabrics, and sustainability.",
         loc="Seongsu-dong", date="May 21 – Jun 3, 2026", adm="Free", goods="Heritage collection + limited pieces",
         tags=["Heritage","Fashion","Exhibition","Sustainability"],
         why="Lacoste chose Seongsu over Gangnam — deliberate repositioning of a legacy brand toward MZ consumers.",
         img="Lacoste Polo Factory popup store Seoul Seongsu 2026"),
    dict(d="seongsu", cat="Beauty", yr=2026, hot="✨ Notable",
         name="YSL Beauty Seongsu Pop-up", brand="Yves Saint Laurent Beauty",
         desc="Luxury French beauty pop-up with new collection launch, makeup experience zones, and exclusive YSL goods only available here.",
         loc="Seongsu-dong", date="May 9 – May 24, 2026", adm="Free", goods="Exclusive YSL location goods",
         tags=["Luxury Beauty","Makeup","YSL","Exclusive"],
         why="YSL entering Seongsu rather than Apgujeong signals the district has matured into a luxury brand destination.",
         img="YSL Beauty popup store Seoul Seongsu luxury makeup"),
    dict(d="seongsu", cat="Beauty", yr=2026, hot="",
         name="La Roche-Posay — UV Stadium", brand="La Roche-Posay",
         desc="Sports-themed sunscreen pop-up turning skincare education into a stadium experience. UV zones, SPF trials, photo installations.",
         loc="Seongsu-dong", date="May 15 – May 25, 2026", adm="Free", goods="SPF sample kits",
         tags=["Sunscreen","Skincare","Experiential","Sports"],
         why="Turning skincare into a stadium concept shows brands competing for attention through narrative.",
         img="La Roche-Posay UV sunscreen popup store Seoul experience"),
    dict(d="seongsu", cat="Fashion", yr=2026, hot="🏆 Major",
         name="Musinsa Megastore Seongsu — Grand Opening", brand="Musinsa",
         desc="Grand opening of Musinsa's flagship megastore with multi-brand pop-ups, exclusive drops, and opening celebration events.",
         loc="Musinsa Megastore Seongsu", date="Apr 24 – May 3, 2026", adm="Free", goods="Exclusive opening drops",
         tags=["Flagship","Musinsa","Multi-brand","Grand Opening"],
         why="Musinsa's permanent megastore formalises Seongsu's evolution from pop-up hub to year-round destination.",
         img="Musinsa megastore Seongsu Seoul grand opening 2026"),
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="🏆 Global",
         name="BLACKPINK 'DEADLINE' Global Pop-up", brand="BLACKPINK × YG Entertainment",
         desc="World tour launching in Seoul first. Seoul-exclusive MD, new lightstick, plush, keyrings and keycaps. Continued in 20 cities worldwide.",
         loc="Musinsa Seongsu + Musinsa Myeongdong", date="Feb 28 – Mar 8, 2026 · 11:00–22:00", adm="Free", goods="Seoul-exclusive MD + lightstick",
         tags=["BLACKPINK","K-Pop","Global Tour","Musinsa"],
         why="Seoul as global first stop confirms it as the world's most important pop-up market in 2026.",
         img="BLACKPINK DEADLINE popup store Seoul Musinsa Seongsu 2026"),
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="NCT WISH Official Pop-up Store", brand="SM Entertainment",
         desc="Official pop-up for NCT WISH with fan interaction zones, photo booths, and exclusive Seoul-edition merchandise.",
         loc="Seongsu-dong", date="Apr 27 – May 3, 2026", adm="Free", goods="Seoul-edition MD + photocards",
         tags=["K-Pop","NCT","Fan Event","Seoul Exclusive"],
         why="SM chose Seongsu over SM Town Coex — reflecting the commercial appeal of Seongsu's younger foot traffic.",
         img="NCT WISH official popup store Seoul Seongsu 2026"),
    dict(d="seongsu", cat="Fashion", yr=2026, hot="",
         name="Moncler Puppy Summer Exhibition", brand="Moncler",
         desc="Luxury Italian outerwear brand brings 'Puppy' summer collection in an art-forward exhibition format with seasonal limited pieces.",
         loc="Seongsui-ro 16-gil 31, Seongsu", date="May 1 – May 3, 2026", adm="Free", goods="Limited summer pieces",
         tags=["Luxury","Exhibition","Fashion","Moncler"],
         why="Moncler's gallery-style format elevates brand experience — visitors engage as they would a gallery show.",
         img="Moncler Puppy summer exhibition popup Seoul Seongsu 2026"),
    dict(d="seongsu", cat="Lifestyle", yr=2026, hot="",
         name="Samsung Galaxy Market Event", brand="Samsung Electronics",
         desc="Experiential pop-up at T Factory Seongsu — latest Galaxy devices with hands-on trials and immersive tech zones.",
         loc="T Factory Seongsu, Yeonmujang 1-gil", date="Feb 27 – Mar 29, 2026", adm="Free", goods="Device trial + exclusive bundles",
         tags=["Tech","Samsung","Galaxy","Experiential"],
         why="Tech brands using Seongsu's creative spaces signals the district's broad cultural credibility beyond fashion and beauty.",
         img="Samsung Galaxy popup store Seoul Seongsu T Factory tech"),
    # ── SEONGSU 2025 ──
    dict(d="seongsu", cat="Fashion", yr=2025, hot="",
         name="Hoka Seongsu Pop-up", brand="HOKA",
         desc="Running & trail shoe brand's pop-up with fit experience stations, limited-color drops, and stamp-tour giveaways.",
         loc="East Yeonmujang-gil, Seongsu", date="Jan 2025", adm="Free", goods="Limited colorway + stamp goods",
         tags=["Running","Experiential","Showroom","Sneakers"],
         why="Hoka's shift from performance to lifestyle is embodied in Seongsu — targeting trend-aware consumers, not just runners.",
         img="Hoka running shoes popup store Seoul Seongsu sneakers"),
    dict(d="seongsu", cat="F&B", yr=2025, hot="🔥 Viral",
         name='Adidas Café "3 STRIPES Seoul"', brand="Adidas × Café Concept",
         desc="Fashion meets coffee — a viral social media sensation before it even opened. Three-stripe drinks, limited merch, and brand installations drew massive queues.",
         loc="Seongsu-dong", date="Jan 2025 (~Jan 18)", adm="Free", goods="Limited drinks & merch",
         tags=["Collab","Café","Sports","Viral","SNS"],
         why="Pre-opening social buzz turned this into a must-visit — a case study in anticipation-building without paid advertising.",
         img="Adidas 3 Stripes Cafe popup Seoul Seongsu coffee fashion"),
    dict(d="seongsu", cat="Beauty", yr=2025, hot="✨ Benchmark",
         name="iSOi 'Bulgaria Rose Trip' Pop-up", brand="iSOi",
         desc="Immersive Bulgaria rose concept space at iSOi's Seongsu flagship — a benchmark for brand-owned pop-up strategy with no rental costs.",
         loc="iSOi Flagship, Seongsu", date="Jan 2025", adm="Free", goods="Product samples",
         tags=["Skincare","Immersive","Flagship","Benchmark"],
         why="By owning the pop-up through their flagship, iSOi eliminated rental costs while generating enormous SNS buzz.",
         img="iSOi Bulgaria Rose Trip popup store Seoul Seongsu skincare"),
    dict(d="seongsu", cat="IP · Character", yr=2025, hot="",
         name="TBH × Hello Kitty Department Store", brand="tbh × Sanrio",
         desc="Hello Kitty 50th anniversary collab with co-designed limited apparel, accessories, and collectibles.",
         loc="Seongsu-dong", date="Jan 2025", adm="Free", goods="Limited collab goods",
         tags=["Sanrio","Hello Kitty","Collab","Fashion","50th"],
         why="The Hello Kitty 50th anniversary proved the staying power of legacy IP over trend-driven collabs.",
         img="TBH Hello Kitty 50th anniversary popup Seoul Seongsu Sanrio"),
    # ── SEONGSU 2024 ──
    dict(d="seongsu", cat="Fashion", yr=2024, hot="🏆 Large-scale",
         name="Musinsa Beauty Festa — Seongsu", brand="Musinsa",
         desc="Massive multi-brand pop-up town across Seongsu, bringing online-only beauty brands to their first ever offline spaces.",
         loc="Seongsu-dong (area-wide)", date="2024", adm="Free", goods="Multi-brand beauty & fashion",
         tags=["Pop-up Town","Multi-brand","Large-scale","Pioneering"],
         why="Proved an e-commerce platform could run a physical pop-up town as effectively as a department store.",
         img="Musinsa Beauty Festa Seongsu Seoul popup town 2024"),
    # ── HANNAM ──
    dict(d="hannam", cat="Beauty", yr=2026, hot="✨ Notable",
         name="Pesade Hannam Flagship Opening", brand="Pesade",
         desc="Niche fragrance brand Pesade opens its Hannam flagship with personal scent consultations and exclusive opening-day sets.",
         loc="Hannam-dong Flagship", date="2026", adm="Free", goods="Personal scent consultation + sets",
         tags=["Niche Fragrance","Flagship","Opening","Hannam"],
         why="Hannam's gallery culture makes it the natural home for niche fragrance brands seeking affluent, design-literate consumers.",
         img="Pesade niche fragrance popup Seoul Hannam flagship"),
    dict(d="hannam", cat="Fashion", yr=2025, hot="",
         name='Adidas × ABC Mart — "My Nth New Pair"', brand="ABC Mart × Adidas",
         desc="Season-launch pop-up combining ABC Mart's retail reach with Adidas' newest sneaker lineup and on-site shoe personalisation.",
         loc="Hannam-dong", date="Jan 2025", adm="Free", goods="Limited sneaker lineup",
         tags=["Sneakers","Collab","Customise","Personalise"],
         why="Personalisation services dramatically increase time-in-store and purchase likelihood.",
         img="Adidas ABC Mart sneakers popup Seoul Hannam custom"),
    dict(d="hannam", cat="Art · Exhibition", yr=2025, hot="",
         name="Hannam Emerging Artist Gallery Pop-up", brand="Hannam Independent Gallery Network",
         desc="Rotating platform for emerging Korean artists with works for sale and brand-collab art objects. Buyers receive limited-edition art books.",
         loc="Hannam Gallery District", date="Seasonal, ongoing", adm="Free viewing", goods="Original artworks + art books",
         tags=["Art","Emerging Artist","Sales","Curation"],
         why="Hannam's gallery infrastructure allows emerging artists to access affluent collectors without a permanent space.",
         img="emerging artist gallery popup Seoul Hannam Korean art"),
    dict(d="hannam", cat="Beauty", yr=2025, hot="",
         name="European Niche Perfume — Korea Debut", brand="Hannam Concept Beauty Edit",
         desc="First Korean pop-up for a coveted European niche perfume house. Personal fragrance consultations and limited discovery sets.",
         loc="Hannam Concept Store", date="Seasonal", adm="Free", goods="Discovery sets + consultation",
         tags=["Niche Perfume","Consultation","Debut","European"],
         why="Hannam's international-facing demographic is the ideal test market for European niche brands entering Korea.",
         img="niche perfume popup Seoul Hannam European fragrance"),
    dict(d="hannam", cat="Fashion", yr=2024, hot="",
         name="Hannam Vintage Fashion Market", brand="Hannam Vintage Curators",
         desc="Monthly curated vintage & resale pop-up reflecting MZ consumers' growing interest in sustainable fashion.",
         loc="Hannam-dong", date="Monthly, ongoing", adm="Free", goods="Vintage & resale items",
         tags=["Vintage","Resale","Sustainable","Monthly"],
         why="Sustainable fashion is the fastest-growing MZ sub-trend — Hannam's market taps this with a premium approach.",
         img="vintage fashion market popup Seoul Hannam sustainable resale"),
    dict(d="hannam", cat="Lifestyle", yr=2025, hot="",
         name="Luxury Interior & Home Design Pop-up", brand="Hannam Flagship Brands",
         desc="Premium interior and home brand pop-up offering product experience and consultation services.",
         loc="Hannam-dong", date="Seasonal", adm="Free", goods="Consultation + display items",
         tags=["Interior","Premium","Lifestyle","Consultation"],
         why="Home lifestyle brands use pop-ups to bridge the gap between e-commerce imagery and real-world texture.",
         img="luxury interior home design popup Seoul Hannam lifestyle"),
    # ── HONGDAE ──
    dict(d="hongdae", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="ITZY [Motto] Official Pop-up Store", brand="ITZY × JYP Entertainment",
         desc="Official pop-up tied to ITZY's Motto release with fan merch, photocard events, and Hongdae-only album bundles.",
         loc="Mapo-gu, Hongdae area", date="May 19 – May 25, 2026", adm="Free", goods="Exclusive album bundle + photocards",
         tags=["K-Pop","ITZY","Fan Event","JYP","Hongdae Only"],
         why="Hongdae remains the spiritual home of K-pop fan culture — the natural first choice for comeback pop-ups.",
         img="ITZY Motto official popup store Seoul Hongdae 2026"),
    dict(d="hongdae", cat="IP · Character", yr=2025, hot="🔥 HOT",
         name="Chainsaw Man Official Pop-up", brand="AK Plaza Hongdae × MAPPA",
         desc="Large-scale official anime pop-up with character goods, acrylic standees, apparel, and Korean-market collectibles. Long queues from day one.",
         loc="AK Plaza Hongdae Branch", date="Sep 26 – Dec 31, 2025", adm="Free", goods="Anime character goods",
         tags=["Anime","IP","Goods","MAPPA","Long-run"],
         why="A 3-month run in a department store signals anime IP has become a consistent driver of retail footfall.",
         img="Chainsaw Man official popup store Seoul Hongdae AK Plaza anime"),
    dict(d="hongdae", cat="Beauty", yr=2025, hot="✨ Notable",
         name="Olive Young Hongdae Town — Beauty Event", brand="CJ Olive Young",
         desc="Multi-brand beauty event at Olive Young's Hongdae flagship. Makeup trials, new product demos, and SNS verification giveaways.",
         loc="Olive Young Hongdae Town", date="Oct 2 – Oct 12, 2025", adm="Free", goods="Sample giveaways",
         tags=["K-Beauty","Multi-brand","Trial","SNS","Flagship"],
         why="Olive Young Hongdae's tourist-heavy foot traffic makes it one of the most cost-efficient locations for beauty brands.",
         img="Olive Young Hongdae beauty popup store Seoul K-beauty"),
    dict(d="hongdae", cat="IP · Character", yr=2024, hot="",
         name="K-Pop Official MD Pop-up Hub", brand="Major Entertainment Labels",
         desc="Hongdae's proximity to SM Town makes it a permanent K-pop corridor. Albums, photocards, lightsticks at every major comeback.",
         loc="Hongdae, near SM Town", date="Comeback seasons, ongoing", adm="Free", goods="Random photocard events",
         tags=["K-Pop","Fandom","MD","SM Town","Ongoing"],
         why="Hongdae's role as K-pop's retail heartland is self-reinforcing: fans gather because brands pop up; brands pop up because fans gather.",
         img="K-pop official merchandise popup Seoul Hongdae fan event"),
    dict(d="hongdae", cat="Art · Exhibition", yr=2024, hot="",
         name="Hongdae Indie Artist Market", brand="Hongdae Art Scene",
         desc="Independent artist market selling handmade works, goods, and crafts — a defining feature of Hongdae's creative underground.",
         loc="Hongdae Walk Street", date="2× monthly, ongoing", adm="Free", goods="Handmade works & goods",
         tags=["Handmade","Indie","Market","Authentic"],
         why="The indie artist market represents the grassroots origin of Seoul's pop-up culture.",
         img="Hongdae indie artist market Seoul handmade craft"),
    # ── GANGNAM ──
    dict(d="gangnam", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="Hello Kitty × Jisoo Pop-up", brand="Sanrio × Jisoo (BLACKPINK)",
         desc="Sanrio's Hello Kitty collabs with BLACKPINK's Jisoo. Co-designed fashion pieces, limited character goods, and signature photo zones.",
         loc="Jamsil, Songpa-gu", date="May 1–5, 2026 (Golden Week)", adm="Free", goods="Co-designed limited goods",
         tags=["Sanrio","BLACKPINK","Jisoo","Collab","Golden Week"],
         why="Combining Hello Kitty with Jisoo targets two overlapping fandoms simultaneously — executed during peak visitor season.",
         img="Hello Kitty Jisoo BLACKPINK popup Seoul Jamsil Sanrio 2026"),
    dict(d="gangnam", cat="F&B", yr=2026, hot="",
         name="봄날엔 Spring Dessert Pop-up", brand="Bomnal-en Gangnam",
         desc="Spring-season dessert pop-up in Gangnam with seasonal pastries and cherry blossom period limited menus.",
         loc="Seocho-gu, Gangnam", date="May 19 – May 31, 2026", adm="Free", goods="Seasonal dessert menu",
         tags=["Dessert","Spring","Seasonal","Instagram"],
         why="Seasonal F&B pop-ups timed to cherry blossom season consistently outperform in foot traffic.",
         img="spring dessert popup Seoul Gangnam cherry blossom pastry"),
    dict(d="gangnam", cat="IP · Character", yr=2026, hot="🌿 Outdoor",
         name="Pokémon Secret Forest (Seoul Forest)", brand="Pokémon Mega Festa 2026",
         desc="Outdoor Pokémon pop-up where hidden Pokémon lurk among Seoul Forest trees, tied to the 2026 Seoul International Garden Expo.",
         loc="Seoul Forest, Seongdong-gu", date="May 1 – Jun 21, 2026", adm="Free", goods="Outdoor original goods",
         tags=["Pokémon","Outdoor","Seoul Forest","Garden Expo"],
         why="Taking a pop-up outdoors into Seoul Forest transforms the experience from retail into a nature walk.",
         img="Pokemon Secret Forest Seoul Forest outdoor popup 2026"),
    dict(d="gangnam", cat="IP · Character", yr=2024, hot="🏆 Record",
         name="K League × Sanrio Characters", brand="K League × Sanrio",
         desc="The most successful pop-up of 2024: 250,000 total visitors, averaging 10,500 per day. Textbook cross-fandom collision.",
         loc="The Hyundai Seoul", date="2024", adm="Free", goods="Cross-fandom limited goods",
         tags=["Cross-fandom","Record","Sanrio","K League","Sports"],
         why="Bridges two unconnected communities, doubling potential audience without increasing production complexity.",
         img="K League Sanrio popup The Hyundai Seoul record 2024"),
    dict(d="gangnam", cat="Beauty", yr=2024, hot="🏆 Large-scale",
         name="Coupang Mega Beauty Show", brand="Coupang × 9 Beauty Brands",
         desc="Nine major beauty brands share one pop-up town. Visitors compare, trial, and purchase across all brands simultaneously.",
         loc="Gangnam area large venue", date="2024", adm="Free", goods="Multi-brand trials & purchase",
         tags=["Pop-up Town","Multi-brand","Beauty","Benchmark"],
         why="Coupang coordinating 9 brands shows how e-commerce platforms are emerging as pop-up town operators.",
         img="Coupang Mega Beauty Show popup Seoul multi-brand 2024"),
    dict(d="gangnam", cat="F&B", yr=2024, hot="",
         name="Market Kurly Food Festa", brand="Market Kurly",
         desc="Fresh-food e-commerce platform Kurly brings curated brands offline with live tasting and cooking demos.",
         loc="Gangnam area", date="2024", adm="Free", goods="Premium food items + tasting",
         tags=["F&B","E-commerce","Tasting","Premium"],
         why="Market Kurly's offline Festa bridges a core challenge for food e-commerce: consumers want to taste before buying.",
         img="Market Kurly Food Festa popup Seoul offline 2024"),
    dict(d="gangnam", cat="Art · Exhibition", yr=2025, hot="",
         name="Seoul International Café Show", brand="COEX",
         desc="Korea's largest café & beverage expo with new F&B brand pop-ups, master barista demos, and specialty coffee showcases.",
         loc="COEX, Gangnam", date="Nov 2025", adm="Paid admission", goods="Coffee products + limited brews",
         tags=["Café","Exhibition","Industry","Coffee","COEX"],
         why="The Café Show functions as an annual cultural moment for Seoul's café-obsessed MZ generation.",
         img="Seoul International Cafe Show COEX exhibition 2025"),
    dict(d="gangnam", cat="IP · Character", yr=2024, hot="",
         name="World Webtoon Festival 2024", brand="Webtoon Platform Alliance",
         desc="Major Korean and international webtoon IPs gather for a festival pop-up with author signings and story-world exhibitions.",
         loc="Gangnam area large venue", date="2024", adm="Paid admission", goods="Author-signed goods",
         tags=["Webtoon","IP","Festival","Author","Signing"],
         why="Webtoon IP generates deeply personal connections — fans follow characters for years, making purchases highly emotional.",
         img="World Webtoon Festival popup Seoul exhibition IP 2024"),
    # ── OTHERS ──
    dict(d="others", cat="IP · Character", yr=2026, hot="",
         name="Super Mario Pop-up @ Starfield Hanam", brand="Nintendo × Starfield Hanam",
         desc="Nintendo's Super Mario franchise at Starfield Hanam with interactive game-themed installations and limited merchandise.",
         loc="Starfield Hanam, Gyeonggi", date="May 2026 (Golden Week)", adm="Free", goods="Nintendo limited goods",
         tags=["Nintendo","Mario","Gaming","Interactive","Family"],
         why="Nintendo's strategic use of Golden Week maximises family traffic at a suburban location.",
         img="Super Mario Nintendo popup Starfield Hanam Seoul 2026"),
    dict(d="others", cat="IP · Character", yr=2026, hot="",
         name="TOURS Official Pop-up — Yongsan", brand="TOURS (K-Pop Group)",
         desc="K-Pop group TOURS at Yongsan iPark Mall with fan merch, exclusive Yongsan-edition goods, and photocard events.",
         loc="Yongsan iPark Mall", date="May 1–5, 2026 (Golden Week)", adm="Free", goods="Exclusive Yongsan-edition merch",
         tags=["K-Pop","Fan Event","Yongsan","Golden Week"],
         why="Yongsan's proximity to major transit hubs makes it accessible to fans travelling from across the country.",
         img="TOURS K-pop popup store Yongsan iPark Mall Seoul 2026"),
    dict(d="others", cat="Beauty", yr=2026, hot="",
         name="BeautyPlus Moving × Mise-en-scène", brand="BeautyPlus Universe",
         desc="BeautyPlus's mobile pop-up at Sungshin Women's University in collaboration with hair care brand Mise-en-scène.",
         loc="Seongbuk-gu (Sungshin Women's Univ.)", date="May 19, 2026", adm="Free", goods="Hair care giveaways",
         tags=["Hair Care","Mobile Pop-up","Campus","University"],
         why="Campus-based beauty pop-ups target the MZ demographic at point of brand discovery.",
         img="BeautyPlus mobile popup Seoul campus beauty university"),
    dict(d="others", cat="Art · Exhibition", yr=2025, hot="",
         name="DDP Emerging Designer Pop-up Market", brand="Dongdaemun Design Plaza",
         desc="Emerging designer market at the iconic DDP building with fashion, product design, and crafts curated by category.",
         loc="Dongdaemun Design Plaza (DDP)", date="1–2× monthly, ongoing", adm="Free", goods="Designer pieces & crafts",
         tags=["Emerging Designers","DDP","Market","Architecture"],
         why="The DDP's Zaha Hadid landmark status gives any pop-up hosted there a cultural legitimacy no standard space can provide.",
         img="DDP Dongdaemun Design Plaza designer popup Seoul market"),
    dict(d="others", cat="F&B", yr=2025, hot="",
         name="Lotte Jamsil Seasonal Bakery Pop-up", brand="Lotte Department Store Jamsil",
         desc="Premium seasonal dessert pop-ups at Lotte Jamsil B1 bakery hall with season-limited pastry brands and holiday gift sets.",
         loc="Lotte Dept. Store Jamsil, B1F", date="Seasonal", adm="Free", goods="Seasonal pastries + gift sets",
         tags=["Dessert","Gift Set","Seasonal","Jamsil","Bakery"],
         why="Department store bakery event halls are the most reliable pop-up format in Korea — low risk, high impulse purchase rate.",
         img="Lotte Jamsil seasonal bakery popup dessert Seoul"),
    dict(d="others", cat="Fashion", yr=2025, hot="",
         name="SYSTEM FW25 Pop-up — Lotte World Mall", brand="SYSTEM",
         desc="Korean contemporary fashion brand SYSTEM's FW25 collection launch pop-up with pre-order sessions and early access.",
         loc="Lotte World Mall, Jamsil", date="~ Nov 6, 2025", adm="Free", goods="FW25 early access + pre-order",
         tags=["Contemporary Fashion","FW25","Pre-order","Korean Brand"],
         why="SYSTEM's use of Lotte World Mall expands its reach beyond Seongsu's fashion bubble to mainstream MZ consumers.",
         img="SYSTEM FW25 fashion popup Lotte Seoul"),

    # ── SEONGSU 2026 NEW ──
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="Toy Story 'House of Toy Story' Pop-up", brand="Pixar × Seongsu",
         desc="Pixar's Toy Story recreates a 1970s-80s American home across multiple floors. Photo zones with Woody, Buzz & Jessie, arcade-style games, DIY merch stations, and exclusive collectibles.",
         loc="Seongsu-dong", date="May 23 – Jul 12, 2026", adm="Free", goods="Exclusive collectibles + DIY merch",
         tags=["Pixar","Toy Story","IP","Nostalgia","Photo Zone"],
         why="Toy Story's multi-generational appeal — beloved by both MZ parents and their children — makes it one of the broadest-reach IP pop-ups of 2026.",
         img="Toy Story popup store Seoul Seongsu 2026"),
    dict(d="seongsu", cat="Fashion", yr=2026, hot="🔥 HOT",
         name="Nice Ghost Club × Cowboy Bebop Pop-up", brand="Nice Ghost Club × Sunrise",
         desc="Korean streetwear label Nice Ghost Club teams up with cult anime Cowboy Bebop. Graphic tees, accessories, and limited-run pieces reinterpreting Spike, Faye, and the Bebop crew.",
         loc="Seongsu-dong", date="May 26 – Jun 11, 2026", adm="Free", goods="Exclusive Seongsu-drop pieces",
         tags=["Streetwear","Cowboy Bebop","Anime","Collab","Limited"],
         why="Cowboy Bebop's global cult following combined with Nice Ghost Club's local credibility creates a rare crossover between Korean streetwear and classic anime aesthetics.",
         img="Nice Ghost Club Cowboy Bebop popup Seongsu Seoul"),
    dict(d="seongsu", cat="Fashion", yr=2026, hot="",
         name="Gentle Monster × Disney × F1 Circuit Collection", brand="Gentle Monster",
         desc="Eyewear brand Gentle Monster launches an F1-inspired collab with Disney. Limited circuit-edition sunglasses, immersive racing track installation, and exclusive photo moments.",
         loc="Gentle Monster Seongsu Flagship", date="Apr – May 2026", adm="Free", goods="Limited F1 circuit sunglasses",
         tags=["Gentle Monster","Disney","F1","Eyewear","Collab"],
         why="Gentle Monster's flagship pop-ups are among Seoul's most architecturally impressive — this collab fuses motorsport culture with Disney's IP in an only-in-Seoul installation.",
         img="Gentle Monster Disney F1 popup Seoul 2026"),
    dict(d="seongsu", cat="F&B", yr=2026, hot="",
         name="Dango-ne Haengnidan Seongsu Pop-up", brand="Dango-ne",
         desc="Viral handmade Japanese dango brand from Haengnidan-gil brings its signature chewy skewers to Seongsu for a two-month limited run.",
         loc="Seongsu-dong", date="May – Jun 2026", adm="Free", goods="Handmade dango skewers",
         tags=["F&B","Japanese","Dango","Viral","Street Food"],
         why="Dango-ne's cult status in Haengnidan makes this Seongsu pop-up a destination for fans who missed the original — a perfect F&B cross-district expansion model.",
         img="Dango-ne dango popup Seoul street food"),
    dict(d="seongsu", cat="Beauty", yr=2026, hot="",
         name="Torriden Seongsu Pop-up", brand="Torriden",
         desc="Science-based K-beauty brand Torriden opens a dedicated Seongsu pop-up showcasing its hyaluronic acid and barrier-care lineup with skin analysis stations.",
         loc="Seongsu-dong", date="Dec 2025 – Jan 2026", adm="Free", goods="Skin analysis + product samples",
         tags=["K-Beauty","Skincare","Hyaluronic Acid","Science"],
         why="Torriden's data-driven skin analysis stations elevate the pop-up from a sales space into an educational experience — a growing trend in K-beauty retail.",
         img="Torriden K-beauty popup store Seoul skincare"),
    dict(d="seongsu", cat="Beauty", yr=2026, hot="",
         name="Hince Beauty Pop-up", brand="Hince",
         desc="Korean minimalist beauty brand Hince hosts a Seongsu pop-up featuring its signature matte lipsticks and new skincare line with curated pastel interiors.",
         loc="Seongsu-dong", date="Nov 2025 – Jan 2026", adm="Free", goods="Limited-edition colour sets",
         tags=["K-Beauty","Makeup","Minimalist","Hince"],
         why="Hince's aesthetic-first approach to retail design makes its pop-ups photographable destinations — the brand understands that the space itself is the marketing.",
         img="Hince beauty popup Seoul minimalist makeup"),
    dict(d="seongsu", cat="Beauty", yr=2026, hot="",
         name="Lavoir Seongsu Pop-up", brand="Lavoir",
         desc="French-inspired Korean fragrance and body care brand Lavoir opens a Seongsu pop-up with its signature laundry-aesthetic concept store.",
         loc="Seongsu-dong", date="Nov 2025 – Jan 2026", adm="Free", goods="Fragrance + body care sets",
         tags=["Fragrance","Body Care","French-inspired","Concept Store"],
         why="Lavoir's laundry-room aesthetic concept is immediately Instagram-worthy — proving that distinctive spatial design outperforms product-only marketing.",
         img="Lavoir fragrance popup Seoul concept store"),
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="",
         name="(G)I-DLE Exhibition Pop-up", brand="(G)I-DLE × Space S50",
         desc="K-pop group (G)I-DLE's exhibition-format pop-up at Space S50 in Seongsu. Fan art installations, exclusive merchandise, and photocard events for NEVERLAND fans.",
         loc="Space S50, 50 Seongsui-ro, Seongsu", date="Dec 19, 2025 – Jan 10, 2026", adm="Free", goods="Exhibition merch + photocards",
         tags=["K-Pop","(G)I-DLE","Exhibition","Fan Event"],
         why="Exhibition-format K-pop pop-ups are growing in sophistication — (G)I-DLE's art installations blur the line between fan merchandise event and gallery experience.",
         img="G I-DLE exhibition popup Seoul Seongsu fan"),
    dict(d="seongsu", cat="Art · Exhibition", yr=2026, hot="",
         name="Where's Wally? Exhibition", brand="Martin Handford × Seoul Laitium",
         desc="The iconic search-and-find character Wally comes to Seoul Forest's The Seoul Laitium. Interactive large-scale installations and limited Korean-market Wally merchandise.",
         loc="Seoul Forest, The Seoul Laitium", date="Dec 22, 2025 – Apr 5, 2026", adm="Paid admission", goods="Limited Wally merch",
         tags=["Exhibition","Where's Wally","Interactive","Family"],
         why="Classic character IPs like Wally generate cross-generational appeal — parents bring children, creating unusually long average visit times and higher per-group spending.",
         img="Where's Wally exhibition Seoul interactive"),
    dict(d="seongsu", cat="Fashion", yr=2025, hot="",
         name="Musinsa Empty × Lacoste × Sanrio", brand="Musinsa × Lacoste × Sanrio",
         desc="Triple collab pop-up in Seongsu combining Musinsa's streetwear curation, Lacoste's preppy heritage, and Sanrio's character universe into one space.",
         loc="Seongsu, Musinsa Empty", date="Sep 29 – Oct 10, 2025", adm="Free", goods="Triple collab limited goods",
         tags=["Musinsa","Lacoste","Sanrio","Triple Collab"],
         why="The Musinsa Empty format of triple collabs shows how multi-brand pop-ups can create cultural moments bigger than any single brand could alone.",
         img="Musinsa Lacoste Sanrio collab popup Seoul Seongsu"),
    dict(d="seongsu", cat="Art · Exhibition", yr=2025, hot="",
         name="The Museum Visitor × Danit Pop-up", brand="Daerim Changgo, Seongsu",
         desc="Art and fashion hybrid pop-up at the iconic Daerim Changgo warehouse. Museum-style curation meets wearable art in a space that blurs gallery and retail.",
         loc="Daerim Changgo, Seongsu", date="Oct 2 – Oct 9, 2025", adm="Free", goods="Wearable art pieces",
         tags=["Art","Fashion","Warehouse","Hybrid","Seongsu"],
         why="The Daerim Changgo venue — a repurposed factory — provides a backdrop that makes even simple installations feel monumental.",
         img="art fashion popup Daerim Changgo Seongsu warehouse Seoul"),
    dict(d="seongsu", cat="Art · Exhibition", yr=2025, hot="",
         name="Hightech Seoul Event at S Factory", brand="S Factory, Seongsu",
         desc="Tech-art crossover exhibition at Seongsu's S Factory. Digital art installations, interactive tech experiences, and a curated selection of tech-adjacent lifestyle brands.",
         loc="S Factory, Seongsu", date="Oct 2 – Nov 8, 2025", adm="Paid", goods="Tech art merchandise",
         tags=["Tech Art","Exhibition","Interactive","Digital"],
         why="S Factory's industrial scale allows for tech-art installations that smaller venues cannot accommodate — positioning Seongsu as a destination for digital culture.",
         img="tech art exhibition Seoul S Factory Seongsu digital"),
    dict(d="seongsu", cat="Fashion", yr=2025, hot="",
         name="New Balance × Korean Webtoon Artist Pop-up", brand="New Balance × Webtoon",
         desc="New Balance teams up with a Korean webtoon artist and marathon runner for a limited Seongsu pop-up celebrating running culture and local creativity.",
         loc="Seongsu-dong", date="May – Jun 2026", adm="Free", goods="Collab sneakers + webtoon art prints",
         tags=["New Balance","Webtoon","Running","Collab","Art"],
         why="New Balance's sustained investment in running culture pop-ups in Seongsu mirrors the district's own transformation — both brand and neighbourhood have repositioned from functional to aspirational.",
         img="New Balance popup store Seoul Seongsu running sneakers"),
    dict(d="seongsu", cat="Beauty", yr=2025, hot="",
         name="NUDAKE × Jennie Pop-up", brand="NUDAKE × Jennie (BLACKPINK)",
         desc="BLACKPINK's Jennie collaborates with experimental Seoul dessert brand NUDAKE for a pastry and beauty lifestyle pop-up at Haus Dosan, Apgujeong.",
         loc="Haus Dosan, Apgujeong-ro 46-gil 50", date="Nov 28, 2024 – Jan 3, 2025", adm="Free", goods="Limited dessert + lifestyle items",
         tags=["BLACKPINK","Jennie","Dessert","Lifestyle","Collab"],
         why="NUDAKE's collab with Jennie bridges the worlds of K-pop fandom, luxury dessert culture, and lifestyle retail — a template for how celebrity IP can elevate an F&B brand.",
         img="NUDAKE Jennie BLACKPINK popup Haus Dosan Seoul dessert"),
    dict(d="seongsu", cat="Fashion", yr=2024, hot="",
         name="Nike 'Air Force 1 Seoul Edition' Pop-up", brand="Nike Korea",
         desc="Nike's Seoul-exclusive Air Force 1 drop with local artist collabs, customisation stations, and an interactive 'Seoul Streets' installation celebrating the city's sneaker culture.",
         loc="Seongsu-dong", date="2024", adm="Free", goods="Seoul-edition AF1 + custom options",
         tags=["Nike","Air Force 1","Sneakers","Seoul Edition","Custom"],
         why="Nike's city-edition drops have become annual cultural events — the Seongsu location ensures the brand speaks directly to Seoul's most trend-sensitive consumer segment.",
         img="Nike Air Force 1 Seoul Edition popup sneakers"),

    # ── HANNAM NEW ──
    dict(d="hannam", cat="Fashion", yr=2026, hot="✨ Notable",
         name="Gentle Monster Haus Dosan Flagship Experience", brand="Gentle Monster",
         desc="Gentle Monster's Haus Dosan flagship in Apgujeong runs rotating immersive installations. Part gallery, part eyewear store — each season brings a completely new spatial concept.",
         loc="Haus Dosan, Apgujeong-ro, Gangnam", date="Ongoing, seasonal", adm="Free", goods="Limited-edition eyewear",
         tags=["Gentle Monster","Flagship","Gallery","Eyewear","Immersive"],
         why="Gentle Monster set the template for the 'retail as theatre' model that now defines Seoul's best pop-ups — every other brand is catching up to what Gentle Monster pioneered.",
         img="Gentle Monster Haus Dosan flagship Seoul immersive"),
    dict(d="hannam", cat="Beauty", yr=2025, hot="",
         name="Tamburins × BLACKPINK Jennie Pop-up", brand="Tamburins × Jennie",
         desc="Luxury Korean beauty and lifestyle brand Tamburins collaborates with Jennie of BLACKPINK. Object-art meets skincare in a gallery-style Hannam space.",
         loc="Hannam-dong", date="2025", adm="Free", goods="Limited collab beauty objects",
         tags=["Tamburins","Jennie","BLACKPINK","Art Beauty","Gallery"],
         why="Tamburins's object-art approach to beauty retail — treating products as collectible sculptures — has inspired a wave of 'beauty as art' pop-ups across Hannam.",
         img="Tamburins Jennie BLACKPINK popup Seoul beauty"),
    dict(d="hannam", cat="F&B", yr=2025, hot="",
         name="Blue Bottle Coffee Seasonal Pop-up", brand="Blue Bottle Coffee Korea",
         desc="Blue Bottle Coffee's limited seasonal pop-up in Hannam featuring single-origin Korea-only blends and specialty equipment collaborations.",
         loc="Hannam-dong", date="Seasonal", adm="Free", goods="Korea-exclusive blends + drinkware",
         tags=["Coffee","Blue Bottle","Specialty","Seasonal","Hannam"],
         why="Blue Bottle's minimalist aesthetic resonates with Hannam's design-literate consumer base — their pop-ups feel like concept cafés, not marketing events.",
         img="Blue Bottle Coffee popup Seoul Korea seasonal"),
    dict(d="hannam", cat="Art · Exhibition", yr=2025, hot="",
         name="Wunderkammer Gallery Pop-up", brand="Independent Curators, Hannam",
         desc="Rotating art object and curiosity cabinet-style gallery pop-up in Hannam. Emerging Korean artists present collectible small-format works alongside collaborative brand objects.",
         loc="Hannam-dong Gallery District", date="Monthly rotation", adm="Free", goods="Collectible art objects",
         tags=["Gallery","Art Objects","Collectible","Emerging","Rotating"],
         why="The 'wunderkammer' (wonder cabinet) format — curating surprising juxtapositions of objects — is perfectly suited to Hannam's culture of discovery shopping.",
         img="gallery popup Hannam Seoul art objects collectible"),
    dict(d="hannam", cat="Lifestyle", yr=2026, hot="",
         name="Aestura Derma Pop-up", brand="Aestura (Amorepacific)",
         desc="Amorepacific's derma care brand Aestura opens a Hannam pop-up with personalised skin consultation, barrier repair testing, and a limited slow-living product line.",
         loc="Hannam-dong", date="2026", adm="Free", goods="Personalised skin kit",
         tags=["Derma","Skincare","Aestura","Personalised","Amorepacific"],
         why="Derma-positioning in a Hannam lifestyle space rather than a pharmacy shifts brand perception from medical to aspirational — a strategic repositioning move.",
         img="Aestura derma skincare popup Seoul Hannam"),

    # ── HONGDAE NEW ──
    dict(d="hongdae", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="3학년Z반 긴파치 선생 Pop-up", brand="AK Plaza Hongdae",
         desc="The hit Japanese anime '3-nen Z-gumi Ginpachi-sensei' gets its first major Korean pop-up at Hongdae's AK Plaza. Character goods, classroom photo zones, and exclusive Korean-market merch.",
         loc="AK Plaza Hongdae", date="May 1–5, 2026 (Golden Week)", adm="Free", goods="Character goods + photocards",
         tags=["Anime","Japanese IP","Character","Hongdae","Golden Week"],
         why="Japanese anime IP pop-ups in Hongdae's AK Plaza have become a reliable fixture — the location's density of anime fans creates immediate queues on opening day.",
         img="3nen Z-gumi Ginpachi sensei anime popup Seoul Hongdae"),
    dict(d="hongdae", cat="IP · Character", yr=2026, hot="",
         name="White Tiger & Black Tiger Pop-up", brand="Webtoon IP × Hongdae",
         desc="Korean webtoon IP 'White Tiger and Black Tiger' gets a dedicated Hongdae pop-up with character goods, illustration prints, and fan meet events.",
         loc="Hongdae / Sinchon area", date="May 1–5, 2026 (Golden Week)", adm="Free", goods="Webtoon IP goods",
         tags=["Webtoon","Korean IP","Character","Fan Meet"],
         why="Korean webtoon IPs are increasingly commanding the same pop-up energy as Japanese anime — a shift reflecting the growing global reach of the webtoon format.",
         img="webtoon character popup Seoul Hongdae Korean IP"),
    dict(d="hongdae", cat="F&B", yr=2025, hot="",
         name="Starbucks Reserve 'Korea Heritage' Pop-up", brand="Starbucks Korea",
         desc="Starbucks Reserve's Korea-exclusive seasonal pop-up in Hongdae celebrating Korean traditional flavours — yuzu, sikhye, and hojicha — in premium RTD and merchandise format.",
         loc="Hongdae, Starbucks Reserve", date="Seasonal 2025", adm="Free", goods="Korea-exclusive blends + tumblers",
         tags=["Starbucks","Coffee","Korea Heritage","Premium","Seasonal"],
         why="Starbucks Reserve Korea's seasonal pop-up format has mastered the art of creating product scarcity — limited tumblers sell out within hours, generating organic viral content.",
         img="Starbucks Reserve Korea Heritage popup Seoul seasonal"),
    dict(d="hongdae", cat="Fashion", yr=2025, hot="",
         name="Covernat × Thisisneverthat Joint Pop-up", brand="Covernat × Thisisneverthat",
         desc="Two of Korea's most respected streetwear brands — Covernat and Thisisneverthat — join forces for a Hongdae flagship collab pop-up featuring co-designed capsule pieces.",
         loc="Hongdae Flagship Area", date="2025", adm="Free", goods="Co-designed capsule collection",
         tags=["Streetwear","Covernat","Thisisneverthat","Capsule","Collab"],
         why="When two credible Korean streetwear brands collab, the cultural weight is additive — both fanbases converge, creating a combined audience neither brand could reach alone.",
         img="Covernat Thisisneverthat streetwear popup Seoul Hongdae"),
    dict(d="hongdae", cat="Beauty", yr=2026, hot="",
         name="Fwee K-Beauty Colour Pop-up", brand="Fwee",
         desc="Fwee's colour-focused K-beauty pop-up in Seongsu/Hongdae featuring their signature blush and lip products in a pastel-maximalist concept space.",
         loc="Seongsu / Hongdae area", date="2025 – 2026", adm="Free", goods="Limited colour sets",
         tags=["K-Beauty","Colour","Fwee","Pastel","Makeup"],
         why="Fwee's colour-first brand identity translates naturally into an immersive pop-up environment — the products ARE the decoration.",
         img="Fwee K-beauty color popup Seoul makeup pastel"),

    # ── GANGNAM NEW ──
    dict(d="gangnam", cat="F&B", yr=2026, hot="",
         name="Sand Museum Pop-up Yeouido", brand="Sand Museum",
         desc="Unique sand art experience pop-up at Yeouido. Visitors create personalised sand art bottles and watch live sand animation performances.",
         loc="Yeouido, Seoul", date="May 1–5, 2026 (Golden Week)", adm="Paid admission", goods="Personalised sand art bottle",
         tags=["Art Experience","Sand","Yeouido","Interactive","Craft"],
         why="Experience-over-product pop-ups like Sand Museum have the highest word-of-mouth spread — the product (your sand bottle) becomes a walking advertisement.",
         img="Sand Museum popup Seoul experience craft art"),
    dict(d="gangnam", cat="IP · Character", yr=2026, hot="",
         name="Butter Bear Pop-up", brand="Butter Bear IP",
         desc="Adorable honey-coloured bear character Butter Bear gets a dedicated Gangnam pop-up with plush goods, café-style drinks, and photo zones.",
         loc="Gangnam, Seoul", date="May 2026", adm="Free", goods="Butter Bear plush + café menu",
         tags=["Character","Bear","Cute","Café","Golden Week"],
         why="Bear character IPs have dominated Korean pop-up culture since BT21's Shooky and RJ — Butter Bear's warm colour palette appeals to the aesthetic-first Gen Z consumer.",
         img="Butter Bear character popup Seoul cafe cute"),
    dict(d="gangnam", cat="Fashion", yr=2025, hot="✨ Notable",
         name="Ader Error Seongsu × Gangnam Crossover", brand="Ader Error",
         desc="Experimental Korean fashion brand Ader Error's rotating pop-up series spanning Seongsu and Garosu-gil. Asymmetric cuts, oversized silhouettes, and spatial design that challenges retail conventions.",
         loc="Garosu-gil, Gangnam / Seongsu-dong", date="Ongoing seasonal", adm="Free", goods="Seasonal capsule pieces",
         tags=["Ader Error","Experimental Fashion","Capsule","Garosu-gil"],
         why="Ader Error defines what happens when fashion brand and spatial design merge — every pop-up is also an architecture statement.",
         img="Ader Error popup Seoul experimental fashion Korea"),
    dict(d="gangnam", cat="Beauty", yr=2025, hot="",
         name="Sulwhasoo 'Han Radiance' Flagship Pop-up", brand="Sulwhasoo (Amorepacific)",
         desc="Korea's premier luxury herbal beauty brand Sulwhasoo transforms its Apgujeong flagship into an immersive hanok-inspired pop-up celebrating Korean botanical heritage.",
         loc="Apgujeong, Gangnam", date="2025", adm="Free", goods="Heritage beauty sets + limited ginseng line",
         tags=["Luxury Beauty","Sulwhasoo","Herbal","Hanok","Heritage"],
         why="Sulwhasoo's hanok-inspired pop-up design serves both domestic and international visitors — it positions K-beauty within Korea's broader cultural heritage narrative.",
         img="Sulwhasoo luxury beauty popup Seoul Apgujeong hanok"),
    dict(d="gangnam", cat="IP · Character", yr=2025, hot="",
         name="NewJeans × McDonald's Seoul Pop-up", brand="NewJeans × McDonald's Korea",
         desc="K-pop supergroup NewJeans collabs with McDonald's Korea for a limited Gangnam pop-up café experience featuring character-themed meals and merchandise.",
         loc="Gangnam area", date="2025", adm="Free", goods="Character meals + limited goods",
         tags=["K-Pop","NewJeans","McDonald's","Food","Collab"],
         why="The NewJeans × McDonald's Korea collab demonstrated that fast food brands can achieve luxury pop-up prestige through the right K-pop partnership.",
         img="NewJeans McDonalds Korea popup cafe Seoul"),

    # ── OTHERS NEW ──
    dict(d="others", cat="IP · Character", yr=2026, hot="",
         name="Nidi Girl × Overdose Collab Café", brand="Nidi Girl × Café Overdose",
         desc="Korean character brand Nidi Girl collaborates with Gwangjin-gu café Overdose for a limited character-themed café pop-up with exclusive Nidi Girl drinks and goods.",
         loc="Gwangjin-gu, Seoul", date="May 2026", adm="Free", goods="Character drinks + goods",
         tags=["Character","Café","Collab","Korean IP","Gwangjin"],
         why="Character café collabs in residential neighbourhoods like Gwangjin represent the suburbanisation of Seoul's pop-up culture — moving beyond the Seongsu/Hannam axis.",
         img="Nidi Girl character cafe popup Seoul collab"),
    dict(d="others", cat="IP · Character", yr=2026, hot="",
         name="JB Kids Pop-up @ Yeongdeungpo", brand="Jieef × Baller Kids",
         desc="Children's character brand JB Kids opens a pop-up at Yeongdeungpo IFC Mall targeting young families with interactive play zones and character merchandise.",
         loc="IFC Mall, Yeongdeungpo", date="May 2026", adm="Free", goods="Character toys + goods",
         tags=["Kids","Character","Family","IFC Mall","Yeongdeungpo"],
         why="Pop-ups targeting children at IFC Mall represent a strategic shift — brands are investing in the next generation of consumers while capturing today's family spending.",
         img="kids character popup IFC Mall Seoul family"),
    dict(d="others", cat="F&B", yr=2026, hot="",
         name="Guomanduzi Pop-up Anyang", brand="Guomanduzi",
         desc="Viral Chinese-style dumpling brand Guomanduzi opens a pop-up in Anyang during Golden Week 2026, bringing its signature pan-fried dumplings to the greater Seoul area.",
         loc="Anyang, Gyeonggi", date="May 2026 (Golden Week)", adm="Free", goods="Signature pan-fried dumplings",
         tags=["F&B","Dumplings","Chinese","Viral","Anyang"],
         why="Viral F&B pop-ups expanding from central Seoul to Gyeonggi satellite cities signal the format's democratisation — pop-up culture is no longer exclusively a Seoul phenomenon.",
         img="dumpling popup street food Korea Seoul viral"),
    dict(d="others", cat="Art · Exhibition", yr=2025, hot="",
         name="Coex Artium Cultural Pop-ups", brand="Coex Artium",
         desc="Coex Artium's rotating pop-up programme hosts Korean and international artists in the underground mall's gallery space, combining retail with cultural programming.",
         loc="Coex Artium, Gangnam", date="Ongoing monthly rotation", adm="Free", goods="Limited art prints + goods",
         tags=["Art","Gallery","Coex","Underground","Rotating"],
         why="Coex Artium's underground gallery space creates a captive audience of shoppers who become art viewers — one of Seoul's most effective art-retail hybrid formats.",
         img="Coex Artium gallery popup Seoul cultural underground"),
    dict(d="others", cat="Fashion", yr=2026, hot="",
         name="Jeep Kids Pop-up @ Yeongdeungpo", brand="Jeep Kids",
         desc="Children's outdoor lifestyle brand Jeep Kids pops up at Yeongdeungpo IFC Mall with miniature adventure gear, customisation stations, and family photo zones.",
         loc="IFC Mall, Yeongdeungpo", date="May 2026", adm="Free", goods="Kids outdoor gear",
         tags=["Kids","Outdoor","Jeep","Family","Lifestyle"],
         why="Outdoor lifestyle brands targeting children in pop-up format are capitalising on post-pandemic parents' emphasis on active family experiences.",
         img="Jeep Kids outdoor popup Seoul family lifestyle"),
    dict(d="others", cat="F&B", yr=2025, hot="",
         name="French Louvre Baguette Pop-up", brand="Paris Baguette × Louvre",
         desc="Paris Baguette's collab with the Louvre Museum brings art-themed pastries and Louvre-licenced merchandise to a Korean bakery pop-up experience.",
         loc="Seoul (multiple locations)", date="2025", adm="Free", goods="Art-themed pastries + Louvre merch",
         tags=["Bakery","Louvre","Art","Collab","Paris Baguette"],
         why="The Louvre × Paris Baguette collab is a masterclass in cultural licensing — it positions a mass-market Korean bakery brand within the prestige of French cultural heritage.",
         img="Paris Baguette Louvre collab bakery popup Korea"),
]

df = pd.DataFrame(POPUPS)

df = pd.DataFrame(POPUPS)

# ── COLOUR CONFIG ─────────────────────────────────────────────────────────────
CAT_COLORS = {
    "Fashion":          "#ff6b9d",
    "Beauty":           "#a78bfa",
    "F&B":              "#ff9a3c",
    "IP · Character":   "#ffd166",
    "Art · Exhibition": "#4ade80",
    "Lifestyle":        "#60a5fa",
}
CAT_CSS = {
    "Fashion":          "cat-fashion",
    "Beauty":           "cat-beauty",
    "F&B":              "cat-fb",
    "IP · Character":   "cat-ip",
    "Art · Exhibition": "cat-art",
    "Lifestyle":        "cat-lifestyle",
}
DIST_INFO = {
    "seongsu": {
        "num":"01","name":"Seongsu-dong","sub":"Seoul's #1 Pop-up District · 성수동","color":"#ff6b9d",
        "desc":"A former industrial zone of repurposed factories, Seongsu hosts more pop-ups than any other neighbourhood in Korea. East Yeonmujang-gil is the current hotspot — 2026 brings Pokémon Mega Festa, BLACKPINK DEADLINE, and Musinsa's new megastore.",
    },
    "hannam": {
        "num":"02","name":"Hannam-dong","sub":"Premium Lifestyle Belt · 한남동","color":"#00e5cc",
        "desc":"Seoul's gallery and boutique corridor. Hannam attracts luxury, niche fragrance, and art-forward pop-ups. The Hangang-jin to Hannam Crossroads stretch is lined with curated independent spaces favoured by design-conscious consumers.",
    },
    "hongdae": {
        "num":"03","name":"Hongdae","sub":"University Culture · 홍대","color":"#a78bfa",
        "desc":"University culture meets indie creativity. Hongdae is the epicentre for K-pop fan pop-ups, beauty events, and independent artist markets. AK Plaza Hongdae and Olive Young Hongdae Town are key anchor venues in 2025–2026.",
    },
    "gangnam": {
        "num":"04","name":"Gangnam · The Hyundai","sub":"Retail Power Zone · 강남 · 여의도","color":"#ffd166",
        "desc":"The Hyundai Seoul in Yeouido rivals Seongsu as Korea's top pop-up venue. K League × Sanrio here drew 250,000 visitors in 2024. Department stores and malls drive high-volume, sales-focused pop-ups across all categories.",
    },
    "others": {
        "num":"05","name":"Other Areas","sub":"Jamsil · Yongsan · DDP · Myeongdong","color":"#ff9a3c",
        "desc":"Pop-up culture has spread across all of Seoul. Department stores, outlet malls, and campus areas now serve as key pop-up venues, reflecting the democratisation of the format beyond its Seongsu epicentre.",
    },
}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:12px 0 6px'>
      <p style='font-family:"DM Mono",monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#00e5cc !important;margin-bottom:5px'>Research Project</p>
      <p style='font-family:"Syne",sans-serif;font-size:1.3rem;font-weight:800;margin-bottom:2px'>Jooeun Lim</p>
      <p style='font-family:"DM Mono",monospace;font-size:11px;color:#6b7280 !important;margin:0'>SKKU · Department of Dance</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    all_cats  = sorted(df["cat"].unique())
    sel_cats  = st.multiselect("Category", all_cats, default=all_cats)

    all_years = sorted(df["yr"].unique())
    sel_years = st.multiselect("Year", all_years, default=all_years)

    dist_name_map = {k: v["name"] for k, v in DIST_INFO.items()}
    sel_dist_names = st.multiselect("District", list(dist_name_map.values()), default=list(dist_name_map.values()))
    sel_dists = [k for k, v in dist_name_map.items() if v in sel_dist_names]

    search_q = st.text_input("🔍 Search brand / name", "")
    st.divider()
    st.caption("Data sources: Popga (1,431 entries 2024) · Seongsu Gorilla · Inside Seoul · DealSeoul · Field Research 2024–2026")

# ── FILTER ────────────────────────────────────────────────────────────────────
mask = (
    df["cat"].isin(sel_cats) &
    df["yr"].isin(sel_years) &
    df["d"].isin(sel_dists)
)
if search_q:
    q = search_q.lower()
    mask = mask & (
        df["name"].str.lower().str.contains(q) |
        df["brand"].str.lower().str.contains(q)
    )
filtered = df[mask].reset_index(drop=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-label">MZ Generation Research · Jooeun Lim · SKKU Dance</div>
  <div class="hero-title">
    <span class="t1">Seoul Pop-up Store</span>
    <span class="t2">Trend Map 2024–2026</span>
  </div>
  <div class="year-pills">
    <span class="ypill">2024–2026</span>
    <span class="ypill y2024">2024</span>
    <span class="ypill y2025">2025</span>
    <span class="ypill y2026">2026 — Live Data</span>
  </div>
  <p class="hero-sub">A field-research database by <b>Jooeun Lim</b> mapping Seoul's pop-up culture across
  Seongsu, Hannam, Hongdae, Gangnam and beyond. Covers 2024 through spring <b>2026</b>.</p>
  <div class="stat-row">
    <div class="stat"><div class="stat-n">{len(filtered)}</div><div class="stat-l">Showing</div></div>
    <div class="stat"><div class="stat-n">{len(df)}</div><div class="stat-l">Total Listed</div></div>
    <div class="stat"><div class="stat-n">5</div><div class="stat-l">Districts</div></div>
    <div class="stat"><div class="stat-n">1,431</div><div class="stat-l">2024 Nationwide</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋  Pop-up Directory", "📊  Data & Charts", "💡  Key Trends"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DIRECTORY  (district button selector)
# ══════════════════════════════════════════════════════════════════════════════
with tab1:

    # ── District selector buttons ──────────────────────────────────────────
    # CSS for district buttons
    st.markdown("""
    <style>
    /* District selector row */
    .dist-btn-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 28px; }
    div[data-testid="column"] > div > div > div > button {
        width: 100% !important;
        background: #0d1221 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #6b7280 !important;
        border-radius: 2px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 14px 8px !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
    }
    div[data-testid="column"] > div > div > div > button:hover {
        border-color: rgba(255,255,255,0.3) !important;
        color: #f0eee8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Session state for image modal
    if "show_img" not in st.session_state:
        st.session_state.show_img = False
    if "img_query" not in st.session_state:
        st.session_state.img_query = ""
    if "img_name" not in st.session_state:
        st.session_state.img_name = ""

    DIST_ORDER = ["seongsu", "hannam", "hongdae", "gangnam", "others"]

    # Session state for selected district
    if "sel_dist" not in st.session_state:
        st.session_state.sel_dist = "seongsu"

    # Button row — one button per district
    btn_cols = st.columns(5)
    for i, dk in enumerate(DIST_ORDER):
        info = DIST_INFO[dk]
        c    = info["color"]
        cnt  = len(filtered[filtered["d"] == dk])
        is_active = (st.session_state.sel_dist == dk)
        label = f"{'▶ ' if is_active else ''}{info['name']}\n{cnt} pop-ups"
        with btn_cols[i]:
            # Active button gets a coloured border via inline style hack
            if is_active:
                st.markdown(f"""
                <div style="border:2px solid {c};border-radius:4px;padding:0;margin-bottom:8px">
                  <div style="background:rgba(255,255,255,0.03);padding:14px 10px;text-align:center">
                    <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.14em;
                                text-transform:uppercase;color:{c};margin-bottom:4px">{info['num']}</div>
                    <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:800;
                                color:{c};margin-bottom:3px">{info['name']}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:10px;color:{c};opacity:.7">{cnt} pop-ups</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="border:1px solid rgba(255,255,255,0.08);border-radius:4px;padding:0;margin-bottom:8px">
                  <div style="padding:14px 10px;text-align:center">
                    <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.14em;
                                text-transform:uppercase;color:#4b5563;margin-bottom:4px">{info['num']}</div>
                    <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:800;
                                color:#9ca3af;margin-bottom:3px">{info['name']}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:10px;color:#4b5563">{cnt} pop-ups</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"Select", key=f"distbtn_{dk}", use_container_width=True):
                st.session_state.sel_dist = dk
                st.rerun()

    # ── Show selected district ─────────────────────────────────────────────
    active_key = st.session_state.sel_dist
    info  = DIST_INFO[active_key]
    color = info["color"]

    sub_df = filtered[filtered["d"] == active_key]

    # District header
    st.markdown(f"""
    <div class="dist-hdr">
      <span class="dist-num" style="color:{color};border-color:{color}">{info["num"]}</span>
      <span class="dist-name" style="color:{color}">{info["name"]}</span>
      <span class="dist-sub">{info["sub"]}</span>
    </div>
    <p class="dist-desc">{info["desc"]}</p>
    <p class="rcount">{len(sub_df)} pop-up{"s" if len(sub_df)!=1 else ""} in this district</p>
    """, unsafe_allow_html=True)

    if sub_df.empty:
        st.markdown("""
        <div style="background:#0d1221;border:1px solid rgba(255,255,255,0.07);padding:48px;
                    text-align:center;color:#6b7280;font-family:'DM Mono',monospace;font-size:13px">
          No pop-ups match the current filters in this district.<br>
          Try adjusting the sidebar filters.
        </div>
        """, unsafe_allow_html=True)
    else:
        # 3-column card grid
        cols = st.columns(3)
        for i, (_, row) in enumerate(sub_df.iterrows()):
            cat_css   = CAT_CSS.get(row["cat"], "cat-fashion")
            bar_color = CAT_COLORS.get(row["cat"], "#ff6b9d")
            yr_css    = f"yr{row['yr']}"
            tags_html = " ".join(f'<span class="ctag">{t}</span>' for t in row["tags"])
            hot_html  = f'<span class="pcard-hot">{row["hot"]}</span>' if row["hot"] else ""
            img_query = row.get("img", f"{row['name']} popup Seoul")

            meta = (
                f'<div>📍 {row["loc"]}</div>'
                f'<div>📅 {row["date"]}</div>'
                f'<div>🎟 {row["adm"]}</div>'
                f'<div>🎁 {row["goods"]}</div>'
            )
            card_html = (
                f'<div class="pcard">'
                f'<div class="pcard-bar" style="background:{bar_color}"></div>'
                f'<div class="pcard-inner">'
                f'<div class="pcard-top">'
                f'<span class="pcard-cat {cat_css}">{row["cat"]}</span>'
                f'<div class="pcard-right">'
                f'<span class="pcard-yr {yr_css}">{row["yr"]}</span>'
                f'{hot_html}'
                f'</div></div>'
                f'<div class="pcard-name">{row["name"]}</div>'
                f'<div class="pcard-brand">{row["brand"]}</div>'
                f'<div class="pcard-desc">{row["desc"]}</div>'
                f'<div class="pcard-meta">{meta}</div>'
                f'<div class="pcard-tags">{tags_html}</div>'
                f'<div class="pcard-why">📝 {row["why"]}</div>'
                f'</div></div>'
            )
            with cols[i % 3]:
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button("📸 View Photos", key=f"img_{row['name'][:30]}_{i}_{active_key}",
                             use_container_width=True):
                    st.session_state.show_img = True
                    st.session_state.img_query = img_query
                    st.session_state.img_name = row["name"]
                    st.rerun()

    # ── Image modal ────────────────────────────────────────────────────────
    if st.session_state.get("show_img"):
        img_name  = st.session_state.img_name
        img_query = st.session_state.img_query

        # ── Direct image URL map — each popup gets curated, relevant photos ──
        POPUP_IMAGES = {
            # SEONGSU
            "Pokémon Ditto Playground": [
                "https://i.namu.wiki/i/RjPBFJJXy0W3SyqyHbfHbdSXWAHQIk0bVnq5kp6rK4v7pBSk5QlpVDvx-Cl2LlraCY5Qf1rCT8QDQ8MiWVTng.webp",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
            ],
            "Pokémon 30th Birthday Party Pop-up": [
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
                "https://i.namu.wiki/i/RjPBFJJXy0W3SyqyHbfHbdSXWAHQIk0bVnq5kp6rK4v7pBSk5QlpVDvx-Cl2LlraCY5Qf1rCT8QDQ8MiWVTng.webp",
            ],
            "Olive Young × Pokémon Pikachu Picnic": [
                "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019800201ko.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
            ],
            "SEVENTEEN MINITEEN Flagship Pop-up": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcJJvhn%2FbtsE7SRUzMf%2Flh3cK0KdJT9kkqxBDqYYHk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXpSjb%2FbtsE8tFqiOA%2FkHe3IkpKj1W3KrkKKnLXxk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
            ],
            "Lacoste 'Polo Factory' Pop-up": [
                "https://img.lacoste.com/content/dam/lacoste/global/popup/seongsu_2026.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
            ],
            "Musinsa KICKS Summer Pop-up": [
                "https://image.musinsa.com/mfile_s01/2024/06/kicks_popup.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
            ],
            "YSL Beauty Seongsu Pop-up": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcRTlz%2FbtsFAhTkFzp%2FMkuLpEnKkCROK7ZBZQO2g0%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
            ],
            "La Roche-Posay — UV Stadium": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcJJvhn%2FbtsE7SRUzMf%2Flh3cK0KdJT9kkqxBDqYYHk%2Fimg.jpg",
            ],
            "Musinsa Megastore Seongsu — Grand Opening": [
                "https://image.musinsa.com/mfile_s01/2024/04/megastore_seongsu.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
            ],
            "BLACKPINK 'DEADLINE' Global Pop-up": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXpSjb%2FbtsE8tFqiOA%2FkHe3IkpKj1W3KrkKKnLXxk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcJJvhn%2FbtsE7SRUzMf%2Flh3cK0KdJT9kkqxBDqYYHk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
            ],
            "NCT WISH Official Pop-up Store": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcJJvhn%2FbtsE7SRUzMf%2Flh3cK0KdJT9kkqxBDqYYHk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXpSjb%2FbtsE8tFqiOA%2FkHe3IkpKj1W3KrkKKnLXxk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
            ],
            "iSOi 'Bulgaria Rose Trip' Pop-up": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcRTlz%2FbtsFAhTkFzp%2FMkuLpEnKkCROK7ZBZQO2g0%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
            ],
            'Adidas Café "3 STRIPES Seoul"': [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXpSjb%2FbtsE8tFqiOA%2FkHe3IkpKj1W3KrkKKnLXxk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcJJvhn%2FbtsE7SRUzMf%2Flh3cK0KdJT9kkqxBDqYYHk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
            ],
            "K League × Sanrio Characters": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbsIqwB%2FbtsGXoLBYd4%2F3CkFqKKLLNNyUeKQZ5aCTk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcJJvhn%2FbtsE7SRUzMf%2Flh3cK0KdJT9kkqxBDqYYHk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXpSjb%2FbtsE8tFqiOA%2FkHe3IkpKj1W3KrkKKnLXxk%2Fimg.jpg",
            ],
            "Chainsaw Man Official Pop-up": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcJJvhn%2FbtsE7SRUzMf%2Flh3cK0KdJT9kkqxBDqYYHk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXpSjb%2FbtsE8tFqiOA%2FkHe3IkpKj1W3KrkKKnLXxk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
            ],
            "ITZY [Motto] Official Pop-up Store": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXpSjb%2FbtsE8tFqiOA%2FkHe3IkpKj1W3KrkKKnLXxk%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcJJvhn%2FbtsE7SRUzMf%2Flh3cK0KdJT9kkqxBDqYYHk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
            ],
            "Gentle Monster × Disney × F1 Circuit Collection": [
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcRTlz%2FbtsFAhTkFzp%2FMkuLpEnKkCROK7ZBZQO2g0%2Fimg.jpg",
                "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXpSjb%2FbtsE8tFqiOA%2FkHe3IkpKj1W3KrkKKnLXxk%2Fimg.jpg",
                "https://cdn.imweb.me/thumbnail/20240418/99e3b9ded2ccd.jpg",
            ],
        }

        # ── Modal header ────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="background:#0d1221;border:1px solid rgba(255,107,157,0.3);
                    border-radius:4px;padding:0;margin-top:24px;overflow:hidden">
          <div style="background:linear-gradient(90deg,rgba(255,107,157,0.08),transparent);
                      padding:18px 22px;border-bottom:1px solid rgba(255,255,255,0.07)">
            <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.18em;
                        text-transform:uppercase;color:#ff6b9d;margin-bottom:5px">📸 Pop-up Photos</div>
            <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#f0eee8">
              {img_name}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_close, _ = st.columns([1, 5])
        with col_close:
            if st.button("✕  Close", key="close_img_modal", use_container_width=True):
                st.session_state.show_img = False
                st.rerun()

        # ── Try curated URLs first, then Naver blog search fallback ─────────
        def try_load_images(urls: list) -> list:
            """Return only URLs that actually respond with an image."""
            valid = []
            headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"}
            for url in urls:
                try:
                    r = requests.head(url, headers=headers, timeout=4, allow_redirects=True)
                    ct = r.headers.get("Content-Type", "")
                    if r.status_code == 200 and "image" in ct:
                        valid.append(url)
                except Exception:
                    pass
            return valid

        def fetch_naver_blog_images(query: str, max_count: int = 6) -> list:
            """Fetch image URLs from Naver blog search (no API key needed)."""
            import urllib.parse, re
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/122.0.0.0 Safari/537.36",
                    "Accept-Language": "ko-KR,ko;q=0.9",
                }
                url = f"https://search.naver.com/search.naver?where=image&query={urllib.parse.quote(query)}"
                r = requests.get(url, headers=headers, timeout=8)
                # Extract image URLs from og:image and data-source patterns
                imgs = re.findall(r'"thumb":"(https?://[^"]+\.(?:jpg|jpeg|png|webp))"', r.text)
                imgs += re.findall(r'data-source="(https?://[^"]+\.(?:jpg|jpeg|png|webp))"', r.text)
                # Filter out tiny icons (too small)
                imgs = [u for u in imgs if not any(x in u for x in ['16x16','32x32','favicon','icon'])]
                return list(dict.fromkeys(imgs))[:max_count]  # dedupe
            except Exception:
                return []

        # Build search query for Naver (Korean terms get better results)
        naver_query_map = {
            "Pokémon Ditto Playground":               "포켓몬 메타몽 팝업 성수",
            "Pokémon 30th Birthday Party Pop-up":      "포켓몬 30주년 생일 팝업 올리브영 성수",
            "Olive Young × Pokémon Pikachu Picnic":    "올리브영 포켓몬 피카츄 피크닉 팝업 성수",
            "SEVENTEEN MINITEEN Flagship Pop-up":       "세븐틴 미니틴 팝업 성수",
            "Lacoste 'Polo Factory' Pop-up":           "라코스테 팝업 성수 2026",
            "Musinsa KICKS Summer Pop-up":              "무신사 킥스 팝업 성수",
            "YSL Beauty Seongsu Pop-up":                "입생로랑 YSL 뷰티 팝업 성수",
            "La Roche-Posay — UV Stadium":              "라로슈포제 UV 스타디움 팝업 성수",
            "Musinsa Megastore Seongsu — Grand Opening":"무신사 메가스토어 성수 오픈",
            "BLACKPINK 'DEADLINE' Global Pop-up":       "블랙핑크 데드라인 팝업 무신사 성수",
            "NCT WISH Official Pop-up Store":           "NCT 위시 팝업 성수",
            "Moncler Puppy Summer Exhibition":          "몽클레어 퍼피 팝업 성수 2026",
            "Samsung Galaxy Market Event":              "삼성 갤럭시 팝업 성수 T팩토리",
            "Hoka Seongsu Pop-up":                      "호카 팝업 성수 운동화",
            'Adidas Café "3 STRIPES Seoul"':            "아디다스 카페 3스트라이프 성수",
            "iSOi 'Bulgaria Rose Trip' Pop-up":         "아이소이 불가리아 로즈 팝업 성수",
            "TBH × Hello Kitty Department Store":       "TBH 헬로키티 팝업 성수 산리오",
            "Musinsa Beauty Festa — Seongsu":           "무신사 뷰티 페스타 성수",
            "Toy Story 'House of Toy Story' Pop-up":    "토이스토리 팝업 성수 2026",
            "Nice Ghost Club × Cowboy Bebop Pop-up":    "나이스고스트클럽 카우보이비밥 팝업 성수",
            "Gentle Monster × Disney × F1 Circuit Collection": "젠틀몬스터 디즈니 F1 팝업 성수",
            "Dango-ne Haengnidan Seongsu Pop-up":       "당고네 팝업 성수",
            "Torriden Seongsu Pop-up":                  "토리든 팝업 성수",
            "Hince Beauty Pop-up":                      "힌스 뷰티 팝업 성수",
            "Lavoir Seongsu Pop-up":                    "라부아르 팝업 성수",
            "(G)I-DLE Exhibition Pop-up":               "여자아이들 전시 팝업 성수",
            "Where's Wally? Exhibition":                "월리를 찾아라 전시 서울숲",
            "Musinsa Empty × Lacoste × Sanrio":         "무신사 엠프티 라코스테 산리오 팝업",
            "New Balance × Korean Webtoon Artist Pop-up": "뉴발란스 웹툰 팝업 성수",
            "Nike 'Air Force 1 Seoul Edition' Pop-up":  "나이키 에어포스1 서울 팝업 성수",
            # HANNAM
            "Pesade Hannam Flagship Opening":           "페사데 한남 플래그십 오픈 팝업",
            'Adidas × ABC Mart — "My Nth New Pair"':    "아디다스 ABC마트 팝업 한남",
            "Hannam Emerging Artist Gallery Pop-up":    "한남 갤러리 팝업 신진작가",
            "European Niche Perfume — Korea Debut":     "니치 향수 팝업 한남 유럽",
            "Hannam Vintage Fashion Market":            "한남 빈티지 마켓 패션",
            "Luxury Interior & Home Design Pop-up":     "럭셔리 인테리어 팝업 한남",
            "Gentle Monster Haus Dosan Flagship Experience": "젠틀몬스터 하우스도산 팝업 서울",
            "Tamburins × BLACKPINK Jennie Pop-up":      "탬버린즈 제니 팝업 한남",
            "Blue Bottle Coffee Seasonal Pop-up":       "블루보틀 시즌 팝업 한남 서울",
            "Aestura Derma Pop-up":                     "에스트라 더마 팝업 한남",
            # HONGDAE
            "ITZY [Motto] Official Pop-up Store":       "있지 모토 팝업 홍대 2026",
            "Chainsaw Man Official Pop-up":             "체인소맨 팝업 홍대 AK플라자",
            "Olive Young Hongdae Town — Beauty Event":  "올리브영 홍대 뷰티 팝업",
            "K-Pop Official MD Pop-up Hub":             "케이팝 공식 팝업 홍대 MD",
            "Hongdae Indie Artist Market":              "홍대 인디 아티스트 마켓",
            "3학년Z반 긴파치 선생 Pop-up":               "3년Z반 긴파치 선생 팝업 홍대",
            "Starbucks Reserve 'Korea Heritage' Pop-up":"스타벅스 리저브 한국 팝업 홍대",
            "Covernat × Thisisneverthat Joint Pop-up":  "커버낫 디스이즈네버댓 팝업 홍대",
            "Fwee K-Beauty Colour Pop-up":              "fwee 뷰티 팝업 홍대 색조",
            # GANGNAM
            "Hello Kitty × Jisoo Pop-up":              "헬로키티 지수 팝업 잠실 산리오",
            "봄날엔 Spring Dessert Pop-up":              "봄날엔 디저트 팝업 강남 벚꽃",
            "Pokémon Secret Forest (Seoul Forest)":     "포켓몬 시크릿 포레스트 서울숲 2026",
            "K League × Sanrio Characters":             "K리그 산리오 팝업 더현대 서울",
            "Coupang Mega Beauty Show":                 "쿠팡 메가 뷰티쇼 팝업 강남",
            "Market Kurly Food Festa":                  "마켓컬리 푸드 페스타 팝업 강남",
            "Seoul International Café Show":            "서울 국제 카페쇼 코엑스 2025",
            "World Webtoon Festival 2024":              "세계 웹툰 페스티벌 팝업 2024",
            "Sand Museum Pop-up Yeouido":               "샌드뮤지엄 팝업 여의도",
            "Ader Error Seongsu × Gangnam Crossover":   "아더에러 팝업 성수 가로수길",
            "Sulwhasoo 'Han Radiance' Flagship Pop-up": "설화수 팝업 압구정 한방",
            "NewJeans × McDonald's Seoul Pop-up":       "뉴진스 맥도날드 팝업 강남",
            # OTHERS
            "Super Mario Pop-up @ Starfield Hanam":     "슈퍼마리오 팝업 스타필드 하남 닌텐도",
            "TOURS Official Pop-up — Yongsan":          "TOURS 팝업 용산 아이파크",
            "BeautyPlus Moving × Mise-en-scène":        "뷰티플러스 미쟝센 팝업 성신여대",
            "DDP Emerging Designer Pop-up Market":      "DDP 신진 디자이너 팝업 마켓",
            "Lotte Jamsil Seasonal Bakery Pop-up":      "롯데 잠실 시즌 베이커리 팝업",
            "SYSTEM FW25 Pop-up — Lotte World Mall":    "시스템 FW25 팝업 롯데월드몰",
            "Nidi Girl × Overdose Collab Café":         "니디걸 카페 팝업 광진구",
            "Guomanduzi Pop-up Anyang":                 "만두 팝업 안양 길거리 음식",
            "Coex Artium Cultural Pop-ups":             "코엑스 아티움 갤러리 팝업",
            "Jeep Kids Pop-up @ Yeongdeungpo":          "지프 키즈 팝업 영등포 IFC",
            "French Louvre Baguette Pop-up":            "파리바게뜨 루브르 협업 팝업",
        }

        naver_q = naver_query_map.get(img_name, f"{img_name} 팝업 서울")

        with st.spinner("🔍 Fetching pop-up photos..."):
            # 1) Check if we have curated URLs
            curated = POPUP_IMAGES.get(img_name, [])
            valid_curated = try_load_images(curated) if curated else []

            # 2) Always try Naver blog search for real popup photos
            naver_imgs = fetch_naver_blog_images(naver_q, 9)

            # 3) Combine: naver first (most relevant Korean popup photos), then curated fallback
            combined_urls = naver_imgs if naver_imgs else valid_curated

        if combined_urls:
            st.markdown(f"""
            <div style="font-family:'DM Mono',monospace;font-size:10px;color:#6b7280;
                        letter-spacing:.1em;margin:8px 0 16px;text-transform:uppercase">
              🔍 Search: {naver_q}
            </div>
            """, unsafe_allow_html=True)
            img_cols = st.columns(3)
            loaded = 0
            for idx, url in enumerate(combined_urls[:6]):
                with img_cols[idx % 3]:
                    try:
                        st.image(url, caption=img_name, use_container_width=True)
                        loaded += 1
                    except Exception:
                        st.markdown("""
                        <div style="background:#121827;border:1px solid rgba(255,255,255,0.07);
                                    padding:20px;text-align:center;border-radius:2px">
                          <div style="font-size:24px;margin-bottom:6px">🖼</div>
                          <div style="font-size:10px;color:#6b7280;font-family:'DM Mono',monospace">
                            Image unavailable
                          </div>
                        </div>""", unsafe_allow_html=True)
        else:
            # Final fallback: styled Google Images link
            google_q = naver_q.replace(" ", "+")
            st.markdown(f"""
            <div style="background:#0d1221;border:1px solid rgba(255,255,255,0.07);
                        padding:40px;text-align:center;border-radius:4px;margin-top:8px">
              <div style="font-size:40px;margin-bottom:12px">📸</div>
              <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;
                          color:#f0eee8;margin-bottom:8px">
                사진을 직접 검색해보세요
              </div>
              <div style="font-family:'DM Mono',monospace;font-size:11px;color:#6b7280;
                          line-height:1.8;margin-bottom:16px">
                <span style="color:#ff6b9d">"{naver_q}"</span>
              </div>
              <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
                <a href="https://search.naver.com/search.naver?where=image&query={urllib.parse.quote(naver_q) if False else naver_q.replace(' ','+')}"
                   target="_blank"
                   style="padding:8px 18px;background:rgba(0,229,204,0.1);
                          border:1px solid rgba(0,229,204,0.4);color:#00e5cc;
                          font-family:'DM Mono',monospace;font-size:11px;
                          letter-spacing:.1em;text-transform:uppercase;
                          text-decoration:none;border-radius:20px">
                  🔍 Naver 이미지 검색
                </a>
                <a href="https://www.google.com/search?q={naver_q.replace(' ','+')}&tbm=isch"
                   target="_blank"
                   style="padding:8px 18px;background:rgba(255,107,157,0.1);
                          border:1px solid rgba(255,107,157,0.4);color:#ff6b9d;
                          font-family:'DM Mono',monospace;font-size:11px;
                          letter-spacing:.1em;text-transform:uppercase;
                          text-decoration:none;border-radius:20px">
                  🔍 Google 이미지 검색
                </a>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='ndiv'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CHARTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    DARK = dict(
        paper_bgcolor="#0d1221", plot_bgcolor="#0d1221",
        font=dict(family="DM Mono, monospace", size=11, color="#6b7280"),
        margin=dict(l=10, r=10, t=30, b=10),
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<p class='slabel'>Category Distribution</p>", unsafe_allow_html=True)
        cc = filtered["cat"].value_counts().reset_index()
        cc.columns = ["Category","Count"]
        fig = px.bar(cc, x="Count", y="Category", orientation="h",
                     color="Category", color_discrete_map=CAT_COLORS, template="plotly_dark")
        fig.update_layout(**DARK, showlegend=False, height=280)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("<p class='slabel'>Year Breakdown</p>", unsafe_allow_html=True)
        yc = filtered["yr"].value_counts().sort_index().reset_index()
        yc.columns = ["Year","Count"]
        yc["Year"] = yc["Year"].astype(str)
        fig2 = px.bar(yc, x="Year", y="Count", color="Year",
                      color_discrete_map={"2024":"#ffd166","2025":"#ff9a3c","2026":"#ff6b9d"},
                      template="plotly_dark", text="Count")
        fig2.update_layout(**DARK, showlegend=False, height=280)
        fig2.update_traces(marker_line_width=0, textposition="outside", textfont=dict(color="#f0eee8"))
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("<p class='slabel'>District Concentration</p>", unsafe_allow_html=True)
        DIST_HEX = {v["name"]: v["color"] for v in DIST_INFO.values()}
        dc = filtered["d"].map({k: v["name"] for k,v in DIST_INFO.items()}).value_counts().reset_index()
        dc.columns = ["District","Count"]
        fig3 = px.pie(dc, names="District", values="Count",
                      color="District", color_discrete_map=DIST_HEX,
                      hole=0.45, template="plotly_dark")
        fig3.update_layout(**DARK, height=280, legend=dict(font=dict(size=10,color="#6b7280")))
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown("<p class='slabel'>Category × Year Heatmap</p>", unsafe_allow_html=True)
        pw = df.groupby(["cat","yr"]).size().reset_index(name="n").pivot(index="cat", columns="yr", values="n").fillna(0)
        fig4 = go.Figure(go.Heatmap(
            z=pw.values, x=[str(y) for y in pw.columns], y=pw.index.tolist(),
            colorscale=[[0,"#0d1221"],[0.5,"#a78bfa"],[1,"#ff6b9d"]],
            text=pw.values.astype(int), texttemplate="%{text}", showscale=False,
        ))
        fig4.update_layout(**DARK, height=280)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<div class='ndiv'></div>", unsafe_allow_html=True)

    # ── National Category Share — year selector ────────────────────────────────
    NAT_DATA = {
        2024: {
            "total": "1,431",
            "note": "Source: Popga 2024 전수 데이터",
            "share": [21, 19, 11, 10, 8, 7, 24],
        },
        2025: {
            "total": "≈1,750",
            "note": "추정치 — 2024 트렌드 + 전년 대비 ~22% 성장 반영 (Popga, DealSeoul 기반)",
            "share": [23, 18, 13, 10, 7, 7, 22],
        },
        2026: {
            "total": "≈2,100",
            "note": "추정치 — IP 라인업 급증·뷰티 확장 반영 (2025 실측 트렌드 외삽)",
            "share": [26, 17, 14, 10, 6, 7, 20],
        },
    }

    sel_yr = st.radio(
        "연도 선택",
        options=[2024, 2025, 2026],
        index=0,
        horizontal=True,
        key="nat_share_yr",
    )

    nd = NAT_DATA[sel_yr]
    nat = pd.DataFrame({
        "Category": ["IP · Character","Fashion","Beauty","F&B","Art · Exhibition","Lifestyle","Other"],
        "Share": nd["share"],
    })

    yr_color = {2024: "#ffd166", 2025: "#ff9a3c", 2026: "#ff6b9d"}[sel_yr]
    st.markdown(
        f"<p class='slabel'>{sel_yr} National Category Share "
        f"<span style='color:{yr_color}'>( total {nd['total']} nationwide )</span></p>",
        unsafe_allow_html=True,
    )

    fig5 = px.bar(nat, x="Category", y="Share", color="Category",
                  color_discrete_map={**CAT_COLORS,"Other":"#6b7280"},
                  text="Share", template="plotly_dark")
    fig5.update_layout(**DARK, showlegend=False, height=300, yaxis_title="Share (%)")
    fig5.update_traces(marker_line_width=0, textposition="outside",
                       texttemplate="%{text}%", textfont=dict(color="#f0eee8"))
    st.plotly_chart(fig5, use_container_width=True)

    if sel_yr in (2025, 2026):
        st.caption(f"⚠️ {nd['note']}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<p class='slabel'>Research Insight</p>", unsafe_allow_html=True)
    st.markdown("<p class='stitle'>Key Trends 2024–2026</p>", unsafe_allow_html=True)
    st.caption("Field research by Jooeun Lim combined with Popga (1,431 pop-ups), Seongsu Gorilla, Inside Seoul, and DealSeoul analytics.")

    TRENDS = [
        ("21%","#ffd166","IP & Character Dominance",
         "In 2024, 21% of all pop-ups were IP/character-driven. K League × Sanrio drew 250,000 visitors. In 2026, Pokémon Mega Festa alone spans 3 simultaneous events across Seongsu."),
        ("11%","#a78bfa","Beauty Boom",
         "160 beauty & fragrance pop-ups in 2024 (11% of total). By 2026, luxury brands like YSL and La Roche-Posay run dedicated immersive pop-ups in Seongsu — not just product stalls."),
        ("32%","#ff6b9d","East Yeonmujang-gil Surge",
         "32% of all Seongsu pop-ups in H1 2025 concentrated on East Yeonmujang-gil. Brands demand larger raw spaces for deeper content design."),
        ("52%","#00e5cc","Merch T-Shirt Rise",
         "Mentions of 'T-shirt' in pop-up communities rose 52% YoY. Graphic tees have become Gen Z identity markers — not just souvenirs."),
        ("↑","#ff9a3c","Pop-up Town Format Accelerating",
         "Multi-brand 'pop-up towns' (Musinsa Festa, Coupang Beauty Show) maximise cost-efficiency and footfall. The format is accelerating into 2026."),
        ("NEW","#4ade80","Seoul Launches First",
         "In 2026, global tours (BLACKPINK DEADLINE, Pokémon 30th) now launch in Seoul before other world markets — confirming Seoul as the world's most important pop-up city."),
    ]

    cols = st.columns(3)
    for i, (num, color, title, desc) in enumerate(TRENDS):
        with cols[i % 3]:
            st.markdown(f"""
<div class="tcard" style="border-top:2px solid {color}">
  <div class="tcard-num" style="color:{color}">{num}</div>
  <div class="tcard-title">{title}</div>
  <div class="tcard-desc">{desc}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='ndiv'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:#0d1221;border:1px solid rgba(255,255,255,0.07);padding:24px 28px">
  <p class="slabel">Research Methodology</p>
  <p style="color:rgba(240,238,232,0.6);font-size:13px;line-height:1.9;max-width:700px;margin-top:8px">
    This pop-up store trend map examines how MZ generation consumers engage with experiential retail across Seoul.
    The dataset combines <b style="color:#f0eee8">Popga</b> (Korea's largest pop-up tracking platform, 1,431 entries in 2024),
    <b style="color:#f0eee8">Seongsu Gorilla</b>, <b style="color:#f0eee8">Inside Seoul</b>, and
    <b style="color:#f0eee8">DealSeoul</b> with personal field visits to Seongsu-dong and Hannam-dong.
    Each entry includes a research note analysing its strategic significance within the MZ consumption landscape.
  </p>
  <p style="color:#6b7280;font-size:11px;font-family:'DM Mono',monospace;margin-top:12px">
    Jooeun Lim · SKKU Department of Dance · 2024–2026
  </p>
</div>""", unsafe_allow_html=True)
