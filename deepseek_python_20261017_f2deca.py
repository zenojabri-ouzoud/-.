import streamlit as st
from utils import (
    load_css, init_session, page_title, get_user_level, get_next_level_info,
    USER_LEVELS, USER_POINTS, COLORS, get_user_predictions, daily_check_in
)

st.set_page_config(page_title="الإنجازات", page_icon="🏅", layout="wide")
load_css()
init_session()

st.markdown(page_title("🏅 الإنجازات"), unsafe_allow_html=True)
st.markdown("---")

points = st.session_state.user_points
level = get_user_level(points)
next_level, progress = get_next_level_info(points)

# بطاقة المستخدم
st.markdown(f"""
<div class="user-level" style="padding:25px; justify-content:center; flex-direction:column; text-align:center;">
    <div style="font-size:72px;">{level['icon']}</div>
    <div style="font-size:28px; font-weight:bold; margin:10px 0;">{level['name']}</div>
    <div style="font-size:18px; color:{COLORS['success']};">{points} نقطة</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# شريط التقدم
if next_level:
    st.markdown(f"### 📈 التقدم للمستوى {next_level['icon']} {next_level['name']}")
    st.progress(progress)
    st.caption(f"باقي {next_level['min'] - points} نقطة")
else:
    st.success("🎉 وصلت لأعلى مستوى!")

st.markdown("---")

# جميع المستويات
st.markdown("### 🏆 جميع المستويات")

for lvl in USER_LEVELS:
    achieved = points >= lvl["min"]
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

# إحصائيات
st.markdown("### 📊 إحصائياتك")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("⭐ النقاط", points)
with c2:
    st.metric("🔮 التنبؤات", len(get_user_predictions()))
with c3:
    st.metric("📅 سلسلة الحضور", st.session_state.check_in_streak)
with c4:
    st.metric("⭐ المفضلة", len(st.session_state.favorites))

st.markdown("---")
if st.button("📅 تسجيل الحضور اليومي", use_container_width=True, type="primary"):
    daily_check_in()
    st.rerun()
