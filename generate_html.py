import json
import os
import html

def generate_html():
    docc_dir = 'c:/Users/human-bot/projects/docc'
    output_file = os.path.join(docc_dir, 'index.html')
    
    all_questions = []
    domains_set = set()

    for filename in sorted(os.listdir(docc_dir)):
        if filename.endswith('.json'):
            domain_name = filename.replace('.json', '').replace('_', ' ').title()
            filepath = os.path.join(docc_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            item['domain'] = domain_name
                            domains_set.add(domain_name)
                        all_questions.extend(data)
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    diff_rank = {'easy': 0, 'medium': 1, 'hard': 2}
    all_questions.sort(key=lambda x: (
        x.get('domain', ''), 
        diff_rank.get(x.get('difficulty', 'medium').lower(), 1),
        x.get('id', 0)
    ))
    
    sorted_domains = sorted(list(domains_set))
    groups = {
        "Core Engineering": ["Python", "Web Frameworks", "Dsa"],
        "Architecture & Systems": ["System Architecture", "Async Systems", "Api Design", "Microservices Architecture"],
        "Infrastructure & Security": ["Devops Infra", "Security Mastery", "Reliability Engineering"],
        "Data & AI": ["Databases", "Data Engineering", "Ai Mlops"],
        "Frontend & UI": ["Frontend Mastery"],
        "Soft Skills": ["Scenarios", "Soft Skills Industry"]
    }

    all_categorized = []
    for g in groups.values(): all_categorized.extend(g)
    remaining = [d for d in sorted_domains if d not in all_categorized]
    if remaining: groups["Other"] = remaining

    sidebar_html = f'<li class="domain-item active" data-domain="all" onclick="selectDomain(\'all\')">🏠 All Domains ({len(all_questions)})</li>'
    for group_name, items in groups.items():
        exists = any(item in sorted_domains for item in items)
        if exists:
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
    
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />

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
            --mastered: #238636;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background-color: var(--bg-deep); color: var(--text-main); font-family: 'Inter', sans-serif; line-height: 1.6; overflow-x: hidden; }}

        header {{
            position: sticky; top: 0; z-index: 1100; background: rgba(10, 12, 16, 0.95);
            backdrop-filter: blur(12px); border-bottom: 1px solid var(--border);
            padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem;
        }}

        .logo {{ font-family: 'Outfit', sans-serif; font-size: 1.5rem; font-weight: 800; color: var(--text-bright); cursor: pointer; white-space: nowrap; }}
        .logo span {{ color: var(--accent-primary); }}

        .header-actions {{ display: flex; align-items: center; gap: 1rem; flex: 1; justify-content: flex-end; min-width: 0; }}
        #searchBar {{ width: 100%; max-width: 400px; background: var(--bg-deep); border: 1px solid var(--border); border-radius: 8px; padding: 0.6rem 1rem; color: var(--text-bright); outline: none; }}

        .btn-toggle {{ background: var(--bg-surface); border: 1px solid var(--border); color: var(--text-bright); padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; white-space: nowrap; }}
        .btn-toggle.active {{ background: var(--accent-primary); color: var(--bg-deep); border-color: var(--accent-primary); }}

        .layout {{ display: grid; grid-template-columns: 320px 1fr; min-height: calc(100vh - 70px); }}
        
        aside {{ 
            padding: 1.5rem; border-right: 1px solid var(--border); background: var(--bg-surface); 
            height: calc(100vh - 70px); position: sticky; top: 70px; overflow-y: auto; z-index: 1000;
        }}
        
        .sidebar-category {{ font-size: 0.7rem; font-weight: 800; color: var(--text-dim); text-transform: uppercase; margin: 1.5rem 0 0.5rem 0.8rem; letter-spacing: 1px; }}
        .domain-item {{ padding: 0.6rem 0.8rem; border-radius: 6px; cursor: pointer; font-size: 0.9rem; margin-bottom: 0.2rem; transition: 0.2s; }}
        .domain-item:hover {{ background: var(--bg-card); }}
        .domain-item.active {{ background: var(--accent-primary); color: var(--bg-deep); font-weight: 700; }}

        main {{ padding: clamp(1rem, 5vw, 3rem); max-width: 1400px; margin: 0 auto; width: 100%; min-width: 0; }}
        .registry-info {{ margin-bottom: 3rem; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; }}
        
        .question-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 2rem; margin-bottom: 2.5rem; position: relative; }}
        .question-card.mastered {{ border-left: 5px solid var(--mastered); }}
        .mastery-checkbox {{ position: absolute; top: 1.5rem; right: 1.5rem; width: 20px; height: 20px; cursor: pointer; }}
        
        .card-header {{ display: flex; gap: 0.5rem; margin-bottom: 1rem; }}
        .domain-tag {{ font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: var(--accent-primary); background: rgba(88, 166, 255, 0.1); padding: 0.2rem 0.5rem; border-radius: 4px; }}
        .difficulty-badge {{ font-size: 0.7rem; font-weight: 700; text-transform: uppercase; padding: 0.2rem 0.5rem; border-radius: 4px; border: 1px solid transparent; }}
        .easy {{ color: var(--difficulty-easy); border-color: var(--difficulty-easy); }}
        .medium {{ color: var(--difficulty-medium); border-color: var(--difficulty-medium); }}
        .hard {{ color: var(--difficulty-hard); border-color: var(--difficulty-hard); }}
        
        .question-text {{ font-size: 1.4rem; font-weight: 700; color: var(--text-bright); margin-bottom: 1rem; cursor: pointer; line-height: 1.4; }}
        
        .answer-section {{ border-left: 3px solid var(--border); padding-left: 1.5rem; margin-top: 1rem; }}
        .test-mode .answer-section {{ filter: blur(12px); opacity: 0.1; transition: 0.3s; cursor: pointer; user-select: none; }}
        .test-mode .answer-section.revealed {{ filter: blur(0); opacity: 1; user-select: text; }}

        .analogy-container {{ background: rgba(126, 231, 135, 0.05); border: 1px solid rgba(126, 231, 135, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem; color: var(--text-bright); font-style: italic; }}
        .code-container {{ background: #0d1117; border-radius: 8px; padding: 1rem; border: 1px solid var(--border); margin-top: 1rem; overflow-x: auto; }}
        
        .tag {{ font-size: 0.75rem; color: var(--text-dim); background: var(--bg-surface); padding: 0.2rem 0.6rem; border-radius: 4px; margin-right: 0.5rem; cursor: pointer; }}

        /* Mobile */
        .menu-toggle {{ display: none; background: none; border: none; color: var(--text-bright); font-size: 1.5rem; cursor: pointer; padding: 0.5rem; }}
        .overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.8); z-index: 1500; }}
        
        @media (max-width: 900px) {{
            header {{ padding: 1rem; gap: 0.5rem; }}
            .menu-toggle {{ display: block; }}
            .header-actions #searchBar {{ display: none; }}
            .layout {{ grid-template-columns: 1fr; }}
            aside {{ position: fixed; left: -320px; top: 0; bottom: 0; z-index: 2000; width: 300px; transition: 0.3s; background: var(--bg-surface); box-shadow: 10px 0 30px rgba(0,0,0,0.5); }}
            aside.open {{ left: 0; }}
            .overlay.open {{ display: block; }}
            .search-mobile {{ display: block !important; width: 100%; margin-bottom: 1.5rem; background: var(--bg-deep); border: 1px solid var(--border); border-radius: 8px; padding: 0.6rem 1rem; color: var(--text-bright); }}
        }}
    </style>
</head>
<body>
    <div class="overlay" id="overlay" onclick="toggleMenu()"></div>
    <header>
        <button class="menu-toggle" onclick="toggleMenu()">☰</button>
        <div class="logo" onclick="selectDomain('all')">TECH<span>REGISTRY</span></div>
        <div class="header-actions">
            <input type="text" id="searchBar" placeholder="Search..." onkeyup="filterQuestions()">
            <button class="btn-toggle" id="testModeBtn" onclick="toggleTestMode()">🎯 Test Mode</button>
        </div>
    </header>

    <div class="layout">
        <aside id="sidebar">
            <input type="text" id="searchBarMobile" class="search-mobile" style="display: none;" placeholder="Search..." onkeyup="syncSearch(this)">
            <ul class="domain-list">
                {sidebar_html}
            </ul>
        </aside>
        <main>
            <div class="registry-info">
                <div><h1 id="domainTitle">All Domains</h1><p id="domainStats">{len(all_questions)} Questions</p></div>
                <button class="btn-toggle" id="highlyAskedFilter" onclick="toggleHighlyAsked()">🔥 Highly Asked</button>
            </div>
            <div id="questionContainer"></div>
        </main>
    </div>

    <script id="question-data" type="application/json">
        {json.dumps(all_questions)}
    </script>

    <script>
        const questions = JSON.parse(document.getElementById('question-data').textContent);
        let currentDomain = 'all', testMode = false, highlyAskedOnly = false;
        const mastered = new Set(JSON.parse(localStorage.getItem('techMastered') || '[]'));

        function escapeHTML(str) {{
            const p = document.createElement('p');
            p.textContent = str;
            return p.innerHTML;
        }}

        function render(filtered) {{
            const container = document.getElementById('questionContainer');
            container.innerHTML = '';
            
            // Limit initial render to improve performance for "All Domains"
            const toRender = filtered.slice(0, 100); 
            
            toRender.forEach(q => {{
                const card = document.createElement('div');
                card.className = `question-card ${{mastered.has(q.id) ? 'mastered' : ''}}`;
                card.id = `q-${{q.id}}`;
                
                let tagsHtml = (q.tags || []).map(t => `<span class="tag" onclick="setSearch('${{t.replace(/'/g, "\\'")}}')">#${{t}}</span>`).join('');
                
                card.innerHTML = `
                    <input type="checkbox" class="mastery-checkbox" ${{mastered.has(q.id) ? 'checked' : ''}}>
                    <div class="card-header">
                        <span class="domain-tag">${{q.domain}}</span>
                        <span class="difficulty-badge ${{q.difficulty}}">${{q.difficulty}}</span>
                    </div>
                    <div class="question-text"></div>
                    <div class="answer-section">
                        <div class="markdown-body"></div>
                        ${{q.analogy ? `<div class="analogy-container">💡 ${{escapeHTML(q.analogy)}}</div>` : ''}}
                        ${{q.code ? `<div class="code-container markdown-body"></div>` : ''}}
                    </div>
                    <div style="margin-top: 1rem;">${{tagsHtml}}</div>
                `;
                
                card.querySelector('.question-text').textContent = q.question;
                card.querySelector('.question-text').onclick = () => revealCard(q.id);
                card.querySelector('.mastery-checkbox').onclick = (e) => toggleMastery(q.id, e);
                
                const bodies = card.querySelectorAll('.markdown-body');
                bodies[0].innerHTML = marked.parse(q.answer || '');
                if (q.code && bodies[1]) bodies[1].innerHTML = marked.parse(q.code);
                
                container.appendChild(card);
            }});
            
            if (filtered.length > 100) {{
                const more = document.createElement('div');
                more.style.textAlign = 'center';
                more.style.padding = '2rem';
                more.innerHTML = `<button class="btn-toggle" onclick="renderAll()">Load All ${{filtered.length}} Questions</button>`;
                container.appendChild(more);
            }}
            
            Prism.highlightAll();
        }}

        function renderAll() {{
            const query = document.getElementById('searchBar').value.toLowerCase();
            const filtered = questions.filter(q => {{
                const matchesDomain = currentDomain === 'all' || q.domain === currentDomain;
                const matchesHighly = !highlyAskedOnly || (q.tags || []).includes('highly_asked');
                const matchesSearch = q.question.toLowerCase().includes(query) || (q.tags || []).some(t => t.toLowerCase().includes(query));
                return matchesDomain && matchesHighly && matchesSearch;
            }});
            
            const container = document.getElementById('questionContainer');
            container.innerHTML = '';
            filtered.forEach(q => {{
                // (Same logic as above, but for all)
                const card = document.createElement('div');
                card.className = `question-card ${{mastered.has(q.id) ? 'mastered' : ''}}`;
                card.id = `q-${{q.id}}`;
                let tagsHtml = (q.tags || []).map(t => `<span class="tag" onclick="setSearch('${{t.replace(/'/g, "\\'")}}')">#${{t}}</span>`).join('');
                card.innerHTML = `
                    <input type="checkbox" class="mastery-checkbox" ${{mastered.has(q.id) ? 'checked' : ''}}>
                    <div class="card-header">
                        <span class="domain-tag">${{q.domain}}</span>
                        <span class="difficulty-badge ${{q.difficulty}}">${{q.difficulty}}</span>
                    </div>
                    <div class="question-text"></div>
                    <div class="answer-section">
                        <div class="markdown-body"></div>
                        ${{q.analogy ? `<div class="analogy-container">💡 ${{escapeHTML(q.analogy)}}</div>` : ''}}
                        ${{q.code ? `<div class="code-container markdown-body"></div>` : ''}}
                    </div>
                    <div style="margin-top: 1rem;">${{tagsHtml}}</div>
                `;
                card.querySelector('.question-text').textContent = q.question;
                card.querySelector('.question-text').onclick = () => revealCard(q.id);
                card.querySelector('.mastery-checkbox').onclick = (e) => toggleMastery(q.id, e);
                const bodies = card.querySelectorAll('.markdown-body');
                bodies[0].innerHTML = marked.parse(q.answer || '');
                if (q.code && bodies[1]) bodies[1].innerHTML = marked.parse(q.code);
                container.appendChild(card);
            }});
            Prism.highlightAll();
        }}

        function filterQuestions() {{
            const query = document.getElementById('searchBar').value.toLowerCase();
            const filtered = questions.filter(q => {{
                const matchesDomain = currentDomain === 'all' || q.domain === currentDomain;
                const matchesHighly = !highlyAskedOnly || (q.tags || []).includes('highly_asked');
                const matchesSearch = q.question.toLowerCase().includes(query) || (q.tags || []).some(t => t.toLowerCase().includes(query));
                return matchesDomain && matchesHighly && matchesSearch;
            }});
            document.getElementById('domainStats').innerText = filtered.length + " Questions Found";
            render(filtered);
        }}

        function selectDomain(d) {{
            currentDomain = d;
            document.querySelectorAll('.domain-item').forEach(el => el.classList.toggle('active', el.getAttribute('data-domain') === d));
            document.getElementById('domainTitle').innerText = d === 'all' ? 'All Domains' : d;
            filterQuestions();
            if (window.innerWidth <= 900) toggleMenu();
        }}

        function toggleHighlyAsked() {{ highlyAskedOnly = !highlyAskedOnly; document.getElementById('highlyAskedFilter').classList.toggle('active', highlyAskedOnly); filterQuestions(); }}
        function toggleTestMode() {{ testMode = !testMode; document.getElementById('testModeBtn').classList.toggle('active', testMode); document.getElementById('questionContainer').classList.toggle('test-mode', testMode); }}
        function revealCard(id) {{ if (testMode) document.querySelector('#q-' + id + ' .answer-section').classList.toggle('revealed'); }}
        function toggleMastery(id, event) {{ event.stopPropagation(); if (mastered.has(id)) mastered.delete(id); else mastered.add(id); localStorage.setItem('techMastered', JSON.stringify(Array.from(mastered))); document.getElementById('q-' + id).classList.toggle('mastered'); }}
        function toggleMenu() {{ document.getElementById('sidebar').classList.toggle('open'); document.getElementById('overlay').classList.toggle('open'); }}
        function setSearch(t) {{ document.getElementById('searchBar').value = t; filterQuestions(); }}
        function syncSearch(el) {{ document.getElementById('searchBar').value = el.value; filterQuestions(); }}

        selectDomain('all');
    </script>
</body>
</html>
    """
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Generated index.html at {{output_file}}")

if __name__ == "__main__":
    generate_html()
