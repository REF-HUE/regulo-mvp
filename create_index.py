content = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Regulo Systems — Zoning Intelligence for South Africa</title>
<link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
<link rel="stylesheet" href="/static/style.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
.home{max-width:680px;margin:0 auto;padding:48px 20px 64px}
.nav{display:flex;align-items:center;gap:12px;margin-bottom:56px}
.nav-logo{display:flex;align-items:center;justify-content:center;width:38px;height:32px;border:2.5px solid #1a1a2e;border-radius:5px}
.nav-r{font-family:'Inter',sans-serif;font-size:20px;font-weight:700;color:#1a1a2e;line-height:1;letter-spacing:-1px}
.nav-s{font-family:'Inter',sans-serif;font-size:20px;font-weight:300;color:#4361ee;line-height:1;letter-spacing:-1px}
.nav-text{font-family:'Inter',sans-serif;font-size:16px;font-weight:600;color:#1a1a2e;letter-spacing:0.3px}
.nav-sub{font-family:'Inter',sans-serif;font-size:9px;font-weight:400;color:#9ca3af;letter-spacing:2.5px;text-transform:uppercase}
.nav-wordmark{display:flex;flex-direction:column;gap:0}
.hero{margin-bottom:48px}
.hero h1{font-size:32px;font-weight:800;color:#1a1a2e;letter-spacing:-1px;line-height:1.2;margin-bottom:12px}
.hero p{font-size:16px;color:#666;line-height:1.7;max-width:520px}
.search-card{background:#fff;border:1px solid #e2e5ea;border-radius:14px;padding:28px;margin-bottom:40px}
.search-card h2{font-size:14px;font-weight:600;color:#1a1a2e;margin-bottom:4px}
.search-card .hint{font-size:13px;color:#9ca3af;margin-bottom:20px}
.search-row{display:grid;grid-template-columns:1fr 1fr auto;gap:12px;align-items:end}
.search-row label{display:block;font-size:12px;font-weight:500;color:#666;margin-bottom:4px}
.search-row input{width:100%;padding:12px 14px;border:1.5px solid #d1d5db;border-radius:8px;font-size:15px;font-family:'Inter',sans-serif;color:#1a1a2e;background:#fff;outline:none;transition:border-color 0.15s;box-sizing:border-box}
.search-row input:focus{border-color:#4361ee;box-shadow:0 0 0 3px rgba(67,97,238,0.08)}
.search-btn{padding:12px 28px;background:#4361ee;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;font-family:'Inter',sans-serif;cursor:pointer;white-space:nowrap;transition:background 0.15s}
.search-btn:hover{background:#3451d1}
.muni-tabs{display:flex;gap:8px;margin-bottom:20px}
.muni-tab{padding:8px 16px;font-size:13px;font-weight:500;font-family:'Inter',sans-serif;color:#666;background:#f0f2f5;border:1.5px solid transparent;border-radius:8px;cursor:pointer;text-decoration:none;transition:all 0.15s}
.muni-tab:hover{border-color:#d1d5db;color:#1a1a2e}
.muni-tab.active{background:#f0f2ff;border-color:#4361ee;color:#4361ee;font-weight:600}
.muni-tab .badge{display:inline-block;font-size:9px;font-weight:600;padding:1px 6px;border-radius:6px;margin-left:6px;vertical-align:middle}
.badge-live{background:#d4edda;color:#155724}
.badge-new{background:#fff3cd;color:#856404}
.features{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:40px}
.feature{padding:16px 18px;background:#fff;border:1px solid #e2e5ea;border-radius:10px}
.feature h3{font-size:13px;font-weight:600;color:#1a1a2e;margin-bottom:4px}
.feature p{font-size:12px;color:#9ca3af;line-height:1.5}
.stats{display:flex;gap:24px;padding:20px 0;border-top:1px solid #e2e5ea;border-bottom:1px solid #e2e5ea;margin-bottom:40px}
.stat{flex:1;text-align:center}
.stat-value{font-size:24px;font-weight:800;color:#1a1a2e;letter-spacing:-0.5px}
.stat-label{font-size:11px;color:#9ca3af;letter-spacing:1px;text-transform:uppercase;margin-top:2px}
.home-footer{text-align:center;padding-top:24px}
.home-footer p{font-size:12px;color:#9ca3af;line-height:1.6}
.home-footer .company{font-size:11px;color:#d1d5db;margin-top:12px;letter-spacing:2px;text-transform:uppercase}
.home-error{background:#fef2f2;border:1px solid #fecaca;border-radius:10px;padding:14px 18px;margin-bottom:20px;font-size:14px;color:#991b1b}
@media(max-width:640px){.home{padding:32px 16px 48px}.hero h1{font-size:24px}.hero p{font-size:14px}.search-row{grid-template-columns:1fr}.search-btn{width:100%}.muni-tabs{flex-wrap:wrap}.features{grid-template-columns:1fr}.stats{flex-direction:column;gap:16px}}
</style>
</head>
<body>
<div class="home">
    <div class="nav">
        <div class="nav-logo"><span class="nav-r">R</span><span class="nav-s">S</span></div>
        <div class="nav-wordmark"><span class="nav-text">Regulo</span><span class="nav-sub">Systems</span></div>
    </div>
    <div class="hero">
        <h1>Know what you can build,<br>before you start designing.</h1>
        <p>Enter an ERF number. Get zoning parameters, coverage, height limits, setbacks, and a downloadable report — instantly.</p>
    </div>
    <div class="search-card">
        <div class="muni-tabs">
            <span class="muni-tab active">Gqeberha <span class="badge badge-live">LIVE</span></span>
            <a href="/joburg-lookup" class="muni-tab">Johannesburg <span class="badge badge-live">LIVE</span></a>
            <a href="/capetown-lookup" class="muni-tab">Cape Town <span class="badge badge-new">NEW</span></a>
        </div>
        <h2>Search NMBM property</h2>
        <p class="hint">If this ERF is in our registry, you'll get an instant result.</p>
        {% if error %}
        <div class="home-error">{{ error }}</div>
        {% endif %}
        <form id="nmbm-form" action="/search" method="POST">
            <div class="search-row">
                <div><label for="erf_number">ERF number</label><input type="text" id="erf_number" name="erf_number" placeholder="e.g. 3864" required autocomplete="off"></div>
                <div><label for="suburb">Suburb (optional)</label><input type="text" id="suburb" name="suburb" placeholder="e.g. Summerstrand" autocomplete="off"></div>
                <div><button type="submit" class="search-btn">Search &rarr;</button></div>
            </div>
        </form>
    </div>
    <div class="stats">
        <div class="stat"><div class="stat-value">67</div><div class="stat-label">Zones</div></div>
        <div class="stat"><div class="stat-value">3</div><div class="stat-label">Municipalities</div></div>
        <div class="stat"><div class="stat-value">&lt;10s</div><div class="stat-label">Per lookup</div></div>
    </div>
    <div class="features">
        <div class="feature"><h3>Zoning parameters</h3><p>Coverage, height, setbacks, floor area ratio — all in one place.</p></div>
        <div class="feature"><h3>Feasibility score</h3><p>A–F grade based on development constraints. Know before you design.</p></div>
        <div class="feature"><h3>PDF report</h3><p>Downloadable zoning report and Town Planning Enquiry document.</p></div>
        <div class="feature"><h3>Growing registry</h3><p>Every ERF searched builds the database for the next architect.</p></div>
    </div>
    <div class="home-footer">
        <p>For preliminary zoning analysis and feasibility screening.<br>Always verify with the relevant municipality before development.</p>
        <p class="company">Regulo Systems (Pty) Ltd</p>
    </div>
</div>
</body>
</html>'''

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Created templates/index.html')