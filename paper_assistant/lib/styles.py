CSS = """
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css');

:root {
    --pa-bg: #FAF7F3;
    --pa-surface: #FFFFFF;
    --pa-surface-alt: #FFF6EF;
    --pa-text: #2B2531;
    --pa-text-muted: #8A8296;
    --pa-accent: #E8664D;
    --pa-accent-2: #6C5CE7;
    --pa-border: #F0E7DD;
    --pa-shadow: 0 10px 30px rgba(43, 37, 49, 0.06);
}

html, body, [class*="css"] {
    font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: var(--pa-bg);
}

header[data-testid="stHeader"] {
    background: var(--pa-bg) !important;
    box-shadow: none !important;
    border-bottom: none !important;
}

[data-testid="stDecoration"] {
    background: var(--pa-bg) !important;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--pa-border);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.6rem;
}

.pa-brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 800;
    font-size: 1.05rem;
    color: var(--pa-text);
    margin-bottom: 0.3rem;
}

.pa-brand-sub {
    color: var(--pa-text-muted);
    font-size: 0.78rem;
    margin-bottom: 1.2rem;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, var(--pa-accent), var(--pa-accent-2));
    color: white !important;
    font-weight: 600;
    padding: 0.55rem 1.4rem;
    box-shadow: var(--pa-shadow);
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 34px rgba(232, 102, 77, 0.28);
}
.stButton > button:focus:not(:active) {
    color: white !important;
}

/* Secondary (ghost) buttons: any button whose label starts with an emoji we treat as secondary via data attr not available,
   so keep all primary-styled; delete buttons get a muted variant class applied through container */
.pa-danger .stButton > button {
    background: #FFFFFF;
    color: var(--pa-accent) !important;
    border: 1px solid #F3D9CC;
    box-shadow: none;
}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border: 1px solid var(--pa-border) !important;
    background: var(--pa-surface) !important;
}

[data-testid="stFileUploaderDropzone"] {
    border-radius: 18px;
    background: var(--pa-surface-alt);
    border: 1.5px dashed #F0CBBB;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--pa-surface);
    border: 1px solid var(--pa-border);
    border-radius: 18px;
    padding: 1rem 1.2rem;
    box-shadow: var(--pa-shadow);
}

/* Native bordered containers (st.container(border=True)) used as cards
   that hold real widgets (buttons) so everything sits inside one box */
div[data-testid="stVerticalBlock"][data-test-scroll-behavior="normal"] {
    border-radius: 20px !important;
    border: 1px solid var(--pa-border) !important;
    box-shadow: var(--pa-shadow) !important;
    padding: 1.4rem 1.6rem 1.1rem 1.6rem !important;
    background: var(--pa-surface) !important;
    margin-bottom: 1.1rem;
}

div[data-testid="stVerticalBlock"][data-test-scroll-behavior="normal"] .stButton > button,
div[data-testid="stVerticalBlock"][data-test-scroll-behavior="normal"] .stDownloadButton > button {
    padding: 0.4rem 0.9rem;
    font-size: 0.82rem;
    box-shadow: none;
    margin-top: 0.6rem;
}

/* Hero */
.pa-hero {
    background: linear-gradient(135deg, #FDEEE4 0%, #F6E9F5 55%, #E8F0FB 100%);
    border-radius: 28px;
    padding: 2.6rem 2.4rem;
    margin-bottom: 1.8rem;
    box-shadow: var(--pa-shadow);
}
.pa-hero-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.75);
    color: var(--pa-accent);
    font-weight: 700;
    font-size: 0.78rem;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}
.pa-hero h1 {
    font-size: 2rem;
    margin: 0 0 0.6rem 0;
    color: var(--pa-text);
    line-height: 1.35;
    font-weight: 800;
}
.pa-hero p {
    color: var(--pa-text-muted);
    font-size: 1rem;
    margin: 0;
    max-width: 640px;
}

/* Section titles */
.pa-section-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--pa-text);
    margin: 0.4rem 0 1rem 0;
}

/* Cards */
.pa-card {
    background: var(--pa-surface);
    border: 1px solid var(--pa-border);
    border-radius: 20px;
    padding: 1.4rem 1.6rem;
    box-shadow: var(--pa-shadow);
    margin-bottom: 1.1rem;
}

.pa-field-label {
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--pa-text);
    margin-bottom: 0.3rem;
    display: flex;
    gap: 0.4rem;
    align-items: center;
}
.pa-field-text {
    color: var(--pa-text);
    font-size: 0.93rem;
    line-height: 1.65;
    white-space: pre-wrap;
    margin: 0 0 1rem 0;
}
.pa-field-text:last-child {
    margin-bottom: 0;
}

.pa-chip {
    display: inline-block;
    background: var(--pa-surface-alt);
    color: var(--pa-accent);
    border: 1px solid #F3D9CC;
    font-size: 0.76rem;
    font-weight: 600;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    margin: 0 0.35rem 0.35rem 0;
}

.pa-paper-title {
    font-size: 1.08rem;
    font-weight: 800;
    color: var(--pa-text);
    margin-bottom: 0.15rem;
}
.pa-paper-meta {
    font-size: 0.78rem;
    color: var(--pa-text-muted);
    margin-bottom: 0.7rem;
}

.pa-empty {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--pa-text-muted);
}
.pa-empty-emoji {
    font-size: 2.4rem;
    margin-bottom: 0.6rem;
}
"""
