import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Seoul Pop-up Store Trend Map 2024–2026",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS (exact design from uploaded HTML) ──────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400&family=Inter:wght@300;400;500;600&display=swap');

:root{
  --bg:#04060d;--surface:#080c18;--card:#0d1221;--card2:#121827;
  --pink:#ff6b9d;--cyan:#00e5cc;--yellow:#ffd166;--purple:#a78bfa;
  --orange:#ff9a3c;--green:#4ade80;--blue:#60a5fa;
  --text:#f0eee8;--muted:#6b7280;--border:rgba(255,255,255,0.07);
}

html,body,[class*="css"]{
  font-family:'Inter',sans-serif !important;
  background:#04060d !important;
  color:#f0eee8 !important;
}

/* Remove streamlit default padding */
.block-container{padding:0 !important;max-width:100% !important;}
section.main > div{padding:0 !important;}
[data-testid="stAppViewContainer"]{background:#04060d !important;}
[data-testid="stHeader"]{background:transparent !important;}

/* Sidebar */
[data-testid="stSidebar"]{
  background:rgba(4,6,13,0.97) !important;
  border-right:1px solid var(--border) !important;
}
[data-testid="stSidebar"] *{color:#f0eee8 !important;}
[data-testid="stSidebar"] label{
  font-size:10px !important;letter-spacing:.16em !important;
  text-transform:uppercase !important;color:var(--muted) !important;
  font-family:'DM Mono',monospace !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"]{
  background:rgba(0,229,204,.15) !important;
  border:1px solid var(--cyan) !important;
  color:var(--cyan) !important;
}
[data-testid="stSidebar"] input{
  background:var(--card) !important;
  border:1px solid var(--border) !important;
  color:var(--text) !important;
  border-radius:20px !important;
}

/* Hero */
.hero-wrap{
  background:var(--bg);
  padding:100px 48px 64px;
  position:relative;overflow:hidden;
  border-bottom:1px solid var(--border);
}
.hero-wrap::before{
  content:'';position:absolute;inset:0;
  background:
    radial-gradient(ellipse 60% 50% at 15% 20%,rgba(255,107,157,.07) 0%,transparent 65%),
    radial-gradient(ellipse 50% 40% at 85% 70%,rgba(0,229,204,.06) 0%,transparent 60%),
    radial-gradient(ellipse 40% 60% at 50% 100%,rgba(167,139,250,.05) 0%,transparent 60%);
  pointer-events:none;
}
.hero-eyebrow{
  font-size:10px;letter-spacing:.22em;text-transform:uppercase;
  color:var(--cyan);margin-bottom:16px;display:flex;align-items:center;gap:10px;
  font-family:'DM Mono',monospace;
}
.hero-eyebrow::before{content:'';width:32px;height:1px;background:var(--cyan);display:inline-block;}
.hero-h1{
  font-family:'Syne',sans-serif !important;
  font-size:clamp(42px,8vw,90px);font-weight:800;
  letter-spacing:-.04em;line-height:.93;margin-bottom:28px;
}
.hero-h1 .l1{color:var(--text);}
.hero-h1 .l2{
  background:linear-gradient(90deg,var(--pink),var(--purple),var(--cyan));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-sub{max-width:580px;color:var(--muted);font-size:15px;line-height:1.9;margin-bottom:32px;}
.hero-sub strong{color:var(--text);}
.year-bar{display:flex;gap:6px;margin-bottom:32px;flex-wrap:wrap;}
.year-tag{font-size:10px;letter-spacing:.14em;text-transform:uppercase;padding:5px 14px;
  border:1px solid var(--border);border-radius:20px;color:var(--muted);
  font-family:'DM Mono',monospace;}
.year-tag.y2024{border-color:var(--yellow);color:var(--yellow);}
.year-tag.y2025{border-color:var(--orange);color:var(--orange);}
.year-tag.y2026{border-color:var(--pink);color:var(--pink);}
.stats-row{display:flex;gap:40px;flex-wrap:wrap;}
.stat{border-left:2px solid var(--pink);padding-left:16px;}
.stat-num{font-family:'Syne',sans-serif;font-size:30px;font-weight:800;color:var(--pink);line-height:1;}
.stat-label{font-size:10px;color:var(--muted);letter-spacing:.08em;margin-top:4px;text-transform:uppercase;}
.stat:nth-child(2){border-color:var(--cyan);} .stat:nth-child(2) .stat-num{color:var(--cyan);}
.stat:nth-child(3){border-color:var(--yellow);} .stat:nth-child(3) .stat-num{color:var(--yellow);}
.stat:nth-child(4){border-color:var(--purple);} .stat:nth-child(4) .stat-num{color:var(--purple);}

/* Filter bar */
.filter-bar{
  background:rgba(4,6,13,.95);backdrop-filter:blur(14px);
  border-bottom:1px solid var(--border);padding:14px 48px;
  display:flex;gap:8px;flex-wrap:wrap;align-items:center;
  position:sticky;top:0;z-index:100;
}
.filter-label{font-size:10px;letter-spacing:.15em;text-transform:uppercase;
  color:var(--muted);margin-right:4px;font-family:'DM Mono',monospace;}
.filter-btn{padding:6px 14px;border:1px solid var(--border);background:transparent;
  color:var(--muted);font-family:'Inter',sans-serif;font-size:12px;cursor:pointer;
  transition:all .25s;border-radius:20px;white-space:nowrap;}
.filter-btn:hover{border-color:var(--cyan);color:var(--cyan);}
.filter-btn.active{background:var(--cyan);border-color:var(--cyan);color:#04060d;font-weight:600;}

/* District section */
.district-wrap{padding:56px 48px 32px;}
.district-wrap.alt{background:var(--surface);}
.district-badge{font-size:10px;letter-spacing:.18em;text-transform:uppercase;
  padding:4px 12px;border:1px solid currentColor;border-radius:20px;
  font-family:'DM Mono',monospace;margin-right:12px;}
.district-name{font-family:'Syne',sans-serif;font-size:clamp(26px,4vw,42px);
  font-weight:800;letter-spacing:-.03em;display:inline;}
.district-sub{font-size:12px;color:var(--muted);font-family:'DM Mono',monospace;
  display:block;margin-top:6px;}
.district-desc{max-width:620px;color:var(--muted);font-size:13px;line-height:1.9;
  margin:14px 0 28px;}

/* Pop-up cards */
.popup-card{
  background:var(--card);border:1px solid var(--border);padding:22px;
  cursor:pointer;transition:all .3s;position:relative;overflow:hidden;
  margin-bottom:14px;border-radius:2px;
}
.popup-card:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.14);background:var(--card2);}
.pc-topbar{height:2px;margin:-22px -22px 18px;}
.pc-row1{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;}
.pc-cat{font-size:9px;letter-spacing:.14em;text-transform:uppercase;
  padding:3px 8px;border-radius:10px;font-family:'DM Mono',monospace;}
.pc-right{display:flex;flex-direction:column;align-items:flex-end;gap:3px;}
.pc-year{font-size:9px;font-family:'DM Mono',monospace;border:1px solid var(--border);
  padding:2px 6px;border-radius:6px;color:var(--muted);}
.pc-year.y2026{border-color:var(--pink);color:var(--pink);}
.pc-year.y2025{border-color:var(--orange);color:var(--orange);}
.pc-year.y2024{border-color:var(--yellow);color:var(--yellow);}
.pc-hot{font-size:9px;color:var(--pink);font-family:'DM Mono',monospace;}
.pc-name{font-size:15px;font-weight:600;color:var(--text);margin-bottom:4px;line-height:1.35;
  font-family:'Inter',sans-serif;}
.pc-brand{font-size:11px;color:var(--muted);margin-bottom:10px;font-family:'DM Mono',monospace;}
.pc-desc{font-size:12px;color:var(--muted);line-height:1.75;margin-bottom:12px;}
.pc-meta{font-size:11px;color:var(--muted);font-family:'DM Mono',monospace;}
.pc-meta-row{display:flex;gap:6px;margin-bottom:4px;}
.card-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:12px;}
.ctag{font-size:9px;letter-spacing:.1em;text-transform:uppercase;
  padding:3px 8px;border:1px solid var(--border);color:var(--muted);border-radius:10px;}

/* Category colors */
.cat-fashion{background:rgba(255,107,157,.15);color:var(--pink);}
.cat-beauty{background:rgba(167,139,250,.15);color:var(--purple);}
.cat-fb{background:rgba(255,154,60,.15);color:var(--orange);}
.cat-ip{background:rgba(255,209,102,.15);color:var(--yellow);}
.cat-art{background:rgba(74,222,128,.15);color:var(--green);}
.cat-lifestyle{background:rgba(96,165,250,.15);color:var(--blue);}
.bar-fashion{background:var(--pink);}
.bar-beauty{background:var(--purple);}
.bar-fb{background:var(--orange);}
.bar-ip{background:var(--yellow);}
.bar-art{background:var(--green);}
.bar-lifestyle{background:var(--blue);}

/* Modal overlay */
.modal-overlay{
  position:fixed;inset:0;background:rgba(4,6,13,.8);z-index:9000;
  display:flex;align-items:center;justify-content:center;padding:20px;
  backdrop-filter:blur(6px);
}
.modal{
  background:var(--card2);border:1px solid rgba(255,255,255,.1);
  max-width:640px;width:100%;max-height:90vh;overflow-y:auto;
  position:relative;border-radius:4px;
  box-shadow:0 32px 80px rgba(0,0,0,.6);
}
.modal-topbar{height:3px;border-radius:4px 4px 0 0;}
.modal-body{padding:32px 36px 36px;}
.modal-cat-row{font-size:9px;letter-spacing:.18em;text-transform:uppercase;
  font-family:'DM Mono',monospace;margin-bottom:14px;
  display:flex;align-items:center;gap:10px;}
.modal-cat-row::after{content:'';flex:1;height:1px;background:var(--border);}
.modal-name{font-family:'Syne',sans-serif;font-size:clamp(20px,3vw,28px);
  font-weight:800;margin-bottom:6px;line-height:1.2;}
.modal-brand{font-size:12px;color:var(--muted);font-family:'DM Mono',monospace;margin-bottom:20px;}
.modal-desc{font-size:14px;color:rgba(240,238,232,.75);line-height:1.9;margin-bottom:24px;}
.modal-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:22px;}
.modal-info{background:rgba(255,255,255,.03);border:1px solid var(--border);padding:14px 16px;border-radius:2px;}
.mi-label{font-size:9px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--muted);margin-bottom:5px;font-family:'DM Mono',monospace;}
.mi-val{font-size:13px;color:var(--text);line-height:1.5;}
.modal-why{
  background:rgba(255,107,157,.06);border-left:2px solid var(--pink);
  padding:14px 18px;font-size:13px;color:rgba(240,238,232,.65);
  line-height:1.8;font-style:italic;border-radius:0 2px 2px 0;
}
.modal-why strong{color:var(--pink);font-style:normal;}

/* Trend cards */
.trend-card{
  background:var(--card);border:1px solid var(--border);padding:28px;
  border-radius:2px;margin-bottom:16px;
}
.trend-num{font-family:'Syne',sans-serif;font-size:44px;font-weight:800;line-height:1;margin-bottom:12px;}
.trend-title{font-size:14px;font-weight:600;margin-bottom:8px;color:var(--text);}
.trend-desc{font-size:12px;color:var(--muted);line-height:1.8;}

/* Section label */
.sec-label{font-size:10px;letter-spacing:.22em;text-transform:uppercase;
  color:var(--cyan);margin-bottom:8px;font-family:'DM Mono',monospace;}
.sec-title{font-family:'Syne',sans-serif;font-size:clamp(26px,3.5vw,40px);
  font-weight:800;letter-spacing:-.03em;margin-bottom:20px;}

/* Divider */
.neon-div{height:1px;background:linear-gradient(90deg,transparent,var(--pink),var(--cyan),transparent);margin:48px 0;}

/* Plotly dark override */
.js-plotly-plot .plotly .bg{fill:#0d1221 !important;}

/* Result count */
.result-count{font-family:'DM Mono',monospace;font-size:11px;color:var(--muted);
  padding:8px 48px 0;}

/* Streamlit tabs */
[data-testid="stTab"]{color:var(--muted) !important;font-size:12px !important;letter-spacing:.1em !important;}
[aria-selected="true"]{color:var(--cyan) !important;border-bottom:2px solid var(--cyan) !important;}
</style>
""", unsafe_allow_html=True)

# ── DATA ─────────────────────────────────────────────────────────────────────
POPUPS = [
    # SEONGSU 2026
    dict(district="seongsu",cat="IP · Character",year=2026,hot="🔥 HOT",
         name="Pokémon Ditto (Metamon) Playground",brand="Pokémon Mega Festa 2026",
         desc="Enter a pink, squishy world where Ditto has copied everything — slides, plush toys, and décor. Part of Pokémon's 30th Anniversary celebrations in Seoul.",
         location="Seongsui-ro 7ga-gil 9, Seongsu",date="May 1 – Jun 21, 2026 · 10:00–21:00",
         admission="Free",goods="Limited Ditto-only merchandise",
         tags=["Pokémon","30th Anniversary","Free","Photo Zone"],
         why="One of three simultaneous Pokémon events in Seongsu — the scale of Pokémon Mega Festa 2026 is unprecedented, transforming the entire district into a fan pilgrimage site."),
    dict(district="seongsu",cat="IP · Character",year=2026,hot="🏆 Major",
         name="Pokémon 30th Birthday Party Pop-up",brand="Pokémon Mega Festa 2026 × Olive Young N Seongsu",
         desc="Birthday-party themed pop-up with cake, ribbon & balloon photo zones, a coloring corner, and exclusive 'Birthday Party Edition' merchandise.",
         location="Olive Young N Seongsu, Trend Pot (1F)",date="May 1 – Jun 21, 2026",
         admission="Free",goods="Limited Birthday Edition goods",
         tags=["Pokémon","Birthday","30th","Limited Ed."],
         why="Olive Young's strategic collab leverages Pokémon mania to drive flagship traffic — a perfect channel partnership model for K-beauty retail."),
    dict(district="seongsu",cat="Beauty",year=2026,hot="",
         name="Olive Young × Pokémon Pikachu Picnic",brand="Olive Young N Seongsu",
         desc="K-Beauty meets Pokémon. Olive Young's 1F Trend Fountain becomes a Pikachu & Minibu picnic with photo spots, collab merchandise, and themed beauty bundles.",
         location="Olive Young N Seongsu, 1F",date="May 1 – May 31, 2026",
         admission="Free",goods="Collab beauty bundles",
         tags=["K-Beauty","Pokémon","Collab","Seasonal"],
         why="Shows how a beauty retailer can use IP licensing to create destination-worthy experiences rather than a simple product display."),
    dict(district="seongsu",cat="IP · Character",year=2026,hot="🔥 HOT",
         name="SEVENTEEN MINITEEN Flagship Pop-up",brand="SEVENTEEN × Pledis Entertainment",
         desc="Two-story flagship pop-up for SEVENTEEN's MINITEEN character lineup. Floor 1: themed café with ice cream & signature drinks. Floor 2: full character merchandise floor.",
         location="Seongsu-dong (2-story space)",date="May 23 – Jun 2, 2026",
         admission="Free",goods="Character merch + café menu",
         tags=["K-Pop","SEVENTEEN","Café","Flagship"],
         why="The two-floor café + shop format maximises dwell time and spend per visitor — a growing blueprint for K-pop pop-ups."),
    dict(district="seongsu",cat="Fashion",year=2026,hot="",
         name="Lacoste 'Polo Factory' Pop-up",brand="Lacoste",
         desc="French heritage brand celebrates 90+ years of the polo shirt through an immersive walk-through of the iconic silhouette's construction — fabrics, colorways, sustainability.",
         location="Seongsu-dong",date="May 21 – Jun 3, 2026",
         admission="Free",goods="Heritage collection + limited pieces",
         tags=["Heritage","Fashion","Exhibition","Sustainability"],
         why="Lacoste chose Seongsu over Gangnam to reach younger MZ consumers — a deliberate repositioning of a legacy brand toward a new generation."),
    dict(district="seongsu",cat="Fashion",year=2026,hot="",
         name="Musinsa KICKS Summer Pop-up",brand="Musinsa KICKS × HOTEL POCO Seongsu",
         desc="Musinsa's sneaker vertical gathers seasonal silhouettes from multiple brands under one roof. Compare moods, materials, and styling side by side.",
         location="HOTEL POCO Seongsu",date="May 26 – Jun 13, 2026",
         admission="Free",goods="Multi-brand sneaker selection",
         tags=["Sneakers","Streetwear","Musinsa","Multi-brand"],
         why="Using Seongsu's boutique hotel culture as a pop-up venue signals the premium direction Musinsa is pursuing for its sneaker brand."),
    dict(district="seongsu",cat="Beauty",year=2026,hot="✨ Notable",
         name="YSL Beauty Seongsu Pop-up",brand="Yves Saint Laurent Beauty",
         desc="Luxury French beauty brand's immersive pop-up. New collection launch, makeup experience zones, and exclusive YSL merchandise only available at this location.",
         location="Seongsu-dong",date="May 9 – May 24, 2026",
         admission="Free",goods="Exclusive YSL location goods",
         tags=["Luxury Beauty","Makeup","YSL","Exclusive"],
         why="YSL entering Seongsu rather than Apgujeong signals how the district has matured into a credible luxury brand destination."),
    dict(district="seongsu",cat="Beauty",year=2026,hot="",
         name="La Roche-Posay — UV Stadium",brand="La Roche-Posay",
         desc="Sports-themed sunscreen pop-up turning skincare education into a stadium experience. UV protection zones, SPF trials, and high-concept photo installations.",
         location="Seongsu-dong",date="May 15 – May 25, 2026",
         admission="Free",goods="SPF sample kits",
         tags=["Sunscreen","Skincare","Experiential","Sports"],
         why="Turning skincare into a stadium concept shows how brands compete for attention through narrative rather than product specs alone."),
    dict(district="seongsu",cat="Fashion",year=2026,hot="🏆 Major",
         name="Musinsa Megastore Seongsu — Grand Opening",brand="Musinsa",
         desc="Grand opening of Musinsa's flagship megastore. Multi-brand fashion pop-ups, exclusive drops, and opening celebration events spanning the entire building.",
         location="Musinsa Megastore Seongsu",date="Apr 24 – May 3, 2026",
         admission="Free",goods="Exclusive opening drops",
         tags=["Flagship","Musinsa","Multi-brand","Grand Opening"],
         why="Musinsa's permanent megastore formalises Seongsu's evolution from pop-up hub to year-round fashion destination."),
    dict(district="seongsu",cat="Fashion",year=2026,hot="",
         name="Moncler Puppy Summer Exhibition",brand="Moncler",
         desc="Luxury Italian outerwear brand brings its playful 'Puppy' summer collection to Seongsu in an art-forward exhibition format with seasonal limited-edition pieces.",
         location="Seongsui-ro 16-gil 31, Seongsu",date="May 1 – May 3, 2026",
         admission="Free",goods="Limited summer pieces",
         tags=["Luxury","Exhibition","Fashion","Moncler"],
         why="Moncler's gallery-style format elevates the brand experience — visitors engage with the collection as they would a gallery show."),
    dict(district="seongsu",cat="IP · Character",year=2026,hot="🔥 HOT",
         name="NCT WISH Official Pop-up Store",brand="SM Entertainment",
         desc="Official pop-up for NCT WISH timed to their new release. Fan interaction zones, photo booths, and exclusive Seoul-edition merchandise.",
         location="Seongsu-dong",date="Apr 27 – May 3, 2026",
         admission="Free",goods="Seoul-edition MD + photocards",
         tags=["K-Pop","NCT","Fan Event","Seoul Exclusive"],
         why="SM chose Seongsu over SM Town Coex — reflecting the commercial appeal of Seongsu's younger, style-conscious foot traffic."),
    dict(district="seongsu",cat="IP · Character",year=2026,hot="🏆 Global",
         name="BLACKPINK 'DEADLINE' Global Pop-up",brand="BLACKPINK × YG Entertainment",
         desc="World pop-up tour launching in Seoul first at Musinsa Seongsu & Musinsa Myeongdong. Exclusive Seoul-edition MD, new lightstick, plush, keyrings and keycaps. Continued in 20 cities worldwide.",
         location="Musinsa Seongsu + Musinsa Myeongdong",date="Feb 28 – Mar 8, 2026 · 11:00–22:00",
         admission="Free",goods="Seoul-exclusive MD + lightstick",
         tags=["BLACKPINK","K-Pop","Global Tour","Album","Musinsa"],
         why="Seoul as the global first stop for BLACKPINK's world pop-up tour confirms the city's status as the world's most important pop-up market in 2026."),
    dict(district="seongsu",cat="Lifestyle",year=2026,hot="",
         name="Samsung Galaxy Market Event",brand="Samsung Electronics",
         desc="Samsung's experiential pop-up at T Factory Seongsu — latest Galaxy devices with hands-on trials, exclusive launch bundles, and immersive tech zones.",
         location="T Factory Seongsu, Yeonmujang 1-gil",date="Feb 27 – Mar 29, 2026",
         admission="Free",goods="Device trial + exclusive bundles",
         tags=["Tech","Samsung","Galaxy","Experiential"],
         why="Tech brands using Seongsu's creative spaces signals the district's broad cultural credibility — it's no longer just fashion and beauty."),
    # SEONGSU 2025
    dict(district="seongsu",cat="Fashion",year=2025,hot="",
         name="Hoka Seongsu Pop-up",brand="HOKA",
         desc="Running & trail shoe brand's Seongsu pop-up with fit experience stations, limited-color drops, and stamp-tour giveaways.",
         location="East Yeonmujang-gil, Seongsu",date="Jan 2025",
         admission="Free",goods="Limited colorway + stamp goods",
         tags=["Running","Experiential","Showroom","Sneakers"],
         why="Hoka's shift from performance to lifestyle is embodied in Seongsu — it targets trend-aware consumers, not just runners."),
    dict(district="seongsu",cat="F&B",year=2025,hot="🔥 Viral",
         name='Adidas Café "3 STRIPES Seoul"',brand="Adidas × Café Concept",
         desc="Fashion meets coffee — a viral social media sensation before it even opened. Three-stripe signature drinks, limited merch, and brand installations drew massive queues.",
         location="Seongsu-dong",date="Jan 2025 (~Jan 18)",
         admission="Free",goods="Limited drinks & merch",
         tags=["Collab","Café","Sports","Viral","SNS"],
         why="Pre-opening social buzz turned this into a must-visit — a case study in anticipation-building driving pop-up traffic without paid advertising."),
    dict(district="seongsu",cat="Beauty",year=2025,hot="✨ Benchmark",
         name="iSOi 'Bulgaria Rose Trip' Pop-up",brand="iSOi",
         desc="Opened to celebrate iSOi's Seongsu flagship. An immersive Bulgaria rose concept space praised as a benchmark for brand-owned pop-up strategy — no rental costs, maximum organic buzz.",
         location="iSOi Flagship Store, Seongsu",date="Jan 2025",
         admission="Free",goods="Product samples",
         tags=["Skincare","Immersive","Flagship","Benchmark"],
         why="By owning the pop-up through their flagship, iSOi eliminated rental costs while generating enormous SNS buzz — the ideal model for mid-size beauty brands."),
    dict(district="seongsu",cat="IP · Character",year=2025,hot="",
         name="TBH × Hello Kitty Department Store",brand="tbh × Sanrio",
         desc="Hello Kitty 50th anniversary collab pop-up with co-designed limited apparel, accessories, and collectibles.",
         location="Seongsu-dong",date="Jan 2025",
         admission="Free",goods="Limited collab goods",
         tags=["Sanrio","Hello Kitty","Collab","Fashion","50th"],
         why="The Hello Kitty 50th anniversary proved the staying power of legacy IP — nostalgia-driven collabs consistently outperform trend-driven ones in purchase intent."),
    # SEONGSU 2024
    dict(district="seongsu",cat="Fashion",year=2024,hot="🏆 Large-scale",
         name="Musinsa Beauty Festa — Seongsu",brand="Musinsa",
         desc="Massive multi-brand pop-up town across Seongsu, bringing online-only beauty brands to their first ever offline experience spaces.",
         location="Seongsu-dong (area-wide)",date="2024",
         admission="Free",goods="Multi-brand beauty & fashion",
         tags=["Pop-up Town","Multi-brand","Large-scale","Pioneering"],
         why="The Musinsa Seongsu Festa proved that an e-commerce platform could run a physical pop-up town as effectively as a department store."),
    # HANNAM
    dict(district="hannam",cat="Beauty",year=2026,hot="✨ Notable",
         name="Pesade Hannam Flagship Opening",brand="Pesade",
         desc="Niche fragrance brand Pesade opens its Hannam flagship with a launch pop-up featuring personal scent consultations and exclusive opening-day sets.",
         location="Hannam-dong Flagship",date="2026",
         admission="Free",goods="Personal scent consultation + sets",
         tags=["Niche Fragrance","Flagship","Opening","Hannam"],
         why="Hannam's gallery culture makes it the natural home for niche fragrance brands seeking affluent, design-literate consumers."),
    dict(district="hannam",cat="Fashion",year=2025,hot="",
         name='Adidas × ABC Mart — "My Nth New Pair"',brand="ABC Mart × Adidas",
         desc="Season-launch pop-up combining ABC Mart's retail reach with Adidas' newest sneaker lineup. Limited silhouettes and on-site shoe personalisation service.",
         location="Hannam-dong",date="Jan 2025",
         admission="Free",goods="Limited sneaker lineup",
         tags=["Sneakers","Collab","Customise","Personalise"],
         why="Personalisation services dramatically increase time-in-store and purchase likelihood."),
    dict(district="hannam",cat="Art · Exhibition",year=2025,hot="",
         name="Hannam Emerging Artist Gallery Pop-up",brand="Hannam Independent Gallery Network",
         desc="Rotating platform for emerging Korean artists with works for sale alongside brand-collab art objects. Buyers receive limited-edition art books.",
         location="Hannam Gallery District",date="Seasonal, ongoing",
         admission="Free viewing",goods="Original artworks + art books",
         tags=["Art","Emerging Artist","Sales","Curation"],
         why="Hannam's gallery infrastructure allows emerging artists to access affluent collectors without a permanent gallery space."),
    dict(district="hannam",cat="Beauty",year=2025,hot="",
         name="European Niche Perfume — Korea Debut",brand="Hannam Concept Beauty Edit",
         desc="First Korean pop-up for a coveted European niche perfume house. Personal fragrance consultations and limited discovery sets.",
         location="Hannam Concept Store",date="Seasonal",
         admission="Free",goods="Discovery sets + consultation",
         tags=["Niche Perfume","Consultation","Debut","European"],
         why="Hannam's international-facing, luxury-comfortable demographic makes it the ideal test market for European niche brands entering Korea."),
    dict(district="hannam",cat="Fashion",year=2024,hot="",
         name="Hannam Vintage Fashion Market",brand="Hannam Vintage Curators",
         desc="Monthly curated vintage & resale pop-up market reflecting MZ consumers' growing interest in sustainable fashion.",
         location="Hannam-dong",date="Monthly, ongoing",
         admission="Free",goods="Vintage & resale items",
         tags=["Vintage","Resale","Sustainable","Monthly"],
         why="Sustainable fashion is the fastest-growing sub-trend in MZ consumption — Hannam's market taps this with a premium, curated approach."),
    dict(district="hannam",cat="Lifestyle",year=2025,hot="",
         name="Luxury Interior & Home Design Pop-up",brand="Hannam Flagship Brands",
         desc="Premium interior and home brand pop-up offering product experience and interior consultation services.",
         location="Hannam-dong",date="Seasonal",
         admission="Free",goods="Consultation + display items",
         tags=["Interior","Premium","Lifestyle","Consultation"],
         why="Home lifestyle brands use pop-ups to bridge the gap between e-commerce imagery and real-world texture."),
    # HONGDAE
    dict(district="hongdae",cat="IP · Character",year=2026,hot="🔥 HOT",
         name="ITZY [Motto] Official Pop-up Store",brand="ITZY × JYP Entertainment",
         desc="Official pop-up tied to ITZY's Motto release. Fan merch, photocard events, and exclusive Hongdae-only album bundles.",
         location="Mapo-gu, Hongdae area",date="May 19 – May 25, 2026",
         admission="Free",goods="Exclusive album bundle + photocards",
         tags=["K-Pop","ITZY","Fan Event","JYP","Hongdae Only"],
         why="Hongdae remains the spiritual home of K-pop fan culture — its density of dedicated fans makes it the natural first choice for comeback pop-ups."),
    dict(district="hongdae",cat="IP · Character",year=2025,hot="🔥 HOT",
         name="Chainsaw Man Official Pop-up",brand="AK Plaza Hongdae × MAPPA",
         desc="Large-scale official pop-up for the hit anime Chainsaw Man. Character goods, acrylic standees, apparel, and exclusive Korean-market collectibles. Long queues from day one.",
         location="AK Plaza Hongdae Branch",date="Sep 26 – Dec 31, 2025",
         admission="Free",goods="Anime character goods",
         tags=["Anime","IP","Goods","MAPPA","Long-run"],
         why="A 3-month run in a department store signals how anime IP has become a consistent, reliable driver of retail footfall."),
    dict(district="hongdae",cat="Beauty",year=2025,hot="✨ Notable",
         name="Olive Young Hongdae Town — Beauty Event",brand="CJ Olive Young",
         desc="Multi-brand beauty event at Olive Young's flagship Hongdae location. Makeup trials, new product demos, and SNS verification giveaways.",
         location="Olive Young Hongdae Town",date="Oct 2 – Oct 12, 2025",
         admission="Free",goods="Sample giveaways",
         tags=["K-Beauty","Multi-brand","Trial","SNS","Flagship"],
         why="Olive Young Hongdae's tourist-heavy foot traffic makes it one of the most cost-efficient locations for beauty brands to reach international shoppers."),
    dict(district="hongdae",cat="IP · Character",year=2024,hot="",
         name="K-Pop Official MD Pop-up Hub",brand="Major Entertainment Labels",
         desc="Hongdae's proximity to SM Town makes it a permanent K-pop corridor. Albums, photocards, lightsticks at every major comeback.",
         location="Hongdae, near SM Town",date="Comeback seasons, ongoing",
         admission="Free",goods="Random photocard events",
         tags=["K-Pop","Fandom","MD","SM Town","Ongoing"],
         why="Hongdae's structural role as K-pop's retail heartland is self-reinforcing: fans gather because brands pop up; brands pop up because fans gather."),
    dict(district="hongdae",cat="Art · Exhibition",year=2024,hot="",
         name="Hongdae Indie Artist Market",brand="Hongdae Art Scene",
         desc="Independent artist market selling handmade works, goods, and crafts — a defining feature of Hongdae's creative underground.",
         location="Hongdae Walk Street",date="2× monthly, ongoing",
         admission="Free",goods="Handmade works & goods",
         tags=["Handmade","Indie","Market","Authentic","Regular"],
         why="The indie artist market represents the grassroots origin of Seoul's pop-up culture — artists were using temporary spaces long before brands arrived."),
    # GANGNAM
    dict(district="gangnam",cat="IP · Character",year=2026,hot="🔥 HOT",
         name="Hello Kitty × Jisoo Pop-up",brand="Sanrio × Jisoo (BLACKPINK)",
         desc="Sanrio's Hello Kitty collabs with BLACKPINK's Jisoo for a Jamsil pop-up. Co-designed fashion pieces, limited character goods, and signature photo zones.",
         location="Jamsil, Songpa-gu",date="May 1–5, 2026 (Golden Week)",
         admission="Free",goods="Co-designed limited goods",
         tags=["Sanrio","BLACKPINK","Jisoo","Collab","Golden Week"],
         why="Combining Hello Kitty with BLACKPINK's Jisoo targets two overlapping fandoms simultaneously — commercially precise, executed during peak visitor season."),
    dict(district="gangnam",cat="F&B",year=2026,hot="",
         name="봄날엔 Spring Dessert Pop-up",brand="Bomnal-en Gangnam",
         desc="Spring-season dessert pop-up in Seocho/Gangnam. Seasonal pastries and limited menus for cherry blossom period with Instagram-ready floral setup.",
         location="Seocho-gu, Gangnam",date="May 19 – May 31, 2026",
         admission="Free",goods="Seasonal dessert menu",
         tags=["Dessert","Spring","Seasonal","Instagram"],
         why="Seasonal F&B pop-ups timed to cherry blossom season consistently outperform in foot traffic — the natural backdrop drives organic social sharing."),
    dict(district="gangnam",cat="IP · Character",year=2026,hot="🌿 Outdoor",
         name="Pokémon Secret Forest (Seoul Forest)",brand="Pokémon Mega Festa 2026",
         desc="Outdoor Pokémon pop-up where hidden Pokémon lurk among Seoul Forest trees, tied to the 2026 Seoul International Garden Expo.",
         location="Seoul Forest, Seongdong-gu",date="May 1 – Jun 21, 2026 · 10:00–20:00",
         admission="Free",goods="Outdoor original goods",
         tags=["Pokémon","Outdoor","Seoul Forest","Garden Expo"],
         why="Taking a pop-up outdoors into Seoul Forest transforms the experience from retail into a nature walk with brand discovery built in."),
    dict(district="gangnam",cat="IP · Character",year=2024,hot="🏆 Record",
         name="K League × Sanrio Characters",brand="K League × Sanrio",
         desc="The most successful pop-up of 2024: 250,000 total visitors, averaging 10,500 per day. A textbook example of cross-fandom collision.",
         location="The Hyundai Seoul",date="2024",
         admission="Free",goods="Cross-fandom limited goods",
         tags=["Cross-fandom","Record","Sanrio","K League","Sports"],
         why="This proves the most powerful pop-ups bridge two previously unconnected communities, doubling potential audience without increasing production complexity."),
    dict(district="gangnam",cat="Beauty",year=2024,hot="🏆 Large-scale",
         name="Coupang Mega Beauty Show",brand="Coupang × 9 Beauty Brands",
         desc="Nine major domestic and international beauty brands share one pop-up town. Visitors compare, trial, and purchase across all brands simultaneously.",
         location="Gangnam area large venue",date="2024",
         admission="Free",goods="Multi-brand trials & purchase",
         tags=["Pop-up Town","Multi-brand","Beauty","Benchmark"],
         why="Coupang coordinating 9 brands simultaneously shows how e-commerce platforms are emerging as the new department store operators of the pop-up era."),
    dict(district="gangnam",cat="F&B",year=2024,hot="",
         name="Market Kurly Food Festa",brand="Market Kurly",
         desc="Fresh-food e-commerce platform Kurly brings its curated brands offline. Live tasting experiences, cooking demos, and instant purchase of premium food items.",
         location="Gangnam area",date="2024",
         admission="Free",goods="Premium food items + tasting",
         tags=["F&B","E-commerce","Tasting","Premium"],
         why="Market Kurly's offline Festa addresses a core challenge for food e-commerce: consumers want to taste before buying."),
    dict(district="gangnam",cat="Art · Exhibition",year=2025,hot="",
         name="Seoul International Café Show",brand="COEX",
         desc="Korea's largest café & beverage industry expo. New F&B brand pop-ups, master barista demos, and specialty coffee showcases under one roof.",
         location="COEX, Gangnam",date="Nov 2025",
         admission="Paid admission",goods="Coffee products + limited brews",
         tags=["Café","Exhibition","Industry","Coffee","COEX"],
         why="The Café Show functions as an annual cultural moment for Seoul's café-obsessed MZ generation — not just an industry expo."),
    dict(district="gangnam",cat="IP · Character",year=2024,hot="",
         name="World Webtoon Festival 2024",brand="Webtoon Platform Alliance",
         desc="Major Korean and international webtoon IPs gather for a festival pop-up. Author signings, character goods, and interactive story-world exhibitions.",
         location="Gangnam area large venue",date="2024",
         admission="Paid admission",goods="Author-signed goods",
         tags=["Webtoon","IP","Festival","Author","Signing"],
         why="Webtoon IP generates deeply personal connections — fans follow characters for years, making purchase decisions highly emotional."),
    # OTHERS
    dict(district="others",cat="IP · Character",year=2026,hot="",
         name="Super Mario Pop-up @ Starfield Hanam",brand="Nintendo × Starfield Hanam",
         desc="Nintendo's Super Mario franchise lands at Starfield Hanam with interactive game-themed installations, character photo spots, and limited merchandise.",
         location="Starfield Hanam, Gyeonggi",date="May 2026 (Golden Week)",
         admission="Free",goods="Nintendo limited goods",
         tags=["Nintendo","Mario","Gaming","Interactive","Family"],
         why="Nintendo's strategic use of Golden Week maximises family traffic — Starfield's suburban location serves consumers who can't easily access central Seoul."),
    dict(district="others",cat="IP · Character",year=2026,hot="",
         name="TOURS Official Pop-up — Yongsan",brand="TOURS (K-Pop Group)",
         desc="K-Pop group TOURS brings their official pop-up to Yongsan iPark Mall. Fan merch, exclusive Yongsan-edition goods, and photocard event during Golden Week 2026.",
         location="Yongsan iPark Mall",date="May 1–5, 2026 (Golden Week)",
         admission="Free",goods="Exclusive Yongsan-edition merch",
         tags=["K-Pop","Fan Event","Yongsan","Golden Week"],
         why="Yongsan's proximity to major transit hubs makes it accessible to fans travelling from across the country."),
    dict(district="others",cat="Beauty",year=2026,hot="",
         name="BeautyPlus Moving × Mise-en-scène",brand="BeautyPlus Universe",
         desc="BeautyPlus's mobile pop-up at Sungshin Women's University in collaboration with hair care brand Mise-en-scène. Live demos and giveaways.",
         location="Seongbuk-gu (Sungshin Women's Univ.)",date="May 19, 2026",
         admission="Free",goods="Hair care giveaways",
         tags=["Hair Care","Mobile Pop-up","Campus","University"],
         why="Campus-based beauty pop-ups target precisely the MZ demographic at point of brand discovery."),
    dict(district="others",cat="Art · Exhibition",year=2025,hot="",
         name="DDP Emerging Designer Pop-up Market",brand="Dongdaemun Design Plaza",
         desc="Emerging designer market at the iconic DDP building. Fashion, product design, and crafts curated by category.",
         location="Dongdaemun Design Plaza (DDP)",date="1–2× monthly, ongoing",
         admission="Free",goods="Designer pieces & crafts",
         tags=["Emerging Designers","DDP","Market","Architecture"],
         why="The DDP's Zaha Hadid landmark status gives any pop-up hosted there a cultural legitimacy no standard commercial space can provide."),
    dict(district="others",cat="F&B",year=2025,hot="",
         name="Lotte Jamsil Seasonal Bakery Pop-up",brand="Lotte Department Store Jamsil",
         desc="Premium seasonal dessert pop-ups at Lotte Jamsil B1 bakery event hall. Season-limited pastry brands and holiday gift sets.",
         location="Lotte Dept. Store Jamsil, B1F",date="Seasonal",
         admission="Free",goods="Seasonal pastries + gift sets",
         tags=["Dessert","Gift Set","Seasonal","Jamsil","Bakery"],
         why="Department store bakery event halls are the most reliable pop-up format in Korea — low risk, high impulse purchase rate."),
    dict(district="others",cat="Fashion",year=2025,hot="",
         name="SYSTEM FW25 Pop-up — Lotte World Mall",brand="SYSTEM",
         desc="Korean contemporary fashion brand SYSTEM's FW25 collection launch pop-up at Lotte World Mall. Pre-order sessions and exclusive early access.",
         location="Lotte World Mall, Jamsil",date="~ Nov 6, 2025",
         admission="Free",goods="FW25 early access + pre-order",
         tags=["Contemporary Fashion","FW25","Pre-order","Korean Brand"],
         why="SYSTEM's use of Lotte World Mall expands its reach beyond Seongsu's fashion bubble to mainstream MZ consumers."),
]

df = pd.DataFrame(POPUPS)

# ── COLOUR MAPS ───────────────────────────────────────────────────────────────
CAT_COLOR = {
    "Fashion":         "#ff6b9d",
    "Beauty":          "#a78bfa",
    "F&B":             "#ff9a3c",
    "IP · Character":  "#ffd166",
    "Art · Exhibition":"#4ade80",
    "Lifestyle":       "#60a5fa",
}
CAT_CLASS = {
    "Fashion":"cat-fashion","Beauty":"cat-beauty","F&B":"cat-fb",
    "IP · Character":"cat-ip","Art · Exhibition":"cat-art","Lifestyle":"cat-lifestyle",
}
BAR_CLASS = {
    "Fashion":"bar-fashion","Beauty":"bar-beauty","F&B":"bar-fb",
    "IP · Character":"bar-ip","Art · Exhibition":"bar-art","Lifestyle":"bar-lifestyle",
}
DIST_META = {
    "seongsu":  {"label":"01","name":"Seongsu-dong",           "sub":"Seoul's #1 Pop-up District · 성수동",     "color":"var(--pink)",   "alt":False},
    "hannam":   {"label":"02","name":"Hannam-dong",             "sub":"Premium Lifestyle Belt · 한남동",          "color":"var(--cyan)",   "alt":True},
    "hongdae":  {"label":"03","name":"Hongdae",                 "sub":"University Culture · 홍대",                "color":"var(--purple)", "alt":False},
    "gangnam":  {"label":"04","name":"Gangnam · The Hyundai",   "sub":"Retail Power Zone · 강남 · 여의도",        "color":"var(--yellow)", "alt":True},
    "others":   {"label":"05","name":"Other Areas",             "sub":"Jamsil · Yongsan · DDP · Myeongdong",    "color":"var(--orange)", "alt":False},
}
DIST_DESC = {
    "seongsu":"A former industrial zone of repurposed factories, Seongsu hosts more pop-ups than any other neighbourhood in Korea. East Yeonmujang-gil is the current hotspot — 2026 brings Pokémon Mega Festa, BLACKPINK DEADLINE, and Musinsa's new megastore.",
    "hannam":"Seoul's gallery and boutique corridor. Hannam attracts luxury, niche fragrance, and art-forward pop-ups. The Hangang-jin to Hannam Crossroads stretch is lined with curated independent spaces favoured by design-conscious consumers.",
    "hongdae":"University culture meets indie creativity. Hongdae is the epicentre for K-pop fan pop-ups, beauty events, and independent artist markets. AK Plaza Hongdae and Olive Young Hongdae Town are key anchor venues in 2025–2026.",
    "gangnam":"The Hyundai Seoul in Yeouido rivals Seongsu as Korea's top pop-up venue. K League × Sanrio here drew 250,000 visitors in 2024. Department stores and malls drive high-volume, sales-focused pop-ups across all categories.",
    "others":"Pop-up culture has spread across all of Seoul. Department stores, outlet malls, and campus areas now serve as key pop-up venues, reflecting the democratisation of the format beyond its Seongsu epicentre.",
}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 8px'>
      <div style='color:#00e5cc;font-size:10px;letter-spacing:.2em;text-transform:uppercase;margin-bottom:6px;font-family:"DM Mono",monospace'>Research Project</div>
      <div style='font-family:"Syne",sans-serif;font-size:1.4rem;font-weight:800;color:#f0eee8;letter-spacing:-.02em'>Jooeun Lim</div>
      <div style='font-size:11px;color:#6b7280;margin-top:2px;font-family:"DM Mono",monospace'>SKKU · Department of Dance</div>
    </div>
    <hr style='border-color:rgba(255,255,255,.07);margin:14px 0'>
    """, unsafe_allow_html=True)

    st.markdown("<div style='color:#ff6b9d;font-size:10px;letter-spacing:.18em;text-transform:uppercase;margin-bottom:10px;font-family:\"DM Mono\",monospace'>Filters</div>", unsafe_allow_html=True)

    all_cats = sorted(df["cat"].unique())
    sel_cats = st.multiselect("Category", all_cats, default=all_cats)

    all_years = sorted(df["year"].unique())
    sel_years = st.multiselect("Year", all_years, default=all_years)

    all_dists = ["seongsu","hannam","hongdae","gangnam","others"]
    dist_labels = {d: DIST_META[d]["name"] for d in all_dists}
    sel_dists = st.multiselect("District", list(dist_labels.values()), default=list(dist_labels.values()))
    sel_dists_keys = [k for k,v in dist_labels.items() if v in sel_dists]

    search_q = st.text_input("🔍 Search brand / name", "")

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,.07);margin:14px 0'>
    <div style='font-size:11px;color:#6b7280;line-height:1.9;font-family:"DM Mono",monospace'>
      Data:<br>Popga (1,431 entries 2024)<br>Seongsu Gorilla<br>Inside Seoul · DealSeoul<br>Field Research 2024–2026
    </div>
    """, unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
mask = (
    df["cat"].isin(sel_cats) &
    df["year"].isin(sel_years) &
    df["district"].isin(sel_dists_keys)
)
if search_q:
    sq = search_q.lower()
    mask = mask & (df["name"].str.lower().str.contains(sq) | df["brand"].str.lower().str.contains(sq))
filtered = df[mask].reset_index(drop=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-eyebrow">MZ Generation Research · Jooeun Lim · SKKU Dance</div>
  <div class="hero-h1">
    <span class="l1">Seoul Pop-up Store</span><br>
    <span class="l2">Trend Map 2024–2026</span>
  </div>
  <div class="year-bar">
    <span class="year-tag">2024–2026</span>
    <span class="year-tag y2024">2024</span>
    <span class="year-tag y2025">2025</span>
    <span class="year-tag y2026">2026 — Live Data</span>
  </div>
  <p class="hero-sub">
    A field-research database by <strong>Jooeun Lim</strong> mapping Seoul's pop-up culture across Seongsu, Hannam, Hongdae, Gangnam and beyond.
    Covers 2024 through spring <strong>2026</strong> — filter by category, year, or district using the sidebar.
  </p>
  <div class="stats-row">
    <div class="stat"><div class="stat-num">{len(filtered)}</div><div class="stat-label">Showing</div></div>
    <div class="stat"><div class="stat-num">{len(df)}</div><div class="stat-label">Total Listed</div></div>
    <div class="stat"><div class="stat-num">5</div><div class="stat-label">Districts</div></div>
    <div class="stat"><div class="stat-num">1,431</div><div class="stat-label">2024 Nationwide</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋  Pop-up Directory", "📊  Data & Charts", "💡  Key Trends"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DIRECTORY
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"<div class='result-count'>Showing {len(filtered)} pop-up{'s' if len(filtered)!=1 else ''}</div>", unsafe_allow_html=True)

    if filtered.empty:
        st.markdown("<div style='padding:60px 48px;color:#6b7280;font-family:\"DM Mono\",monospace'>No pop-ups match the current filters. Try adjusting the sidebar.</div>", unsafe_allow_html=True)

    for dist_key in ["seongsu","hannam","hongdae","gangnam","others"]:
        dist_df = filtered[filtered["district"] == dist_key]
        if dist_df.empty:
            continue

        meta = DIST_META[dist_key]
        color = meta["color"]
        bg = "background:var(--surface);" if meta["alt"] else ""

        st.markdown(f"""
        <div style='{bg}padding:48px 48px 8px'>
          <div style='display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:8px'>
            <span class='district-badge' style='color:{color};border-color:{color}'>{meta["label"]}</span>
            <span class='district-name' style='color:{color}'>{meta["name"]}</span>
            <span class='district-sub'>{meta["sub"]}</span>
          </div>
          <p class='district-desc'>{DIST_DESC[dist_key]}</p>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        for i, (_, row) in enumerate(dist_df.iterrows()):
            cc = CAT_CLASS.get(row["cat"], "cat-fashion")
            bc = BAR_CLASS.get(row["cat"], "bar-fashion")
            yc = f"y{row['year']}"
            tags_html = "".join(f'<span class="ctag">{t}</span>' for t in row["tags"])
            col_bg = "background:var(--surface);" if meta["alt"] else ""

            with cols[i % 3]:
                with st.expander(f"{'🔥 ' if row['hot'] else ''}{row['name']}"):
                    st.markdown(f"""
                    <div style='{col_bg}'>
                      <div class='pc-topbar {bc}'></div>
                      <div class='pc-row1'>
                        <span class='pc-cat {cc}'>{row["cat"]}</span>
                        <div class='pc-right'>
                          <span class='pc-year {yc}'>{row["year"]}</span>
                          {f'<span class="pc-hot">{row["hot"]}</span>' if row["hot"] else ''}
                        </div>
                      </div>
                      <div class='pc-brand'>{row["brand"]}</div>
                      <div class='pc-desc'>{row["desc"]}</div>
                      <div class='pc-meta'>
                        <div class='pc-meta-row'>📍 {row["location"]}</div>
                        <div class='pc-meta-row'>📅 {row["date"]}</div>
                        <div class='pc-meta-row'>🎟 {row["admission"]}</div>
                        <div class='pc-meta-row'>🎁 {row["goods"]}</div>
                      </div>
                      <div class='card-tags'>{tags_html}</div>
                      <div class='modal-why' style='margin-top:14px'>
                        <strong>📝 Research Note:</strong> {row["why"]}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<div class='neon-div' style='margin:0 48px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CHARTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div style='padding:32px 48px 0'>", unsafe_allow_html=True)

    PLOT_LAYOUT = dict(
        paper_bgcolor="#0d1221", plot_bgcolor="#0d1221",
        font=dict(family="DM Mono, monospace", size=11, color="#6b7280"),
        margin=dict(l=10, r=10, t=30, b=10),
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='sec-label' style='padding:0 0 4px'>Category Distribution</div>", unsafe_allow_html=True)
        cat_c = filtered["cat"].value_counts().reset_index()
        cat_c.columns = ["Category","Count"]
        fig1 = px.bar(cat_c, x="Count", y="Category", orientation="h",
                      color="Category", color_discrete_map=CAT_COLOR, template="plotly_dark")
        fig1.update_layout(**PLOT_LAYOUT, showlegend=False, height=300)
        fig1.update_traces(marker_line_width=0)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown("<div class='sec-label' style='padding:0 0 4px'>Year Breakdown</div>", unsafe_allow_html=True)
        yr_c = filtered["year"].value_counts().sort_index().reset_index()
        yr_c.columns = ["Year","Count"]
        yr_c["Year"] = yr_c["Year"].astype(str)
        fig2 = px.bar(yr_c, x="Year", y="Count", color="Year",
                      color_discrete_map={"2024":"#ffd166","2025":"#ff9a3c","2026":"#ff6b9d"},
                      template="plotly_dark", text="Count")
        fig2.update_layout(**PLOT_LAYOUT, showlegend=False, height=300)
        fig2.update_traces(marker_line_width=0, textposition="outside",
                           textfont=dict(color="#f0eee8"))
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("<div class='sec-label' style='padding:0 0 4px'>District Concentration</div>", unsafe_allow_html=True)
        dist_c = filtered["district"].map({k:v["name"] for k,v in DIST_META.items()}).value_counts().reset_index()
        dist_c.columns = ["District","Count"]
        DIST_COLORS_HEX = {"Seongsu-dong":"#ff6b9d","Hannam-dong":"#00e5cc",
                           "Hongdae":"#a78bfa","Gangnam · The Hyundai":"#ffd166","Other Areas":"#ff9a3c"}
        fig3 = px.pie(dist_c, names="District", values="Count",
                      color="District", color_discrete_map=DIST_COLORS_HEX,
                      hole=0.45, template="plotly_dark")
        fig3.update_layout(**PLOT_LAYOUT, height=300,
                           legend=dict(font=dict(size=11, color="#6b7280")))
        fig3.update_traces(textfont_size=11)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown("<div class='sec-label' style='padding:0 0 4px'>Category × Year Heatmap</div>", unsafe_allow_html=True)
        pivot = df.groupby(["cat","year"]).size().reset_index(name="count")
        pw = pivot.pivot(index="cat", columns="year", values="count").fillna(0)
        fig4 = go.Figure(data=go.Heatmap(
            z=pw.values, x=[str(y) for y in pw.columns], y=pw.index.tolist(),
            colorscale=[[0,"#0d1221"],[0.5,"#a78bfa"],[1,"#ff6b9d"]],
            text=pw.values.astype(int), texttemplate="%{text}", showscale=False,
        ))
        fig4.update_layout(**PLOT_LAYOUT, height=300)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<div class='neon-div' style='margin:0 48px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-label' style='padding:0 48px 4px'>2024 National Category Share (1,431 nationwide)</div>", unsafe_allow_html=True)
    nat = pd.DataFrame({"Category":["IP · Character","Fashion","Beauty","F&B","Art · Exhibition","Lifestyle","Other"],
                         "Share":[21,19,11,10,8,7,24]})
    fig5 = px.bar(nat, x="Category", y="Share", color="Category",
                  color_discrete_map={**CAT_COLOR,"Other":"#6b7280"},
                  text="Share", template="plotly_dark")
    fig5.update_layout(**PLOT_LAYOUT, showlegend=False, height=320,
                       yaxis_title="Share (%)")
    fig5.update_traces(marker_line_width=0, textposition="outside",
                       texttemplate="%{text}%", textfont=dict(color="#f0eee8"))
    st.plotly_chart(fig5, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div style='padding:48px 48px 0'>
      <div class='sec-label'>Research Insight</div>
      <div class='sec-title'>Key Trends 2024–2026</div>
      <p style='color:#6b7280;font-size:13px;line-height:1.9;max-width:600px;margin-bottom:36px'>
        Field research by Jooeun Lim combined with data from Popga (1,431 pop-ups),
        Seongsu Gorilla, Inside Seoul, and DealSeoul platform analytics.
      </p>
    </div>
    """, unsafe_allow_html=True)

    trends = [
        {"num":"21%","color":"#ffd166","title":"IP & Character Dominance",
         "desc":"In 2024, 21% of all pop-ups were IP/character-driven. K League × Sanrio drew 250,000 visitors. In 2026, Pokémon Mega Festa alone spans 3 simultaneous events across Seongsu."},
        {"num":"11%","color":"#a78bfa","title":"Beauty Boom",
         "desc":"160 beauty & fragrance pop-ups in 2024 (11% of total). By 2026, luxury brands like YSL and La Roche-Posay run dedicated immersive pop-ups in Seongsu — not just product stalls."},
        {"num":"32%","color":"#ff6b9d","title":"East Yeonmujang-gil Surge",
         "desc":"32% of all Seongsu pop-ups in H1 2025 concentrated on East Yeonmujang-gil. Brands demand larger raw spaces for deeper content design — the east side is the creative frontier."},
        {"num":"52%","color":"#00e5cc","title":"Merch T-Shirt Rise",
         "desc":"Mentions of 'T-shirt' in pop-up communities rose 52% year-on-year. Graphic tees have become Gen Z identity markers — not just souvenirs, but statements of cultural participation."},
        {"num":"↑","color":"#ff9a3c","title":"Pop-up Town Format Accelerating",
         "desc":"Multi-brand 'pop-up towns' (Musinsa Festa, Coupang Beauty Show) maximise cost-efficiency and footfall. The format is accelerating sharply into 2026."},
        {"num":"NEW","color":"#4ade80","title":"Seoul Launches First",
         "desc":"In 2026, global tours (BLACKPINK DEADLINE, Pokémon 30th) now launch in Seoul before other world markets — confirming Seoul as the world's most important pop-up city."},
    ]

    cols = st.columns(3)
    for i, tr in enumerate(trends):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='trend-card' style='border-top:2px solid {tr["color"]}'>
              <div class='trend-num' style='color:{tr["color"]}'>{tr["num"]}</div>
              <div class='trend-title'>{tr["title"]}</div>
              <div class='trend-desc'>{tr["desc"]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding:32px 48px 48px'>
      <div class='neon-div'></div>
      <div class='sec-label'>Research Methodology</div>
      <div style='background:var(--card);border:1px solid var(--border);padding:28px 32px;margin-top:8px'>
        <p style='color:rgba(240,238,232,.65);font-size:13px;line-height:1.9;max-width:700px'>
          This pop-up store trend map is part of a broader research project examining how MZ generation consumers
          engage with experiential retail across Seoul. The dataset combines platform data from
          <strong style='color:#f0eee8'>Popga</strong> (Korea's largest pop-up tracking platform, 1,431 entries in 2024),
          <strong style='color:#f0eee8'>Seongsu Gorilla</strong>, <strong style='color:#f0eee8'>Inside Seoul</strong>,
          and <strong style='color:#f0eee8'>DealSeoul</strong> with personal field visits to Seongsu-dong and Hannam-dong.
          Each pop-up entry includes a research note analysing its strategic significance within the MZ consumption landscape.
        </p>
        <p style='color:#6b7280;font-size:11px;margin-top:14px;font-family:"DM Mono",monospace'>
          Jooeun Lim · SKKU Department of Dance · 2024–2026
        </p>
      </div>
    </div>
    """, unsafe_allow_html=True)
