# ============================================================
# ⚽ كورة لايف برو — كلشي فملف واحد
# تشغيل: streamlit run app.py
# ============================================================

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# ============================================================
# 1. الإعدادات (config)
# ============================================================
APP_NAME = "⚽ كورة لايف برو"
APP_VERSION = "2.0.0"

API_BASE = "https://www.thesportsdb.com/api/v1/json/3"

LEAGUES = {
    "4328": {"name": "الدوري الإنجليزي الممتاز", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "country": "إنجلترا", "conf": "UEFA"},
    "4335": {"name": "الدوري الإسباني", "flag": "🇪🇸", "country": "إسبانيا", "conf": "UEFA"},
    "4332": {"name": "الدوري الإيطالي", "flag": "🇮🇹", "country": "إيطاليا", "conf": "UEFA"},
    "4331": {"name": "الدوري الألماني", "flag": "🇩🇪", "country": "ألمانيا", "conf": "UEFA"},
    "4334": {"name": "الدوري الفرنسي", "flag": "🇫🇷", "country": "فرنسا", "conf": "UEFA"},
    "4344": {"name": "الدوري البرتغالي", "flag": "🇵🇹", "country": "البرتغال", "conf": "UEFA"},
    "4337": {"name": "الدوري الهولندي", "flag": "🇳🇱", "country": "هولندا", "conf": "UEFA"},
    "4338": {"name": "الدوري البلجيكي", "flag": "🇧🇪", "country": "بلجيكا", "conf": "UEFA"},
    "4340": {"name": "الدوري التركي", "flag": "🇹🇷", "country": "تركيا", "conf": "UEFA"},
    "4345": {"name": "الدوري الروسي", "flag": "🇷🇺", "country": "روسيا", "conf": "UEFA"},
    "4346": {"name": "الدوري الأوكراني", "flag": "🇺🇦", "country": "أوكرانيا", "conf": "UEFA"},
    "4351": {"name": "الدوري البرازيلي", "flag": "🇧🇷", "country": "البرازيل", "conf": "CONMEBOL"},
    "4350": {"name": "الدوري الأرجنتيني", "flag": "🇦🇷", "country": "الأرجنتين", "conf": "CONMEBOL"},
    "4352": {"name": "الدوري المكسيكي", "flag": "🇲🇽", "country": "المكسيك", "conf": "CONCACAF"},
    "4358": {"name": "الدوري السعودي", "flag": "🇸🇦", "country": "السعودية", "conf": "AFC"},
    "4359": {"name": "الدوري الإماراتي", "flag": "🇦🇪", "country": "الإمارات", "conf": "AFC"},
    "4360": {"name": "الدوري المصري", "flag": "🇪🇬", "country": "مصر", "conf": "CAF"},
    "4361": {"name": "الدوري المغربي", "flag": "🇲🇦", "country": "المغرب", "conf": "CAF"},
    "4362": {"name": "الدوري التونسي", "flag": "🇹🇳", "country": "تونس", "conf": "CAF"},
    "4363": {"name": "الدوري الجزائري", "flag": "🇩🇿", "country": "الجزائر", "conf": "CAF"},
    "4480": {"name": "دوري أبطال أوروبا", "flag": "🏆", "country": "أوروبا", "conf": "UEFA"},
    "4481": {"name": "الدوري الأوروبي", "flag": "🥈", "country": "أوروبا", "conf": "UEFA"},
}

COLORS = {
    "bg": "#0f1720",
    "card": "#1a2332",
    "card_hover": "#223047",
    "primary": "#1a7f37",
    "success": "#4ade80",
    "danger": "#dc2626",
    "warning": "#f59e0b",
    "info": "#3b82f6",
    "purple": "#8b5cf6",
    "text": "#ffffff",
    "text_muted": "#94a3b8",
}

CACHE_LIVE = 30
CACHE_TODAY = 120
CACHE_STANDINGS = 300
CACHE_TOP_SCORERS = 3600

USER_POINTS = {"check_in": 5, "predict_correct": 10, "predict_wrong": -2}
USER_LEVELS = [
    {"name": "مبتدئ", "icon": "🥉", "min": 0, "max": 100},
    {"name": "مشجع", "icon": "🥈", "min": 100, "max": 500},
    {"name": "خبير", "icon": "🥇", "min": 500, "max": 2000},
    {"name": "محلل", "icon": "🏆", "min": 2000, "max": 10000},
    {"name": "أسطورة", "icon": "👑", "min": 10000, "max": 999999},
]
PREDICTION_TYPES = {
    "1x2": "نتيجة المباراة",
    "over_under": "أكثر/أقل من 2.5",
    "both_score": "الفريقان يسجلان",
    "exact": "النتيجة الدقيقة",
    "first_goal": "من يسجل أولاً",
}

# ============================================================
# 2. دوال مساعدة (helpers)
# ============================================================
def today_str():
    return datetime.now().strftime("%Y-%m-%d")

def format_date_ar(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        days = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
        months = ["يناير", "فبراير", "مارس", "أبريل", "ماي", "يونيو",
                  "يوليوز", "غشت", "شتنبر", "أكتوبر", "نونبر", "دجنبر"]
        return f"{days[d.weekday()]} {d.day} {months[d.month-1]} {d.year}"
    except:
        return date_str

def get_match_status(event):
    status = (event.get("strStatus") or "").lower()
    if status in ["ft", "match finished", "aet", "pen"]:
        return "finished"
    if status in ["1h", "2h", "ht", "et", "live", "p"]:
        return "live"
    return "upcoming"

def get_minute(event):
    progress = event.get("strProgress")
    if progress:
        return str(progress).replace("'", "").strip()
    return ""

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def get_team_logo(event, side):
    return event.get(f"str{side}TeamBadge", "") or ""

def get_team_name(event, side):
    return event.get(f"str{side}Team", "غير معروف") or "غير معروف"

def get_score(event, side):
    score = event.get(f"int{side}Score")
    return str(score) if score is not None else "0"

def group_by_league(events):
    groups = {}
    for e in events:
        league = e.get("strLeague") or "غير معروف"
        groups.setdefault(league, []).append(e)
    return groups

def init_session():
    defaults = {
        "favorites": [], "notifications": True, "auto_refresh": False,
        "user_points": 0, "predictions": [], "check_in_streak": 0,
        "last_check_in": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def add_points(amount, reason=""):
    st.session_state.user_points += amount
    if amount > 0:
        st.toast(f"🎉 +{amount} نقطة! {reason}", icon="⭐")

def get_user_level(points):
    for level in USER_LEVELS:
        if level["min"] <= points < level["max"]:
            return level
    return USER_LEVELS[-1]

def get_next_level_info(points):
    for i, level in enumerate(USER_LEVELS):
        if level["min"] <= points < level["max"]:
            if i + 1 < len(USER_LEVELS):
                nxt = USER_LEVELS[i + 1]
                prog = (points - level["min"]) / (level["max"] - level["min"])
                return nxt, prog
            return None, 1.0
    return None, 1.0

def daily_check_in():
    today = today_str()
    if st.session_state.last_check_in == today:
        st.warning("✅ سجلت حضورك اليوم بالفعل!")
        return False
    if st.session_state.last_check_in:
        last = datetime.strptime(st.session_state.last_check_in, "%Y-%m-%d")
        diff = (datetime.now() - last).days
        st.session_state.check_in_streak = st.session_state.check_in_streak + 1 if diff == 1 else 1
    else:
        st.session_state.check_in_streak = 1
    st.session_state.last_check_in = today
    bonus = USER_POINTS["check_in"] + (st.session_state.check_in_streak * 2)
    add_points(bonus, f"حضور يوم {st.session_state.check_in_streak}")
    return True

def make_prediction(match_id, match_name, prediction, confidence):
    pred = {
        "id": match_id, "match": match_name, "prediction": prediction,
        "confidence": confidence, "points_potential": int(confidence / 10),
        "created_at": datetime.now().isoformat(), "result": None,
    }
    st.session_state.predictions.append(pred)
    st.toast(f"🎯 تم تسجيل تنبؤك: {prediction}", icon="🔮")

# ============================================================
# 3. API (api)
# ============================================================
def _get(endpoint, params=None):
    try:
        url = f"{API_BASE}/{endpoint}"
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json() or {}
    except requests.exceptions.Timeout:
        st.warning("⏱️ انتهت مدة الاتصال")
        return {}
    except requests.exceptions.ConnectionError:
        st.error("🌐 تعذر الاتصال")
        return {}
    except Exception as e:
        st.error(f"❌ خطأ: {str(e)}")
        return {}

@st.cache_data(ttl=CACHE_LIVE, show_spinner=False)
def get_live_scores():
    return _get("livescore.php", {"s": "Soccer"}).get("events") or []

@st.cache_data(ttl=CACHE_TODAY, show_spinner=False)
def get_matches_by_date(date_str, league_id=None):
    events = _get("eventsday.php", {"d": date_str, "s": "Soccer"}).get("events") or []
    if league_id:
        events = [e for e in events if e.get("idLeague") == league_id]
    return events

@st.cache_data(ttl=CACHE_STANDINGS, show_spinner=False)
def get_standings(league_id, season="2024-2025"):
    return _get("lookuptable.php", {"l": league_id, "s": season}).get("table") or []

@st.cache_data(ttl=CACHE_TOP_SCORERS, show_spinner=False)
def get_top_scorers(league_id, season="2024-2025"):
    return _get("lookuptopscorers.php", {"l": league_id, "s": season}).get("topscorers") or []

# ============================================================
# 4. CSS (styles)
# ============================================================
def load_css():
    st.markdown(f"""
    <style>
        .stApp {{ background: linear-gradient(180deg, {COLORS['bg']} 0%, #0a1119 100%); color: {COLORS['text']}; }}
        #MainMenu, footer, header {{visibility: hidden;}}
        .block-container {{ padding-top: 1rem; }}
        .match-card {{
            background: {COLORS['card']}; border-radius: 14px; padding: 16px 20px;
            margin: 10px 0; border-right: 4px solid {COLORS['primary']};
            transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        .match-card:hover {{ background: {COLORS['card_hover']}; transform: translateX(-4px); }}
        .match-card.live {{ border-right-color: {COLORS['danger']}; animation: pulse-border 2s infinite; }}
        @keyframes pulse-border {{
            0%, 100% {{ box-shadow: 0 2px 8px rgba(220,38,38,0.2); }}
            50% {{ box-shadow: 0 2px 20px rgba(220,38,38,0.6); }}
        }}
        .team-name {{ color: {COLORS['text']}; font-size: 15px; font-weight: 600; }}
        .score-box {{
            background: #0a1119; color: {COLORS['success']}; padding: 8px 20px;
            border-radius: 10px; font-size: 20px; font-weight: bold; text-align: center;
        }}
        .score-box.live {{ background: {COLORS['danger']}; color: white; animation: pulse-bg 1.5s infinite; }}
        @keyframes pulse-bg {{ 50% {{ opacity: 0.7; }} }}
        .league-header {{
            color: {COLORS['success']}; font-size: 17px; font-weight: bold;
            padding: 18px 0 8px 0; border-bottom: 2px solid {COLORS['card']};
        }}
        .page-title {{
            font-size: 32px; font-weight: 800; text-align: center;
            background: linear-gradient(90deg, {COLORS['success']}, {COLORS['primary']});
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .badge {{
            display: inline-block; padding: 3px 10px; border-radius: 12px;
            font-size: 11px; font-weight: bold; margin: 2px;
        }}
        .badge-live {{ background: {COLORS['danger']}; color: white; animation: blink 1.5s infinite; }}
        .badge-finished {{ background: {COLORS['text_muted']}; color: {COLORS['bg']}; }}
        .badge-upcoming {{ background: {COLORS['info']}; color: white; }}
        .badge-purple {{ background: {COLORS['purple']}; color: white; }}
        @keyframes blink {{ 50% {{ opacity: 0.5; }} }}
        .info-card {{
            background: {COLORS['card']}; border-radius: 12px; padding: 15px;
            margin: 8px 0; border: 1px solid #2a3a52;
        }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: {COLORS['success']}; }}
        .stat-label {{ font-size: 12px; color: {COLORS['text_muted']}; }}
        .prediction-card {{
            background: linear-gradient(135deg, {COLORS['card']}, #1e2d42);
            border-radius: 12px; padding: 15px; margin: 10px 0;
            border: 2px solid {COLORS['purple']};
        }}
        .user-level {{
            display: flex; align-items: center; gap: 10px;
            background: {COLORS['card']}; border-radius: 12px; padding: 12px;
        }}
        section[data-testid="stSidebar"] {{ background: {COLORS['card']}; }}
    </style>
    """, unsafe_allow_html=True)

def match_card(home, away, home_score, away_score, status, minute="", time_str="",
               home_logo="", away_logo="", extra_class=""):
    if status == "live":
        css, score_cls = "live", "live"
        status_html = f'<span class="badge badge-live">🔴 {minute}′</span>'
    elif status == "finished":
        css, score_cls = "finished", ""
        status_html = f'<span class="badge badge-finished">✅ انتهت</span>'
    else:
        css, score_cls = "", ""
        status_html = f'<span class="badge badge-upcoming">🕐 {time_str}</span>'
        home_score = "-"
        away_score = "-"
    hl = f'<img src="{home_logo}" width="28" height="28" style="border-radius:50%;">' if home_logo else ""
    al = f'<img src="{away_logo}" width="28" height="28" style="border-radius:50%;">' if away_logo else ""
    return f"""
    <div class="match-card {css} {extra_class}">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:15px;">
            <div style="flex:1; display:flex; align-items:center; gap:10px;">{hl}<div class="team-name">{home}</div></div>
            <div style="text-align:center;">
                <div class="score-box {score_cls}">{home_score} - {away_score}</div>
                {status_html}
            </div>
            <div style="flex:1; display:flex; align-items:center; justify-content:flex-end; gap:10px;">
                <div class="team-name">{away}</div>{al}</div>
        </div>
    </div>
    """

def league_title(name, flag=""):
    return f'<div class="league-header">{flag} {name}</div>'

def page_title(text):
    return f'<div class="page-title">{text}</div>'

def info_card(label, value, icon="📊", color=None):
    c = color or COLORS["success"]
    return f"""
    <div class="info-card" style="text-align:center;">
        <div style="font-size:28px;">{icon}</div>
        <div class="stat-value" style="color:{c};">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """

# ============================================================
# 5. الصفحات (pages)
# ============================================================
def page_home():
    st.markdown(page_title("⚽ كورة لايف برو"), unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#94a3b8;'>{format_date_ar(today_str())}</p>", unsafe_allow_html=True)
    st.markdown("---")

    live_events = get_live_scores()
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(info_card("مباريات مباشرة", len(live_events), "🔴", COLORS["danger"]), unsafe_allow_html=True)
    with c2: st.markdown(info_card("الدوريات", len(LEAGUES), "🏆", COLORS["warning"]), unsafe_allow_html=True)
    with c3: st.markdown(info_card("نقاطك", st.session_state.user_points, "⭐", COLORS["success"]), unsafe_allow_html=True)
    with c4:
        nxt, prog = get_next_level_info(st.session_state.user_points)
        if nxt:
            st.markdown(info_card(f"للمستوى {nxt['name']}", f"{int(prog*100)}%", nxt['icon'], COLORS["purple"]), unsafe_allow_html=True)
        else:
            st.markdown(info_card("المستوى", "أقصى", "👑", COLORS["warning"]), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">🔴 مباشر الآن</div>', unsafe_allow_html=True)

    if not live_events:
        st.info("😴 ما كاينش مباريات مباشرة دابا.")
    else:
        grouped = group_by_league(live_events)
        for league, events in list(grouped.items())[:5]:
            st.markdown(league_title(league, "🏆"), unsafe_allow_html=True)
            for e in events[:4]:
                st.markdown(match_card(
                    home=get_team_name(e, "Home"), away=get_team_name(e, "Away"),
                    home_score=get_score(e, "Home"), away_score=get_score(e, "Away"),
                    status="live", minute=get_minute(e),
                    home_logo=get_team_logo(e, "Home"), away_logo=get_team_logo(e, "Away"),
                ), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">📅 مباريات اليوم</div>', unsafe_allow_html=True)

    today_events = get_matches_by_date(today_str())
    if not today_events:
        st.info("ما كاينش مباريات اليوم.")
    else:
        grouped = group_by_league(today_events)
        for league, events in list(grouped.items())[:5]:
            st.markdown(league_title(league, "⚽"), unsafe_allow_html=True)
            for e in events[:3]:
                status = get_match_status(e)
                st.markdown(match_card(
                    home=get_team_name(e, "Home"), away=get_team_name(e, "Away"),
                    home_score=get_score(e, "Home"), away_score=get_score(e, "Away"),
                    status=status, minute=get_minute(e), time_str=e.get("strTime", "")[:5],
                    home_logo=get_team_logo(e, "Home"), away_logo=get_team_logo(e, "Away"),
                ), unsafe_allow_html=True)


def page_live():
    st.markdown(page_title("🔴 مباشر الآن"), unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2: auto = st.toggle("🔄 تحديث تلقائي", value=False)
    with col3:
        if st.button("🔃 تحديث"):
            st.cache_data.clear(); st.rerun()
    st.markdown("---")

    events = get_live_scores()
    if not events:
        st.info("😴 ما كاينش مباريات مباشرة دابا.")
        return

    grouped = group_by_league(events)
    leagues = ["الكل"] + list(grouped.keys())
    selected = st.selectbox("🏆 اختر الدوري", leagues)
    if selected != "الكل":
        grouped = {selected: grouped[selected]}

    st.markdown(f"**عدد المباريات المباشرة:** {len(events)}")
    st.markdown("---")

    for league, evs in grouped.items():
        st.markdown(league_title(league, "🔴"), unsafe_allow_html=True)
        for e in evs:
            st.markdown(match_card(
                home=get_team_name(e, "Home"), away=get_team_name(e, "Away"),
                home_score=get_score(e, "Home"), away_score=get_score(e, "Away"),
                status="live", minute=get_minute(e),
                home_logo=get_team_logo(e, "Home"), away_logo=get_team_logo(e, "Away"),
            ), unsafe_allow_html=True)

    if auto:
        time.sleep(15); st.cache_data.clear(); st.rerun()


def page_matches():
    st.markdown(page_title("📅 المباريات"), unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ أمس"):
            st.session_state.selected_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    with col3:
        if st.button("غدا ➡️"):
            st.session_state.selected_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    if "selected_date" not in st.session_state:
        st.session_state.selected_date = today_str()

    with col2:
        sel = st.date_input("اختر التاريخ", value=datetime.strptime(st.session_state.selected_date, "%Y-%m-%d"))
        st.session_state.selected_date = sel.strftime("%Y-%m-%d")

    st.markdown(f"### 📆 {format_date_ar(st.session_state.selected_date)}")
    st.markdown("---")

    league_opts = {"الكل": None}
    for lid, info in LEAGUES.items():
        league_opts[info["name"]] = lid
    sel_name = st.selectbox("🏆 الدوري", list(league_opts.keys()))
    events = get_matches_by_date(st.session_state.selected_date, league_opts[sel_name])

    if not events:
        st.warning("لا توجد مباريات في هذا التاريخ.")
        return

    st.markdown(f"**عدد المباريات:** {len(events)}")
    st.markdown("---")

    grouped = group_by_league(events)
    for league, evs in grouped.items():
        st.markdown(league_title(league, "⚽"), unsafe_allow_html=True)
        for e in evs:
            status = get_match_status(e)
            st.markdown(match_card(
                home=get_team_name(e, "Home"), away=get_team_name(e, "Away"),
                home_score=get_score(e, "Home"), away_score=get_score(e, "Away"),
                status=status, minute=get_minute(e), time_str=e.get("strTime", "")[:5],
                home_logo=get_team_logo(e, "Home"), away_logo=get_team_logo(e, "Away"),
            ), unsafe_allow_html=True)


def page_standings():
    st.markdown(page_title("🏆 ترتيب الدوريات"), unsafe_allow_html=True)
    st.markdown("---")

    league_names = {v["name"]: k for k, v in LEAGUES.items()}
    sel_name = st.selectbox("🏆 اختر الدوري", list(league_names.keys()))
    league_id = league_names[sel_name]

    with st.spinner("⏳ جاري تحميل الترتيب..."):
        table = get_standings(league_id) or get_standings(league_id, "2023-2024")

    if not table:
        st.warning("⚠️ لا يوجد ترتيب متاح لهذا الدوري.")
        return

    rows = [{
        "المركز": t.get("intRank", "-"), "الفريق": t.get("strTeam", "-"),
        "لعب": safe_int(t.get("intPlayed")), "فاز": safe_int(t.get("intWin")),
        "تعادل": safe_int(t.get("intDraw")), "خسر": safe_int(t.get("intLoss")),
        "له": safe_int(t.get("intGoalsFor")), "عليه": safe_int(t.get("intGoalsAgainst")),
        "الفارق": safe_int(t.get("intGoalDifference")), "النقاط": safe_int(t.get("intPoints")),
    } for t in table]

    df = pd.DataFrame(rows)

    c1, c2, c3 = st.columns(3)
    if not df.empty:
        with c1:
            lead = df.iloc[0]
            st.metric("🥇 المتصدر", lead["الفريق"], f"{lead['النقاط']} نقطة")
        with c2:
            ba = df.loc[df["له"].idxmax()]
            st.metric("⚽ أفضل هجوم", ba["الفريق"], f"{ba['له']} هدف")
        with c3:
            bd = df.loc[df["عليه"].idxmin()]
            st.metric("🛡️ أفضل دفاع", bd["الفريق"], f"{bd['عليه']} هدف")

    st.markdown("---")
    st.dataframe(df, use_container_width=True, hide_index=True)


def page_stats():
    st.markdown(page_title("📊 الإحصائيات"), unsafe_allow_html=True)
    st.markdown("---")

    league_names = {v["name"]: k for k, v in LEAGUES.items()}
    sel_name = st.selectbox("🏆 اختر الدوري", list(league_names.keys()))
    league_id = league_names[sel_name]

    with st.spinner("⏳ جاري التحميل..."):
        table = get_standings(league_id)

    if not table:
        st.warning("⚠️ لا توجد بيانات.")
        return

    df = pd.DataFrame([{
        "الفريق": t.get("strTeam", "-"),
        "لعب": safe_int(t.get("intPlayed")), "فاز": safe_int(t.get("intWin")),
        "تعادل": safe_int(t.get("intDraw")), "خسر": safe_int(t.get("intLoss")),
        "له": safe_int(t.get("intGoalsFor")), "عليه": safe_int(t.get("intGoalsAgainst")),
        "النقاط": safe_int(t.get("intPoints")),
    } for t in table])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🥇 أعلى 10 فرق بالنقاط")
        top = df.nlargest(10, "النقاط")
        fig = px.bar(top, x="النقاط", y="الفريق", orientation="h",
                     color="النقاط", color_continuous_scale="greens", template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["card"], paper_bgcolor=COLORS["card"],
                          font_color="white", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("### ⚽ أعلى 10 فرق تهديفاً")
        top = df.nlargest(10, "له")
        fig = px.bar(top, x="له", y="الفريق", orientation="h",
                     color="له", color_continuous_scale="reds", template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["card"], paper_bgcolor=COLORS["card"],
                          font_color="white", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)


def page_favorites():
    st.markdown(page_title("⭐ الفرق المفضلة"), unsafe_allow_html=True)
    st.markdown("---")

    ALL_TEAMS = [
        "Real Madrid", "Barcelona", "Manchester City", "Liverpool",
        "Arsenal", "Chelsea", "Manchester United", "Tottenham",
        "Bayern Munich", "Borussia Dortmund", "PSG", "Juventus",
        "Inter Milan", "AC Milan", "Napoli", "Atletico Madrid",
        "Raja Casablanca", "Wydad Casablanca", "AS FAR", "MAS Fes",
    ]
    favs = st.multiselect("🔍 اختر الفرق:", ALL_TEAMS, default=st.session_state.favorites)
    st.session_state.favorites = favs

    if not favs:
        st.info("ℹ️ اختر على الأقل فريق واحد.")
        return

    st.success(f"✅ كتتبع **{len(favs)}** فريق")
    st.markdown("---")

    events = get_matches_by_date(today_str())
    fav_events = [e for e in events if get_team_name(e, "Home") in favs or get_team_name(e, "Away") in favs]

    if not fav_events:
        st.info("لا توجد مباريات لفرقك المفضلة اليوم.")
    else:
        grouped = group_by_league(fav_events)
        for league, evs in grouped.items():
            st.markdown(league_title(league, "⚽"), unsafe_allow_html=True)
            for e in evs:
                status = get_match_status(e)
                home = get_team_name(e, "Home")
                away = get_team_name(e, "Away")
                hs = "⭐ " if home in favs else ""
                aws = "⭐ " if away in favs else ""
                st.markdown(match_card(
                    home=f"{hs}{home}", away=f"{aws}{away}",
                    home_score=get_score(e, "Home"), away_score=get_score(e, "Away"),
                    status=status, minute=get_minute(e), time_str=e.get("strTime", "")[:5],
                    home_logo=get_team_logo(e, "Home"), away_logo=get_team_logo(e, "Away"),
                ), unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ مسح جميع المفضلة"):
        st.session_state.favorites = []
        st.rerun()


def page_predictions():
    st.markdown(page_title("🔮 التنبؤات"), unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    ### 🎯 توقع نتائج المباريات واربح نقاط!
    - **+10 نقاط** لكل تنبؤ صحيح
    - **-2 نقاط** لكل تنبؤ خاطئ
    """)
    st.markdown("---")

    events = get_matches_by_date(today_str())
    upcoming = [e for e in events if get_match_status(e) == "upcoming"]

    if not upcoming:
        st.info("لا توجد مباريات قادمة للتنبؤ بها.")
        return

    match_opts = {f"{get_team_name(e, 'Home')} vs {get_team_name(e, 'Away')}": e for e in upcoming}
    sel_name = st.selectbox("🏟️ اختر مباراة", list(match_opts.keys()))
    sel = match_opts[sel_name]

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🎯 نوع التنبؤ")
        pred_type = st.radio("اختر", list(PREDICTION_TYPES.values()), label_visibility="collapsed")
        pred_key = [k for k, v in PREDICTION_TYPES.items() if v == pred_type][0]
    with c2:
        st.markdown("#### 📊 نسبة الثقة")
        conf = st.slider("", 50, 100, 75, label_visibility="collapsed")

    st.markdown("---")
    home = get_team_name(sel, "Home")
    away = get_team_name(sel, "Away")

    if pred_key == "1x2":
        pred = st.radio("النتيجة", [f"فوز {home}", "تعادل", f"فوز {away}"])
    elif pred_key == "over_under":
        pred = st.radio("", ["أكثر من 2.5 هدف", "أقل من 2.5 هدف"])
    elif pred_key == "both_score":
        pred = st.radio("", ["نعم، الفريقان يسجلان", "لا، فريق واحد يسجل"])
    elif pred_key == "exact":
        c1, c2 = st.columns(2)
        with c1: hs = st.number_input(f"أهداف {home}", 0, 10, 1)
        with c2: aws = st.number_input(f"أهداف {away}", 0, 10, 1)
        pred = f"{hs} - {aws}"
    else:
        pred = st.radio("من يسجل أولاً؟", [home, away, "لا أهداف"])

    st.markdown("---")
    pts = int(conf / 10)
    st.markdown(f"""
    <div class="prediction-card">
        <div style="text-align:center;">
            <div style="font-size:14px; color:{COLORS['text_muted']};">النقاط المحتملة</div>
            <div style="font-size:36px; font-weight:bold; color:{COLORS['success']};">+{pts}</div>
            <div style="font-size:12px; color:{COLORS['text_muted']};">{pred_type} • ثقة {conf}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎯 سجل التنبؤ", use_container_width=True, type="primary"):
        make_prediction(sel.get("idEvent", ""), sel_name, pred, conf)
        st.success(f"✅ تم تسجيل تنبؤك: **{pred}**")

    st.markdown("---")
    st.markdown("### 📋 تنبؤاتي")
    preds = st.session_state.predictions
    if not preds:
        st.info("ما عندكش تنبؤات حتى دابا.")
    else:
        for p in reversed(preds[-10:]):
            st.markdown(f"""
            <div class="prediction-card" style="border-color:{COLORS['info']};">
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <div style="font-weight:bold;">{p['match']}</div>
                        <div style="font-size:12px; color:{COLORS['text_muted']};">{p['prediction']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="badge badge-purple">ثقة {p['confidence']}%</div>
                        <div style="font-size:11px; color:{COLORS['success']};">+{p['points_potential']} نقطة</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def page_scorers():
    st.markdown(page_title("📈 أفضل الهدافين"), unsafe_allow_html=True)
    st.markdown("---")

    league_names = {v["name"]: k for k, v in LEAGUES.items()}
    sel_name = st.selectbox("🏆 اختر الدوري", list(league_names.keys()))
    league_id = league_names[sel_name]

    with st.spinner("⏳ جاري التحميل..."):
        scorers = get_top_scorers(league_id)

    if not scorers:
        st.warning("⚠️ لا توجد بيانات هدافين لهذا الدوري.")
        return

    rows = [{
        "اللاعب": s.get("strPlayer", "-"), "الفريق": s.get("strTeam", "-"),
        "المركز": s.get("strPosition", "-"),
        "أهداف": safe_int(s.get("intGoals")),
        "صناعة": safe_int(s.get("intAssists")),
        "المباريات": safe_int(s.get("intAppearances")),
    } for s in scorers]

    df = pd.DataFrame(rows)
    c1, c2, c3 = st.columns(3)
    if not df.empty:
        with c1:
            top = df.iloc[0]
            st.metric("🥇 الهداف", top["اللاعب"], f"{top['أهداف']} هدف")
        with c2:
            ba = df.loc[df["صناعة"].idxmax()]
            st.metric("🎯 أفضل صانع", ba["اللاعب"], f"{ba['صناعة']} تمريرة")
        with c3:
            st.metric("📊 عدد اللاعبين", len(df))

    st.markdown("---")
    st.dataframe(df, use_container_width=True, hide_index=True)


def page_compare():
    st.markdown(page_title("⚖️ مقارنة الفرق"), unsafe_allow_html=True)
    st.markdown("---")

    league_names = {v["name"]: k for k, v in LEAGUES.items()}
    sel_name = st.selectbox("🏆 اختر الدوري", list(league_names.keys()))
    league_id = league_names[sel_name]
    table = get_standings(league_id)

    if not table:
        st.warning("لا توجد بيانات.")
        return

    teams = [t.get("strTeam") for t in table if t.get("strTeam")]
    c1, c2 = st.columns(2)
    with c1: t1 = st.selectbox("الفريق الأول", teams, index=0)
    with c2: t2 = st.selectbox("الفريق الثاني", teams, index=1 if len(teams) > 1 else 0)

    if t1 == t2:
        st.warning("⚠️ اختر فريقين مختلفين.")
        return

    d1 = next((t for t in table if t.get("strTeam") == t1), {})
    d2 = next((t for t in table if t.get("strTeam") == t2), {})

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="info-card" style="text-align:center; border:2px solid {COLORS['success']};">
            <div style="font-size:24px; font-weight:bold;">{t1}</div>
            <div style="font-size:36px; font-weight:bold; color:{COLORS['success']};">{safe_int(d1.get('intPoints'))}</div>
            <div style="color:{COLORS['text_muted']};">نقطة</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="info-card" style="text-align:center; border:2px solid {COLORS['danger']};">
            <div style="font-size:24px; font-weight:bold;">{t2}</div>
            <div style="font-size:36px; font-weight:bold; color:{COLORS['danger']};">{safe_int(d2.get('intPoints'))}</div>
            <div style="color:{COLORS['text_muted']};">نقطة</div>
        </div>
        """, unsafe_allow_html=True)

    cats = ["فاز", "تعادل", "خسر", "له", "عليه"]
    v1 = [safe_int(d1.get("intWin")), safe_int(d1.get("intDraw")), safe_int(d1.get("intLoss")),
          safe_int(d1.get("intGoalsFor")), safe_int(d1.get("intGoalsAgainst"))]
    v2 = [safe_int(d2.get("intWin")), safe_int(d2.get("intDraw")), safe_int(d2.get("intLoss")),
          safe_int(d2.get("intGoalsFor")), safe_int(d2.get("intGoalsAgainst"))]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=v1, theta=cats, fill='toself', name=t1, line_color=COLORS["success"]))
    fig.add_trace(go.Scatterpolar(r=v2, theta=cats, fill='toself', name=t2, line_color=COLORS["danger"]))
    fig.update_layout(polar=dict(bgcolor=COLORS["card"], radialaxis=dict(visible=True, color="white"),
                                  angularaxis=dict(color="white")),
                      template="plotly_dark", paper_bgcolor=COLORS["bg"], font_color="white", height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 مقارنة تفصيلية")
    cmp_df = pd.DataFrame({
        "المعيار": ["النقاط", "لعب", "فاز", "تعادل", "خسر", "له", "عليه", "الفارق"],
        t1: [safe_int(d1.get("intPoints")), safe_int(d1.get("intPlayed")), safe_int(d1.get("intWin")),
             safe_int(d1.get("intDraw")), safe_int(d1.get("intLoss")), safe_int(d1.get("intGoalsFor")),
             safe_int(d1.get("intGoalsAgainst")), safe_int(d1.get("intGoalDifference"))],
        t2: [safe_int(d2.get("intPoints")), safe_int(d2.get("intPlayed")), safe_int(d2.get("intWin")),
             safe_int(d2.get("intDraw")), safe_int(d2.get("intLoss")), safe_int(d2.get("intGoalsFor")),
             safe_int(d2.get("intGoalsAgainst")), safe_int(d2.get("intGoalDifference"))],
    })
    st.dataframe(cmp_df, use_container_width=True, hide_index=True)


def page_achievements():
    st.markdown(page_title("🏅 الإنجازات"), unsafe_allow_html=True)
    st.markdown("---")

    pts = st.session_state.user_points
    level = get_user_level(pts)
    nxt, prog = get_next_level_info(pts)

    st.markdown(f"""
    <div class="user-level" style="padding:25px; justify-content:center; flex-direction:column; text-align:center;">
        <div style="font-size:72px;">{level['icon']}</div>
        <div style="font-size:28px; font-weight:bold; margin:10px 0;">{level['name']}</div>
        <div style="font-size:18px; color:{COLORS['success']};">{pts} نقطة</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if nxt:
        st.markdown(f"### 📈 التقدم للمستوى {nxt['icon']} {nxt['name']}")
        st.progress(prog)
        st.caption(f"باقي {nxt['min'] - pts} نقطة")
    else:
        st.success("🎉 وصلت لأعلى مستوى!")

    st.markdown("---")
    st.markdown("### 🏆 جميع المستويات")
    for lvl in USER_LEVELS:
        achieved = pts >= lvl["min"]
        css = f"border:2px solid {COLORS['success']};" if achieved else "opacity:0.5;"
        badge = "✅" if achieved else "🔒"
        st.markdown(f"""
        <div class="info-card" style="{css}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:15px;">
                    <div style="font-size:36px;">{lvl['icon']}</div>
                    <div>
                        <div style="font-weight:bold; font-size:16px;">{lvl['name']}</div>
                        <div style="font-size:12px; color:{COLORS['text_muted']};">{lvl['min']} - {lvl['max']} نقطة</div>
                    </div>
                </div>
                <div style="font-size:24px;">{badge}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 إحصائياتك")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("⭐ النقاط", pts)
    with c2: st.metric("🔮 التنبؤات", len(st.session_state.predictions))
    with c3: st.metric("📅 سلسلة الحضور", st.session_state.check_in_streak)
    with c4: st.metric("⭐ المفضلة", len(st.session_state.favorites))

    st.markdown("---")
    if st.button("📅 تسجيل الحضور اليومي", use_container_width=True, type="primary"):
        daily_check_in()
        st.rerun()


def page_settings():
    st.markdown(page_title("⚙️ الإعدادات"), unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🔔 الإشعارات")
    st.toggle("تفعيل الإشعارات", value=st.session_state.notifications, key="notif_toggle")

    st.markdown("### 🎨 المظهر")
    st.selectbox("الثيم", ["داكن", "فاتح", "تلقائي"])
    st.selectbox("اللغة", ["العربية", "English", "Français"])

    st.markdown("### 🔄 التحديث")
    st.slider("مدة التحديث التلقائي (ثانية)", 5, 120, 30)

    st.markdown("### 💾 البيانات")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🗑️ مسح الكاش"):
            st.cache_data.clear(); st.success("✅ تم")
    with c2:
        if st.button("🔄 إعادة تحميل"):
            st.rerun()
    with c3:
        if st.button("❌ مسح المفضلة"):
            st.session_state.favorites = []; st.success("✅ تم")

    st.markdown("---")
    st.markdown("### ℹ️ حول")
    st.markdown(f"""
    - **الاسم:** كورة لايف برو
    - **الإصدار:** {APP_VERSION}
    - **الدوريات:** {len(LEAGUES)}+
    - **الميزات:** تنبؤات، إنجازات، مقارنة، هدافين
    """)
    st.caption("© 2024 كورة لايف برو")


# ============================================================
# 6. التطبيق الرئيسي (main)
# ============================================================
st.set_page_config(page_title="كورة لايف برو", page_icon="⚽", layout="wide")
load_css()
init_session()

with st.sidebar:
    st.markdown(f"# {APP_NAME}")
    lvl = get_user_level(st.session_state.user_points)
    st.markdown(f"""
    <div class="user-level">
        <div style="font-size:32px;">{lvl['icon']}</div>
        <div>
            <div style="font-weight:bold;">{lvl['name']}</div>
            <div style="font-size:12px; color:{COLORS['text_muted']};">{st.session_state.user_points} نقطة</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📅 تسجيل الحضور اليومي", use_container_width=True):
        daily_check_in()

    st.markdown("---")
    st.markdown(f"*الإصدار {APP_VERSION}*")
    st.caption(f"📡 TheSportsDB API | {len(LEAGUES)} دوري")

# ===== التنقل =====
pages = {
    "🏠 الرئيسية": page_home,
    "🔴 مباشر": page_live,
    "📅 المباريات": page_matches,
    "🏆 الترتيب": page_standings,
    "📊 الإحصائيات": page_stats,
    "⭐ المفضلة": page_favorites,
    "🔮 التنبؤات": page_predictions,
    "📈 الهدافين": page_scorers,
    "⚖️ المقارنة": page_compare,
    "🏅 الإنجازات": page_achievements,
    "⚙️ الإعدادات": page_settings,
}

selected_page = st.sidebar.radio("📌 التنقل", list(pages.keys()), label_visibility="collapsed")
pages[selected_page]()

# ===== Footer =====
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; color:#94a3b8; padding:20px; font-size:12px;">
    ⚽ كورة لايف برو — {len(LEAGUES)} دوري | جميع الحقوق محفوظة © 2024<br>
    البيانات مقدمة من TheSportsDB
</div>
""", unsafe_allow_html=True)
