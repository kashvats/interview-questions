import json
import os
import html
from datetime import datetime

def generate_html():
    docc_dir = 'c:/Users/human-bot/projects/docc'
    output_file = os.path.join(docc_dir, 'index.html')
    
    all_questions = []
    domains_set = set()

    # Read all JSON files
    for filename in sorted(os.listdir(docc_dir)):
        if filename.endswith('.json'):
            domain_name = filename.replace('.json', '').replace('_', ' ').title()
            filepath = os.path.join(docc_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            item['domain'] = domain_name
                            domains_set.add(domain_name)
                        all_questions.extend(data)
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # Define difficulty ranking for sorting
    diff_rank = {'easy': 0, 'medium': 1, 'hard': 2}
    
    # Sort: Domain -> Difficulty (Beginner to Advanced) -> ID
    all_questions.sort(key=lambda x: (
        x.get('domain', ''), 
        diff_rank.get(x.get('difficulty', 'medium').lower(), 1),
        x.get('id', 0)
    ))
    sorted_domains = sorted(list(domains_set))

    # Helper to escape HTML and clean strings for data-attributes if needed
    def safe_html(text):
        if not text: return ""
        return html.escape(str(text))

    # Define Groups
    groups = {
        "Core Engineering": ["Python", "Web Frameworks", "Dsa"],
        "Architecture & Systems": ["System Architecture", "Async Systems", "Api Design", "Microservices Architecture"],
        "Infrastructure & Security": ["Devops Infra", "Security Mastery", "Reliability Engineering"],
        "Data & AI": ["Databases", "Data Engineering", "Ai Mlops"],
        "Frontend & UI": ["Frontend Mastery"],
        "Soft Skills & Expert Scenarios": ["Scenarios", "Soft Skills Industry"]
    }

    all_categorized_domains = []
    for g in groups.values():
        all_categorized_domains.extend(g)
    
    # Add any remaining domains that didn't fit in a group
    remaining = [d for d in sorted_domains if d not in all_categorized_domains]
    if remaining:
        groups["Other"] = remaining

    sidebar_html = f'''
        <li class="domain-item active" data-domain="all" onclick="selectDomain(\'all\')">
            <span class="domain-icon">🏠</span> All Domains ({len(all_questions)})
        </li>
    '''
    for group_name, items in groups.items():
        # Check if any item from this group exists in our sorted_domains
        group_exists = any(item in sorted_domains for item in items)
        if group_exists:
            sidebar_html += f'<div class="sidebar-category">{group_name}</div>'
            for item in items:
                if item in sorted_domains:
                    sidebar_html += f'<li class="domain-item" data-domain="{item}" onclick="selectDomain(\'{item}\')">{item}</li>'

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical Interview Registry | Mastery</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Libraries for Rich Content -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>

    <style>
        :root {{
            --bg-deep: #0a0c10;
            --bg-surface: #161b22;
            --bg-card: #1c2128;
            --accent-primary: #58a6ff;
            --accent-secondary: #7ee787;
            --text-main: #adbac7;
            --text-bright: #cdd9e5;
            --text-dim: #768390;
            --border: #30363d;
            --difficulty-easy: #238636;
            --difficulty-medium: #d29922;
            --difficulty-hard: #f85149;
            --difficulty-hard: #f85149;
            --glass: rgba(22, 27, 34, 0.8);
            --mastered: #238636;
            --analogy-bg: rgba(126, 231, 135, 0.05);
            --analogy-border: rgba(126, 231, 135, 0.2);
            --code-bg: #0d1117;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            scrollbar-width: thin;
            scrollbar-color: var(--border) transparent;
        }}

        body {{
            background-color: var(--bg-deep);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
        }}

        header {{
            position: sticky;
            top: 0;
            z-index: 1000;
            background: var(--glass);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 2rem;
        }}

        .logo {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--text-bright);
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .logo span {{ color: var(--accent-primary); }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }}

        .search-container {{
            position: relative;
            width: 400px;
        }}

        #searchBar {{
            width: 100%;
            background: var(--bg-deep);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.6rem 1rem;
            color: var(--text-bright);
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}

        #searchBar:focus {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
        }}

        .layout {{
            display: grid;
            grid-template-columns: 300px 1fr;
            min-height: calc(100vh - 70px);
            transition: all 0.3s ease;
        }}

        aside {{
            padding: 1.5rem;
            border-right: 1px solid var(--border);
            background: var(--bg-surface);
            height: calc(100vh - 70px);
            position: sticky;
            top: 70px;
            overflow-y: auto;
            z-index: 900;
        }}

        .sidebar-category {{
            font-size: 0.7rem;
            font-weight: 800;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin: 1.5rem 0 0.5rem 0.8rem;
        }}

        .domain-list {{ list-style: none; }}

        .domain-item {{
            padding: 0.6rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            color: var(--text-main);
            transition: all 0.2s;
            margin-bottom: 0.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .domain-item:hover, .domain-item.active {{
            background: var(--bg-card);
            color: var(--accent-primary);
        }}

        main {{
            padding: clamp(1rem, 5vw, 3rem);
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }}

        .registry-info {{
            margin-bottom: 3rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--border);
        }}

        .registry-info h1 {{
            font-family: 'Outfit', sans-serif;
            color: var(--text-bright);
            font-size: clamp(1.8rem, 4vw, 2.8rem);
            margin-bottom: 0.5rem;
            letter-spacing: -1px;
        }}

        .question-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: clamp(1.2rem, 3vw, 2.5rem);
            margin-bottom: 2.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            position: relative;
            transition: transform 0.2s, box-shadow 0.2s;
            overflow-wrap: break-word;
            word-wrap: break-word;
        }}

        .question-card:hover {{
            border-color: var(--accent-primary);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}

        .question-card.mastered {{
            border-color: var(--mastered);
            background: rgba(35, 134, 54, 0.05);
        }}

        .mastery-checkbox {{
            position: absolute;
            top: 1.5rem;
            right: 1.5rem;
            width: 28px;
            height: 28px;
            cursor: pointer;
            accent-color: var(--mastered);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
        }}

        .domain-tag {{
            background: rgba(88, 166, 255, 0.1);
            color: var(--accent-primary);
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .difficulty-badge {{
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }}

        .easy {{ color: var(--difficulty-easy); border: 1px solid var(--difficulty-easy); }}
        .medium {{ color: var(--difficulty-medium); border: 1px solid var(--difficulty-medium); }}
        .hard {{ color: var(--difficulty-hard); border: 1px solid var(--difficulty-hard); }}

        .question-text {{
            font-size: clamp(1.1rem, 2.5vw, 1.5rem);
            font-weight: 700;
            color: var(--text-bright);
            line-height: 1.4;
            font-family: 'Outfit', sans-serif;
            cursor: pointer;
        }}

        .test-mode .answer-section, 
        .test-mode .counter-section {{
            filter: blur(10px);
            opacity: 0.3;
            transition: filter 0.3s, opacity 0.3s;
            cursor: pointer;
            user-select: none;
        }}

        .test-mode .answer-section.revealed, 
        .test-mode .counter-section.revealed {{
            filter: blur(0);
            opacity: 1;
            user-select: text;
        }}

        .mode-toggle {{
            display: flex;
            background: var(--bg-deep);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2px;
            cursor: pointer;
        }}

        .mode-btn {{
            padding: 0.4rem 1rem;
            border-radius: 18px;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.2s;
        }}

        .mode-btn.active {{
            background: var(--accent-primary);
            color: var(--bg-deep);
        }}

        .btn-action {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-bright);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .btn-action:hover {{
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }}

        /* Framework Tabs */
        .code-tabs {{
            margin-top: 1rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            background: var(--code-bg);
        }}

        .tab-headers {{
            display: flex;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border);
            padding: 0 0.5rem;
        }}

        .tab-header {{
            padding: 0.6rem 1.2rem;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-dim);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .tab-header:hover {{
            color: var(--text-bright);
        }}

        .tab-header.active {{
            color: var(--accent-primary);
            border-bottom-color: var(--accent-primary);
        }}

        .tab-content {{
            display: none;
            padding: 0;
        }}

        .tab-content.active {{
            display: block;
        }}

        .tab-content pre {{
            margin: 0 !important;
            border-radius: 0 !important;
            border: none !important;
        }}

        .mode-toggle {{
            background: var(--bg-surface);
            border: 1px solid var(--border);
            color: var(--text-bright);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s;
        }}

        .mode-toggle:hover {{
            border-color: var(--accent-primary);
            background: var(--bg-card);
        }}

        .mode-toggle.active {{
            background: var(--accent-primary);
            color: var(--bg-deep);
            border-color: var(--accent-primary);
        }}

        footer {{
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-dim);
            font-size: 0.9rem;
            border-top: 1px solid var(--border);
            margin-top: 4rem;
        }}

        /* Responsive Mobile */
        @media (max-width: 900px) {{
            .layout {{ grid-template-columns: 1fr; }}
            aside {{ display: none; }}
            .search-container {{ width: 100%; }}
            header {{ padding: 1rem; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="logo">TECHNICAL<span>REGISTRY</span></div>
        <div class="header-actions">
            <div class="search-container">
                <input type="text" id="searchBar" placeholder="Search questions, topics, or tags..." onkeyup="filterQuestions()">
            </div>
            <button class="mode-toggle" id="testModeBtn" onclick="toggleTestMode()">
                <span>🎯</span> Test Mode
            </button>
        </div>
    </header>

    <div class="layout">
        <aside>
            <ul class="domain-list">
                {sidebar_html}
            </ul>
        </aside>

        <main>
            <div class="registry-info">
                <h1 id="domainTitle">All Domains</h1>
                <p id="domainStats">{len(all_questions)} Master Questions across {len(sorted_domains)} Technical Domains</p>
            </div>

            <div id="questionContainer">
                <!-- Questions will be injected here via JavaScript -->
            </div>
        </main>
    </div>

    <footer>
        &copy; {datetime.now().year} Engineering Mastery Registry. All rights reserved.
    </footer>

    <script>
        const questions = {json.dumps(all_questions)};
        const masteredQuestions = new Set(JSON.parse(localStorage.getItem('masteredQuestions') || '[]'));
        let testMode = false;

        function renderQuestions(filtered) {{
            const container = document.getElementById('questionContainer');
            container.innerHTML = '';

            filtered.forEach(q => {{
                const card = document.createElement('div');
                card.className = `question-card ${{masteredQuestions.has(q.id) ? 'mastered' : ''}}`;
                card.id = `q-${{q.id}}`;
                
                // Process Code for Tabs
                // We look for a specific pattern in the 'code' field to create tabs
                // Pattern: [DJANGO] ... [FASTAPI] ...
                let codeHtml = '';
                const codeRaw = q.code || '';
                
                if (codeRaw.includes('[DJANGO]') || codeRaw.includes('[FASTAPI]') || codeRaw.includes('[PYDANTIC]') || codeRaw.includes('[DRF]') || codeRaw.includes('[SQLALCHEMY]')) {{
                    const sections = [];
                    const patterns = ['[DJANGO]', '[FASTAPI]', '[PYDANTIC]', '[DRF]', '[SQLALCHEMY]', '[AWS]', '[AZURE]', '[GCP]', '[KUBERNETES]', '[DOCKER]'];
                    
                    let currentText = codeRaw;
                    let foundAny = true;
                    
                    while (foundAny) {{
                        let earliestMatch = -1;
                        let earliestLabel = '';
                        
                        patterns.forEach(p => {{
                            const idx = currentText.indexOf(p);
                            if (idx !== -1 && (earliestMatch === -1 || idx < earliestMatch)) {{
                                earliestMatch = idx;
                                earliestLabel = p;
                            }}
                        }});
                        
                        if (earliestMatch !== -1) {{
                            // Found a label
                            const label = earliestLabel.replace('[', '').replace(']', '');
                            currentText = currentText.substring(earliestMatch + earliestLabel.length);
                            
                            // Find next label
                            let nextMatch = -1;
                            patterns.forEach(p => {{
                                const idx = currentText.indexOf(p);
                                if (idx !== -1 && (nextMatch === -1 || idx < nextMatch)) {{
                                    nextMatch = idx;
                                }}
                            }});
                            
                            let content = nextMatch !== -1 ? currentText.substring(0, nextMatch) : currentText;
                            sections.push({{ label, content: marked.parse(content.trim()) }});
                        }} else {{
                            foundAny = false;
                        }}
                    }}
                    
                    if (sections.length > 0) {{
                        let headers = '';
                        let contents = '';
                        sections.forEach((s, i) => {{
                            headers += `<div class="tab-header ${{i === 0 ? 'active' : ''}}" onclick="switchTab(this, '${{q.id}}', ${{i}})">${{s.label}}</div>`;
                            contents += `<div class="tab-content ${{i === 0 ? 'active' : ''}}" id="tab-content-${{q.id}}-${{i}}">${{s.content}}</div>`;
                        }});
                        codeHtml = `<div class="code-tabs"><div class="tab-headers">${{headers}}</div><div class="tab-body">${{contents}}</div></div>`;
                    }} else {{
                        codeHtml = marked.parse(codeRaw);
                    }}
                }} else {{
                    codeHtml = marked.parse(codeRaw);
                }}

                card.innerHTML = `
                    <input type="checkbox" class="mastery-checkbox" ${{masteredQuestions.has(q.id) ? 'checked' : ''}} onclick="toggleMastery(${{q.id}})">
                    <div class="card-header">
                        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                            <span class="domain-tag">${{q.domain}}</span>
                            <span class="difficulty-badge ${{q.difficulty}}">${{q.difficulty}}</span>
                        </div>
                        <div style="color: var(--text-dim); font-size: 0.8rem; font-weight: 600;">ID: ${{q.id}}</div>
                    </div>
                    
                    <div class="question-text" onclick="revealCard(${{q.id}})">${{q.question}}</div>
                    
                    <div class="answer-section">
                        <div class="answer-text markdown-body">${{marked.parse(q.answer || '')}}</div>
                        
                        ${{q.analogy ? `
                        <div class="analogy-container">
                            <div class="analogy-label">💡 ANALOGY</div>
                            <div class="analogy-text">${{q.analogy}}</div>
                        </div>` : ''}}
                        
                        <div class="code-section">${{codeHtml}}</div>
                    </div>

                    ${{q.counterQuestion ? `
                    <div class="counter-section">
                        <div class="counter-label">🔄 COUNTER-QUESTION</div>
                        <div class="counter-question">${{q.counterQuestion}}</div>
                        <div class="counter-answer markdown-body">${{marked.parse(q.counterQuestionAnswer || '')}}</div>
                    </div>` : ''}}
                    
                    <div class="tags-container">
                        ${{(q.tags || []).map(t => `<span class="tag" onclick="filterByTag('${{t}}')">${{t}}</span>`).join('')}}
                    </div>
                `;
                container.appendChild(card);
            }});
            
            // Re-highlight code
            Prism.highlightAll();
        }}

        function switchTab(el, qId, index) {{
            const card = document.getElementById(`q-${{qId}}`);
            const headers = card.querySelectorAll('.tab-header');
            const contents = card.querySelectorAll('.tab-content');
            
            headers.forEach(h => h.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            el.classList.add('active');
            card.querySelector(`#tab-content-${{qId}}-${{index}}`).classList.add('active');
        }}

        function selectDomain(domain) {{
            document.querySelectorAll('.domain-item').forEach(el => {{
                el.classList.toggle('active', el.getAttribute('data-domain') === domain);
            }});
            
            const title = domain === 'all' ? 'All Domains' : domain;
            document.getElementById('domainTitle').innerText = title;
            
            filterQuestions();
        }}

        function filterByTag(tag) {{
            document.getElementById('searchBar').value = tag;
            filterQuestions();
        }}

        function filterQuestions() {{
            const query = document.getElementById('searchBar').value.toLowerCase();
            const activeDomain = document.querySelector('.domain-item.active').getAttribute('data-domain');
            
            const filtered = questions.filter(q => {{
                const matchesSearch = q.question.toLowerCase().includes(query) || 
                                     (q.tags || []).some(t => t.toLowerCase().includes(query)) ||
                                     (q.topic || '').toLowerCase().includes(query);
                
                const matchesDomain = activeDomain === 'all' || q.domain === activeDomain;
                
                return matchesSearch && matchesDomain;
            }});

            document.getElementById('domainStats').innerText = `${{filtered.length}} Questions Found`;
            renderQuestions(filtered);
            
            if (testMode) {{
                document.getElementById('questionContainer').classList.add('test-mode');
            }}
        }}

        function toggleMastery(id) {{
            if (masteredQuestions.has(id)) {{
                masteredQuestions.delete(id);
            }} else {{
                masteredQuestions.add(id);
            }}
            localStorage.setItem('masteredQuestions', JSON.stringify(Array.from(masteredQuestions)));
            document.getElementById(`q-${{id}}`).classList.toggle('mastered');
        }}

        function toggleTestMode() {{
            testMode = !testMode;
            const btn = document.getElementById('testModeBtn');
            btn.classList.toggle('active', testMode);
            document.getElementById('questionContainer').classList.toggle('test-mode', testMode);
            
            if (!testMode) {{
                document.querySelectorAll('.revealed').forEach(el => el.classList.remove('revealed'));
            }}
        }}

        function revealCard(id) {{
            if (!testMode) return;
            const card = document.getElementById(`q-${{id}}`);
            card.querySelector('.answer-section').classList.toggle('revealed');
            const counter = card.querySelector('.counter-section');
            if (counter) counter.classList.toggle('revealed');
        }}

        // Initial Render
        selectDomain('all');
    </script>
</body>
</html>

        .answer-section, .analogy-section, .code-section, .counter-section {{
            padding-left: 1.5rem;
            border-left: 3px solid var(--border);
        }}

        .analogy-section {{
            background: var(--analogy-bg);
            border-left-color: var(--accent-secondary);
            padding: 1.2rem 1.5rem;
            border-radius: 0 8px 8px 0;
            margin: 0.5rem 0;
        }}

        .analogy-text {{
            font-style: italic;
            color: var(--text-bright);
            font-size: 0.95rem;
        }}

        .code-section {{
            border-left-color: var(--accent-primary);
        }}

        .section-label {{
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            color: var(--text-dim);
            margin-bottom: 0.8rem;
            display: block;
            letter-spacing: 1px;
        }}

        /* Restore Missing Markdown Styling */
        .markdown-body pre {{
            background: #0d1117 !important;
            padding: 1rem !important;
            border-radius: 8px !important;
            border: 1px solid var(--border) !important;
            margin: 1rem 0 !important;
        }}
        .markdown-body code {{
            font-family: 'Fira Code', monospace !important;
            font-size: 0.9rem !important;
        }}
        .markdown-body p {{ margin-bottom: 1rem; }}
        .markdown-body strong {{ color: var(--text-bright); }}
        .markdown-body ul {{ margin-left: 1.5rem; margin-bottom: 1rem; }}

        .mermaid {{
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            display: flex;
            justify-content: center;
        }}

        .counter-question {{
            font-weight: 700;
            color: var(--accent-primary);
            margin-bottom: 0.8rem;
            display: block;
            font-size: clamp(1rem, 2vw, 1.1rem);
        }}

        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }}

        .tag {{
            background: #282e33;
            color: var(--text-dim);
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.7rem;
        }}

        #noResults {{
            display: none;
            text-align: center;
            padding: 4rem;
            color: var(--text-dim);
            font-size: 1.2rem;
        }}

        /* Responsive Breakpoints */
        @media (max-width: 1440px) {{
            main {{ max-width: 1100px; }}
        }}

        @media (max-width: 1024px) {{
            .layout {{
                grid-template-columns: 260px 1fr;
            }}
            .search-container {{ width: 300px; }}
        }}

        @media (max-width: 768px) {{
            header {{
                padding: 0.8rem 1.2rem;
                flex-wrap: wrap;
                gap: 1rem;
            }}

            .menu-toggle {{ display: block; }}

            .header-actions {{
                order: 3;
                width: 100%;
                justify-content: space-between;
                gap: 0.5rem;
            }}

            .search-container {{
                width: 100%;
                order: 2;
            }}

            .layout {{
                display: block;
                position: relative;
            }}

            aside {{
                position: fixed;
                left: -320px;
                top: 0;
                bottom: 0;
                width: 300px;
                height: 100vh;
                background: var(--bg-surface);
                box-shadow: 20px 0 50px rgba(0,0,0,0.5);
                transition: left 0.3s ease;
                z-index: 2000;
            }}

            aside.open {{
                left: 0;
            }}

            .overlay {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.7);
                backdrop-filter: blur(4px);
                z-index: 1500;
            }}

            .overlay.open {{ display: block; }}

            main {{
                padding: 1.5rem 1rem;
            }}

            .question-card {{
                padding: 1.5rem 1.2rem;
                gap: 1rem;
            }}

            .mode-toggle {{ scale: 0.9; }}
            .btn-action {{ font-size: 0.8rem; padding: 0.5rem 0.8rem; }}
        }}

        @media (max-width: 480px) {{
            .logo {{ font-size: 1.2rem; }}
            .header-actions {{ flex-direction: column; align-items: stretch; }}
            .mode-toggle {{ width: 100%; justify-content: center; }}
            .mode-btn {{ flex: 1; text-align: center; }}
        }}
        /* Filter Controls */
        .filter-controls {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 0.5rem 1.2rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}

        .filter-btn:hover {{
            border-color: var(--accent-primary);
            background: var(--bg-surface);
        }}

        .filter-btn.active {{
            background: rgba(210, 153, 34, 0.15);
            color: var(--difficulty-medium);
            border-color: var(--difficulty-medium);
            box-shadow: 0 0 15px rgba(210, 153, 34, 0.1);
        }}

        .filter-btn span {{
            font-size: 1rem;
        }}
    </style>
</head>
<body>
    <div class="overlay" id="overlay" onclick="toggleMenu()"></div>
    <header>
        <button class="menu-toggle" onclick="toggleMenu()">☰</button>
        <div class="logo">TECHNICAL<span>REGISTRY</span></div>
        <div class="header-actions">
            <div class="search-container">
                <input type="text" id="searchBar" placeholder="Search across all questions..." onkeyup="applyFilters()">
            </div>
            <div class="mode-toggle">
                <div id="studyBtn" class="mode-btn active" onclick="setMode('study')">Study</div>
                <div id="testBtn" class="mode-btn" onclick="setMode('test')">Test</div>
            </div>
            <button class="btn-action" onclick="randomize()">
                <span>🔀</span> Randomize
            </button>
        </div>
    </header>

    <div class="layout">
        <aside id="sidebar">
            <ul class="domain-list">
                {sidebar_html}
            </ul>
        </aside>

        <main id="registry">
            <div class="registry-info">
                <h1>Technical Interview Mastery</h1>
                <p>High-fidelity engineering registry with code examples and system flows.</p>
            </div>

            <div class="filter-controls">
                <button id="highlyAskedFilter" class="filter-btn" onclick="toggleHighlyAsked()">
                    <span>🔥</span> Highly Asked Only
                </button>
            </div>

            <div id="noResults">No questions found matching your criteria.</div>

            <div class="questions-container" id="questionsContainer">
                {"".join([f'''
                <div class="question-card" data-domain="{safe_html(q.get('domain', ''))}" id="q-{q.get('id', 0)}-{safe_html(q.get('domain', ''))}">
                    <input type="checkbox" class="mastery-checkbox" title="Mark as Mastered" onchange="toggleMastery(this)">
                    <div class="card-header">
                        <span class="domain-tag">{safe_html(q.get('domain', ''))}</span>
                        <span class="difficulty-badge {safe_html(q.get('difficulty', 'medium'))}">{safe_html(q.get('difficulty', 'medium'))}</span>
                    </div>
                    <div class="question-text">{safe_html(q.get('question', ''))}</div>
                    
                    <button class="btn-action reveal-btn" onclick="revealCard(this)" style="display: none; width: fit-content;">👁️ Show Answer</button>

                    <div class="answer-section">
                        <span class="section-label">High-Fidelity Answer</span>
                        <div class="answer-text markdown-body" data-markdown-content="{safe_html(q.get('answer', ''))}"></div>
                    </div>

                    {f"""
                    <div class="analogy-section">
                        <span class="section-label">Conceptual Analogy</span>
                        <div class="analogy-text">{safe_html(q.get('analogy', ''))}</div>
                    </div>
                    """ if q.get('analogy') else ""}

                    {f"""
                    <div class="code-section">
                        <span class="section-label">Production Implementation</span>
                        <div class="markdown-body" data-markdown-content="{safe_html(q.get('code', ''))}"></div>
                    </div>
                    """ if q.get('code') else ""}

                    {f"""
                    <div class="counter-section">
                        <span class="section-label">The Deep Dive (Follow-up Scenarios)</span>
                        <span class="counter-question">{safe_html(q.get('counterQuestion', ''))}</span>
                        <div class="answer-text markdown-body" data-markdown-content="{safe_html(q.get('counterQuestionAnswer', ''))}"></div>
                    </div>
                    """ if q.get('counterQuestion') else ""}

                    <div class="tags">
                        {''.join([f'<span class="tag">#{(t[1:] if t.startswith("#") else t)}</span>' for t in q.get('tags', [])])}
                    </div>
                </div>
                ''' for q in all_questions])}
            </div>
        </main>
    </div>

    <script>
        // Initialize Mermaid
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});

        function toggleMenu() {{
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('overlay');
            sidebar.classList.toggle('open');
            overlay.classList.toggle('open');
            document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : 'auto';
        }}

        // Close menu when selecting a domain on mobile
        const originalSelectDomain = selectDomain;
        selectDomain = function(domain) {{
            if (window.innerWidth <= 768) toggleMenu();
            originalSelectDomain(domain);
        }};

        // Initialize Markdown rendering
        document.querySelectorAll('.markdown-body').forEach(el => {{
            const content = el.getAttribute('data-markdown-content');
            el.innerHTML = marked.parse(content);
        }});

        // Highlight code
        Prism.highlightAll();

        let currentDomain = 'all';
        let isTestMode = false;
        let isHighlyAskedOnly = false;
        const cards = Array.from(document.querySelectorAll('.question-card'));
        const container = document.getElementById('questionsContainer');
        const domainItems = document.querySelectorAll('.domain-item');
        const noResults = document.getElementById('noResults');

        // Load Mastery State
        const masteryData = JSON.parse(localStorage.getItem('techRegistryMastery') || '{{}}');
        document.querySelectorAll('.question-card').forEach(card => {{
            if (masteryData[card.id]) {{
                card.classList.add('mastered');
                card.querySelector('.mastery-checkbox').checked = true;
            }}
        }});

        function setMode(mode) {{
            isTestMode = (mode === 'test');
            document.body.classList.toggle('test-mode', isTestMode);
            document.getElementById('studyBtn').classList.toggle('active', !isTestMode);
            document.getElementById('testBtn').classList.toggle('active', isTestMode);
            
            // Show/Hide Reveal buttons
            document.querySelectorAll('.reveal-btn').forEach(btn => {{
                btn.style.display = isTestMode ? 'block' : 'none';
            }});

            // Reset revealed states when switching
            document.querySelectorAll('.revealed').forEach(el => el.classList.remove('revealed'));
        }}

        function revealCard(btn) {{
            const card = btn.closest('.question-card');
            card.querySelectorAll('.answer-section, .analogy-section, .code-section, .counter-section').forEach(s => s.classList.add('revealed'));
            btn.style.display = 'none';
        }}

        function toggleMastery(checkbox) {{
            const card = checkbox.closest('.question-card');
            const id = card.id;
            if (checkbox.checked) {{
                card.classList.add('mastered');
                masteryData[id] = true;
            }} else {{
                card.classList.remove('mastered');
                delete masteryData[id];
            }}
            localStorage.setItem('techRegistryMastery', JSON.stringify(masteryData));
        }}

        function randomize() {{
            const visibleCards = cards.filter(c => c.style.display !== 'none');
            for (let i = visibleCards.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                container.insertBefore(visibleCards[j], visibleCards[i]);
                [visibleCards[i], visibleCards[j]] = [visibleCards[j], visibleCards[i]];
            }}
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function selectDomain(domain) {{
            currentDomain = domain;
            domainItems.forEach(item => {{
                if (item.getAttribute('data-domain') === domain) {{
                    item.classList.add('active');
                }} else {{
                    item.classList.remove('active');
                }}
            }});
            applyFilters();
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function toggleHighlyAsked() {{
            isHighlyAskedOnly = !isHighlyAskedOnly;
            const btn = document.getElementById('highlyAskedFilter');
            btn.classList.toggle('active', isHighlyAskedOnly);
            applyFilters();
        }}

        function applyFilters() {{
            const query = document.getElementById('searchBar').value.toLowerCase();
            let visibleCount = 0;
            const difficultyRank = {{ 'easy': 0, 'medium': 1, 'hard': 2 }};

            cards.forEach(card => {{
                const domain = card.getAttribute('data-domain');
                const text = card.innerText.toLowerCase();
                const tags = Array.from(card.querySelectorAll('.tag')).map(t => t.innerText.toLowerCase());
                
                const isHighlyAsked = tags.some(t => t.includes('highly_asked'));
                
                let matchesDomain = (currentDomain === 'all' || domain === currentDomain);
                const matchesHighlyAsked = isHighlyAskedOnly ? isHighlyAsked : true;
                const matchesSearch = text.includes(query);

                if (matchesDomain && matchesHighlyAsked && matchesSearch) {{
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            // Handle sequence sorting if filter is active
            if (isHighlyAskedOnly) {{
                const visibleCards = cards.filter(c => c.style.display !== 'none');
                visibleCards.sort((a, b) => {{
                    const diffA = a.querySelector('.difficulty-badge').innerText.toLowerCase().trim();
                    const diffB = b.querySelector('.difficulty-badge').innerText.toLowerCase().trim();
                    return difficultyRank[diffA] - difficultyRank[diffB];
                }});
                visibleCards.forEach(c => container.appendChild(c));
            }} else {{
                // Restore original order
                cards.forEach(c => container.appendChild(c));
            }}

            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        }}
    </script>
</body>
</html>
    """

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Generated {output_file}")

if __name__ == "__main__":
    generate_html()
