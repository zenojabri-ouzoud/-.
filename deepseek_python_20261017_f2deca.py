import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="مكتبتي الرقمية", layout="wide")

# الكود كامل ديال الموقع (HTML + CSS + JS)
html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مكتبتي الرقمية</title>
    <!-- مكتبة PDF.js باش نقدرو نقراو ملفات PDF -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.min.js"></script>
    <style>
        /* ==================== CSS (التصميم) ==================== */
        :root {
            --bg-color: #f4f4f9;
            --text-color: #333;
            --header-bg: #2c3e50;
            --card-bg: #ffffff;
            --card-text: #2c3e50;
            --card-author: #7f8c8d;
            --btn-primary: #3498db;
            --btn-hover: #2980b9;
            --btn-success: #2ecc71;
            --btn-success-hover: #27ae60;
            --btn-danger: #e74c3c;
            --btn-danger-hover: #c0392b;
        }

        /* الوضع الليلي */
        body.dark-mode {
            --bg-color: #121212;
            --text-color: #e0e0e0;
            --header-bg: #1e1e1e;
            --card-bg: #2c2c2c;
            --card-text: #e0e0e0;
            --card-author: #a0a0a0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--bg-color);
            color: var(--text-color);
            transition: background-color 0.3s, color 0.3s;
        }

        /* الهيدر */
        header {
            background-color: var(--header-bg);
            color: white;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            transition: background-color 0.3s;
        }

        header h1 {
            margin: 0;
            font-size: 1.8rem;
        }

        .header-controls {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        #search-input {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            border: none;
            width: 250px;
            font-size: 1rem;
            outline: none;
        }

        #theme-toggle {
            background: transparent;
            border: 2px solid white;
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background 0.3s;
        }

        #theme-toggle:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        /* شبكة الكتب */
        .books-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 2rem;
            padding: 2rem;
        }

        /* بطاقة الكتاب */
        .book-card {
            background: var(--card-bg);
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            border: 1px solid rgba(0,0,0,0.05);
        }

        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        /* صورة غلاف الكتاب */
        .book-cover {
            width: 100%;
            height: 180px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
            background-color: #ddd;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #666;
            font-size: 0.9rem;
        }

        .book-cover img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 8px;
        }

        .book-card h3 {
            margin-top: 0;
            font-size: 1.2rem;
            color: var(--card-text);
            min-height: 50px;
        }

        .book-card p {
            color: var(--card-author);
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }

        /* الأزرار */
        .book-card button, .book-card .download-btn {
            background-color: var(--btn-primary);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            font-size: 0.9rem;
            margin: 0.2rem;
            transition: background-color 0.3s ease;
            display: inline-block;
        }

        .book-card .download-btn {
            background-color: var(--btn-success);
        }

        .book-card button:hover {
            background-color: var(--btn-hover);
        }

        .book-card .download-btn:hover {
            background-color: var(--btn-success-hover);
        }

        /* شاشة القراءة */
        #reader-screen {
            background-color: var(--bg-color);
            min-height: 100vh;
            transition: background-color 0.3s;
        }

        #reader-screen header {
            background-color: var(--header-bg);
            padding: 0.8rem 2rem;
        }

        #reader-screen #back-btn {
            background-color: var(--btn-danger);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
        }

        #reader-screen #back-btn:hover {
            background-color: var(--btn-danger-hover);
        }

        #reader-title {
            margin: 0;
            font-size: 1.4rem;
            color: white;
        }

        #reader-content {
            padding: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-y: auto;
            background-color: #525659; /* خلفية ناعمة للقراءة */
            min-height: 80vh;
        }

        #pdf-canvas {
            background: white;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            max-width: 100%;
            height: auto;
        }

        #pdf-controls {
            margin-top: 1.5rem;
            display: flex;
            gap: 1rem;
            align-items: center;
            font-size: 1.1rem;
            color: white;
            background: rgba(0,0,0,0.5);
            padding: 0.5rem 1rem;
            border-radius: 10px;
        }

        #pdf-controls button {
            background-color: var(--btn-primary);
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 5px;
            cursor: pointer;
        }

        #pdf-controls button:hover {
            background-color: var(--btn-hover);
        }

        #pdf-controls button:disabled {
            background-color: #7f8c8d;
            cursor: not-allowed;
        }

        .download-btn {
            background-color: var(--btn-success);
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        /* للشاشات الصغيرة */
        @media (max-width: 600px) {
            header {
                flex-direction: column;
                gap: 1rem;
            }
            #search-input {
                width: 100%;
            }
            .books-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>

    <!-- الشاشة الرئيسية: قائمة الكتب -->
    <div id="home-screen">
        <header>
            <h1>مكتبتي الرقمية</h1>
            <div class="header-controls">
                <input type="text" id="search-input" placeholder="بحث عن كتاب أو مؤلف...">
                <button id="theme-toggle">🌙 الوضع الليلي</button>
            </div>
        </header>
        <div id="books-container" class="books-grid">
            <!-- هنا غادي يتعرضو الكتب -->
        </div>
    </div>

    <!-- شاشة القراءة (مخفية فالأول) -->
    <div id="reader-screen" style="display: none;">
        <header>
            <button id="back-btn">← رجوع للمكتبة</button>
            <h2 id="reader-title">عنوان الكتاب</h2>
            <a id="download-link" href="#" target="_blank" class="download-btn" download>تحميل PDF</a>
        </header>
        <div id="reader-content">
            <!-- هنا غادي يظهر النص ديال الكتاب -->
            <canvas id="pdf-canvas"></canvas>
            <div id="pdf-controls">
                <button id="prev-page">السابق</button>
                <span>صفحة <span id="page-num">1</span> من <span id="page-count">--</span></span>
                <button id="next-page">التالي</button>
            </div>
        </div>
    </div>

    <!-- ==================== JavaScript (المنطق) ==================== -->
    <script>
        // 1. البيانات (الكتب) - هنا فين غادي تحط الكتب ديالك
        const allBooks = [
            {
                id: 1,
                title: "وادي الذئاب المنسية",
                author: "عمرو عبد الحميد",
                content: "هذا الكتاب هو الأول في سلسلة أرض زيكولا. تدور أحداثه في قرية البهو فريك...",
                downloadUrl: "books/وادي-الذئاب-المنسية.pdf",
                coverUrl: "" 
            },
            {
                id: 2,
                title: "السجيل",
                author: "أحمد آل حمدان",
                content: "هذا الكتاب هو الرابع في سلسلة أبابيل. تدور أحداثه حول ملحمة الطين والنار...",
                downloadUrl: "books/السجيل-1.pdf",
                coverUrl: ""
            },
            {
                id: 3,
                title: "الجساسة",
                author: "أحمد آل حمدان",
                content: "هذا الكتاب هو الأول في سلسلة أبابيل. يحكي قصة عاصف وجومانا...",
                downloadUrl: "books/الجساسة.pdf",
                coverUrl: ""
            },
            {
                id: 4,
                title: "آرسس",
                author: "أحمد آل حمدان",
                content: "هذا الكتاب هو الثاني في سلسلة أبابيل. يكمل قصة عاصف ورحلته...",
                downloadUrl: "books/آرسس.pdf",
                coverUrl: ""
            },
            {
                id: 5,
                title: "آرسس 2",
                author: "أحمد آل حمدان",
                content: "هذا الكتاب هو الثالث في سلسلة أبابيل. الجزء الثاني من آرسس...",
                downloadUrl: "books/آرسس-2.pdf",
                coverUrl: ""
            },
            {
                id: 6,
                title: "الياقوت",
                author: "شهد قربان",
                content: "رواية الياقوت، الكتاب الرابع من سلسلة 005. تدور أحداثها حول...",
                downloadUrl: "books/124.pdf",
                coverUrl: ""
            },
            {
                id: 7,
                title: "أتابيل",
                author: "أحمد آل حمدان",
                content: "رواية أتابيل، الطب هو التوأم اللطيف للموت...",
                downloadUrl: "books/79.pdf",
                coverUrl: ""
            }
        ];

        // 2. المتغيرات
        let currentBook = null;
        let pdfDoc = null;
        let pageNum = 1;
        let pageRendering = false;
        let pageNumPending = null;
        const scale = 1.5;
        const canvas = document.getElementById('pdf-canvas');
        const ctx = canvas.getContext('2d');

        // 3. عرض الكتب فالشاشة
        function displayBooks(books) {
            const container = document.getElementById('books-container');
            container.innerHTML = ''; 

            if (books.length === 0) {
                container.innerHTML = '<p>ماكاينش كتب.</p>';
                return;
            }

            books.forEach(book => {
                const bookCard = document.createElement('div');
                bookCard.className = 'book-card';
                
                let coverHtml = `<div class="book-cover">لا توجد صورة</div>`;
                if (book.coverUrl) {
                    coverHtml = `<div class="book-cover"><img src="${book.coverUrl}" alt="${book.title}"></div>`;
                }

                bookCard.innerHTML = `
                    ${coverHtml}
                    <h3>${book.title}</h3>
                    <p>${book.author}</p>
                    <button onclick="readBook(${book.id})">قراءة</button>
                    <a href="${book.downloadUrl}" target="_blank" class="download-btn" download>تحميل PDF</a>
                `;
                container.appendChild(bookCard);
            });
        }

        // 4. القراءة (كنبدلو الشاشة)
        function readBook(id) {
            const book = allBooks.find(b => b.id === id);
            if (!book) return;

            currentBook = book;
            document.getElementById('home-screen').style.display = 'none';
            document.getElementById('reader-screen').style.display = 'block';
            document.getElementById('reader-title').textContent = book.title;
            document.getElementById('download-link').href = book.downloadUrl;
            document.getElementById('download-link').download = book.title + '.pdf';

            loadPdf(book.downloadUrl);
        }

        // 5. دالة تحميل PDF
        function loadPdf(url) {
            if (!url || url === '#') {
                alert('رابط التحميل غير متوفر.');
                return;
            }
            pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {
                pdfDoc = pdfDoc_;
                document.getElementById('page-count').textContent = pdfDoc.numPages;
                pageNum = 1;
                renderPage(pageNum);
            }).catch(function(error) {
                console.error("خطأ في تحميل PDF:", error);
                alert('ما قدرناش نحملو ملف PDF. يمكن الرابط ماشي صحيح أو الملف ماشي موجود.');
            });
        }

        // 6. دالة عرض الصفحة
        function renderPage(num) {
            pageRendering = true;
            pdfDoc.getPage(num).then(function(page) {
                const viewport = page.getViewport({ scale: scale });
                canvas.height = viewport.height;
                canvas.width = viewport.width;

                const renderContext = {
                    canvasContext: ctx,
                    viewport: viewport
                };
                const renderTask = page.render(renderContext);

                renderTask.promise.then(function() {
                    pageRendering = false;
                    if (pageNumPending !== null) {
                        renderPage(pageNumPending);
                        pageNumPending = null;
                    }
                });
            });

            document.getElementById('page-num').textContent = num;
            updateButtons();
        }

        // 7. تحديث حالة الأزرار
        function updateButtons() {
            document.getElementById('prev-page').disabled = (pageNum <= 1);
            document.getElementById('next-page').disabled = (pageNum >= pdfDoc.numPages);
        }

        // 8. دالة الانتقال للصفحة اللي بعدها
        function queueRenderPage(num) {
            if (pageRendering) {
                pageNumPending = num;
            } else {
                renderPage(num);
            }
        }

        // 9. الأزرار ديال الصفحات
        document.getElementById('prev-page').addEventListener('click', function() {
            if (pageNum <= 1) return;
            pageNum--;
            queueRenderPage(pageNum);
        });

        document.getElementById('next-page').addEventListener('click', function() {
            if (pageNum >= pdfDoc.numPages) return;
            pageNum++;
            queueRenderPage(pageNum);
        });

        // 10. الرجوع للمكتبة
        document.getElementById('back-btn').addEventListener('click', () => {
            document.getElementById('reader-screen').style.display = 'none';
            document.getElementById('home-screen').style.display = 'block';
            currentBook = null;
            pdfDoc = null;
            pageNum = 1;
        });

        // 11. البحث (فلترة بسيطة)
        document.getElementById('search-input').addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = allBooks.filter(book => 
                book.title.toLowerCase().includes(term) || 
                book.author.toLowerCase().includes(term)
            );
            displayBooks(filtered);
        });

        // 12. الوضع الليلي
        const themeToggle = document.getElementById('theme-toggle');
        const body = document.body;

        if (localStorage.getItem('theme') === 'dark') {
            body.classList.add('dark-mode');
            themeToggle.textContent = '☀️ الوضع النهاري';
        }

        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('theme', 'dark');
                themeToggle.textContent = '☀️ الوضع النهاري';
            } else {
                localStorage.setItem('theme', 'light');
                themeToggle.textContent = '🌙 الوضع الليلي';
            }
        });

        // 13. بدء التطبيق
        displayBooks(allBooks);
    </script>
</body>
</html>
"""

# عرض الموقع فـ Streamlit
components.html(html_code, height=1000, scrolling=True)
