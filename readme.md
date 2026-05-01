<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>W++ Token Analyzer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --bg-gradient: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 100%);
            --card-bg: #1e293b;
            --card-border: rgba(255, 255, 255, 0.1);
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.5);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --btn-primary: #6366f1;
            --btn-primary-hover: #818cf8;
            --shadow-color: rgba(0, 0, 0, 0.5);
            --cursor-color: #f8fafc;
        }

        [data-theme="light"] {
            --bg-color: #f1f5f9;
            --bg-gradient: radial-gradient(circle at 50% 0%, #e0e7ff 0%, #f1f5f9 100%);
            --card-bg: rgba(255, 255, 255, 0.9);
            --card-border: rgba(0, 0, 0, 0.08);
            --accent: #4f46e5;
            --accent-glow: rgba(79, 70, 229, 0.2);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --btn-primary: #4f46e5;
            --btn-primary-hover: #4338ca;
            --shadow-color: rgba(0, 0, 0, 0.05);
            --cursor-color: #0f172a;
        }

        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
            transition: background-color 0.3s, color 0.3s, border-color 0.3s; 
            cursor: none !important;
        }

        html, body {
            cursor: none !important;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-gradient);
            color: var(--text-primary);
            min-height: 100vh;
            background-attachment: fixed;
            overflow-x: hidden;
        }

        /* ─── Fix System Cursor Visibility ─── */
        a, button, .btn, .theme-switch, input, textarea, .file-zone, .hero-btn, label, .theme-pill {
            cursor: none !important;
        }

        /* ─── Scroll Progress Bar ─── */
        #top-progress {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 4px;
            background: linear-gradient(to right, #4f46e5, #ec4899, #06b6d4);
            z-index: 9999;
            transition: width 0.1s ease-out;
        }

        /* ─── Custom Cursor ─── */
        #gb-cursor {
            position: fixed;
            top: 0;
            left: 0;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 2px solid var(--cursor-color);
            background-color: transparent;
            display: grid;
            place-items: center;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 10000;
        }

        #gb-cursor-text {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: var(--cursor-color);
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        /* ─── Theme Toggle ─── */
        .theme-toggle {
            position: fixed; top: 30px; right: 30px;
            background: var(--card-bg); border: 1px solid var(--card-border);
            padding: 10px 15px; border-radius: 12px; backdrop-filter: blur(10px);
            z-index: 1000; display: flex; align-items: center; gap: 10px;
            box-shadow: 0 4px 15px var(--shadow-color);
        }
        .theme-switch { position: relative; width: 44px; height: 22px; cursor: pointer; }
        .theme-switch input { display: none; }
        .theme-slider {
            position: absolute; inset: 0; background: #475569;
            border-radius: 20px; transition: 0.3s;
        }
        .theme-slider:before {
            content: ""; position: absolute; height: 16px; width: 16px;
            left: 3px; bottom: 3px; background: white;
            border-radius: 50%; transition: 0.3s;
        }
        input:checked + .theme-slider { background: #6366f1; }
        input:checked + .theme-slider:before { transform: translateX(22px); }

        /* ─── Container ─── */
        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 90px 20px 60px;
            position: relative;
            z-index: 1;
        }

        /* ─── Hero ─── */
        .hero {
            text-align: center;
            margin-bottom: 70px;
            animation: fadeInDown 1s ease-out;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(79, 70, 229, 0.14);
            color: var(--btn-primary);
            border: 1px solid rgba(79, 70, 229, 0.3);
            padding: 7px 20px;
            border-radius: 50px;
            font-size: 0.82rem;
            font-weight: 700;
            margin-bottom: 22px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        .hero h1 {
            font-size: clamp(2.4rem, 6vw, 4.8rem);
            font-weight: 900;
            line-height: 1.08;
            background: linear-gradient(135deg, #4f46e5 0%, #ec4899 50%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 22px;
            letter-spacing: -2px;
        }

        .hero p {
            font-size: clamp(0.98rem, 2vw, 1.2rem);
            color: var(--text-secondary);
            max-width: 620px;
            margin: 0 auto 42px;
            line-height: 1.75;
        }

        .hero-btn {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: var(--btn-primary);
            color: white;
            padding: 17px 40px;
            border-radius: 50px;
            font-size: 1.08rem;
            font-weight: 700;
            text-decoration: none;
            box-shadow: 0 12px 32px rgba(79, 70, 229, 0.38);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: pulseBtn 3s ease-in-out infinite;
        }

        .hero-btn:hover {
            background: var(--btn-primary-hover);
            transform: translateY(-4px);
            box-shadow: 0 18px 40px rgba(79, 70, 229, 0.55);
        }

        @keyframes pulseBtn {
            0%, 100% { box-shadow: 0 12px 32px rgba(79, 70, 229, 0.38); }
            50%       { box-shadow: 0 12px 45px rgba(79, 70, 229, 0.65); }
        }

        /* ─── Team Section ─── */
        .section-label {
            font-size: 1.75rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 32px;
            color: var(--text-primary);
        }

        .section-label span {
            background: linear-gradient(to right, #4f46e5, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .team-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
            gap: 24px;
            margin-bottom: 60px;
        }

        .team-card {
            background: var(--card-bg);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid var(--card-border);
            border-radius: 22px;
            padding: 32px 28px;
            text-align: center;
            box-shadow: 0 10px 28px -5px var(--shadow-color);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .team-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 28px 45px -8px var(--shadow-color);
        }

        .avatar {
            width: 82px;
            height: 82px;
            border-radius: 50%;
            margin: 0 auto 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.9rem;
            font-weight: 900;
            color: white;
            letter-spacing: -1px;
        }

        .av-1 { background: linear-gradient(135deg, #4f46e5, #7c3aed); box-shadow: 0 8px 20px rgba(79,70,229,0.4); }
        .av-2 { background: linear-gradient(135deg, #ec4899, #f43f5e); box-shadow: 0 8px 20px rgba(236,72,153,0.4); }
        .av-3 { background: linear-gradient(135deg, #06b6d4, #0284c7); box-shadow: 0 8px 20px rgba(6,182,212,0.4); }

        .member-name {
            font-size: 1.12rem;
            font-weight: 800;
            color: var(--text-primary);
            margin-bottom: 8px;
        }

        .member-id {
            font-size: 0.83rem;
            color: var(--btn-primary);
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        /* ─── Supported Files ─── */
        .supported-files {
            margin-top: 60px;
            padding: 40px;
            background: var(--card-bg);
            border-radius: 24px;
            border: 1px solid var(--card-border);
            animation: fadeInUp 1s ease-out 0.5s both;
        }

        .supported-title {
            font-size: 1.4rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 30px;
            color: var(--text-primary);
        }

        .extensions-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
        }

        .ext-tag {
            padding: 8px 14px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--text-secondary);
            transition: all 0.2s;
        }

        [data-theme="light"] .ext-tag {
            background: rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(0, 0, 0, 0.2);
            color: var(--text-primary);
        }

        .ext-tag:hover {
            background: rgba(79, 70, 229, 0.15);
            color: var(--text-primary);
            border-color: var(--btn-primary);
            transform: scale(1.1);
        }

        .ext-tag.forbidden {
            color: #ef4444;
            border-color: rgba(239, 68, 68, 0.4);
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .footer {
            text-align: center;
            padding: 80px 0 60px;
            color: var(--text-secondary);
            font-size: 0.82rem;
            letter-spacing: 2px;
            font-weight: 700;
            width: 100%;
        }

        ::-webkit-scrollbar { width: 0px; }
    </style>
</head>
<body>

    <!-- Scroll Progress -->
    <div id="top-progress"></div>

    <!-- Custom Cursor -->
    <div id="gb-cursor">
        <div id="gb-cursor-text"></div>
    </div>

    <!-- Theme Toggle -->
    <div class="theme-toggle">
        <span style="font-size:0.7rem; font-weight:900; font-family:'JetBrains Mono';">THEME</span>
        <label class="theme-switch">
            <input type="checkbox" id="theme-chk" checked>
            <span class="theme-slider"></span>
        </label>
    </div>

    <div class="container">

        <!-- Hero -->
        <section class="hero">
            <div class="hero-badge">Compiler Construction &mdash; Semester 6 &mdash; Project Submission</div>
            <h1>W++ Token Analyzer</h1>
            <p>
                An advanced lexical analysis engine for the W++ programming language.
                Upload your source file and get a comprehensive statistical breakdown.
            </p>
            <a href="{{ url_for('analyzer') }}" class="hero-btn">
                <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
                Start Analyzer
            </a>
        </section>

        <!-- Team -->
        <section class="team-section">
            <div class="section-label">Group <span>Members</span></div>
            <div class="team-grid">
                <div class="team-card">
                    <div class="member-name">M Talha</div>
                    <div class="member-id">23-CS-49</div>
                </div>
                <div class="team-card">
                    <div class="member-name">Saleha Naseer</div>
                    <div class="member-id">23-CS-59</div>
                </div>
                <div class="team-card">
                    <div class="member-name">M Abubakar</div>
                    <div class="member-id">23-CS-89</div>
                </div>
            </div>
        </section>

        <!-- Supported File Types -->
        <section class="supported-files">
            <div class="supported-title">Supported File Types</div>
            <div class="extensions-grid">
                <div class="ext-tag">.wpp</div>
                <div class="ext-tag">.cpp</div>
                <div class="ext-tag">.txt</div>
                <div class="ext-tag">.docs</div>
                <div class="ext-tag">.js</div>
                <div class="ext-tag">.py</div>
                <div class="ext-tag">.java</div>
                <div class="ext-tag">.c</div>
                <div class="ext-tag">.h</div>
                <div class="ext-tag">.cs</div>
                <div class="ext-tag">.ts</div>
                <div class="ext-tag">.html</div>
                <div class="ext-tag">.css</div>
                <div class="ext-tag">.xml</div>
                <div class="ext-tag">.json</div>
                <div class="ext-tag">.php</div>
                <div class="ext-tag">.go</div>
                <div class="ext-tag">.rb</div>
                <div class="ext-tag">.rs</div>
                <div class="ext-tag">.kt</div>
                <div class="ext-tag forbidden">.pdf ✕</div>
            </div>
        </section>

        <div class="footer">&mdash; W++ Token Analyzer &copy; 2025 &mdash;</div>

    </div>

    <script>
        // Theme Logic
        const chk = document.getElementById('theme-chk');
        const root = document.documentElement;
        
        const savedTheme = localStorage.getItem('theme') || 'dark';
        root.setAttribute('data-theme', savedTheme);
        chk.checked = (savedTheme === 'dark');

        chk.addEventListener('change', () => {
            const isDark = chk.checked;
            root.setAttribute('data-theme', isDark ? 'dark' : 'light');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });

        /* ── Custom Cursor (GSAP) ── */
        const cursor = document.getElementById('gb-cursor');
        const cursorText = document.getElementById('gb-cursor-text');
        const mouse = { x: 0, y: 0 };
        const smoothMouse = { x: 0, y: 0 };
        const mouseVelocity = { x: 0, y: 0 };
        const lerp = (x, y, a) => x * (1 - a) + y * a;

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        window.addEventListener('mousedown', () => {
            gsap.to(cursorText, { scale: 2.5, duration: 0.15, ease: "power2.out" });
        });

        window.addEventListener('mouseup', () => {
            gsap.to(cursorText, { scale: 1, duration: 0.15, ease: "power2.out" });
        });

        const setter = {
            x: gsap.quickSetter(cursor, 'x', 'px'),
            y: gsap.quickSetter(cursor, 'y', 'px'),
            scaleY: gsap.quickSetter(cursor, 'scaleY'),
            scaleX: gsap.quickSetter(cursor, 'scaleX'),
            rotation: gsap.quickSetter(cursor, 'rotation', 'deg'),
            wc: gsap.quickSetter(cursor, 'willChange'),
            textRotation: gsap.quickSetter(cursorText, 'rotation', 'deg'),
        };

        gsap.ticker.add(() => {
            smoothMouse.x = lerp(smoothMouse.x, mouse.x, 0.15);
            smoothMouse.y = lerp(smoothMouse.y, mouse.y, 0.15);

            mouseVelocity.x = Math.abs(mouse.x - smoothMouse.x);
            mouseVelocity.y = Math.abs(mouse.y - smoothMouse.y);

            const angle = Math.atan2(mouse.y - smoothMouse.y, mouse.x - smoothMouse.x) * (180 / Math.PI);
            const scaleAmount = Math.min((mouseVelocity.x + mouseVelocity.y) * 0.0035, 0.5);

            setter.x(smoothMouse.x);
            setter.y(smoothMouse.y);
            setter.scaleY(1 - scaleAmount);
            setter.scaleX(1 + scaleAmount);
            setter.rotation(angle);
            setter.wc('transform');
            setter.textRotation(-angle);
        });

        /* ── Top Progress Bar ── */
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById("top-progress").style.width = scrolled + "%";
        });
    </script>
</body>
</html>












<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>W++ Token Analyzer &mdash; Analyze</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --bg-gradient: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 100%);
            --card-bg: #1e293b;
            --card-border: rgba(255, 255, 255, 0.1);
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.5);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --btn-primary: #6366f1;
            --btn-primary-hover: #818cf8;
            --btn-secondary: #475569;
            --btn-secondary-hover: #334155;
            --shadow-color: rgba(0, 0, 0, 0.5);
            --cursor-color: #f8fafc;
            --input-bg: rgba(15, 23, 42, 0.8);
            --input-border: #334155;
        }

        [data-theme="light"] {
            --bg-color: #f1f5f9;
            --bg-gradient: radial-gradient(circle at 50% 0%, #e0e7ff 0%, #f1f5f9 100%);
            --card-bg: rgba(255, 255, 255, 0.9);
            --card-border: rgba(0, 0, 0, 0.08);
            --accent: #4f46e5;
            --accent-glow: rgba(79, 70, 229, 0.2);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --btn-primary: #4f46e5;
            --btn-primary-hover: #4338ca;
            --btn-secondary: #94a3b8;
            --btn-secondary-hover: #64748b;
            --shadow-color: rgba(0, 0, 0, 0.05);
            --cursor-color: #0f172a;
            --input-bg: rgba(255, 255, 255, 0.9);
            --input-border: #cbd5e1;
        }

        * {
            box-sizing: border-box;
            cursor: none !important;
        }

        #gb-cursor, #gb-cursor-text { transition: none !important; }

        html, body {
            cursor: none !important;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-gradient);
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            margin: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            background-attachment: fixed;
            overflow-x: hidden;
        }

        /* ─── Scroll Progress Bar ─── */
        #top-progress {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 4px;
            background: linear-gradient(to right, #4f46e5, #ec4899, #06b6d4);
            z-index: 9999;
            transition: width 0.1s ease-out;
        }

        /* ─── Custom Cursor ─── */
        #gb-cursor {
            position: fixed;
            top: 0;
            left: 0;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 2px solid var(--cursor-color);
            background-color: transparent;
            display: grid;
            place-items: center;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 10000;
        }

        #gb-cursor-text {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: var(--cursor-color);
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        /* ─── Theme Toggle ─── */
        .theme-toggle {
            position: fixed; top: 20px; right: 20px;
            background: var(--card-bg); border: 1px solid var(--card-border);
            padding: 10px 15px; border-radius: 12px; backdrop-filter: blur(10px);
            z-index: 1000; display: flex; align-items: center; gap: 10px;
            box-shadow: 0 4px 15px var(--shadow-color);
        }
        .theme-switch { position: relative; width: 44px; height: 22px; cursor: pointer; }
        .theme-switch input { display: none; }
        .theme-slider {
            position: absolute; inset: 0; background: #475569;
            border-radius: 20px; transition: 0.3s;
        }
        .theme-slider:before {
            content: ""; position: absolute; height: 16px; width: 16px;
            left: 3px; bottom: 3px; background: white;
            border-radius: 50%; transition: 0.3s;
        }
        input:checked + .theme-slider { background: #6366f1; }
        input:checked + .theme-slider:before { transform: translateX(22px); }

        /* ─── Home Button ─── */
        .home-btn {
            position: fixed;
            top: 20px;
            left: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--card-bg);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            color: var(--text-primary);
            text-decoration: none;
            padding: 9px 16px;
            border-radius: 50px;
            border: 1px solid var(--card-border);
            font-size: 0.88rem;
            font-weight: 600;
            z-index: 100;
            transition: all 0.2s;
        }

        .home-btn:hover {
            background: var(--btn-primary);
            color: white;
            border-color: var(--btn-primary);
        }

        /* ─── Header ─── */
        .header {
            text-align: center;
            margin-bottom: 36px;
            margin-top: 30px;
            animation: fadeInDown 0.8s ease-out;
        }

        .header h1 {
            font-size: 2.4rem;
            font-weight: 700;
            margin: 0;
            background: linear-gradient(to right, #4f46e5, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }

        .header p {
            color: var(--text-secondary);
            font-size: 1.05rem;
            margin-top: 10px;
        }

        /* ─── Glass Panel ─── */
        .glass-panel {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 40px;
            width: 100%;
            max-width: 800px;
            box-shadow: 0 25px 50px -12px var(--shadow-color);
            animation: fadeInUp 0.8s ease-out;
        }

        h2 {
            font-size: 1.4rem;
            font-weight: 600;
            margin-top: 0;
            margin-bottom: 28px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        h2::before {
            content: '';
            display: block;
            width: 8px; height: 24px;
            background: var(--btn-primary);
            border-radius: 4px;
        }

        .form-group { margin-bottom: 25px; }

        label {
            display: block;
            font-size: 0.93rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 10px;
        }

        /* ─── Custom File Drop Zone ─── */
        .file-zone {
            position: relative;
            border: 2px dashed var(--input-border);
            border-radius: 16px;
            padding: 36px 20px;
            text-align: center;
            cursor: pointer;
            background: var(--input-bg);
            transition: all 0.3s ease;
        }

        .file-zone:hover {
            border-color: var(--btn-primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }

        .file-zone input[type="file"] {
            position: absolute;
            inset: 0;
            opacity: 0;
            cursor: pointer;
            width: 100%;
            height: 100%;
            border: none;
        }

        .file-zone .zone-icon {
            margin: 0 auto 12px;
            width: 52px; height: 52px;
            background: rgba(79, 70, 229, 0.1);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--btn-primary);
            transition: transform 0.3s;
        }

        .file-zone:hover .zone-icon { transform: scale(1.08); }

        .zone-title {
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 5px;
        }

        .zone-hint {
            font-size: 0.82rem;
            color: var(--text-secondary);
            letter-spacing: 0.5px;
        }

        /* Valid state */
        .file-zone.zone-valid {
            border-color: #22c55e;
            border-style: solid;
            background: rgba(34, 197, 94, 0.08);
            box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15);
        }

        .file-zone.zone-valid .zone-icon {
            background: rgba(34, 197, 94, 0.2);
            color: #22c55e;
        }

        /* Invalid state */
        .file-zone.zone-invalid {
            border-color: #ef4444;
            border-style: solid;
            background: rgba(239, 68, 68, 0.08);
            box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.15);
            animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
        }

        .file-zone.zone-invalid .zone-icon {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }

        .zone-filename {
            display: none;
            margin-top: 14px;
            font-size: 0.9rem;
            font-weight: 700;
            padding: 8px 16px;
            border-radius: 8px;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .zone-filename.show { display: flex; }
        .zone-filename.fname-ok  { color: #22c55e; background: rgba(34,197,94,0.1); }
        .zone-filename.fname-err { color: #ef4444; background: rgba(239,68,68,0.1); }

        /* ─── Divider ─── */
        .divider {
            display: flex;
            align-items: center;
            color: var(--text-secondary);
            margin: 28px 0;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .divider::before, .divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid var(--input-border);
        }

        .divider:not(:empty)::before { margin-right: .4em; }
        .divider:not(:empty)::after  { margin-left: .4em; }

        /* ─── Textarea ─── */
        textarea {
            width: 100%;
            height: 200px;
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 12px;
            padding: 16px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            color: var(--text-primary);
            resize: vertical;
            line-height: 1.6;
        }

        textarea:focus {
            outline: none;
            border-color: var(--btn-primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }

        /* ─── Buttons ─── */
        .btn-group {
            display: flex;
            gap: 14px;
            margin-top: 28px;
        }

        .btn {
            flex: 1;
            padding: 14px 24px;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn-primary {
            background-color: var(--btn-primary);
            color: white;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3);
        }

        .btn-primary:hover {
            background-color: var(--btn-primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4);
        }

        .btn-secondary {
            background-color: transparent;
            color: var(--text-primary);
            border: 2px solid var(--input-border);
        }

        /* ─── Fix System Cursor Visibility ─── */
        a, button, .btn, .theme-switch, input, textarea, .file-zone, label, .home-btn, .theme-switch-wrapper {
            cursor: none !important;
        }

        /* ─── Error Message ─── */
        .error-msg {
            background-color: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #ef4444;
            color: #ef4444;
            padding: 16px;
            border-radius: 8px;
            margin-top: 22px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        @keyframes shake {
            10%, 90% { transform: translate3d(-1px, 0, 0); }
            20%, 80% { transform: translate3d(2px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
            40%, 60%      { transform: translate3d(4px, 0, 0); }
        }

        ::-webkit-scrollbar { width: 0px; }
    </style>
</head>
<body>

    <!-- Scroll Progress -->
    <div id="top-progress"></div>

    <!-- Custom Cursor -->
    <div id="gb-cursor">
        <div id="gb-cursor-text"></div>
    </div>

    <!-- Home Button -->
    <a href="{{ url_for('home') }}" class="home-btn">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        Home
    </a>

    <!-- Theme Toggle -->
    <div class="theme-toggle">
        <span style="font-size:0.7rem; font-weight:900; font-family:'JetBrains Mono';">THEME</span>
        <label class="theme-switch">
            <input type="checkbox" id="theme-chk" checked>
            <span class="theme-slider"></span>
        </label>
    </div>

    <div class="header">
        <h1>W++ Token Analyzer</h1>
        <p>Analyze your source code for tokens and metrics</p>
    </div>

    <div class="glass-panel">
        <h2>Input Source Code</h2>

        <form method="POST" action="{{ url_for('analyzer') }}" enctype="multipart/form-data" id="analyzeForm">

            <div class="form-group">
                <label>Upload Source File (.txt, .wpp, .cpp)</label>

                <div class="file-zone" id="dropZone">
                    <input type="file" id="fileInput" name="wpp_file" accept=".txt,.wpp,.cpp,.c">
                    <div id="zoneBody">
                        <div class="zone-icon">
                            <svg width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                            </svg>
                        </div>
                        <div class="zone-title">Click to browse or drag &amp; drop</div>
                        <div class="zone-hint" style="margin-top: 10px; font-size: 0.8rem; opacity: 0.8;">
                            Accepted: .wpp .cpp .txt .docs .js .py .java .c .h .cs .ts and more code files  |  <span style="color: #ef4444; font-weight: 700;">✕ .pdf not allowed</span>
                        </div>
                    </div>
                    <div class="zone-filename" id="zoneFilename"></div>
                </div>
            </div>

            <div class="divider">OR</div>

            <div class="form-group">
                <label>Paste Code Directly</label>
                <textarea name="source_code" placeholder="int main() { ... }"></textarea>
            </div>

            <div class="btn-group">
                <button type="submit" class="btn btn-primary" id="analyzeBtn">Analyze Code</button>
                <button type="reset" class="btn btn-secondary" id="clearBtn">Clear</button>
            </div>

        </form>

        {% if error %}
        <div class="error-msg">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            {{ error }}
        </div>
        {% endif %}

    </div>

    <script>
        // Theme Logic
        const chk = document.getElementById('theme-chk');
        const root = document.documentElement;
        
        const currentSavedTheme = localStorage.getItem('theme') || 'dark';
        root.setAttribute('data-theme', currentSavedTheme);
        chk.checked = (currentSavedTheme === 'dark');

        chk.addEventListener('change', () => {
            const isDark = chk.checked;
            root.setAttribute('data-theme', isDark ? 'dark' : 'light');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });

        /* ── File Validation & Auto-Submit ── */
        const VALID_EXTS = ['wpp', 'txt', 'cpp', 'c'];
        const fileInput    = document.getElementById('fileInput');
        const dropZone     = document.getElementById('dropZone');
        const zoneFilename = document.getElementById('zoneFilename');
        const analyzeForm  = document.getElementById('analyzeForm');

        fileInput.addEventListener('change', function () {
            if (!this.files.length) return;
            const file = this.files[0];
            const ext  = file.name.split('.').pop().toLowerCase();
            const ok   = (ext !== 'pdf'); 

            dropZone.classList.remove('zone-valid', 'zone-invalid');
            dropZone.classList.add(ok ? 'zone-valid' : 'zone-invalid');

            zoneFilename.classList.remove('fname-ok', 'fname-err');
            zoneFilename.classList.add('show', ok ? 'fname-ok' : 'fname-err');
            zoneFilename.innerHTML = (ok ? '✓' : '✕') + ' ' + file.name + (ok ? '' : ' (Unsupported)');
        });

        document.getElementById('clearBtn').addEventListener('click', () => {
            fileInput.value = '';
            dropZone.classList.remove('zone-valid', 'zone-invalid');
            zoneFilename.classList.remove('show', 'fname-ok', 'fname-err');
            zoneFilename.innerHTML = '';
        });

        /* ── Custom Cursor (GSAP) ── */
        const cursor = document.getElementById('gb-cursor');
        const cursorText = document.getElementById('gb-cursor-text');
        const mouse = { x: 0, y: 0 };
        const smoothMouse = { x: 0, y: 0 };
        const mouseVelocity = { x: 0, y: 0 };
        const lerp = (x, y, a) => x * (1 - a) + y * a;

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        window.addEventListener('mousedown', () => {
            gsap.to(cursorText, { scale: 2.5, duration: 0.15, ease: "power2.out" });
        });

        window.addEventListener('mouseup', () => {
            gsap.to(cursorText, { scale: 1, duration: 0.15, ease: "power2.out" });
        });

        const setter = {
            x: gsap.quickSetter(cursor, 'x', 'px'),
            y: gsap.quickSetter(cursor, 'y', 'px'),
            scaleY: gsap.quickSetter(cursor, 'scaleY'),
            scaleX: gsap.quickSetter(cursor, 'scaleX'),
            rotation: gsap.quickSetter(cursor, 'rotation', 'deg'),
            wc: gsap.quickSetter(cursor, 'willChange'),
            textRotation: gsap.quickSetter(cursorText, 'rotation', 'deg'),
        };

        gsap.ticker.add(() => {
            smoothMouse.x = lerp(smoothMouse.x, mouse.x, 0.15);
            smoothMouse.y = lerp(smoothMouse.y, mouse.y, 0.15);

            mouseVelocity.x = Math.abs(mouse.x - smoothMouse.x);
            mouseVelocity.y = Math.abs(mouse.y - smoothMouse.y);

            const angle = Math.atan2(mouse.y - smoothMouse.y, mouse.x - smoothMouse.x) * (180 / Math.PI);
            const scaleAmount = Math.min((mouseVelocity.x + mouseVelocity.y) * 0.0035, 0.5);

            setter.x(smoothMouse.x);
            setter.y(smoothMouse.y);
            setter.scaleY(1 - scaleAmount);
            setter.scaleX(1 + scaleAmount);
            setter.rotation(angle);
            setter.wc('transform');
            setter.textRotation(-angle);
        });

        /* ── Top Progress Bar ── */
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
            document.getElementById("top-progress").style.width = scrolled + "%";
        });
    </script>
</body>
</html>






















<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>W++ Token Analyzer - Premium Statistical Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --bg-gradient: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 100%);
            --card-bg: #1e293b;
            --card-border: rgba(255, 255, 255, 0.1);
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.5);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --table-head: #6366f1;
            --metric-card-bg: #0f172a;
            --summary-item-bg: #0f172a;
            --cursor-color: #f8fafc;
            
            /* Category Colors */
            --kw-color: #a78bfa;
            --id-color: #60a5fa;
            --lit-color: #fb923c;
            --op-color: #4ade80;
            --sep-color: #2dd4bf;
            --cmt-color: #94a3b8;
        }

        [data-theme="light"] {
            --bg-color: #f1f5f9;
            --bg-gradient: radial-gradient(circle at 50% 0%, #e0e7ff 0%, #f1f5f9 100%);
            --card-bg: rgba(255, 255, 255, 0.9);
            --card-border: rgba(0, 0, 0, 0.08);
            --accent: #4f46e5;
            --accent-glow: rgba(79, 70, 229, 0.2);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --table-head: #4f46e5;
            --metric-card-bg: #ffffff;
            --summary-item-bg: #f8fafc;
            --cursor-color: #0f172a;

            --kw-color: #7c3aed;
            --id-color: #2563eb;
            --lit-color: #ea580c;
            --op-color: #16a34a;
            --sep-color: #0d9488;
            --cmt-color: #64748b;
        }

        * { 
            box-sizing: border-box; margin: 0; padding: 0; 
            cursor: none !important;
        }

        /* Prevent CSS transitions from fighting GSAP */
        #gb-cursor, #gb-cursor-text {
            transition: none !important;
        }

        html, body { cursor: none !important; scroll-behavior: smooth; }
        
        /* Hide main scrollbar but keep top progress */
        html {
            scrollbar-width: none;
            -ms-overflow-style: none;
        }
        html::-webkit-scrollbar { display: none; }

        /* Custom Scrollbar for internal sections */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.1); }
        ::-webkit-scrollbar-thumb { 
            background: #6366f1; 
            border-radius: 10px; 
            border: 2px solid #1e293b;
        }
        ::-webkit-scrollbar-thumb:hover { background: #818cf8; }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-gradient);
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 40px 20px;
            background-attachment: fixed;
        }

        #top-progress {
            position: fixed; top: 0; left: 0;
            width: 0%; height: 4px;
            background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
            z-index: 10000;
        }

        #gb-cursor {
            position: fixed; top: 0; left: 0;
            width: 38px; height: 38px;
            border-radius: 50%;
            border: 2px solid var(--cursor-color);
            pointer-events: none; z-index: 10001;
            display: grid; place-items: center;
            transform: translate(-50%, -50%);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
        }
        #gb-cursor-text { 
            width: 8px; height: 8px; border-radius: 50%; 
            background: var(--cursor-color); 
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
        }

        .container { max-width: 1100px; margin: 0 auto; animation: zoomIn 0.8s cubic-bezier(0.16, 1, 0.3, 1); }

        .main-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 900;
            color: var(--kw-color);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 40px;
            text-shadow: 0 0 20px rgba(167, 139, 250, 0.3);
        }

        .back-btn {
            display: inline-flex; align-items: center; gap: 8px;
            background: #6366f1; color: white;
            padding: 10px 20px; border-radius: 10px;
            text-decoration: none; font-weight: 700; font-size: 0.9rem;
            margin-bottom: 30px; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }

        /* ─── Top Info Bar ─── */
        .info-bar {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 15px 30px;
            display: flex; justify-content: space-between;
            align-items: center; margin-bottom: 40px;
            font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
        }
        .info-label { color: var(--text-secondary); text-transform: uppercase; font-weight: 700; margin-right: 8px; }
        .info-val { color: var(--accent); font-weight: 700; }
        .token-badge { background: var(--metric-card-bg); color: var(--accent); padding: 2px 10px; border-radius: 50px; font-weight: 800; border: 1px solid var(--card-border); }

        /* ─── Section Styling ─── */
        .section {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .section-header {
            display: flex; align-items: center; gap: 12px; margin-bottom: 25px;
        }
        .section-num {
            background: var(--metric-card-bg); color: var(--accent);
            width: 28px; height: 28px; border-radius: 6px;
            display: grid; place-items: center; font-weight: 900; font-size: 0.85rem;
            border: 1px solid var(--card-border);
        }
        .section-title { font-size: 1.15rem; font-weight: 800; color: var(--text-primary); }

        /* ─── Metric Cards ─── */
        .metrics-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px; margin-bottom: 30px;
        }
        .metric-card {
            background: var(--metric-card-bg); border-radius: 16px; padding: 25px;
            text-align: center; border: 1px solid var(--card-border);
        }
        .metric-val { font-size: 2.2rem; font-weight: 900; color: var(--accent); line-height: 1; }
        .metric-lbl { color: var(--text-secondary); font-size: 0.8rem; font-weight: 700; margin-top: 8px; text-transform: uppercase; }

        /* ─── Tables ─── */
        .table-container {
            border-radius: 12px; overflow: hidden; border: 1px solid var(--card-border);
        }
        table { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; }
        th {
            background: var(--table-head); color: white;
            text-align: left; padding: 14px 16px;
            font-size: 0.75rem; font-weight: 800; text-transform: uppercase;
        }
        td {
            background: var(--card-bg); padding: 12px 16px;
            border-bottom: 1px solid var(--card-border);
            font-size: 0.88rem; font-weight: 600;
        }
        tr:last-child td { border-bottom: none; }

        .kw-color { color: var(--kw-color); }
        .id-color { color: var(--id-color); }
        .lit-color { color: var(--lit-color); }
        .op-color { color: var(--op-color); }
        .sep-color { color: var(--sep-color); }
        .cmt-color { color: var(--cmt-color); font-style: italic; }

        .line-badge { background: #334155; color: var(--text-primary); padding: 2px 8px; border-radius: 50px; font-size: 0.75rem; font-weight: 800; }

        /* ─── Split Layouts ─── */
        .split-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(480px, 1fr)); gap: 30px;
        }

        /* ─── Summary Lists ─── */
        .summary-list { display: flex; flex-direction: column; gap: 15px; }
        .summary-item {
            display: flex; justify-content: space-between; align-items: center;
            padding: 12px 20px; background: var(--summary-item-bg); border-radius: 12px;
            border: 1px solid var(--card-border);
        }
        .summary-lbl { font-size: 0.9rem; font-weight: 700; color: var(--text-primary); }
        .summary-val { background: var(--card-bg); color: var(--accent); padding: 4px 12px; border-radius: 8px; font-weight: 800; font-size: 0.85rem; border: 1px solid var(--card-border); }

        /* ─── Progress Bars ─── */
        .progress-row { display: flex; align-items: center; gap: 15px; }
        .bar-wrap { flex: 1; height: 8px; background: var(--metric-card-bg); border-radius: 4px; overflow: hidden; border: 1px solid var(--card-border); }
        .bar-fill { height: 100%; background: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }

        .footer {
            text-align: center; margin-top: 60px; padding-bottom: 40px;
            color: var(--text-secondary); font-weight: 800; font-size: 0.9rem; letter-spacing: 2px;
        }

        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
</head>
<body>

    <div id="top-progress"></div>
    <div id="gb-cursor"><div id="gb-cursor-text"></div></div>

    <style>
        .theme-toggle {
            position: fixed; top: 30px; right: 30px;
            background: var(--card-bg); border: 1px solid var(--card-border);
            padding: 10px 15px; border-radius: 12px; backdrop-filter: blur(10px);
            z-index: 1000; display: flex; align-items: center; gap: 10px;
            box-shadow: 0 4px 15px var(--shadow-color);
        }
        .theme-switch { position: relative; width: 44px; height: 22px; cursor: pointer; }
        .theme-switch input { display: none; }
        .theme-slider {
            position: absolute; inset: 0; background: #475569;
            border-radius: 20px; transition: 0.3s;
        }
        .theme-slider:before {
            content: ""; position: absolute; height: 16px; width: 16px;
            left: 3px; bottom: 3px; background: white;
            border-radius: 50%; transition: 0.3s;
        }
        input:checked + .theme-slider { background: #6366f1; }
        input:checked + .theme-slider:before { transform: translateX(22px); }
    </style>

    <div class="theme-toggle">
        <span style="font-size:0.7rem; font-weight:900; font-family:'JetBrains Mono';">THEME</span>
        <label class="theme-switch">
            <input type="checkbox" id="theme-chk" checked>
            <span class="theme-slider"></span>
        </label>
    </div>

    <div class="container">
        
        <h1 class="main-title">Statistical Report</h1>

        <a href="{{ url_for('analyzer') }}" class="back-btn">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Analyze Another File
        </a>

        <!-- TOP BAR -->
        <div class="info-bar">
            <div><span class="info-label">FILE NAME</span> <span class="info-val">{{ filename }}</span></div>
            <div><span class="info-label">TOTAL LINES</span> <span class="info-val">{{ e_data.total_lines }}</span></div>
            <div><span class="info-label">CODE LINES</span> <span class="info-val">{{ e_data.code_lines }}</span></div>
            <div><span class="info-label">TOTAL TOKENS</span> <span class="token-badge">{{ e_data.total_tokens }}</span></div>
        </div>

        <!-- CODE METRICS -->
        <div class="section">
            <div class="section-header">
                <div class="section-num">0</div>
                <h2 class="section-title">Code Metrics Overview</h2>
            </div>
            <div class="metrics-grid">
                <div class="metric-card"><div class="metric-val">{{ e_data.total_tokens }}</div><div class="metric-lbl">Total Tokens</div></div>
                <div class="metric-card"><div class="metric-val">{{ e_data.unique_types }}</div><div class="metric-lbl">Unique Types</div></div>
                <div class="metric-card"><div class="metric-val">{{ e_data.empty_lines }}</div><div class="metric-lbl">Empty Lines</div></div>
                <div class="metric-card"><div class="metric-val">{{ e_data.avg_tokens }}</div><div class="metric-lbl">Avg Tokens/Line</div></div>
                <div class="metric-card"><div class="metric-val">{{ e_data.max_line_count }}</div><div class="metric-lbl">Max Tokens (Line {{ e_data.max_line_nos }})</div></div>
            </div>
        </div>

        <!-- 1. TOKEN TYPE SUMMARY -->
        <div class="section">
            <div class="section-header">
                <div class="section-num">1</div>
                <h2 class="section-title">Token Type Summary Table</h2>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>TOKEN CATEGORY</th>
                            <th>TOKEN TYPE</th>
                            <th style="text-align:center">QUANTITY</th>
                            <th style="text-align:center">PERCENTAGE</th>
                            <th>LINE NUMBERS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% set cats = [('KEYWORD', kw_data, 'kw'), ('IDENTIFIER', id_data, 'id'), ('LITERAL', lit_data, 'lit'), ('OPERATOR', op_data, 'op'), ('SEPARATOR', sep_data, 'sep'), ('COMMENT', cmt_data, 'cmt')] %}
                        {% for cat_name, data_list, cls in cats %}
                            {% for row in data_list %}
                            <tr>
                                <td class="{{cls}}-color"><b>{{ cat_name }}</b></td>
                                <td class="{{cls}}-color">{{ row.type }}</td>
                                <td style="text-align:center"><b>{{ row.count }}</b></td>
                                <td style="text-align:center">{{ ((row.count / e_data.total_tokens) * 100) | round(2) }}%</td>
                                <td style="color:var(--text-secondary); font-size:0.75rem;">{{ row.lines }}</td>
                            </tr>
                            {% endfor %}
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 2. LINE-WISE DISTRIBUTION -->
        <div class="section">
            <div class="section-header">
                <div class="section-num">2</div>
                <h2 class="section-title">Line-wise Token Distribution</h2>
            </div>
            <div class="table-container" style="max-height: 450px; overflow-y: auto;">
                <table>
                    <thead style="position: sticky; top:0; z-index:10;">
                        <tr>
                            <th style="width:120px">LINE NUMBER</th>
                            <th style="width:120px; text-align:center">TOTAL TOKENS</th>
                            <th>CODE SNIPPET</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in b_data %}
                        <tr style="{% if row.is_empty %}opacity:0.3;{% endif %}">
                            <td><b>{{ row.line_no }}</b></td>
                            <td style="text-align:center"><span class="line-badge">{{ row.count }}</span></td>
                            <td><code style="font-family:'JetBrains Mono'; font-size:0.8rem; background:rgba(0,0,0,0.1); padding:2px 8px; border-radius:4px;">{{ row.content if row.content else ' ' }}</code></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="split-grid">
            <!-- 3. IDENTIFIER STATISTICS -->
            <div class="section">
                <div class="section-header">
                    <div class="section-num">3</div>
                    <h2 class="section-title">Identifier Statistics</h2>
                </div>
                <div class="table-container">
                    <table>
                        <thead><tr><th>IDENTIFIER NAME</th><th style="text-align:center">FREQUENCY</th><th>LINES</th></tr></thead>
                        <tbody>
                            {% for row in c_data %}
                            <tr><td class="id-color"><b>{{ row.name }}</b></td><td style="text-align:center"><b>{{ row.count }}</b></td><td style="font-size:0.75rem;">{{ row.lines }}</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 4. LITERAL STATISTICS -->
            <div class="section">
                <div class="section-header">
                    <div class="section-num">4</div>
                    <h2 class="section-title">Literal Statistics</h2>
                </div>
                <div class="table-container">
                    <table>
                        <thead><tr><th>LITERAL VALUE</th><th>TYPE</th><th style="text-align:center">FREQUENCY</th><th>LINES</th></tr></thead>
                        <tbody>
                            {% for row in d_data %}
                            <tr><td class="lit-color"><b>{{ row.value }}</b></td><td>{{ row.short_type }}</td><td style="text-align:center"><b>{{ row.count }}</b></td><td style="font-size:0.75rem;">{{ row.lines }}</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="split-grid">
            <!-- 5. OVERALL SUMMARY -->
            <div class="section">
                <div class="section-header">
                    <div class="section-num">5</div>
                    <h2 class="section-title">Overall Summary</h2>
                </div>
                <div class="summary-list">
                    <div class="summary-item"><span class="summary-lbl">Total Number of Tokens</span> <span class="summary-val">{{ e_data.total_tokens }}</span></div>
                    <div class="summary-item"><span class="summary-lbl">Total Unique Token Types</span> <span class="summary-val">{{ e_data.unique_types }}</span></div>
                    <div class="summary-item"><span class="summary-lbl">Total Lines with Code</span> <span class="summary-val">{{ e_data.code_lines }}</span></div>
                    <div class="summary-item"><span class="summary-lbl">Most Frequent Token Type</span> <span><b class="id-color">{{ e_data.most_freq }}</b> <span class="summary-val" style="margin-left:10px;">{{ e_data.most_freq_count }} times</span></span></div>
                    <div class="summary-item"><span class="summary-lbl">Least Frequent Token Type</span> <span><b class="id-color">{{ e_data.least_freq }}</b> <span class="summary-val" style="margin-left:10px;">{{ e_data.least_freq_count }} times</span></span></div>
                    <div class="summary-item"><span class="summary-lbl">Average Tokens per Line</span> <span class="summary-val">{{ e_data.avg_tokens }}</span></div>
                </div>
            </div>

            <!-- 6. CATEGORY BREAKDOWN -->
            <div class="section">
                <div class="section-header">
                    <div class="section-num">6</div>
                    <h2 class="section-title">Category Breakdown</h2>
                </div>
                <div class="table-container">
                    <table style="border:none;">
                        <thead><tr><th>CATEGORY</th><th style="text-align:center">TOTAL</th><th style="text-align:right">PERCENTAGE</th></tr></thead>
                        <tbody>
                            {% for b in e_data.breakdown %}
                            <tr>
                                <td><b>{{ b.category }}</b></td>
                                <td style="text-align:center"><b>{{ b.count }}</b></td>
                                <td>
                                    <div class="progress-row">
                                        <div class="bar-wrap"><div class="bar-fill" style="width:{{ b.percent }};"></div></div>
                                        <span style="min-width:60px; text-align:right;"><b>{{ b.percent }}</b></span>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="footer">— END OF REPORT —</div>

    </div>

    <script>
        // Theme Logic
        const chk = document.getElementById('theme-chk');
        const root = document.documentElement;
        
        const savedTheme = localStorage.getItem('theme') || 'dark';
        root.setAttribute('data-theme', savedTheme);
        chk.checked = (savedTheme === 'dark');

        chk.addEventListener('change', () => {
            const isDark = chk.checked;
            root.setAttribute('data-theme', isDark ? 'dark' : 'light');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });

        /* ── Custom Cursor (GSAP) ── */
        const cursor = document.getElementById('gb-cursor');
        const cursorText = document.getElementById('gb-cursor-text');
        const mouse = { x: 0, y: 0 };
        const smoothMouse = { x: 0, y: 0 };
        const mouseVelocity = { x: 0, y: 0 };
        const lerp = (x, y, a) => x * (1 - a) + y * a;

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        window.addEventListener('mousedown', () => {
            gsap.to(cursorText, { scale: 2.5, duration: 0.15, ease: "power2.out" });
        });

        window.addEventListener('mouseup', () => {
            gsap.to(cursorText, { scale: 1, duration: 0.15, ease: "power2.out" });
        });

        const setter = {
            x: gsap.quickSetter(cursor, 'x', 'px'),
            y: gsap.quickSetter(cursor, 'y', 'px'),
            scaleY: gsap.quickSetter(cursor, 'scaleY'),
            scaleX: gsap.quickSetter(cursor, 'scaleX'),
            rotation: gsap.quickSetter(cursor, 'rotation', 'deg'),
            wc: gsap.quickSetter(cursor, 'willChange'),
            textRotation: gsap.quickSetter(cursorText, 'rotation', 'deg'),
        };

        gsap.ticker.add(() => {
            smoothMouse.x = lerp(smoothMouse.x, mouse.x, 0.15);
            smoothMouse.y = lerp(smoothMouse.y, mouse.y, 0.15);

            mouseVelocity.x = Math.abs(mouse.x - smoothMouse.x);
            mouseVelocity.y = Math.abs(mouse.y - smoothMouse.y);

            const angle = Math.atan2(mouse.y - smoothMouse.y, mouse.x - smoothMouse.x) * (180 / Math.PI);
            const scaleAmount = Math.min((mouseVelocity.x + mouseVelocity.y) * 0.0035, 0.5);

            setter.x(smoothMouse.x);
            setter.y(smoothMouse.y);
            setter.scaleY(1 - scaleAmount);
            setter.scaleX(1 + scaleAmount);
            setter.rotation(angle);
            setter.wc('transform');
            setter.textRotation(-angle);
        });

        // Progress Bar
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
            document.getElementById("top-progress").style.width = scrolled + "%";
        });
    </script>
</body>
</html>



















from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
import re
import os

_BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(_BASE, 'templates'))

keywords_list = {
    'int'    : 'KEYWORD_INT',
    'float'  : 'KEYWORD_FLOAT',
    'double' : 'KEYWORD_DOUBLE',
    'char'   : 'KEYWORD_CHAR',
    'string' : 'KEYWORD_STRING',
    'bool'   : 'KEYWORD_BOOL',
    'if'     : 'KEYWORD_IF',
    'else'   : 'KEYWORD_ELSE',
    'while'  : 'KEYWORD_WHILE',
    'for'    : 'KEYWORD_FOR',
    'return' : 'KEYWORD_RETURN',
    'print'  : 'KEYWORD_PRINT',
    'read'   : 'KEYWORD_READ',
    'true'   : 'KEYWORD_TRUE',
    'false'  : 'KEYWORD_FALSE',
}
two_char_ops = {
    '==': 'EQUAL TO',
    '!=': 'NOT EQUAL',
    '<=': 'LESS THAN OR EQUAL TO',
    '>=': 'GREATER THAN OR EQUAL TO',
    '&&': 'LOGICAL AND',
    '||': 'LOGICAL OR'
}

one_char_ops = {
    '=': 'ASSIGNMENT OPERATOR (=)',
    '+': 'ADDITION',
    '-': 'SUBTRACTION',
    '*': 'MULTIPLICATION',
    '/': 'DIVISION',
    '%': 'MODULUS',
    '<': 'RELATIONAL OPERATOR (LESS THAN)',
    '>': 'RELATIONAL OPERATOR (GREATER THAN)',
    '!': 'LOGICAL OPERATOR (NOT)'
}

separators_list = {
    '(': 'LPAREN',
    ')': 'RPAREN',
    '{': 'LBRACE',
    '}': 'RBRACE',
    ';': 'SEMICOLON',
    ',': 'COMMA'
}

TOKEN_PATTERN = re.compile(
    r'(?P<COMMENT_ML>  /\*[\s\S]*?\*/          )|'
    r'(?P<COMMENT_SL>  //[^\n]*                )|'
    r'(?P<STRING>      "(?:\\.|[^"\\])*"        )|'
    r'(?P<CHAR>        \'(?:\\.|[^\\\'])?\'     )|'
    r'(?P<FLOAT>       \d+\.\d+                 )|'
    r'(?P<INTEGER>     \d+                      )|'
    r'(?P<OP2>         ==|!=|<=|>=|&&|\|\|      )|'
    r'(?P<OP1>         [=+\-*/%<>!]             )|'
    r'(?P<SEPARATOR>   [;,(){}\[\]]             )|'
    r'(?P<IDENTIFIER>  [a-zA-Z_]\w*             )|'
    r'(?P<SKIP>        [ \t\r\n]+               )|'
    r'(?P<UNKNOWN>     .                         )',
    re.VERBOSE
)


def tokenize(source_code):
    token_list = []
    line_num = 1
    for match in TOKEN_PATTERN.finditer(source_code):

        token_type  = match.lastgroup
        token_value = match.group()

        if token_type == 'SKIP':
            line_num += token_value.count('\n')
            continue

        if token_type == 'UNKNOWN':
            continue

        if token_type == 'COMMENT_SL':
            token_list.append({
                'category': 'COMMENT',
                'type':     'COMMENT_SINGLELINE',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'COMMENT_ML':
            token_list.append({
                'category': 'COMMENT',
                'type':     'COMMENT_MULTILINE',
                'value':    '/* multi-line comment */',
                'line':     line_num
            })
            line_num += token_value.count('\n')
            continue

        if token_type == 'STRING':
            token_list.append({
                'category': 'LITERAL',
                'type':     'LITERAL_STRING',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'CHAR':
            token_list.append({
                'category': 'LITERAL',
                'type':     'LITERAL_CHAR',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'FLOAT':
            token_list.append({
                'category': 'LITERAL',
                'type':     'LITERAL_FLOAT',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'INTEGER':
            token_list.append({
                'category': 'LITERAL',
                'type':     'LITERAL_INTEGER',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'OP2':
            token_list.append({
                'category': 'OPERATOR',
                'type': two_char_ops.get(token_value, 'OPERATOR_UNKNOWN'),
                'value': token_value,
                'line':  line_num
            })
            continue

        if token_type == 'OP1':
            token_list.append({
                'category': 'OPERATOR',
                'type': one_char_ops.get(token_value, 'OPERATOR_UNKNOWN'),
                'value': token_value,
                'line':  line_num
            })
            continue

        if token_type == 'SEPARATOR':
            token_list.append({
                'category': 'SEPARATOR',
                'type': separators_list.get(token_value, 'SEPARATOR_UNKNOWN'),
                'value': token_value,
                'line':  line_num
            })
            continue

        if token_type == 'IDENTIFIER':
            if token_value in keywords_list:
                token_list.append({
                    'category': 'KEYWORD',
                    'type':     'KEYWORD_' + token_value.upper(),
                    'value':    token_value,
                    'line':     line_num
                })
            else:
                token_list.append({
                    'category': 'IDENTIFIER',
                    'type':     'IDENTIFIER',
                    'value':    token_value,
                    'line':     line_num
                })
            continue

    return token_list


def get_type_summary_data(all_tokens, category_name):
    type_data = {}
    for tok in all_tokens:
        if tok['category'] != category_name:
            continue
        t_type = tok['type']
        if t_type not in type_data:
            type_data[t_type] = {'type': t_type, 'count': 0, 'lines': set()}
        type_data[t_type]['count'] += 1
        type_data[t_type]['lines'].add(tok['line'])
    result = []
    for data in type_data.values():
        data['lines'] = ', '.join(str(l) for l in sorted(data['lines']))
        result.append(data)
    return sorted(result, key=lambda x: x['type'])


def get_category_data(all_tokens, category_name):
    token_summary = {}
    total_in_cat = 0
    for tok in all_tokens:
        if tok['category'] != category_name:
            continue
        total_in_cat += 1
        t_type = tok['type']
        t_val = tok['value']
        t_line = tok['line']
        
        # Unique key for type and value
        key = (t_type, t_val)
        if key not in token_summary:
            token_summary[key] = {
                'type': t_type,
                'value': t_val,
                'count': 0,
                'lines': set()
            }
        token_summary[key]['count'] += 1
        token_summary[key]['lines'].add(t_line)
        
    result = []
    for key, data in token_summary.items():
        data['lines'] = ', '.join(str(l) for l in sorted(data['lines']))
        result.append(data)
    
    return sorted(result, key=lambda x: -x['count'])


def get_part_b(all_tokens, source_lines):
    line_count = defaultdict(int)
    for tok in all_tokens:
        line_count[tok['line']] += 1

    result = []
    for ln, raw in enumerate(source_lines, 1):
        result.append({
            'line_no':  ln,
            'content':  raw.strip(),
            'count':    line_count.get(ln, 0),
            'is_empty': raw.strip() == ''
        })
    return result


def get_part_c(all_tokens):
    data = {}
    for tok in all_tokens:
        if tok['category'] != 'IDENTIFIER':
            continue
        name = tok['value']
        if name not in data:
            data[name] = {'name': name, 'count': 0, 'lines': set()}
        data[name]['count'] += 1
        data[name]['lines'].add(tok['line'])

    result = sorted(data.values(), key=lambda x: -x['count'])
    for r in result:
        r['lines'] = ', '.join(str(l) for l in sorted(r['lines']))
    return result


def get_part_d(all_tokens):

    data = {}

    for tok in all_tokens:

        if tok['category'] != 'LITERAL':
            continue

        key = (tok['value'], tok['type'])

        if key not in data:
            data[key] = {
                'value'    : tok['value'],
                'type'     : tok['type'],
                'count'    : 0,
                'line_list': []
            }

        data[key]['count'] += 1

        if tok['line'] not in data[key]['line_list']:
            data[key]['line_list'].append(tok['line'])

    type_order = {
        'LITERAL_INTEGER': 1,
        'LITERAL_FLOAT'  : 2,
        'LITERAL_CHAR'   : 3,
        'LITERAL_STRING' : 4
    }

    def sort_literals(x):
        order_number = type_order.get(x['type'], 9)
        return (order_number, -x['count'])

    result = list(data.values())
    result.sort(key=sort_literals)

    for r in result:
        r['line_list'].sort()
        r['lines']      = ', '.join(str(l) for l in r['line_list'])
        r['short_type'] = r['type'].replace('LITERAL_', '')

    return result


def get_part_e(all_tokens, source_lines):
    non_cmt     = [t for t in all_tokens if t['category'] != 'COMMENT']
    total       = len(non_cmt)
    code_lines  = [l for l in source_lines if l.strip()]
    empty_lines = len(source_lines) - len(code_lines)

    unique_types = len(set(t['type'] for t in non_cmt))

    type_count = defaultdict(int)
    for t in non_cmt:
        type_count[t['type']] += 1

    most_freq  = max(type_count, key=type_count.get) if type_count else '-'
    least_freq = min(type_count, key=type_count.get) if type_count else '-'
    avg_tokens = round(total / len(code_lines), 2) if code_lines else 0

    line_tok = defaultdict(int)
    for t in non_cmt:
        line_tok[t['line']] += 1

    max_count = max(line_tok.values()) if line_tok else 0
    min_count = min(line_tok.values()) if line_tok else 0
    max_lines = sorted([ln for ln, c in line_tok.items() if c == max_count])
    min_lines = sorted([ln for ln, c in line_tok.items() if c == min_count])

    cat_count = defaultdict(int)
    for t in non_cmt:
        cat_count[t['category']] += 1

    breakdown = []
    for cat in ['KEYWORD', 'IDENTIFIER', 'LITERAL', 'OPERATOR', 'SEPARATOR', 'COMMENT']:
        cnt = cat_count.get(cat, 0)
        pct = round(cnt / total * 100, 2) if total > 0 else 0
        breakdown.append({
            'category': cat,
            'count':    cnt,
            'percent':  str(pct) + '%',
            'pct_val':  pct
        })

    mf_pct = str(round(type_count.get(most_freq, 0) / total * 100, 2)) + '%' if total else '0%'
    lf_pct = str(round(type_count.get(least_freq, 0) / total * 100, 2)) + '%' if total else '0%'

    return {
        'total_tokens':     total,
        'unique_types':     unique_types,
        'total_lines':      len(source_lines),
        'code_lines':       len(code_lines),
        'empty_lines':      empty_lines,
        'most_freq':        most_freq,
        'most_freq_count':  type_count.get(most_freq, 0),
        'most_freq_pct':    mf_pct,
        'least_freq':       least_freq,
        'least_freq_count': type_count.get(least_freq, 0),
        'least_freq_pct':   lf_pct,
        'avg_tokens':       avg_tokens,
        'max_line_count':   max_count,
        'max_line_nos':     ', '.join(str(l) for l in max_lines),
        'min_line_count':   min_count,
        'min_line_nos':     ', '.join(str(l) for l in min_lines),
        'breakdown':        breakdown,
    }


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/analyzer', methods=['GET', 'POST'])
def analyzer():
    if request.method == 'GET':
        error = request.args.get('error')
        return render_template('index.html', error=error)

    source   = ''
    filename = '(pasted code)'

    if 'wpp_file' in request.files and request.files['wpp_file'].filename != '':
        uploaded = request.files['wpp_file']
        try:
            source   = uploaded.read().decode('utf-8')
            filename = uploaded.filename
        except UnicodeDecodeError:
            return redirect(url_for('analyzer', error='Error: Please upload a valid text/code file. This file contains invalid characters (like a PDF or Word document).'))

    else:
        source = request.form.get('source_code', '')

    if source.strip() == '':
        return redirect(url_for('analyzer', error='No code found.'))

    all_tokens   = tokenize(source)
    source_lines = source.split('\n')
    non_cmt      = [t for t in all_tokens if t['category'] != 'COMMENT']
    total_toks   = len(non_cmt)

    return render_template('result.html',
        filename = filename,
        b_data   = get_part_b(all_tokens, source_lines),
        c_data   = get_part_c(all_tokens),
        d_data   = get_part_d(all_tokens),
        e_data   = get_part_e(all_tokens, source_lines),
        kw_data  = get_type_summary_data(all_tokens, 'KEYWORD'),
        id_data  = get_type_summary_data(all_tokens, 'IDENTIFIER'),
        lit_data = get_type_summary_data(all_tokens, 'LITERAL'),
        op_data  = get_type_summary_data(all_tokens, 'OPERATOR'),
        sep_data = get_type_summary_data(all_tokens, 'SEPARATOR'),
        cmt_data = get_type_summary_data(all_tokens, 'COMMENT'),
    )


if __name__ == '__main__':
    print("Server is working...")
    print("open in browser: http://localhost:5000")
    app.run(debug=True)#   C o m p i l e r - C o s t r u c t i o n - P r o j e c t  
 #   C C - P r o j e c t  
 