import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Seoul Pop-up Store Trend Map 2024–2026",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  /* Hero banner */
  .hero {
    background: linear-gradient(135deg, #1a1510 0%, #2d2018 100%);
    border-radius: 12px;
    padding: 48px 52px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
  }
  .hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 8px;
    line-height: 1.1;
  }
  .hero h1 em { color: #d4b896; font-style: italic; }
  .hero p { color: rgba(255,255,255,0.55); font-size: 0.95rem; margin-top: 12px; max-width: 580px; }
  .hero .sub { color: #d4b896; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 8px; }

  /* Stat boxes */
  .stat-row { display: flex; gap: 20px; margin-top: 28px; flex-wrap: wrap; }
  .stat-box { border-left: 3px solid #b8966e; padding-left: 14px; }
  .stat-num { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #b8966e; line-height: 1; }
  .stat-label { font-size: 0.72rem; color: rgba(255,255,255,0.4); letter-spacing: 0.1em; text-transform: uppercase; margin-top: 4px; }

  /* Pop-up cards */
  .popup-card {
    background: white;
    border: 1px solid #ede4d8;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 14px;
    transition: box-shadow 0.2s;
    position: relative;
    overflow: hidden;
  }
  .popup-card:hover { box-shadow: 0 8px 28px rgba(90,60,30,0.12); }
  .card-topbar { height: 3px; margin: -20px -20px 16px; border-radius: 8px 8px 0 0; }
  .card-name { font-family: 'Playfair Display', serif; font-size: 1rem; font-weight: 700; color: #1a1510; margin-bottom: 4px; }
  .card-brand { font-size: 0.78rem; color: #9c8878; font-family: monospace; margin-bottom: 8px; }
  .card-desc { font-size: 0.82rem; color: #5c4a3a; line-height: 1.7; margin-bottom: 10px; }
  .card-meta { font-size: 0.78rem; color: #9c8878; font-family: monospace; }
  .card-tags { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px; }
  .ctag { font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 3px 8px;
          border: 1px solid #ede4d8; color: #9c8878; border-radius: 10px; background: #f8f5f0; }
  .badge { display: inline-block; font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase;
           padding: 2px 8px; border-radius: 10px; font-family: monospace; margin-right: 6px; }
  .year-badge { border: 1px solid; border-radius: 6px; }

  /* Research note */
  .research-note {
    background: linear-gradient(135deg, rgba(180,150,110,0.08), rgba(180,150,110,0.04));
    border-left: 3px solid #b8966e;
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    font-size: 0.82rem;
    color: #5c4a3a;
    font-style: italic;
    line-height: 1.7;
    margin-top: 10px;
  }

  /* Section headers */
  .section-label { font-size: 0.72rem; letter-spacing: 0.2em; text-transform: uppercase; color: #b8966e; font-weight: 500; margin-bottom: 4px; }
  .section-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; color: #1a1510; margin-bottom: 16px; }

  /* Sidebar */
  [data-testid="stSidebar"] { background: #1a1510; }
  [data-testid="stSidebar"] * { color: rgba(255,255,255,0.8) !important; }
  [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stMultiSelect label { color: #d4b896 !important; font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase; }

  /* Trend cards */
  .trend-card { background: #1a1510; border-radius: 8px; padding: 24px; color: white; height: 100%; }
  .trend-num { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 700; line-height: 1; margin-bottom: 10px; }
  .trend-title { font-size: 0.95rem; font-weight: 600; margin-bottom: 8px; color: white; }
  .trend-desc { font-size: 0.8rem; color: rgba(255,255,255,0.5); line-height: 1.7; }

  /* Divider */
  .gold-divider { height: 1px; background: linear-gradient(90deg, transparent, #b8966e, transparent); margin: 32px 0; }

  /* District badge */
  .dist-badge { display: inline-block; border: 1px solid; border-radius: 20px; padding: 3px 12px; font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase; font-family: monospace; margin-right: 10px; }
  .dist-title { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; display: inline; }
</style>
""", unsafe_allow_html=True)

# ── DATA ─────────────────────────────────────────────────────────────────────
POPUPS = [
    # ── SEONGSU 2026 ──────────────────────────────────────────────────────────
    dict(district="Seongsu-dong", cat="IP · Character", year=2026, hot="🔥 HOT",
         name="Pokémon Ditto (Metamon) Playground",
         brand="Pokémon Mega Festa 2026",
         desc="Enter a pink, squishy world where Ditto has copied everything — slides, plush toys, and décor. Part of Pokémon's 30th Anniversary celebrations in Seoul.",
         location="Seongsui-ro 7ga-gil 9, Seongsu-dong",
         date="May 1 – Jun 21, 2026 · Daily 10:00–21:00",
         admission="Free",
         goods="Limited Ditto-only merchandise",
         tags=["Pokémon", "30th Anniversary", "Free", "Photo Zone"],
         why="One of three simultaneous Pokémon events in Seongsu — Pokémon Mega Festa 2026 is unprecedented in scale, transforming the entire district into a fan pilgrimage site."),

    dict(district="Seongsu-dong", cat="IP · Character", year=2026, hot="🏆 Major",
         name="Pokémon 30th Birthday Party Pop-up",
         brand="Pokémon Mega Festa 2026 × Olive Young N Seongsu",
         desc="Birthday-party themed pop-up with cake, ribbon and balloon photo zones, a coloring corner, and exclusive 'Birthday Party Edition' merchandise.",
         location="Olive Young N Seongsu, Trend Pot (1F)",
         date="May 1 – Jun 21, 2026",
         admission="Free",
         goods="Limited Birthday Edition goods",
         tags=["Pokémon", "30th Anniversary", "Birthday", "Limited Ed."],
         why="Olive Young's strategic collab leverages Pokémon mania to drive traffic to its flagship — a perfect channel partnership model for beauty retail."),

    dict(district="Seongsu-dong", cat="Beauty", year=2026, hot="",
         name="Olive Young × Pokémon Pikachu Picnic",
         brand="Olive Young N Seongsu",
         desc="K-Beauty meets Pokémon — Olive Young's 1F Trend Fountain becomes a Pikachu & Minibu summer picnic with photo spots, collab merchandise, and themed beauty bundles.",
         location="Olive Young N Seongsu, 1F Trend Fountain",
         date="May 1 – May 31, 2026",
         admission="Free",
         goods="Collab beauty bundles",
         tags=["K-Beauty", "Pokémon", "Collab", "Seasonal"],
         why="Shows how a beauty retailer can use IP licensing to create destination-worthy experiences rather than a simple product display."),

    dict(district="Seongsu-dong", cat="IP · Character", year=2026, hot="🔥 HOT",
         name="SEVENTEEN MINITEEN Flagship Pop-up",
         brand="SEVENTEEN × Pledis Entertainment",
         desc="Two-story flagship pop-up for SEVENTEEN's MINITEEN character lineup. Floor 1: themed café with ice cream and signature drinks. Floor 2: full character merchandise.",
         location="Seongsu-dong (2-story space)",
         date="May 23 – Jun 2, 2026",
         admission="Free",
         goods="Character merch + café menu",
         tags=["K-Pop", "SEVENTEEN", "Café", "Flagship"],
         why="The two-floor café + shop format maximises dwell time and spend per visitor — a growing blueprint for K-pop pop-ups."),

    dict(district="Seongsu-dong", cat="Fashion", year=2026, hot="",
         name="Lacoste 'Polo Factory' Pop-up",
         brand="Lacoste",
         desc="French heritage brand celebrates 90+ years of the polo shirt through an immersive walk-through of the iconic silhouette's construction — fabrics, colorways, and sustainability story.",
         location="Seongsu-dong",
         date="May 21 – Jun 3, 2026",
         admission="Free",
         goods="Heritage collection + limited pieces",
         tags=["Heritage", "Fashion", "Exhibition", "Sustainability"],
         why="Lacoste chose Seongsu over Gangnam to reach younger MZ consumers — a deliberate repositioning of a legacy brand toward a new generation."),

    dict(district="Seongsu-dong", cat="Fashion", year=2026, hot="",
         name="Musinsa KICKS Summer Pop-up",
         brand="Musinsa KICKS × HOTEL POCO Seongsu",
         desc="Musinsa's sneaker vertical gathers seasonal silhouettes from multiple brands under one roof. Compare moods, materials, and styling side by side.",
         location="HOTEL POCO Seongsu",
         date="May 26 – Jun 13, 2026",
         admission="Free",
         goods="Multi-brand sneaker selection",
         tags=["Sneakers", "Streetwear", "Musinsa", "Multi-brand"],
         why="Using Seongsu's boutique hotel culture as a pop-up venue signals the premium direction Musinsa is pursuing for its sneaker brand."),

    dict(district="Seongsu-dong", cat="Beauty", year=2026, hot="✨ Notable",
         name="YSL Beauty Seongsu Pop-up",
         brand="Yves Saint Laurent Beauty",
         desc="Luxury French beauty brand's immersive pop-up. New collection launch, makeup experience zones, and exclusive YSL merchandise only available at this location.",
         location="Seongsu-dong",
         date="May 9 – May 24, 2026",
         admission="Free",
         goods="Exclusive YSL location goods",
         tags=["Luxury Beauty", "Makeup", "YSL", "Exclusive"],
         why="YSL entering Seongsu rather than Apgujeong signals how the district has matured into a credible luxury brand destination."),

    dict(district="Seongsu-dong", cat="Beauty", year=2026, hot="",
         name="La Roche-Posay — UV Stadium",
         brand="La Roche-Posay",
         desc="Sports-themed sunscreen pop-up turning skincare education into a stadium experience. UV protection zones, SPF trials, and high-concept photo installations.",
         location="Seongsu-dong",
         date="May 15 – May 25, 2026",
         admission="Free",
         goods="SPF sample kits",
         tags=["Sunscreen", "Skincare", "Experiential", "Sports"],
         why="Turning skincare into a stadium concept shows how brands compete for attention through narrative rather than product specs."),

    dict(district="Seongsu-dong", cat="Fashion", year=2026, hot="🏆 Major",
         name="Musinsa Megastore Seongsu — Grand Opening",
         brand="Musinsa",
         desc="Grand opening of Musinsa's flagship megastore. Multi-brand fashion pop-ups, exclusive drops, and opening celebration events spanning the entire building.",
         location="Musinsa Megastore Seongsu",
         date="Apr 24 – May 3, 2026",
         admission="Free",
         goods="Exclusive opening drops",
         tags=["Flagship", "Musinsa", "Multi-brand", "Grand Opening"],
         why="Musinsa's permanent megastore formalises Seongsu's evolution from pop-up hub to year-round fashion destination."),

    dict(district="Seongsu-dong", cat="Fashion", year=2026, hot="",
         name="Moncler Puppy Summer Exhibition",
         brand="Moncler",
         desc="Luxury Italian outerwear brand brings its playful 'Puppy' summer collection to Seongsu in an art-forward exhibition format with seasonal limited-edition pieces.",
         location="Seongsui-ro 16-gil 31, Seongsu",
         date="May 1 – May 3, 2026",
         admission="Free",
         goods="Limited summer pieces",
         tags=["Luxury", "Exhibition", "Fashion", "Moncler"],
         why="Moncler's gallery-style format elevates the brand beyond retail — visitors engage with the collection as they would a gallery show."),

    dict(district="Seongsu-dong", cat="IP · Character", year=2026, hot="🔥 HOT",
         name="NCT WISH Official Pop-up Store",
         brand="SM Entertainment",
         desc="Official pop-up for NCT WISH timed to their new release. Fan interaction zones, photo booths, and exclusive Seoul-edition merchandise not available elsewhere.",
         location="Seongsu-dong",
         date="Apr 27 – May 3, 2026",
         admission="Free",
         goods="Seoul-edition MD + photocards",
         tags=["K-Pop", "NCT", "Fan Event", "Seoul Exclusive"],
         why="SM Entertainment chose Seongsu over SM Town Coex — reflecting the commercial appeal of Seongsu's younger, style-conscious foot traffic."),

    dict(district="Seongsu-dong", cat="Fashion", year=2026, hot="",
         name="Misekiseoul × IVE Rei",
         brand="Misekiseoul (Tokyo–Seoul label)",
         desc="Tokyo-Seoul fashion label reunites with IVE's Rei for a month-long pop-up. Inspired by a 'girl's world' theme with daily looks, accessories, and collab story.",
         location="Seongsu-dong",
         date="May 1 – May 31, 2026",
         admission="Free",
         goods="Collab accessories & apparel",
         tags=["Tokyo–Seoul", "IVE", "Collab", "Month-long"],
         why="Misekiseoul × IVE Rei bridges Japanese aesthetics and Korean fandom culture — a growing cross-cultural creative axis in 2026."),

    dict(district="Seongsu-dong", cat="IP · Character", year=2026, hot="🏆 Global",
         name="BLACKPINK 'DEADLINE' Global Pop-up",
         brand="BLACKPINK × YG Entertainment",
         desc="World pop-up tour launching in Seoul first at Musinsa Seongsu and Musinsa Myeongdong. Exclusive Seoul-edition MD, new lightstick, character plush, keyrings and keycaps. Continued in 20 cities worldwide.",
         location="Musinsa Store Seongsu + Musinsa Standard Myeongdong",
         date="Feb 28 – Mar 8, 2026 · Daily 11:00–22:00",
         admission="Free",
         goods="Seoul-exclusive MD + lightstick",
         tags=["BLACKPINK", "K-Pop", "Global Tour", "Album", "Musinsa"],
         why="Seoul as the global first stop for BLACKPINK's world pop-up tour confirms the city's status as the world's most important pop-up market in 2026."),

    dict(district="Seongsu-dong", cat="Lifestyle", year=2026, hot="",
         name="Samsung Galaxy Market Event",
         brand="Samsung Electronics",
         desc="Samsung's experiential pop-up at T Factory Seongsu — latest Galaxy devices with hands-on trials, exclusive launch bundles, and immersive tech zones.",
         location="T Factory Seongsu, Yeonmujang 1-gil",
         date="Feb 27 – Mar 29, 2026",
         admission="Free",
         goods="Device trial + exclusive bundles",
         tags=["Tech", "Samsung", "Galaxy", "Experiential"],
         why="Tech brands using Seongsu's creative spaces signals the district's broad cultural credibility — it's no longer just fashion and beauty."),

    # ── SEONGSU 2025 ──────────────────────────────────────────────────────────
    dict(district="Seongsu-dong", cat="Fashion", year=2025, hot="",
         name="Hoka Seongsu Pop-up",
         brand="HOKA",
         desc="Running & trail shoe brand's Seongsu pop-up with fit experience stations, limited-color drops, and stamp-tour giveaways.",
         location="East Yeonmujang-gil, Seongsu",
         date="Jan 2025",
         admission="Free",
         goods="Limited colorway + stamp goods",
         tags=["Running", "Experiential", "Showroom", "Sneakers"],
         why="Hoka's shift from performance to lifestyle is embodied in the Seongsu location — it targets trend-aware consumers, not just runners."),

    dict(district="Seongsu-dong", cat="F&B", year=2025, hot="🔥 Viral",
         name='Adidas Café "3 STRIPES Seoul"',
         brand="Adidas × Café Concept",
         desc="Fashion meets coffee — a viral social media sensation before it even opened. Three-stripe signature drinks, limited merch, and immersive brand installations drew massive queues.",
         location="Seongsu-dong",
         date="Jan 2025 (~Jan 18)",
         admission="Free",
         goods="Limited drinks & merch",
         tags=["Collab", "Café", "Sports", "Viral", "SNS"],
         why="Pre-opening social buzz turned this into a must-visit — a case study in anticipation-building driving pop-up traffic without paid advertising."),

    dict(district="Seongsu-dong", cat="Beauty", year=2025, hot="✨ Benchmark",
         name="iSOi 'Bulgaria Rose Trip' Pop-up",
         brand="iSOi",
         desc="Opened to celebrate iSOi's Seongsu flagship. An immersive Bulgaria rose concept space praised as a benchmark for brand-owned pop-up strategy — no rental costs, maximum organic buzz.",
         location="iSOi Flagship Store, Seongsu",
         date="Jan 2025",
         admission="Free",
         goods="Product samples",
         tags=["Skincare", "Immersive", "Flagship", "Benchmark"],
         why="By owning the pop-up through their flagship, iSOi eliminated rental costs while generating enormous SNS buzz — the ideal model for mid-size beauty brands."),

    dict(district="Seongsu-dong", cat="IP · Character", year=2025, hot="",
         name="TBH × Hello Kitty Department Store",
         brand="tbh × Sanrio",
         desc="Hello Kitty 50th anniversary collab pop-up with co-designed limited apparel, accessories, and collectibles.",
         location="Seongsu-dong",
         date="Jan 2025",
         admission="Free",
         goods="Limited collab goods",
         tags=["Sanrio", "Hello Kitty", "Collab", "Fashion", "50th"],
         why="The Hello Kitty 50th anniversary proved the staying power of legacy IP — nostalgia-driven collabs outperform trend-driven ones in purchase intent."),

    # ── SEONGSU 2024 ──────────────────────────────────────────────────────────
    dict(district="Seongsu-dong", cat="Fashion", year=2024, hot="🏆 Large-scale",
         name="Musinsa Beauty Festa — Seongsu",
         brand="Musinsa",
         desc="Massive multi-brand pop-up town across Seongsu, bringing online-only beauty brands to their first ever offline experience spaces.",
         location="Seongsu-dong (area-wide)",
         date="2024",
         admission="Free",
         goods="Multi-brand beauty & fashion",
         tags=["Pop-up Town", "Multi-brand", "Large-scale", "Pioneering"],
         why="The Musinsa Seongsu Festa proved that an e-commerce platform could run a physical pop-up town as effectively as a department store."),

    # ── HANNAM 2026 ───────────────────────────────────────────────────────────
    dict(district="Hannam-dong", cat="Beauty", year=2026, hot="✨ Notable",
         name="Pesade Hannam Flagship Opening",
         brand="Pesade",
         desc="Niche fragrance brand Pesade opens its Hannam flagship with a launch pop-up featuring personal scent consultations and exclusive opening-day sets.",
         location="Hannam-dong Flagship Store",
         date="2026",
         admission="Free",
         goods="Personal scent consultation + sets",
         tags=["Niche Fragrance", "Flagship", "Opening", "Hannam"],
         why="Hannam's gallery culture makes it the natural home for niche fragrance brands seeking affluent, design-literate consumers."),

    dict(district="Hannam-dong", cat="Fashion", year=2025, hot="",
         name='Adidas × ABC Mart — "My Nth New Pair"',
         brand="ABC Mart × Adidas",
         desc="Season-launch pop-up combining ABC Mart's retail reach with Adidas' newest sneaker lineup. Limited silhouettes and on-site shoe personalisation service.",
         location="Hannam-dong",
         date="Jan 2025",
         admission="Free",
         goods="Limited sneaker lineup",
         tags=["Sneakers", "Collab", "Customise", "Personalise"],
         why="Personalisation services dramatically increase time-in-store and purchase likelihood — Adidas deploys this across high-traffic pop-ups."),

    dict(district="Hannam-dong", cat="Art · Exhibition", year=2025, hot="",
         name="Hannam Emerging Artist Gallery Pop-up",
         brand="Hannam Independent Gallery Network",
         desc="Rotating platform for emerging Korean artists with works for sale alongside brand-collab art objects. Buyers receive limited-edition art books.",
         location="Hannam Gallery District",
         date="Seasonal, ongoing",
         admission="Free viewing",
         goods="Original artworks + art books",
         tags=["Art", "Emerging Artist", "Sales", "Curation"],
         why="Hannam's gallery infrastructure allows emerging artists to access affluent collectors without a permanent gallery space."),

    dict(district="Hannam-dong", cat="Beauty", year=2025, hot="",
         name="European Niche Perfume — Korea Debut",
         brand="Hannam Concept Beauty Edit",
         desc="First Korean pop-up for a coveted European niche perfume house. Personal fragrance consultations and limited discovery sets curated by in-house parfumeurs.",
         location="Hannam Concept Store",
         date="Seasonal",
         admission="Free",
         goods="Discovery sets + consultation",
         tags=["Niche Perfume", "Consultation", "Debut", "European"],
         why="Hannam's international-facing, luxury-comfortable demographic makes it the ideal test market for European niche brands entering Korea."),

    dict(district="Hannam-dong", cat="Fashion", year=2024, hot="",
         name="Hannam Vintage Fashion Market",
         brand="Hannam Vintage Curators",
         desc="Monthly curated vintage & resale pop-up market reflecting MZ consumers' growing interest in sustainable fashion.",
         location="Hannam-dong",
         date="Monthly, ongoing",
         admission="Free",
         goods="Vintage & resale items",
         tags=["Vintage", "Resale", "Sustainable", "Monthly"],
         why="Sustainable fashion is the fastest-growing sub-trend in MZ consumption — Hannam's vintage market taps this with a premium, curated approach."),

    dict(district="Hannam-dong", cat="Lifestyle", year=2025, hot="",
         name="Luxury Interior & Home Design Pop-up",
         brand="Hannam Flagship Brands",
         desc="Premium interior and home brand pop-up offering product experience and consultation services for Hannam's affluent professional residents.",
         location="Hannam-dong",
         date="Seasonal",
         admission="Free",
         goods="Consultation + display items",
         tags=["Interior", "Premium", "Lifestyle", "Consultation"],
         why="Home lifestyle brands use pop-ups to bridge the gap between e-commerce imagery and real-world texture — Hannam consumers demand tactile experience."),

    # ── HONGDAE 2026 ──────────────────────────────────────────────────────────
    dict(district="Hongdae", cat="IP · Character", year=2026, hot="🔥 HOT",
         name="ITZY [Motto] Official Pop-up Store",
         brand="ITZY × JYP Entertainment",
         desc="Official pop-up tied to ITZY's Motto release. Fan merch, photocard events, and exclusive Hongdae-only album bundles.",
         location="Mapo-gu, Hongdae area",
         date="May 19 – May 25, 2026",
         admission="Free",
         goods="Exclusive album bundle + photocards",
         tags=["K-Pop", "ITZY", "Fan Event", "JYP", "Hongdae Only"],
         why="Hongdae remains the spiritual home of K-pop fan culture — its density of dedicated fans makes it the natural first choice for comeback pop-ups."),

    dict(district="Hongdae", cat="IP · Character", year=2025, hot="🔥 HOT",
         name="Chainsaw Man Official Pop-up",
         brand="AK Plaza Hongdae × MAPPA",
         desc="Large-scale official pop-up for the hit anime Chainsaw Man. Character goods, acrylic standees, apparel, and exclusive Korean-market collectibles. Long queues from opening day.",
         location="AK Plaza Hongdae Branch",
         date="Sep 26 – Dec 31, 2025",
         admission="Free",
         goods="Anime character goods",
         tags=["Anime", "IP", "Goods", "MAPPA", "Long-run"],
         why="A 3-month run in a department store is exceptional — it signals how anime IP has become a consistent, reliable driver of retail footfall."),

    dict(district="Hongdae", cat="Beauty", year=2025, hot="✨ Notable",
         name="Olive Young Hongdae Town — Beauty Event",
         brand="CJ Olive Young",
         desc="Multi-brand beauty event at Olive Young's flagship Hongdae location. Makeup trials, new product demos, and SNS verification giveaways.",
         location="Olive Young Hongdae Town",
         date="Oct 2 – Oct 12, 2025",
         admission="Free",
         goods="Sample giveaways",
         tags=["K-Beauty", "Multi-brand", "Trial", "SNS", "Flagship"],
         why="Olive Young Hongdae's tourist-heavy foot traffic makes it one of the most cost-efficient locations for beauty brands to reach international K-beauty shoppers."),

    dict(district="Hongdae", cat="IP · Character", year=2024, hot="",
         name="K-Pop Official MD Pop-up Hub",
         brand="Major Entertainment Labels",
         desc="Hongdae's proximity to SM Town and dense fan streets makes it a permanent K-pop pop-up corridor. Albums, photocards, lightsticks at every major comeback.",
         location="Hongdae, near SM Town",
         date="Comeback seasons, ongoing",
         admission="Free",
         goods="Random photocard events",
         tags=["K-Pop", "Fandom", "MD", "SM Town", "Ongoing"],
         why="Hongdae's structural role as K-pop's retail heartland is self-reinforcing: fans gather because brands pop up; brands pop up because fans gather."),

    dict(district="Hongdae", cat="Art · Exhibition", year=2024, hot="",
         name="Hongdae Indie Artist Market",
         brand="Hongdae Art Scene",
         desc="Independent artist market selling handmade works, goods, and crafts. Different themes each time — a defining feature of Hongdae's creative underground.",
         location="Hongdae Walk Street",
         date="2× monthly, ongoing",
         admission="Free",
         goods="Handmade works & goods",
         tags=["Handmade", "Indie", "Market", "Authentic", "Regular"],
         why="The indie artist market represents the grassroots origin of Seoul's pop-up culture — artists were using temporary spaces long before brands arrived."),

    # ── GANGNAM 2026 ──────────────────────────────────────────────────────────
    dict(district="Gangnam · The Hyundai", cat="IP · Character", year=2026, hot="🔥 HOT",
         name="Hello Kitty × Jisoo Pop-up",
         brand="Sanrio × Jisoo (BLACKPINK)",
         desc="Sanrio's Hello Kitty collabs with BLACKPINK's Jisoo for a Jamsil pop-up. Co-designed fashion pieces, limited character goods, and signature photo zones drawing both Sanrio and Blink fans.",
         location="Jamsil, Songpa-gu",
         date="May 1–5, 2026 (Golden Week)",
         admission="Free",
         goods="Co-designed limited goods",
         tags=["Sanrio", "BLACKPINK", "Jisoo", "Collab", "Golden Week"],
         why="Combining Hello Kitty with BLACKPINK's Jisoo targets two overlapping fandoms simultaneously — commercially precise, executed during peak visitor season."),

    dict(district="Gangnam · The Hyundai", cat="F&B", year=2026, hot="",
         name="봄날엔 (Bomnal-en) Spring Dessert Pop-up",
         brand="Bomnal-en Gangnam",
         desc="Spring-season dessert pop-up in Seocho/Gangnam. Seasonal pastries and limited menus for cherry blossom period with Instagram-ready floral setup.",
         location="Seocho-gu, Gangnam",
         date="May 19 – May 31, 2026",
         admission="Free",
         goods="Seasonal dessert menu",
         tags=["Dessert", "Spring", "Seasonal", "Instagram"],
         why="Seasonal F&B pop-ups timed to cherry blossom season consistently outperform in foot traffic — the backdrop drives organic social sharing."),

    dict(district="Gangnam · The Hyundai", cat="IP · Character", year=2026, hot="🌿 Outdoor",
         name="Pokémon Secret Forest (Seoul Forest)",
         brand="Pokémon Mega Festa 2026",
         desc="Outdoor Pokémon pop-up where hidden Pokémon lurk among the trees of Seoul Forest, tied to the 2026 Seoul International Garden Expo.",
         location="Seoul Forest, Seongdong-gu",
         date="May 1 – Jun 21, 2026 · Daily 10:00–20:00",
         admission="Free",
         goods="Outdoor original goods",
         tags=["Pokémon", "Outdoor", "Seoul Forest", "Garden Expo"],
         why="Taking a pop-up outdoors into Seoul Forest transforms the experience from retail into a nature walk with brand discovery built in."),

    dict(district="Gangnam · The Hyundai", cat="IP · Character", year=2024, hot="🏆 Record",
         name="K League × Sanrio Characters",
         brand="K League × Sanrio",
         desc="The most successful pop-up of 2024: 250,000 total visitors, averaging 10,500 per day. A textbook example of cross-fandom collision — sports fans + character fans = unstoppable traffic.",
         location="The Hyundai Seoul",
         date="2024",
         admission="Free",
         goods="Cross-fandom limited goods",
         tags=["Cross-fandom", "Record", "Sanrio", "K League", "Sports"],
         why="This proves the most powerful pop-ups bridge two previously unconnected communities, doubling the potential audience without increasing production complexity."),

    dict(district="Gangnam · The Hyundai", cat="Beauty", year=2024, hot="🏆 Large-scale",
         name="Coupang Mega Beauty Show",
         brand="Coupang × 9 Beauty Brands",
         desc="Nine major domestic and international beauty brands share one pop-up town. Visitors compare, trial, and purchase across all brands simultaneously.",
         location="Gangnam area large venue",
         date="2024",
         admission="Free",
         goods="Multi-brand trials & purchase",
         tags=["Pop-up Town", "Multi-brand", "Beauty", "Benchmark"],
         why="Coupang coordinating 9 brands simultaneously shows how e-commerce platforms are emerging as the new department store operators of the pop-up era."),

    dict(district="Gangnam · The Hyundai", cat="F&B", year=2024, hot="",
         name="Market Kurly Food Festa",
         brand="Market Kurly",
         desc="Fresh-food e-commerce platform Kurly brings its curated brands offline. Live tasting experiences, cooking demos, and instant purchase of premium food items.",
         location="Gangnam area",
         date="2024",
         admission="Free",
         goods="Premium food items + tasting",
         tags=["F&B", "E-commerce", "Tasting", "Premium"],
         why="Market Kurly's offline Festa addresses a core challenge for food e-commerce: consumers want to taste before buying — the pop-up bridges that trust gap."),

    dict(district="Gangnam · The Hyundai", cat="Art · Exhibition", year=2025, hot="",
         name="Seoul International Café Show",
         brand="COEX",
         desc="Korea's largest café & beverage industry expo. New F&B brand pop-ups, master barista demos, and specialty coffee equipment showcases under one roof.",
         location="COEX, Gangnam",
         date="Nov 2025",
         admission="Paid admission",
         goods="Coffee products + limited brews",
         tags=["Café", "Exhibition", "Industry", "Coffee", "COEX"],
         why="The Café Show functions as an annual cultural moment for Seoul's café-obsessed MZ generation — not just an industry expo."),

    dict(district="Gangnam · The Hyundai", cat="IP · Character", year=2024, hot="",
         name="World Webtoon Festival 2024",
         brand="Webtoon Platform Alliance",
         desc="Major Korean and international webtoon IPs gather for a festival pop-up. Author signings, character goods, and interactive story-world exhibitions.",
         location="Gangnam area large venue",
         date="2024",
         admission="Paid admission",
         goods="Author-signed goods",
         tags=["Webtoon", "IP", "Festival", "Author", "Signing"],
         why="Webtoon IP is uniquely powerful because of deep personal connections — fans follow characters for years, making purchase decisions highly emotional."),

    # ── OTHERS 2026 ───────────────────────────────────────────────────────────
    dict(district="Other Areas", cat="IP · Character", year=2026, hot="",
         name="Super Mario Pop-up @ Starfield Hanam",
         brand="Nintendo × Starfield Hanam",
         desc="Nintendo's Super Mario franchise lands at Starfield Hanam with interactive game-themed installations, character photo spots, and limited merchandise.",
         location="Starfield Hanam, Gyeonggi-do",
         date="May 2026 (Golden Week)",
         admission="Free",
         goods="Nintendo limited goods",
         tags=["Nintendo", "Mario", "Gaming", "Interactive", "Family"],
         why="Nintendo's strategic use of Golden Week maximises family traffic — Starfield's suburban location serves consumers who can't easily access central Seoul."),

    dict(district="Other Areas", cat="IP · Character", year=2026, hot="",
         name="TOURS Official Pop-up — Yongsan",
         brand="TOURS (K-Pop Group)",
         desc="K-Pop group TOURS brings their official pop-up to Yongsan iPark Mall during Golden Week 2026 with exclusive Yongsan-edition goods.",
         location="Yongsan iPark Mall",
         date="May 1–5, 2026 (Golden Week)",
         admission="Free",
         goods="Exclusive Yongsan-edition merch",
         tags=["K-Pop", "Fan Event", "Yongsan", "Golden Week"],
         why="Yongsan's proximity to major transit hubs makes it accessible to fans travelling from across the country."),

    dict(district="Other Areas", cat="Beauty", year=2026, hot="",
         name="BeautyPlus Moving × Mise-en-scène",
         brand="BeautyPlus Universe",
         desc="BeautyPlus's mobile pop-up at Sungshin Women's University in collaboration with hair care brand Mise-en-scène. Live demos and giveaways.",
         location="Seongbuk-gu (Sungshin Women's Univ.)",
         date="May 19, 2026",
         admission="Free",
         goods="Hair care giveaways",
         tags=["Hair Care", "Mobile Pop-up", "Campus", "University"],
         why="Campus-based beauty pop-ups target precisely the MZ demographic at point of brand discovery — students in their early 20s are the most valuable long-term beauty customers."),

    dict(district="Other Areas", cat="Art · Exhibition", year=2025, hot="",
         name="DDP Emerging Designer Pop-up Market",
         brand="Dongdaemun Design Plaza",
         desc="Emerging designer market at the iconic DDP building. Fashion, product design, and crafts curated by category — one of Seoul's most architecturally striking venues.",
         location="Dongdaemun Design Plaza (DDP)",
         date="1–2× monthly, ongoing",
         admission="Free",
         goods="Designer pieces & crafts",
         tags=["Emerging Designers", "DDP", "Market", "Architecture"],
         why="The DDP's Zaha Hadid landmark status gives any pop-up hosted there a cultural legitimacy that a standard commercial space cannot provide."),

    dict(district="Other Areas", cat="F&B", year=2025, hot="",
         name="Lotte Jamsil Seasonal Bakery Pop-up",
         brand="Lotte Department Store Jamsil",
         desc="Premium seasonal dessert pop-ups at Lotte Jamsil B1 bakery event hall. Season-limited pastry brands and holiday gift sets.",
         location="Lotte Dept. Store Jamsil, B1F",
         date="Seasonal",
         admission="Free",
         goods="Seasonal pastries + gift sets",
         tags=["Dessert", "Gift Set", "Seasonal", "Jamsil", "Bakery"],
         why="Department store bakery event halls are the most reliable pop-up format in Korea — low risk for both brand and retailer, high impulse purchase rate."),

    dict(district="Other Areas", cat="Fashion", year=2025, hot="",
         name="SYSTEM FW25 Pop-up — Lotte World Mall",
         brand="SYSTEM",
         desc="Korean contemporary fashion brand SYSTEM's FW25 collection launch pop-up. Pre-order sessions and exclusive early access to the new season.",
         location="Lotte World Mall, Jamsil",
         date="~ Nov 6, 2025",
         admission="Free",
         goods="FW25 early access + pre-order",
         tags=["Contemporary Fashion", "FW25", "Pre-order", "Korean Brand"],
         why="SYSTEM's use of Lotte World Mall expands its reach beyond Seongsu's fashion bubble to mainstream MZ consumers in traditional retail complexes."),
]

df = pd.DataFrame(POPUPS)

# ── COLOUR CONFIG ────────────────────────────────────────────────────────────
CAT_COLORS = {
    "Fashion":        "#e05c7a",
    "Beauty":         "#9b6fd4",
    "F&B":            "#d47a2a",
    "IP · Character": "#d4a017",
    "Art · Exhibition":"#3aaa6a",
    "Lifestyle":      "#2e86c1",
}
DIST_COLORS = {
    "Seongsu-dong":          "#e05c7a",
    "Hannam-dong":           "#2e86c1",
    "Hongdae":               "#9b6fd4",
    "Gangnam · The Hyundai": "#d4a017",
    "Other Areas":           "#d47a2a",
}
YEAR_COLORS = {2024: "#d4a017", 2025: "#d47a2a", 2026: "#e05c7a"}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 8px'>
      <div style='color:#d4b896;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:4px'>Research Project</div>
      <div style='font-family:"Playfair Display",serif;font-size:1.3rem;font-weight:700;color:white'>Jooeun Lim</div>
      <div style='font-size:0.78rem;color:rgba(255,255,255,0.4);margin-top:2px'>SKKU · Department of Dance</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.08);margin:16px 0'>
    """, unsafe_allow_html=True)

    st.markdown("<div style='color:#d4b896;font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;margin-bottom:10px'>Filters</div>", unsafe_allow_html=True)

    selected_cats = st.multiselect(
        "Category",
        options=sorted(df["cat"].unique()),
        default=sorted(df["cat"].unique()),
    )
    selected_years = st.multiselect(
        "Year",
        options=sorted(df["year"].unique()),
        default=sorted(df["year"].unique()),
    )
    selected_districts = st.multiselect(
        "District",
        options=sorted(df["district"].unique()),
        default=sorted(df["district"].unique()),
    )
    search_q = st.text_input("🔍 Search brand / name", "")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem;color:rgba(255,255,255,0.3);line-height:1.8'>
      Data sources:<br>
      Popga · Seongsu Gorilla<br>
      Inside Seoul · DealSeoul<br>
      Field Research 2024–2026
    </div>
    """, unsafe_allow_html=True)

# ── FILTER DATA ───────────────────────────────────────────────────────────────
mask = (
    df["cat"].isin(selected_cats) &
    df["year"].isin(selected_years) &
    df["district"].isin(selected_districts)
)
if search_q:
    sq = search_q.lower()
    mask = mask & (
        df["name"].str.lower().str.contains(sq) |
        df["brand"].str.lower().str.contains(sq)
    )
filtered = df[mask].reset_index(drop=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="sub">MZ Generation Research · SKKU Dance · Jooeun Lim</div>
  <h1>Seoul Pop-up Store<br><em>Trend Map 2024–2026</em></h1>
  <p>A field-research database mapping Seoul's pop-up culture across Seongsu, Hannam, Hongdae, Gangnam and beyond.
     Covers 2024 through spring <strong style="color:#d4b896">2026</strong> — filter by category, year, or district.</p>
  <div class="stat-row">
    <div class="stat-box">
      <div class="stat-num">{len(filtered)}</div>
      <div class="stat-label">Showing</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">{len(df)}</div>
      <div class="stat-label">Total Listed</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">5</div>
      <div class="stat-label">Districts</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">1,431</div>
      <div class="stat-label">2024 Nationwide</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋  Pop-up Directory", "📊  Data & Charts", "💡  Key Trends"])

# ════════════════════════════════════════════════════════════════════════
# TAB 1 — DIRECTORY
# ════════════════════════════════════════════════════════════════════════
with tab1:
    if filtered.empty:
        st.warning("No pop-ups match the current filters. Try adjusting the sidebar.")
    else:
        for district in ["Seongsu-dong", "Hannam-dong", "Hongdae", "Gangnam · The Hyundai", "Other Areas"]:
            dist_df = filtered[filtered["district"] == district]
            if dist_df.empty:
                continue

            color = DIST_COLORS.get(district, "#b8966e")
            st.markdown(f"""
            <div style='margin-top:36px;margin-bottom:20px'>
              <span class='dist-badge' style='color:{color};border-color:{color}'>{list(DIST_COLORS.keys()).index(district)+1:02d}</span>
              <span class='dist-title' style='color:{color}'>{district}</span>
              <span style='font-size:0.8rem;color:#9c8878;margin-left:12px;font-family:monospace'>{len(dist_df)} pop-up{"s" if len(dist_df)!=1 else ""}</span>
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(3)
            for i, (_, row) in enumerate(dist_df.iterrows()):
                cat_color = CAT_COLORS.get(row["cat"], "#b8966e")
                year_color = YEAR_COLORS.get(row["year"], "#9c8878")
                tags_html = "".join(f'<span class="ctag">{t}</span>' for t in row["tags"])

                with cols[i % 3]:
                    with st.expander(f"{'🔥 ' if row['hot'] else ''}{row['name']}", expanded=False):
                        st.markdown(f"""
                        <div style='margin-bottom:12px'>
                          <span class='badge' style='background:rgba(0,0,0,0.05);color:{cat_color};border:1px solid {cat_color}22'>{row["cat"]}</span>
                          <span class='year-badge badge' style='color:{year_color};border-color:{year_color}'>{row["year"]}</span>
                          {f'<span style="font-size:0.78rem;color:{cat_color}">{row["hot"]}</span>' if row["hot"] else ''}
                        </div>
                        <div style='font-size:0.82rem;color:#9c8878;font-family:monospace;margin-bottom:10px'>{row["brand"]}</div>
                        <div style='font-size:0.88rem;color:#5c4a3a;line-height:1.75;margin-bottom:14px'>{row["desc"]}</div>
                        <div style='background:#f8f5f0;border:1px solid #ede4d8;border-radius:6px;padding:14px 16px;margin-bottom:12px'>
                          <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px'>
                            <div><div style='font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;color:#9c8878;font-family:monospace;margin-bottom:3px'>📍 Location</div><div style='font-size:0.82rem;color:#1a1510'>{row["location"]}</div></div>
                            <div><div style='font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;color:#9c8878;font-family:monospace;margin-bottom:3px'>📅 Date</div><div style='font-size:0.82rem;color:#1a1510'>{row["date"]}</div></div>
                            <div><div style='font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;color:#9c8878;font-family:monospace;margin-bottom:3px'>🎟 Admission</div><div style='font-size:0.82rem;color:#1a1510'>{row["admission"]}</div></div>
                            <div><div style='font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;color:#9c8878;font-family:monospace;margin-bottom:3px'>🎁 Highlights</div><div style='font-size:0.82rem;color:#1a1510'>{row["goods"]}</div></div>
                          </div>
                        </div>
                        <div class="card-tags">{tags_html}</div>
                        <div class="research-note">📝 Research Note: {row["why"]}</div>
                        """, unsafe_allow_html=True)

            st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 2 — CHARTS
# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-label'>Category Distribution</div>", unsafe_allow_html=True)
        cat_counts = filtered["cat"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig1 = px.bar(
            cat_counts, x="Count", y="Category", orientation="h",
            color="Category",
            color_discrete_map=CAT_COLORS,
            template="plotly_white",
        )
        fig1.update_layout(
            showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="DM Sans", size=12, color="#1a1510"),
            xaxis_title="", yaxis_title="",
            margin=dict(l=0, r=20, t=10, b=10), height=280,
        )
        fig1.update_traces(marker_line_width=0)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("<div class='section-label'>Year Breakdown</div>", unsafe_allow_html=True)
        year_counts = filtered["year"].value_counts().sort_index().reset_index()
        year_counts.columns = ["Year", "Count"]
        year_counts["Year"] = year_counts["Year"].astype(str)
        fig2 = px.bar(
            year_counts, x="Year", y="Count",
            color="Year",
            color_discrete_map={"2024": "#d4a017", "2025": "#d47a2a", "2026": "#e05c7a"},
            template="plotly_white",
            text="Count",
        )
        fig2.update_layout(
            showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="DM Sans", size=12, color="#1a1510"),
            xaxis_title="", yaxis_title="",
            margin=dict(l=0, r=20, t=10, b=10), height=280,
        )
        fig2.update_traces(marker_line_width=0, textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='section-label'>District Concentration</div>", unsafe_allow_html=True)
        dist_counts = filtered["district"].value_counts().reset_index()
        dist_counts.columns = ["District", "Count"]
        fig3 = px.pie(
            dist_counts, names="District", values="Count",
            color="District",
            color_discrete_map=DIST_COLORS,
            hole=0.45,
            template="plotly_white",
        )
        fig3.update_layout(
            legend=dict(font=dict(size=11, family="DM Sans")),
            font=dict(family="DM Sans"),
            margin=dict(l=0, r=0, t=20, b=0), height=300,
            paper_bgcolor="white",
        )
        fig3.update_traces(textposition="inside", textfont_size=11)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("<div class='section-label'>Category × Year Heatmap</div>", unsafe_allow_html=True)
        pivot = df.groupby(["cat", "year"]).size().reset_index(name="count")
        pivot_wide = pivot.pivot(index="cat", columns="year", values="count").fillna(0)
        fig4 = go.Figure(data=go.Heatmap(
            z=pivot_wide.values,
            x=[str(y) for y in pivot_wide.columns],
            y=pivot_wide.index.tolist(),
            colorscale=[[0, "#f8f5f0"], [0.5, "#d4b896"], [1, "#b8966e"]],
            text=pivot_wide.values.astype(int),
            texttemplate="%{text}",
            showscale=False,
        ))
        fig4.update_layout(
            font=dict(family="DM Sans", size=12, color="#1a1510"),
            margin=dict(l=0, r=0, t=10, b=10), height=300,
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis_title="", yaxis_title="",
        )
        st.plotly_chart(fig4, use_container_width=True)

    # National comparison bar
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>2024 National Category Share (1,431 pop-ups nationwide)</div>", unsafe_allow_html=True)

    national = pd.DataFrame({
        "Category": ["IP · Character", "Fashion", "Beauty", "F&B", "Art · Exhibition", "Lifestyle", "Other"],
        "Share (%)": [21, 19, 11, 10, 8, 7, 24],
    })
    fig5 = px.bar(
        national, x="Category", y="Share (%)",
        color="Category",
        color_discrete_map={**CAT_COLORS, "Other": "#9c8878"},
        text="Share (%)",
        template="plotly_white",
    )
    fig5.update_layout(
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="DM Sans", size=12, color="#1a1510"),
        xaxis_title="", yaxis_title="Share (%)",
        margin=dict(l=0, r=0, t=10, b=10), height=320,
    )
    fig5.update_traces(marker_line_width=0, textposition="outside", texttemplate="%{text}%")
    st.plotly_chart(fig5, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 3 — TRENDS
# ════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='section-label'>Research Insight</div>
    <div class='section-title'>Key Trends 2024–2026</div>
    <p style='color:#9c8878;font-size:0.88rem;line-height:1.9;max-width:620px;margin-bottom:32px'>
      Field research by Jooeun Lim combined with data from Popga (1,431 pop-ups),
      Seongsu Gorilla, Inside Seoul, and DealSeoul platform analytics.
    </p>
    """, unsafe_allow_html=True)

    trends = [
        {"num": "21%", "color": "#d4a017", "title": "IP & Character Dominance",
         "desc": "In 2024, 21% of all pop-ups were IP/character-driven. K League × Sanrio drew 250,000 visitors. In 2026, Pokémon Mega Festa alone spans 3 simultaneous events across Seongsu."},
        {"num": "11%", "color": "#9b6fd4", "title": "Beauty Boom",
         "desc": "160 beauty & fragrance pop-ups in 2024 (11% of total). By 2026, luxury brands like YSL and La Roche-Posay run dedicated immersive pop-ups in Seongsu — not just product stalls."},
        {"num": "32%", "color": "#e05c7a", "title": "East Yeonmujang-gil Surge",
         "desc": "32% of all Seongsu pop-ups in H1 2025 concentrated on East Yeonmujang-gil. Brands demand larger raw spaces for deeper content design — the east side has become the creative frontier."},
        {"num": "52%", "color": "#2e86c1", "title": "Merch T-Shirt Rise",
         "desc": "Mentions of 'T-shirt' in pop-up communities rose 52% year-on-year. Graphic tees have become Gen Z identity markers — not just souvenirs, but statements of cultural participation."},
        {"num": "↑", "color": "#d47a2a", "title": "Pop-up Town Format Accelerating",
         "desc": "Multi-brand 'pop-up towns' (Musinsa Festa, Coupang Beauty Show) maximise cost-efficiency and footfall advantages. The format is accelerating sharply into 2026."},
        {"num": "NEW", "color": "#3aaa6a", "title": "Seoul Launches First",
         "desc": "In 2026, global tours (BLACKPINK DEADLINE, Pokémon 30th) now launch in Seoul before other world markets — confirming Seoul as the world's most important pop-up city."},
    ]

    t_cols = st.columns(3)
    for i, tr in enumerate(trends):
        with t_cols[i % 3]:
            st.markdown(f"""
            <div class="trend-card" style="margin-bottom:16px;border-top:3px solid {tr['color']}">
              <div class="trend-num" style="color:{tr['color']}">{tr['num']}</div>
              <div class="trend-title">{tr['title']}</div>
              <div class="trend-desc">{tr['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    # Research methodology note
    st.markdown("""
    <div style='background:#f8f5f0;border:1px solid #ede4d8;border-radius:8px;padding:28px 32px'>
      <div class='section-label'>Research Methodology</div>
      <div style='font-family:"Playfair Display",serif;font-size:1.2rem;font-weight:700;color:#1a1510;margin-bottom:12px'>About This Project</div>
      <p style='color:#5c4a3a;font-size:0.88rem;line-height:1.9;max-width:700px'>
        This pop-up store trend map is part of a broader research project examining how MZ generation consumers
        engage with experiential retail across Seoul. The dataset combines platform data from
        <strong>Popga</strong> (Korea's largest pop-up tracking platform, 1,431 entries in 2024),
        <strong>Seongsu Gorilla</strong>, <strong>Inside Seoul</strong>, and <strong>DealSeoul</strong>
        with personal field visits to Seongsu-dong and Hannam-dong. Each pop-up entry includes
        a research note analysing its strategic significance within the MZ consumption landscape.
      </p>
      <p style='color:#9c8878;font-size:0.82rem;margin-top:14px;font-family:monospace'>
        Jooeun Lim · SKKU Department of Dance · 2024–2026
      </p>
    </div>
    """, unsafe_allow_html=True)
