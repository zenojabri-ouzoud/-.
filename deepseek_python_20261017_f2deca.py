import streamlit as st
import json
import os
import base64
from datetime import datetime
import time

# ==============================================================================
# 1. إعدادات الصفحة والتهيئة
# ==============================================================================
st.set_page_config(
    page_title="مكتبة عوالم زيكولا",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# المسارات والملفات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
REVIEWS_FILE = os.path.join(BASE_DIR, "reviews.json")

# إنشاء المجلدات إذا لم تكن موجودة
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)

# ==============================================================================
# 2. بيانات الروايات
# ==============================================================================
BOOKS_DATA = [
    {
        "id": "zicola_1",
        "title": "أرض زيكولا",
        "author": "عمرو عبد الحميد",
        "category": "سلسلة زيكولا",
        "desc": "هل يمكن أن تسرق ذكاءك؟ خالد شاب يجد نفسه في عالم غريب حيث الذكاء هو العملة، والفقراء هم من يُذبحون.",
        "filename": "ard_zicola.pdf",
        "cover_url": "https://m.media-amazon.com/images/I/81Q2P5G2fOL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "id": "zicola_2",
        "title": "أماريتا",
        "author": "عمرو عبد الحميد",
        "category": "سلسلة زيكولا",
        "desc": "رحلة أسيل للبحث عن الأمل في عالم جديد، حيث تلتقي بالملك تميم وتواجه أسراراً خطيرة.",
        "filename": "amareta.pdf",
        "cover_url": "https://m.media-amazon.com/images/I/81x4Y1L6yXL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "id": "zicola_3",
        "title": "وادي الذئاب المنسية",
        "author": "عمرو عبد الحميد",
        "category": "سلسلة زيكولا",
        "desc": "عودة إلى زيكولا بعد قرن من الزمان. موسى، حفيد خالد، يكتشف أن الذئاب لم تنقرض، وأن الأسطورة حقيقية.",
        "filename": "wadi_alzeab.pdf",
        "cover_url": "https://m.media-amazon.com/images/I/71b7Yy4rK-L._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "id": "arses_1",
        "title": "آرسس",
        "author": "أحمد آل حمدان",
        "category": "عوالم مظلمة",
        "desc": "مهمة فضائية، وثقب زمني، ومحاولة لإنقاذ زوجة من الموت. هاشم يعود بالزمن 9 سنوات لتصحيح القدر.",
        "filename": "arses.pdf",
        "cover_url": "https://m.media-amazon.com/images/I/71D5Fq-JiCL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "id": "sijil_1",
        "title": "السجيل",
        "author": "أحمد آل حمدان",
        "category": "عوالم مظلمة",
        "desc": "خوف، حقيقة، وموت. رحلة نفسية عميقة في عالم من الغموض والذكريات المؤلمة. الطب هو التوأم اللطيف للموت.",
        "filename": "alsijil.pdf",
        "cover_url": "https://m.media-amazon.com/images/I/81P7zKq0XAL._AC_UF1000,1000_QL80_.jpg"
    }
]

# ==============================================================================
# 3. دوال إدارة الملفات والتعليقات
# ==============================================================================

def generate_dummy_pdfs():
    """إنشاء ملفات PDF وهمية إذا لم تكن موجودة (للتجربة)."""
    for book in BOOKS_DATA:
        filepath = os.path.join(PDF_DIR, book["filename"])
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"رواية: {book['title']}\nالمؤلف: {book['author']}\nهذا ملف تجريبي.")

def get_binary_file_downloader_html(bin_file, file_label='تحميل'):
    """إنشاء رابط تحميل لملف PDF."""
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
    new_review = {
        "book_id": book_id,
        "name": name,
        "rating": int(rating),
        "text": text,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    reviews.append(new_review)
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

# ==============================================================================
# 4. التصميم المخصص (CSS)
# ==============================================================================
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Tajawal:wght@400;700&display=swap');
        html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; }
        h1, h2, h3 { font-family: 'Cairo', sans-serif; color: #d35400; }
        
        .stImage img { border-radius: 10px; }
        
        .review-box {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-right: 4px solid #2980b9;
        }
        .review-author { font-weight: bold; color: #2c3e50; }
        .review-date { font-size: 0.8rem; color: #7f8c8d; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 5. واجهة التطبيق الرئيسية
# ==============================================================================
def main():
    generate_dummy_pdfs()
    inject_custom_css()

    # الشريط الجانبي
    with st.sidebar:
        st.title("📚 مكتبة زيكولا")
        st.markdown("---")
        categories = list(set([b["category"] for b in BOOKS_DATA]))
        selected_cat = st.radio("تصفح التصنيفات:", ["الكل"] + categories)
        st.markdown("---")
        st.info("💡 استخدم زر التحميل للحصول على نسخة PDF.")
        
        # وضع ليلي بسيط
        theme = st.radio("المظهر:", ["☀️ نهاري", "🌙 ليلي"])
        if theme == "🌙 ليلي":
            st.markdown("<style>.stApp { background-color: #0e1117; color: #fafafa; } .review-box { background-color: #1e2630; }</style>", unsafe_allow_html=True)

    # العنوان الرئيسي
    st.markdown("<h1 style='text-align: center;'>غُص في أعماق الخيال</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>مجموعة مختارة من أفضل روايات الفانتازيا والخيال العلمي</p>", unsafe_allow_html=True)
    st.markdown("---")

    # تصفية الكتب
    filtered_books = BOOKS_DATA if selected_cat == "الكل" else [b for b in BOOKS_DATA if b["category"] == selected_cat]

    # عرض الكتب في 3 أعمدة
    cols = st.columns(3)
    for idx, book in enumerate(filtered_books):
        with cols[idx % 3]:
            with st.container(border=True): # إطار للبطاقة
                st.image(book["cover_url"], use_column_width=True)
                st.subheader(book["title"])
                st.caption(f"✍️ {book['author']} | 📂 {book['category']}")
                st.write(book["desc"])
                
                # زر التحميل
                file_path = os.path.join(PDF_DIR, book["filename"])
                if os.path.exists(file_path):
                    st.markdown(get_binary_file_downloader_html(file_path, "⬇️ تحميل PDF"), unsafe_allow_html=True)
                else:
                    st.warning("الملف غير متوفر.")
                
                st.divider()
                
                # التعليقات
                st.write("**💬 آراء القراء:**")
                reviews = [r for r in load_reviews() if r["book_id"] == book["id"]]
                
                if reviews:
                    for r in reviews[-3:]: # عرض آخر 3 تعليقات
                        st.markdown(f"""
                        <div class="review-box">
                            <span class="review-author">{r['name']}</span> 
                            <span>{'⭐'*r['rating']}</span>
                            <p style="margin:5px 0;">{r['text']}</p>
                            <span class="review-date">{r['date']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("لا توجد تعليقات بعد.")
                
                # نموذج إضافة تعليق
                with st.expander("✍️ أضف تعليقك"):
                    with st.form(key=f"form_{book['id']}"):
                        name = st.text_input("الاسم", key=f"name_{book['id']}")
                        rating = st.slider("التقييم", 1, 5, 5, key=f"rate_{book['id']}")
                        comment = st.text_area("التعليق", key=f"comment_{book['id']}")
                        submitted = st.form_submit_button("نشر")
                        
                        if submitted:
                            if name and comment:
                                save_review(book["id"], name, rating, comment)
                                st.success("تم النشر!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("الرجاء ملء الحقول.")

    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2024 مكتبة عوالم زيكولا</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
