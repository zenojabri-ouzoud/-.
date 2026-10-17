# ==============================================================================
# مشروع: مكتبة عوالم زيكولا (النسخة الاحترافية v2.0)
# الميزات: صور ديناميكية، نظام تعليقات (JSON)، تحميل كسول، وضع ليلي.
# اللغة: Python 3
# ==============================================================================

import http.server
import socketserver
import os
import json
import urllib.parse
import base64
from datetime import datetime

# ==============================================================================
# 1. الإعدادات الأساسية
# ==============================================================================
PORT = 8000
HOST = "127.0.0.1"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
IMG_DIR = os.path.join(BASE_DIR, "images")
REVIEWS_FILE = os.path.join(BASE_DIR, "reviews.json")

# بيانات الكتب (يمكنك إضافة المزيد لاحقاً)
# ملاحظة: تم استخدام روابط صور من الإنترنت كمثال، يمكنك استبدالها بصور محلية
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
# 2. دوال إدارة الملفات (Setup & Data Management)
# ==============================================================================

def setup_environment():
    """إنشاء المجلدات والملفات المطلوبة إذا لم تكن موجودة."""
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    if not os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def generate_dummy_pdfs():
    """إنشاء ملفات PDF وهمية لتجربة التحميل."""
    for book in BOOKS_DATA:
        filepath = os.path.join(PDF_DIR, book["filename"])
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"رواية: {book['title']}\nالمؤلف: {book['author']}\nهذا ملف تجريبي.")

def load_reviews():
    """قراءة التعليقات من ملف JSON."""
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_review(book_id, name, rating, text):
    """حفظ تعليق جديد في ملف JSON."""
    reviews = load_reviews()
    new_review = {
        "book_id": book_id,
        "name": name,
        "rating": int(rating),
        "text": text,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    reviews.append(new_review)
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

# ==============================================================================
# 3. توليد محتوى HTML
# ==============================================================================

def generate_html_content():
    """توليد صفحة HTML كاملة مع الكتب والتعليقات."""
    
    reviews = load_reviews()
    books_html = ""

    # تقسيم الكتب حسب التصنيف
    categories = {}
    for book in BOOKS_DATA:
        if book["category"] not in categories:
            categories[book["category"]] = []
        categories[book["category"]].append(book)

    for cat_name, books in categories.items():
        books_html += f"""
        <section id="{cat_name.replace(' ', '_')}" class="container">
            <h2 class="section-title">{cat_name}</h2>
            <div class="books-grid">
        """
        
        for book in books:
            # جلب تعليقات هذا الكتاب
            book_reviews = [r for r in reviews if r["book_id"] == book["id"]]
            avg_rating = sum([r["rating"] for r in book_reviews]) / len(book_reviews) if book_reviews else 0
            stars = "⭐" * round(avg_rating)
            
            reviews_html = ""
            for r in book_reviews[-3:]: # عرض آخر 3 تعليقات فقط
                reviews_html += f"""
                <div class="review-item">
                    <strong>{r['name']}</strong> <span class="stars">{'⭐'*r['rating']}</span>
                    <p>{r['text']}</p>
                    <small>{r['date']}</small>
                </div>
                """

            books_html += f"""
                <div class="book-card">
                    <div class="cover-wrapper">
                        <img src="{book['cover_url']}" alt="{book['title']}" class="book-cover" loading="lazy">
                    </div>
                    <div class="book-info">
                        <h3 class="book-title">{book['title']}</h3>
                        <p class="book-author">{book['author']}</p>
                        <div class="rating-display">{stars} ({len(book_reviews)} تقييم)</div>
                        <p class="book-desc">{book['desc']}</p>
                        
                        <!-- زر التحميل -->
                        <a href="/pdfs/{book['filename']}" class="download-btn" download>تحميل PDF</a>
                        
                        <!-- قسم التعليقات -->
                        <div class="reviews-section">
                            <h4>آراء القراء:</h4>
                            {reviews_html if reviews_html else '<p class="no-reviews">لا توجد تعليقات بعد. كن الأول!</p>'}
                            
                            <!-- نموذج إضافة تعليق -->
                            <form action="/add_review" method="POST" class="review-form">
                                <input type="hidden" name="book_id" value="{book['id']}">
                                <input type="text" name="name" placeholder="اسمك" required>
                                <select name="rating" required>
                                    <option value="5">⭐⭐⭐⭐⭐ ممتاز</option>
                                    <option value="4">⭐⭐⭐⭐ جيد جداً</option>
                                    <option value="3">⭐⭐⭐ جيد</option>
                                    <option value="2">⭐⭐ مقبول</option>
                                    <option value="1">⭐ ضعيف</option>
                                </select>
                                <textarea name="text" placeholder="اكتب رأيك هنا..." required></textarea>
                                <button type="submit" class="submit-btn">إضافة تعليق</button>
                            </form>
                        </div>
                    </div>
                </div>
            """
        books_html += "</div></section>"

    # قالب HTML الرئيسي
    html = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مكتبة عوالم زيكولا</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #f4f6f9;
            --text-color: #2c3e50;
            --card-bg: #ffffff;
            --primary: #d35400;
            --secondary: #2980b9;
            --border: #e1e8ed;
            --shadow: 0 8px 20px rgba(0,0,0,0.06);
        }}
        body.dark-mode {{
            --bg-color: #0f171e;
            --text-color: #ecf0f1;
            --card-bg: #1a252f;
            --border: #2c3e50;
            --shadow: 0 8px 20px rgba(0,0,0,0.4);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Tajawal', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            transition: background 0.3s, color 0.3s;
        }}
        a {{ text-decoration: none; color: inherit; }}
        
        /* Navbar */
        .navbar {{
            position: fixed; top: 0; width: 100%; height: 70px;
            background: var(--card-bg); box-shadow: var(--shadow);
            display: flex; justify-content: space-between; align-items: center;
            padding: 0 5%; z-index: 100; transition: background 0.3s;
        }}
        .logo {{ font-family: 'Cairo'; font-weight: 900; font-size: 1.5rem; color: var(--primary); }}
        .theme-toggle {{ border: 1px solid var(--border); background: none; color: var(--text-color); padding: 8px 16px; border-radius: 20px; cursor: pointer; font-family: inherit; font-weight: bold; }}
        
        /* Hero */
        .hero {{
            height: 50vh; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1547483238-2cbf881a559f') center/cover;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            color: white; text-align: center; padding: 20px; margin-top: 70px;
        }}
        .hero h1 {{ font-family: 'Cairo'; font-size: 2.5rem; margin-bottom: 10px; }}
        
        /* Container & Grid */
        .container {{ max-width: 1200px; margin: 40px auto; padding: 0 20px; }}
        .section-title {{ font-family: 'Cairo'; font-size: 2rem; text-align: center; margin-bottom: 30px; color: var(--primary); }}
        .books-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }}
        
        /* Book Card */
        .book-card {{
            background: var(--card-bg); border-radius: 12px; overflow: hidden;
            box-shadow: var(--shadow); border: 1px solid var(--border);
            display: flex; flex-direction: column; transition: transform 0.3s;
        }}
        .book-card:hover {{ transform: translateY(-5px); }}
        
        /* Cover */
        .cover-wrapper {{ height: 250px; overflow: hidden; position: relative; background: #eee; }}
        .book-cover {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }}
        .book-card:hover .book-cover {{ transform: scale(1.05); }}
        
        /* Info */
        .book-info {{ padding: 20px; flex-grow: 1; display: flex; flex-direction: column; }}
        .book-title {{ font-family: 'Cairo'; font-size: 1.3rem; margin-bottom: 5px; }}
        .book-author {{ color: var(--primary); font-size: 0.9rem; margin-bottom: 10px; }}
        .rating-display {{ font-size: 0.9rem; margin-bottom: 15px; color: #f1c40f; }}
        .book-desc {{ font-size: 0.95rem; color: #777; margin-bottom: 20px; flex-grow: 1; }}
        body.dark-mode .book-desc {{ color: #aaa; }}
        
        /* Buttons */
        .download-btn {{
            display: block; width: 100%; padding: 12px; text-align: center;
            background: var(--secondary); color: white; border-radius: 8px;
            font-weight: bold; transition: background 0.3s;
        }}
        .download-btn:hover {{ background: #1c5980; }}
        
        /* Reviews */
        .reviews-section {{ margin-top: 25px; border-top: 1px solid var(--border); padding-top: 15px; }}
        .reviews-section h4 {{ font-size: 1rem; margin-bottom: 10px; }}
        .review-item {{ background: rgba(0,0,0,0.03); padding: 10px; border-radius: 8px; margin-bottom: 10px; font-size: 0.9rem; }}
        .review-item .stars {{ font-size: 0.8rem; }}
        .review-item small {{ display: block; color: #999; margin-top: 5px; }}
        .no-reviews {{ font-size: 0.9rem; color: #999; font-style: italic; }}
        
        /* Form */
        .review-form {{ display: flex; flex-direction: column; gap: 8px; margin-top: 15px; }}
        .review-form input, .review-form select, .review-form textarea {{
            width: 100%; padding: 8px; border: 1px solid var(--border); border-radius: 6px;
            background: var(--bg-color); color: var(--text-color); font-family: inherit;
        }}
        .review-form textarea {{ resize: vertical; height: 60px; }}
        .submit-btn {{ padding: 8px; background: var(--primary); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }}
        .submit-btn:hover {{ background: #e67e22; }}
        
        /* Footer */
        footer {{ text-align: center; padding: 30px; background: var(--card-bg); margin-top: 50px; color: #888; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="logo">مكتبة عوالم زيكولا</div>
        <button class="theme-toggle" id="themeToggle">🌙 الوضع الليلي</button>
    </nav>
    
    <header class="hero">
        <h1>غُص في أعماق الخيال</h1>
        <p>مجموعة مختارة من أفضل روايات الفانتازيا والخيال العلمي</p>
    </header>
    
    <main>
        {books_html}
    </main>
    
    <footer>
        <p>&copy; 2024 جميع الحقوق محفوظة - تم التصميم بواسطة Python</p>
    </footer>

    <script>
        // الوضع الليلي
        const toggle = document.getElementById('themeToggle');
        const body = document.body;
        
        if (localStorage.getItem('theme') === 'dark') {{
            body.classList.add('dark-mode');
            toggle.innerText = '☀️ الوضع النهاري';
        }}
        
        toggle.addEventListener('click', () => {{
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {{
                toggle.innerText = '☀️ الوضع النهاري';
                localStorage.setItem('theme', 'dark');
            }} else {{
                toggle.innerText = '🌙 الوضع الليلي';
                localStorage.setItem('theme', 'light');
            }}
        }});
    </script>
</body>
</html>
    """
    return html

# ==============================================================================
# 4. معالج الطلبات (Server Handler)
# ==============================================================================

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            content = generate_html_content().encode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            
        elif self.path.startswith('/pdfs/'):
            filename = self.path.split('/')[-1]
            filepath = os.path.join(PDF_DIR, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header("Content-type", "application/pdf")
                self.send_header("Content-Disposition", f"attachment; filename={filename}")
                self.send_header("Content-Length", str(os.path.getsize(filepath)))
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File Not Found")
        else:
            super().do_GET()

    def do_POST(self):
        # معالجة إرسال نموذج التعليق
        if self.path == '/add_review':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            
            book_id = params.get('book_id', [''])[0]
            name = params.get('name', ['مجهول'])[0]
            rating = params.get('rating', ['5'])[0]
            text = params.get('text', [''])[0]
            
            if book_id and text:
                save_review(book_id, name, rating, text)
            
            # إعادة التوجيه للصفحة الرئيسية بعد الحفظ
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass # إخفاء السجلات المزعجة

# ==============================================================================
# 5. التشغيل
# ==============================================================================

def run():
    setup_environment()
    generate_dummy_pdfs()
    
    print("="*50)
    print("🚀 الخادم يعمل الآن...")
    print(f"🌐 افتح المتصفح على: http://{HOST}:{PORT}")
    print("="*50)
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 تم إيقاف الخادم.")

if __name__ == "__main__":
    run()