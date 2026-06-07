import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
         why="One of three simultaneous Pokémon events in Seongsu — Pokémon Mega Festa 2026 is unprecedented in scale."),
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="🏆 Major",
         name="Pokémon 30th Birthday Party Pop-up", brand="Pokémon Mega Festa × Olive Young N Seongsu",
         desc="Birthday-party themed pop-up: cake, ribbon & balloon photo zones, coloring corner, and exclusive Birthday Edition merch.",
         loc="Olive Young N Seongsu, 1F", date="May 1 – Jun 21, 2026", adm="Free", goods="Birthday Edition limited goods",
         tags=["Pokémon","Birthday","30th","Limited Ed."],
         why="Olive Young's collab leverages Pokémon mania to drive flagship traffic — a perfect channel partnership model."),
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
         why="Two-floor café + shop format maximises dwell time — a growing blueprint for K-pop pop-ups."),
    dict(d="seongsu", cat="Fashion", yr=2026, hot="",
         name="Lacoste 'Polo Factory' Pop-up", brand="Lacoste",
         desc="French heritage brand celebrates 90+ years of the polo shirt through an immersive walk-through of construction, fabrics, and sustainability.",
         loc="Seongsu-dong", date="May 21 – Jun 3, 2026", adm="Free", goods="Heritage collection + limited pieces",
         tags=["Heritage","Fashion","Exhibition","Sustainability"],
         why="Lacoste chose Seongsu over Gangnam — deliberate repositioning of a legacy brand toward MZ consumers."),
    dict(d="seongsu", cat="Beauty", yr=2026, hot="✨ Notable",
         name="YSL Beauty Seongsu Pop-up", brand="Yves Saint Laurent Beauty",
         desc="Luxury French beauty pop-up with new collection launch, makeup experience zones, and exclusive YSL goods only available here.",
         loc="Seongsu-dong", date="May 9 – May 24, 2026", adm="Free", goods="Exclusive YSL location goods",
         tags=["Luxury Beauty","Makeup","YSL","Exclusive"],
         why="YSL entering Seongsu rather than Apgujeong signals the district has matured into a luxury brand destination."),
    dict(d="seongsu", cat="Beauty", yr=2026, hot="",
         name="La Roche-Posay — UV Stadium", brand="La Roche-Posay",
         desc="Sports-themed sunscreen pop-up turning skincare education into a stadium experience. UV zones, SPF trials, photo installations.",
         loc="Seongsu-dong", date="May 15 – May 25, 2026", adm="Free", goods="SPF sample kits",
         tags=["Sunscreen","Skincare","Experiential","Sports"],
         why="Turning skincare into a stadium concept shows brands competing for attention through narrative."),
    dict(d="seongsu", cat="Fashion", yr=2026, hot="🏆 Major",
         name="Musinsa Megastore Seongsu — Grand Opening", brand="Musinsa",
         desc="Grand opening of Musinsa's flagship megastore with multi-brand pop-ups, exclusive drops, and opening celebration events.",
         loc="Musinsa Megastore Seongsu", date="Apr 24 – May 3, 2026", adm="Free", goods="Exclusive opening drops",
         tags=["Flagship","Musinsa","Multi-brand","Grand Opening"],
         why="Musinsa's permanent megastore formalises Seongsu's evolution from pop-up hub to year-round destination."),
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="🏆 Global",
         name="BLACKPINK 'DEADLINE' Global Pop-up", brand="BLACKPINK × YG Entertainment",
         desc="World tour launching in Seoul first. Seoul-exclusive MD, new lightstick, plush, keyrings and keycaps. Continued in 20 cities worldwide.",
         loc="Musinsa Seongsu + Musinsa Myeongdong", date="Feb 28 – Mar 8, 2026 · 11:00–22:00", adm="Free", goods="Seoul-exclusive MD + lightstick",
         tags=["BLACKPINK","K-Pop","Global Tour","Musinsa"],
         why="Seoul as global first stop confirms it as the world's most important pop-up market in 2026."),
    dict(d="seongsu", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="NCT WISH Official Pop-up Store", brand="SM Entertainment",
         desc="Official pop-up for NCT WISH with fan interaction zones, photo booths, and exclusive Seoul-edition merchandise.",
         loc="Seongsu-dong", date="Apr 27 – May 3, 2026", adm="Free", goods="Seoul-edition MD + photocards",
         tags=["K-Pop","NCT","Fan Event","Seoul Exclusive"],
         why="SM chose Seongsu over SM Town Coex — reflecting the commercial appeal of Seongsu's younger foot traffic."),
    dict(d="seongsu", cat="Fashion", yr=2026, hot="",
         name="Moncler Puppy Summer Exhibition", brand="Moncler",
         desc="Luxury Italian outerwear brand brings 'Puppy' summer collection in an art-forward exhibition format with seasonal limited pieces.",
         loc="Seongsui-ro 16-gil 31, Seongsu", date="May 1 – May 3, 2026", adm="Free", goods="Limited summer pieces",
         tags=["Luxury","Exhibition","Fashion","Moncler"],
         why="Moncler's gallery-style format elevates brand experience — visitors engage as they would a gallery show."),
    dict(d="seongsu", cat="Lifestyle", yr=2026, hot="",
         name="Samsung Galaxy Market Event", brand="Samsung Electronics",
         desc="Experiential pop-up at T Factory Seongsu — latest Galaxy devices with hands-on trials and immersive tech zones.",
         loc="T Factory Seongsu, Yeonmujang 1-gil", date="Feb 27 – Mar 29, 2026", adm="Free", goods="Device trial + exclusive bundles",
         tags=["Tech","Samsung","Galaxy","Experiential"],
         why="Tech brands using Seongsu's creative spaces signals the district's broad cultural credibility beyond fashion and beauty."),
    # ── SEONGSU 2025 ──
    dict(d="seongsu", cat="Fashion", yr=2025, hot="",
         name="Hoka Seongsu Pop-up", brand="HOKA",
         desc="Running & trail shoe brand's pop-up with fit experience stations, limited-color drops, and stamp-tour giveaways.",
         loc="East Yeonmujang-gil, Seongsu", date="Jan 2025", adm="Free", goods="Limited colorway + stamp goods",
         tags=["Running","Experiential","Showroom","Sneakers"],
         why="Hoka's shift from performance to lifestyle is embodied in Seongsu — targeting trend-aware consumers, not just runners."),
    dict(d="seongsu", cat="F&B", yr=2025, hot="🔥 Viral",
         name='Adidas Café "3 STRIPES Seoul"', brand="Adidas × Café Concept",
         desc="Fashion meets coffee — a viral social media sensation before it even opened. Three-stripe drinks, limited merch, and brand installations drew massive queues.",
         loc="Seongsu-dong", date="Jan 2025 (~Jan 18)", adm="Free", goods="Limited drinks & merch",
         tags=["Collab","Café","Sports","Viral","SNS"],
         why="Pre-opening social buzz turned this into a must-visit — a case study in anticipation-building without paid advertising."),
    dict(d="seongsu", cat="Beauty", yr=2025, hot="✨ Benchmark",
         name="iSOi 'Bulgaria Rose Trip' Pop-up", brand="iSOi",
         desc="Immersive Bulgaria rose concept space at iSOi's Seongsu flagship — a benchmark for brand-owned pop-up strategy with no rental costs.",
         loc="iSOi Flagship, Seongsu", date="Jan 2025", adm="Free", goods="Product samples",
         tags=["Skincare","Immersive","Flagship","Benchmark"],
         why="By owning the pop-up through their flagship, iSOi eliminated rental costs while generating enormous SNS buzz."),
    dict(d="seongsu", cat="IP · Character", yr=2025, hot="",
         name="TBH × Hello Kitty Department Store", brand="tbh × Sanrio",
         desc="Hello Kitty 50th anniversary collab with co-designed limited apparel, accessories, and collectibles.",
         loc="Seongsu-dong", date="Jan 2025", adm="Free", goods="Limited collab goods",
         tags=["Sanrio","Hello Kitty","Collab","Fashion","50th"],
         why="The Hello Kitty 50th anniversary proved the staying power of legacy IP over trend-driven collabs."),
    # ── SEONGSU 2024 ──
    dict(d="seongsu", cat="Fashion", yr=2024, hot="🏆 Large-scale",
         name="Musinsa Beauty Festa — Seongsu", brand="Musinsa",
         desc="Massive multi-brand pop-up town across Seongsu, bringing online-only beauty brands to their first ever offline spaces.",
         loc="Seongsu-dong (area-wide)", date="2024", adm="Free", goods="Multi-brand beauty & fashion",
         tags=["Pop-up Town","Multi-brand","Large-scale","Pioneering"],
         why="Proved an e-commerce platform could run a physical pop-up town as effectively as a department store."),
    # ── HANNAM ──
    dict(d="hannam", cat="Beauty", yr=2026, hot="✨ Notable",
         name="Pesade Hannam Flagship Opening", brand="Pesade",
         desc="Niche fragrance brand Pesade opens its Hannam flagship with personal scent consultations and exclusive opening-day sets.",
         loc="Hannam-dong Flagship", date="2026", adm="Free", goods="Personal scent consultation + sets",
         tags=["Niche Fragrance","Flagship","Opening","Hannam"],
         why="Hannam's gallery culture makes it the natural home for niche fragrance brands seeking affluent, design-literate consumers."),
    dict(d="hannam", cat="Fashion", yr=2025, hot="",
         name='Adidas × ABC Mart — "My Nth New Pair"', brand="ABC Mart × Adidas",
         desc="Season-launch pop-up combining ABC Mart's retail reach with Adidas' newest sneaker lineup and on-site shoe personalisation.",
         loc="Hannam-dong", date="Jan 2025", adm="Free", goods="Limited sneaker lineup",
         tags=["Sneakers","Collab","Customise","Personalise"],
         why="Personalisation services dramatically increase time-in-store and purchase likelihood."),
    dict(d="hannam", cat="Art · Exhibition", yr=2025, hot="",
         name="Hannam Emerging Artist Gallery Pop-up", brand="Hannam Independent Gallery Network",
         desc="Rotating platform for emerging Korean artists with works for sale and brand-collab art objects. Buyers receive limited-edition art books.",
         loc="Hannam Gallery District", date="Seasonal, ongoing", adm="Free viewing", goods="Original artworks + art books",
         tags=["Art","Emerging Artist","Sales","Curation"],
         why="Hannam's gallery infrastructure allows emerging artists to access affluent collectors without a permanent space."),
    dict(d="hannam", cat="Beauty", yr=2025, hot="",
         name="European Niche Perfume — Korea Debut", brand="Hannam Concept Beauty Edit",
         desc="First Korean pop-up for a coveted European niche perfume house. Personal fragrance consultations and limited discovery sets.",
         loc="Hannam Concept Store", date="Seasonal", adm="Free", goods="Discovery sets + consultation",
         tags=["Niche Perfume","Consultation","Debut","European"],
         why="Hannam's international-facing demographic is the ideal test market for European niche brands entering Korea."),
    dict(d="hannam", cat="Fashion", yr=2024, hot="",
         name="Hannam Vintage Fashion Market", brand="Hannam Vintage Curators",
         desc="Monthly curated vintage & resale pop-up reflecting MZ consumers' growing interest in sustainable fashion.",
         loc="Hannam-dong", date="Monthly, ongoing", adm="Free", goods="Vintage & resale items",
         tags=["Vintage","Resale","Sustainable","Monthly"],
         why="Sustainable fashion is the fastest-growing MZ sub-trend — Hannam's market taps this with a premium approach."),
    dict(d="hannam", cat="Lifestyle", yr=2025, hot="",
         name="Luxury Interior & Home Design Pop-up", brand="Hannam Flagship Brands",
         desc="Premium interior and home brand pop-up offering product experience and consultation services.",
         loc="Hannam-dong", date="Seasonal", adm="Free", goods="Consultation + display items",
         tags=["Interior","Premium","Lifestyle","Consultation"],
         why="Home lifestyle brands use pop-ups to bridge the gap between e-commerce imagery and real-world texture."),
    # ── HONGDAE ──
    dict(d="hongdae", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="ITZY [Motto] Official Pop-up Store", brand="ITZY × JYP Entertainment",
         desc="Official pop-up tied to ITZY's Motto release with fan merch, photocard events, and Hongdae-only album bundles.",
         loc="Mapo-gu, Hongdae area", date="May 19 – May 25, 2026", adm="Free", goods="Exclusive album bundle + photocards",
         tags=["K-Pop","ITZY","Fan Event","JYP","Hongdae Only"],
         why="Hongdae remains the spiritual home of K-pop fan culture — the natural first choice for comeback pop-ups."),
    dict(d="hongdae", cat="IP · Character", yr=2025, hot="🔥 HOT",
         name="Chainsaw Man Official Pop-up", brand="AK Plaza Hongdae × MAPPA",
         desc="Large-scale official anime pop-up with character goods, acrylic standees, apparel, and Korean-market collectibles. Long queues from day one.",
         loc="AK Plaza Hongdae Branch", date="Sep 26 – Dec 31, 2025", adm="Free", goods="Anime character goods",
         tags=["Anime","IP","Goods","MAPPA","Long-run"],
         why="A 3-month run in a department store signals anime IP has become a consistent driver of retail footfall."),
    dict(d="hongdae", cat="Beauty", yr=2025, hot="✨ Notable",
         name="Olive Young Hongdae Town — Beauty Event", brand="CJ Olive Young",
         desc="Multi-brand beauty event at Olive Young's Hongdae flagship. Makeup trials, new product demos, and SNS verification giveaways.",
         loc="Olive Young Hongdae Town", date="Oct 2 – Oct 12, 2025", adm="Free", goods="Sample giveaways",
         tags=["K-Beauty","Multi-brand","Trial","SNS","Flagship"],
         why="Olive Young Hongdae's tourist-heavy foot traffic makes it one of the most cost-efficient locations for beauty brands."),
    dict(d="hongdae", cat="IP · Character", yr=2024, hot="",
         name="K-Pop Official MD Pop-up Hub", brand="Major Entertainment Labels",
         desc="Hongdae's proximity to SM Town makes it a permanent K-pop corridor. Albums, photocards, lightsticks at every major comeback.",
         loc="Hongdae, near SM Town", date="Comeback seasons, ongoing", adm="Free", goods="Random photocard events",
         tags=["K-Pop","Fandom","MD","SM Town","Ongoing"],
         why="Hongdae's role as K-pop's retail heartland is self-reinforcing: fans gather because brands pop up; brands pop up because fans gather."),
    dict(d="hongdae", cat="Art · Exhibition", yr=2024, hot="",
         name="Hongdae Indie Artist Market", brand="Hongdae Art Scene",
         desc="Independent artist market selling handmade works, goods, and crafts — a defining feature of Hongdae's creative underground.",
         loc="Hongdae Walk Street", date="2× monthly, ongoing", adm="Free", goods="Handmade works & goods",
         tags=["Handmade","Indie","Market","Authentic"],
         why="The indie artist market represents the grassroots origin of Seoul's pop-up culture."),
    # ── GANGNAM ──
    dict(d="gangnam", cat="IP · Character", yr=2026, hot="🔥 HOT",
         name="Hello Kitty × Jisoo Pop-up", brand="Sanrio × Jisoo (BLACKPINK)",
         desc="Sanrio's Hello Kitty collabs with BLACKPINK's Jisoo. Co-designed fashion pieces, limited character goods, and signature photo zones.",
         loc="Jamsil, Songpa-gu", date="May 1–5, 2026 (Golden Week)", adm="Free", goods="Co-designed limited goods",
         tags=["Sanrio","BLACKPINK","Jisoo","Collab","Golden Week"],
         why="Combining Hello Kitty with Jisoo targets two overlapping fandoms simultaneously — executed during peak visitor season."),
    dict(d="gangnam", cat="F&B", yr=2026, hot="",
         name="봄날엔 Spring Dessert Pop-up", brand="Bomnal-en Gangnam",
         desc="Spring-season dessert pop-up in Gangnam with seasonal pastries and cherry blossom period limited menus.",
         loc="Seocho-gu, Gangnam", date="May 19 – May 31, 2026", adm="Free", goods="Seasonal dessert menu",
         tags=["Dessert","Spring","Seasonal","Instagram"],
         why="Seasonal F&B pop-ups timed to cherry blossom season consistently outperform in foot traffic."),
    dict(d="gangnam", cat="IP · Character", yr=2026, hot="🌿 Outdoor",
         name="Pokémon Secret Forest (Seoul Forest)", brand="Pokémon Mega Festa 2026",
         desc="Outdoor Pokémon pop-up where hidden Pokémon lurk among Seoul Forest trees, tied to the 2026 Seoul International Garden Expo.",
         loc="Seoul Forest, Seongdong-gu", date="May 1 – Jun 21, 2026", adm="Free", goods="Outdoor original goods",
         tags=["Pokémon","Outdoor","Seoul Forest","Garden Expo"],
         why="Taking a pop-up outdoors into Seoul Forest transforms the experience from retail into a nature walk."),
    dict(d="gangnam", cat="IP · Character", yr=2024, hot="🏆 Record",
         name="K League × Sanrio Characters", brand="K League × Sanrio",
         desc="The most successful pop-up of 2024: 250,000 total visitors, averaging 10,500 per day. Textbook cross-fandom collision.",
         loc="The Hyundai Seoul", date="2024", adm="Free", goods="Cross-fandom limited goods",
         tags=["Cross-fandom","Record","Sanrio","K League","Sports"],
         why="Bridges two unconnected communities, doubling potential audience without increasing production complexity."),
    dict(d="gangnam", cat="Beauty", yr=2024, hot="🏆 Large-scale",
         name="Coupang Mega Beauty Show", brand="Coupang × 9 Beauty Brands",
         desc="Nine major beauty brands share one pop-up town. Visitors compare, trial, and purchase across all brands simultaneously.",
         loc="Gangnam area large venue", date="2024", adm="Free", goods="Multi-brand trials & purchase",
         tags=["Pop-up Town","Multi-brand","Beauty","Benchmark"],
         why="Coupang coordinating 9 brands shows how e-commerce platforms are emerging as pop-up town operators."),
    dict(d="gangnam", cat="F&B", yr=2024, hot="",
         name="Market Kurly Food Festa", brand="Market Kurly",
         desc="Fresh-food e-commerce platform Kurly brings curated brands offline with live tasting and cooking demos.",
         loc="Gangnam area", date="2024", adm="Free", goods="Premium food items + tasting",
         tags=["F&B","E-commerce","Tasting","Premium"],
         why="Market Kurly's offline Festa bridges a core challenge for food e-commerce: consumers want to taste before buying."),
    dict(d="gangnam", cat="Art · Exhibition", yr=2025, hot="",
         name="Seoul International Café Show", brand="COEX",
         desc="Korea's largest café & beverage expo with new F&B brand pop-ups, master barista demos, and specialty coffee showcases.",
         loc="COEX, Gangnam", date="Nov 2025", adm="Paid admission", goods="Coffee products + limited brews",
         tags=["Café","Exhibition","Industry","Coffee","COEX"],
         why="The Café Show functions as an annual cultural moment for Seoul's café-obsessed MZ generation."),
    dict(d="gangnam", cat="IP · Character", yr=2024, hot="",
         name="World Webtoon Festival 2024", brand="Webtoon Platform Alliance",
         desc="Major Korean and international webtoon IPs gather for a festival pop-up with author signings and story-world exhibitions.",
         loc="Gangnam area large venue", date="2024", adm="Paid admission", goods="Author-signed goods",
         tags=["Webtoon","IP","Festival","Author","Signing"],
         why="Webtoon IP generates deeply personal connections — fans follow characters for years, making purchases highly emotional."),
    # ── OTHERS ──
    dict(d="others", cat="IP · Character", yr=2026, hot="",
         name="Super Mario Pop-up @ Starfield Hanam", brand="Nintendo × Starfield Hanam",
         desc="Nintendo's Super Mario franchise at Starfield Hanam with interactive game-themed installations and limited merchandise.",
         loc="Starfield Hanam, Gyeonggi", date="May 2026 (Golden Week)", adm="Free", goods="Nintendo limited goods",
         tags=["Nintendo","Mario","Gaming","Interactive","Family"],
         why="Nintendo's strategic use of Golden Week maximises family traffic at a suburban location."),
    dict(d="others", cat="IP · Character", yr=2026, hot="",
         name="TOURS Official Pop-up — Yongsan", brand="TOURS (K-Pop Group)",
         desc="K-Pop group TOURS at Yongsan iPark Mall with fan merch, exclusive Yongsan-edition goods, and photocard events.",
         loc="Yongsan iPark Mall", date="May 1–5, 2026 (Golden Week)", adm="Free", goods="Exclusive Yongsan-edition merch",
         tags=["K-Pop","Fan Event","Yongsan","Golden Week"],
         why="Yongsan's proximity to major transit hubs makes it accessible to fans travelling from across the country."),
    dict(d="others", cat="Beauty", yr=2026, hot="",
         name="BeautyPlus Moving × Mise-en-scène", brand="BeautyPlus Universe",
         desc="BeautyPlus's mobile pop-up at Sungshin Women's University in collaboration with hair care brand Mise-en-scène.",
         loc="Seongbuk-gu (Sungshin Women's Univ.)", date="May 19, 2026", adm="Free", goods="Hair care giveaways",
         tags=["Hair Care","Mobile Pop-up","Campus","University"],
         why="Campus-based beauty pop-ups target the MZ demographic at point of brand discovery."),
    dict(d="others", cat="Art · Exhibition", yr=2025, hot="",
         name="DDP Emerging Designer Pop-up Market", brand="Dongdaemun Design Plaza",
         desc="Emerging designer market at the iconic DDP building with fashion, product design, and crafts curated by category.",
         loc="Dongdaemun Design Plaza (DDP)", date="1–2× monthly, ongoing", adm="Free", goods="Designer pieces & crafts",
         tags=["Emerging Designers","DDP","Market","Architecture"],
         why="The DDP's Zaha Hadid landmark status gives any pop-up hosted there a cultural legitimacy no standard space can provide."),
    dict(d="others", cat="F&B", yr=2025, hot="",
         name="Lotte Jamsil Seasonal Bakery Pop-up", brand="Lotte Department Store Jamsil",
         desc="Premium seasonal dessert pop-ups at Lotte Jamsil B1 bakery hall with season-limited pastry brands and holiday gift sets.",
         loc="Lotte Dept. Store Jamsil, B1F", date="Seasonal", adm="Free", goods="Seasonal pastries + gift sets",
         tags=["Dessert","Gift Set","Seasonal","Jamsil","Bakery"],
         why="Department store bakery event halls are the most reliable pop-up format in Korea — low risk, high impulse purchase rate."),
    dict(d="others", cat="Fashion", yr=2025, hot="",
         name="SYSTEM FW25 Pop-up — Lotte World Mall", brand="SYSTEM",
         desc="Korean contemporary fashion brand SYSTEM's FW25 collection launch pop-up with pre-order sessions and early access.",
         loc="Lotte World Mall, Jamsil", date="~ Nov 6, 2025", adm="Free", goods="FW25 early access + pre-order",
         tags=["Contemporary Fashion","FW25","Pre-order","Korean Brand"],
         why="SYSTEM's use of Lotte World Mall expands its reach beyond Seongsu's fashion bubble to mainstream MZ consumers."),
]

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
            cols[i % 3].markdown(card_html, unsafe_allow_html=True)

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
    st.markdown("<p class='slabel'>2024 National Category Share (total 1,431 nationwide)</p>", unsafe_allow_html=True)
    nat = pd.DataFrame({
        "Category": ["IP · Character","Fashion","Beauty","F&B","Art · Exhibition","Lifestyle","Other"],
        "Share":    [21, 19, 11, 10, 8, 7, 24],
    })
    fig5 = px.bar(nat, x="Category", y="Share", color="Category",
                  color_discrete_map={**CAT_COLORS,"Other":"#6b7280"},
                  text="Share", template="plotly_dark")
    fig5.update_layout(**DARK, showlegend=False, height=300, yaxis_title="Share (%)")
    fig5.update_traces(marker_line_width=0, textposition="outside",
                       texttemplate="%{text}%", textfont=dict(color="#f0eee8"))
    st.plotly_chart(fig5, use_container_width=True)

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
