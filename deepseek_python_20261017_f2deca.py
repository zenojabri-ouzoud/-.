import streamlit as st
import json
import os
import base64
from datetime import datetime
import time
import random

# ==============================================================================
# 1. إعدادات الصفحة
# ==============================================================================
st.set_page_config(
    page_title="مكتبة عوالم زيكولا | المنصة المتكاملة",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. قاعدة البيانات (الملفات الكاملة + التفاصيل)
# ==============================================================================
BOOKS_DATA = [
    {
        "id": "zicola_1",
        "title": "أرض زيكولا",
        "author": "عمرو عبد الحميد",
        "category": "فانتازيا",
        "desc": "هل يمكن أن تسرق ذكاءك؟ خالد شاب يجد نفسه في عالم غريب حيث الذكاء هو العملة.",
        "cover": "https://m.media-amazon.com/images/I/81Q2P5G2fOL._AC_UF1000,1000_QL80_.jpg",
        "file": "pdfs/ard_zicola.pdf",
        "downloads": 1520,
        "rating": 4.8,
        "preview": "اسمي موسى، عمري ثمانية عشر عامًا، الابن الأخير لأبي وأمي بين تسعة أبناء...",
        "toc": ["الفصل الأول: قرية البهو فريك", "الفصل الثاني: الخواجة فايز", "الفصل الثالث: الطاحونة", "الفصل الرابع: سرداب فوريك"]
    },
    {
        "id": "zicola_2",
        "title": "أماريتا",
        "author": "عمرو عبد الحميد",
        "category": "فانتازيا",
        "desc": "رحلة أسيل للبحث عن الأمل في عالم جديد، حيث تلتقي بالملك تميم وتواجه أسراراً خطيرة.",
        "cover": "https://m.media-amazon.com/images/I/81x4Y1L6yXL._AC_UF1000,1000_QL80_.jpg",
        "file": "pdfs/amareta.pdf",
        "downloads": 980,
        "rating": 4.6,
        "preview": "كانت الشمس قد غربت حين غادرت ألشميل عربة يجرّها حصانان انطلقت في طريقها إلى مدينة أماريتا...",
        "toc": ["الفصل الأول: بيجانا", "الفصل الثاني: السجن الغربي", "الفصل الثالث: القافلة"]
    },
    {
        "id": "zicola_3",
        "title": "وادي الذئاب المنسية",
        "author": "عمرو عبد الحميد",
        "category": "فانتازيا",
        "desc": "عودة إلى زيكولا بعد قرن من الزمان. موسى يكتشف أن الذئاب لم تنقرض.",
        "cover": "https://m.media-amazon.com/images/I/71b7Yy4rK-L._AC_UF1000,1000_QL80_.jpg",
        "file": "pdfs/wadi_alzeab.pdf",
        "downloads": 750,
        "rating": 4.9,
        "preview": "قريبة البهو فريك - الحفصيلة 1921م: اسمي موسى، عمري ثمانية عشر عامًا...",
        "toc": ["الفصل الأول: موسى", "الفصل الثاني: الحريق", "الفصل الثالث: الهجانة"]
    },
    {
        "id": "arses_1",
        "title": "آرسس",
        "author": "أحمد آل حمدان",
        "category": "خيال علمي",
        "desc": "مهمة فضائية، وثقب زمني، ومحاولة لإنقاذ زوجة من الموت.",
        "cover": "https://m.media-amazon.com/images/I/71D5Fq-JiCL._AC_UF1000,1000_QL80_.jpg",
        "file": "pdfs/arses.pdf",
        "downloads": 1200,
        "rating": 4.7,
        "preview": "إنها إحدى الليالي الأكثر هدوءًا، كان القمر مكتملاً في قلب السماء...",
        "toc": ["الفصل الأول: هاشم", "الفصل الثاني: المهمة", "الفصل الثالث: الثقب الزمني"]
    },
    {
        "id": "sijil_1",
        "title": "السجيل",
        "author": "أحمد آل حمدان",
        "category": "غموض",
        "desc": "خوف، حقيقة، وموت. رحلة نفسية عميقة في عالم من الغموض.",
        "cover": "https://m.media-amazon.com/images/I/81P7zKq0XAL._AC_UF1000,1000_QL80_.jpg",
        "file": "pdfs/alsijil.pdf",
        "downloads": 600,
        "rating": 4.5,
        "preview": "هذه الرواية أو السيرة الذاتية أو كما ستصنف لاحقاً...",
        "toc": ["مقدمة", "اليوم الذي اكتشفت فيه القراءة", "الليلة المشؤومة"]
    }
]

# ==============================================================================
# 3. إدارة الملفات والبيانات
# ==============================================================================
PDF_DIR = "pdfs"
REVIEWS_FILE = "reviews.json"

if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)

def generate_dummy_pdfs():
    for book in BOOKS_DATA:
        filepath = os.path.join(PDF_DIR, book["file"].split("/")[-1])
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"رواية: {book['title']}\nالمؤلف: {book['author']}\nهذا ملف تجريبي.")

def get_binary_file_downloader_html(bin_file, file_label='تحميل'):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}" style="display:inline-block; padding:10px 20px; background-color:#2980b9; color:white; text-decoration:none; border-radius:5px; font-weight:bold; text-align:center; width:100%;">{file_label}</a>'
        return href
    except:
        return "<p style='color:red;'>الملف غير متوفر</p>"

def load_reviews():
    if os.path.exists(REVIEWS_FILE):
        try:
            with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_review(book_id, name, rating, text):
    reviews = load_reviews()
    new_review = {"book_id": book_id, "name": name, "rating": int(rating), "text": text, "date": datetime.now().strftime("%Y-%m-%d %H:%M")}
    reviews.append(new_review)
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

# ==============================================================================
# 4. التصميم والسمات
# ==============================================================================
def inject_custom_css(theme="light"):
    if theme == "dark":
        bg, card_bg, text, border = "#0e1117", "#1e2630", "#fafafa", "#2c3e50"
    elif theme == "desert":
        bg, card_bg, text, border = "#fdf5e6", "#fff8dc", "#5c4033", "#d2b48c"
    else:
        bg, card_bg, text, border = "#ffffff", "#f8f9fa", "#2c3e50", "#e1e8ed"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Tajawal:wght@400;700&display=swap');
        .stApp {{ background-color: {bg}; color: {text}; }}
        h1, h2, h3 {{ font-family: 'Cairo', sans-serif; color: #d35400; }}
        div[data-testid="stVerticalBlock"] > div:has(div.stImage) {{ background-color: {card_bg}; border-radius: 15px; padding: 15px; border: 1px solid {border}; }}
        .review-box {{ background-color: {card_bg}; padding: 10px; border-radius: 8px; border-right: 4px solid #2980b9; margin-bottom: 10px; }}
        .quote-box {{ text-align: center; font-style: italic; color: #e67e22; padding: 20px; font-size: 1.2rem; border-radius: 10px; border: 1px dashed #e67e22; }}
        #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 5. الواجهة الرئيسية
# ==============================================================================
def main():
    generate_dummy_pdfs()
    
    if "favorites" not in st.session_state: st.session_state.favorites = []
    if "theme" not in st.session_state: st.session_state.theme = "light"
    if "reader_mode" not in st.session_state: st.session_state.reader_mode = False

    # الشريط الجانبي
    with st.sidebar:
        st.title("📚 مكتبة زيكولا")
        
        # اختيار السمة
        theme_choice = st.selectbox("🎨 السمة:", ["فاتح", "داكن", "صحراوي"])
        if theme_choice == "داكن": st.session_state.theme = "dark"
        elif theme_choice == "صحراوي": st.session_state.theme = "desert"
        else: st.session_state.theme = "light"
        
        # وضع القارئ
        if st.checkbox("👓 وضع القارئ الليلي"):
            st.session_state.reader_mode = True
            st.session_state.theme = "dark"
        else:
            st.session_state.reader_mode = False

        inject_custom_css(st.session_state.theme)
        st.markdown("---")
        
        # البحث
        search_query = st.text_input("🔍 بحث سريع:", "")
        
        # التصنيفات
        categories = list(set([b["category"] for b in BOOKS_DATA]))
        selected_cat = st.radio("📂 التصنيفات:", ["الكل"] + categories)
        
        st.markdown("---")
        # المفضلة
        st.write(f"❤️ المفضلة ({len(st.session_state.favorites)})")
        for fav in st.session_state.favorites: st.write(f"- {fav}")

    # الاقتباس المتحرك (Quote Slider)
    quotes = [
        "الطب هو التوأم اللطيف للموت - السجيل",
        "من يحب سيفعل كل شيء من أجل من يحبه - أماريتا",
        "الذكاء هو العملة، والفقراء هم من يُذبحون - أرض زيكولا",
        "الوقت لم يسعفني لقراءة الورقة التي طلبت مني قراءتها - آرسس"
    ]
    st.markdown(f"<div class='quote-box'>❝ {random.choice(quotes)} ❞</div>", unsafe_allow_html=True)
    st.markdown("---")

    # لوحة الشرف (Leaderboard)
    with st.expander("🏆 لوحة الشرف (الأكثر تحميلاً)"):
        top_books = sorted(BOOKS_DATA, key=lambda x: x["downloads"], reverse=True)[:3]
        for i, b in enumerate(top_books, 1):
            st.write(f"{i}. **{b['title']}** ({b['downloads']} تحميل)")

    # الخريطة التفاعلية (HTML/CSS)
    with st.expander("🗺️ خريطة عالم زيكولا التفاعلية"):
        st.markdown("""
        <div style="display: flex; justify-content: space-around; padding: 20px; background: #f4f4f4; border-radius: 10px;">
            <div style="text-align: center; padding: 10px; border: 2px solid #2980b9; border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; background: white;">أرض زيكولا</div>
            <div style="text-align: center; padding: 10px; border: 2px solid #d35400; border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; background: white;">أماريتا</div>
            <div style="text-align: center; padding: 10px; border: 2px solid #27ae60; border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; background: white;">بيجانا</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # تصفية الكتب
    filtered_books = BOOKS_DATA
    if selected_cat != "الكل":
        filtered_books = [b for b in filtered_books if b["category"] == selected_cat]
    if search_query:
        filtered_books = [b for b in filtered_books if search_query.lower() in b["title"].lower() or search_query.lower() in b["desc"].lower()]

    # عرض الكتب
    cols = st.columns(2)
    for idx, book in enumerate(filtered_books):
        with cols[idx % 2]:
            with st.container(border=True):
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.image(book["cover"], use_column_width=True)
                    st.caption(f"⬇️ {book['downloads']} | ⭐ {book['rating']}")
                with c2:
                    st.subheader(book["title"])
                    st.caption(f"✍️ {book['author']} | 📂 {book['category']}")
                    st.write(book["desc"])
                    
                    # أزرار
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("❤️ مفضلة", key=f"fav_{book['id']}"):
                            if book["title"] not in st.session_state.favorites:
                                st.session_state.favorites.append(book["title"])
                                st.toast("تمت الإضافة للمفضلة!")
                    with col_btn2:
                        if st.button("👁️ معاينة", key=f"prev_{book['id']}"):
                            st.info(f"**مقتطف:** {book['preview']}...")
                    
                    # تحميل
                    file_path = os.path.join(PDF_DIR, book["file"].split("/")[-1])
                    if os.path.exists(file_path):
                        st.markdown(get_binary_file_downloader_html(file_path, "⬇️ تحميل PDF"), unsafe_allow_html=True)
                
                # الفهرس
                with st.expander("📑 فهرس الكتاب"):
                    for chapter in book["toc"]:
                        st.markdown(f"- {chapter}")
                
                # التعليقات
                with st.expander("💬 آراء القراء"):
                    reviews = [r for r in load_reviews() if r["book_id"] == book["id"]]
                    if reviews:
                        for r in reviews:
                            st.markdown(f"""
                            <div class="review-box">
                                <strong>{r['name']}</strong> <span style='color:gold;'>{'⭐'*r['rating']}</span>
                                <p>{r['text']}</p>
                                <small>{r['date']}</small>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("كن أول من يضيف تعليقاً!")
                    
                    with st.form(key=f"form_{book['id']}"):
                        name = st.text_input("الاسم", key=f"n_{book['id']}")
                        rating = st.slider("التقييم", 1, 5, 5, key=f"r_{book['id']}")
                        text = st.text_area("التعليق", key=f"t_{book['id']}")
                        if st.form_submit_button("نشر"):
                            if name and text:
                                save_review(book["id"], name, rating, text)
                                st.success("تم النشر!")
                                time.sleep(1)
                                st.rerun()

    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2024 مكتبة زيكولا - جميع الحقوق محفوظة</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
