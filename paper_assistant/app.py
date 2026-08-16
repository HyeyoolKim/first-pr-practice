import html
import os
from datetime import datetime, timedelta

import streamlit as st
from streamlit_option_menu import option_menu

from lib import auth, db, ui
from lib.pdf_extract import extract_text
from lib.styles import CSS
from lib.summarizer import summarize_paper

st.set_page_config(page_title="연구실 논문 보조 AI", page_icon="📄", layout="wide")
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

db.init_db()

PAGES = ["홈", "업로드", "논문 목록 / 검색", "비교"]
PAGE_ICONS = ["house", "cloud-arrow-up", "search", "bar-chart-line"]


def get_api_key():
    env_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if env_key:
        return env_key
    return st.session_state.get("api_key", "")


def safe_filename(title: str) -> str:
    return (title or "paper").replace("/", "-").replace("\\", "-")[:80]


def render_login_page():
    st.markdown(
        """
        <div class="pa-hero">
            <span class="pa-hero-badge">연구실 AI 도구</span>
            <h1>논문 보조 AI</h1>
            <p>로그인하면 나만의 논문 분석 기록을 만들고 관리할 수 있어요.
            다른 사람의 기록과는 섞이지 않습니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_login, tab_signup = st.tabs(["로그인", "회원가입"])

    with tab_login:
        with st.container(border=True):
            username = st.text_input("아이디", key="login_username")
            password = st.text_input("비밀번호", type="password", key="login_password")
            if st.button("로그인", type="primary", key="login_btn"):
                user = auth.login(username, password)
                if user:
                    st.session_state.user = dict(user)
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    with tab_signup:
        with st.container(border=True):
            new_username = st.text_input("아이디", key="signup_username")
            new_password = st.text_input("비밀번호 (4자 이상)", type="password", key="signup_password")
            new_password2 = st.text_input("비밀번호 확인", type="password", key="signup_password2")
            if st.button("회원가입", type="primary", key="signup_btn"):
                if new_password != new_password2:
                    st.error("비밀번호가 서로 다릅니다.")
                else:
                    try:
                        auth.sign_up(new_username, new_password)
                        st.success("가입 완료! 로그인 탭에서 로그인해주세요.")
                    except ValueError as e:
                        st.error(str(e))


if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    render_login_page()
    st.stop()

user_id = st.session_state.user["id"]
username = st.session_state.user["username"]

if "page" not in st.session_state:
    st.session_state.page = "홈"

with st.sidebar:
    st.markdown(
        '<div class="pa-brand">📄 논문 보조 AI</div>'
        f'<div class="pa-brand-sub">👤 {html.escape(username)}님</div>',
        unsafe_allow_html=True,
    )
    if not os.environ.get("ANTHROPIC_API_KEY"):
        st.session_state["api_key"] = st.text_input(
            "Anthropic API Key",
            type="password",
            value=st.session_state.get("api_key", ""),
        )
        st.caption("환경변수 ANTHROPIC_API_KEY를 설정하면 이 입력은 생략할 수 있습니다.")

    selected = option_menu(
        menu_title=None,
        options=PAGES,
        icons=PAGE_ICONS,
        default_index=PAGES.index(st.session_state.page),
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#E8664D", "font-size": "15px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "3px 0",
                "border-radius": "12px",
                "padding": "10px 14px",
                "color": "#2B2531",
            },
            "nav-link-selected": {"background-color": "#2B2531", "color": "white"},
        },
    )
    st.session_state.page = selected

    if st.button("로그아웃", use_container_width=True):
        st.session_state.user = None
        st.session_state.page = "홈"
        st.rerun()

page = st.session_state.page

if page == "홈":
    rows = db.list_papers(user_id)

    st.markdown(
        f"""
        <div class="pa-hero">
            <span class="pa-hero-badge">연구실 AI 도구</span>
            <h1>{html.escape(username)}님, 안녕하세요.<br/>오늘도 논문을 정리해볼까요?</h1>
            <p>PDF나 초록을 올리면 목적·방법·결과·한계·후속 아이디어로 구조화해 정리하고,
            여러 논문을 검색하고 나란히 비교할 수 있어요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 논문 분석하기", use_container_width=True):
            st.session_state.page = "업로드"
            st.rerun()
    with col2:
        if st.button("📚 논문 둘러보기", use_container_width=True):
            st.session_state.page = "논문 목록 / 검색"
            st.rerun()

    st.markdown('<div class="pa-section-title">현황</div>', unsafe_allow_html=True)
    total = len(rows)
    week_ago = datetime.now() - timedelta(days=7)
    recent_count = sum(
        1 for r in rows if datetime.fromisoformat(r["uploaded_at"]) >= week_ago
    )
    all_keywords = set()
    for r in rows:
        all_keywords.update(k.strip() for k in (r["keywords"] or "").split(",") if k.strip())

    m1, m2, m3 = st.columns(3)
    m1.metric("저장된 논문", f"{total}편")
    m2.metric("최근 7일 추가", f"{recent_count}편")
    m3.metric("키워드", f"{len(all_keywords)}개")

    st.markdown('<div class="pa-section-title">최근 추가된 논문</div>', unsafe_allow_html=True)
    if not rows:
        st.markdown(
            '<div class="pa-empty"><div class="pa-empty-emoji">🗂️</div>'
            '아직 저장된 논문이 없습니다.<br/>PDF를 업로드해서 첫 논문을 분석해보세요.</div>',
            unsafe_allow_html=True,
        )
    else:
        for row in rows[:3]:
            purpose = row["purpose"] or ""
            preview = purpose[:120] + ("..." if len(purpose) > 120 else "")
            st.markdown(
                f"""
                <div class="pa-card">
                    <div class="pa-paper-title">{html.escape(row['title'])}</div>
                    <div class="pa-paper-meta">{row['uploaded_at']}</div>
                    <div class="pa-field-text">{html.escape(preview)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

elif page == "업로드":
    st.markdown('<div class="pa-section-title">📤 논문 업로드 및 구조화 요약</div>', unsafe_allow_html=True)

    with st.container(border=True):
        title_input = st.text_input("논문 제목 (선택, 비워두면 AI가 추정)")
        uploaded_file = st.file_uploader("PDF 업로드", type=["pdf"])
        abstract_text = st.text_area("또는 초록/텍스트 붙여넣기", height=180)
        analyze_clicked = st.button("✨ 분석하기", type="primary")

    if analyze_clicked:
        api_key = get_api_key()
        if not api_key:
            st.error("Anthropic API 키를 입력해주세요.")
        elif not api_key.strip().isascii():
            st.error(
                "API 키에 한글 등 비-ASCII 문자가 섞여 있습니다. "
                "입력기를 영문으로 바꾼 뒤 console.anthropic.com에서 발급받은 키를 다시 붙여넣어 주세요."
            )
        elif not uploaded_file and not abstract_text.strip():
            st.error("PDF를 업로드하거나 텍스트를 붙여넣어 주세요.")
        else:
            with st.spinner("논문을 분석하는 중입니다..."):
                try:
                    if uploaded_file:
                        text = extract_text(uploaded_file)
                        source_filename = uploaded_file.name
                    else:
                        text = abstract_text.strip()
                        source_filename = None

                    if not text:
                        st.error("텍스트를 추출하지 못했습니다. 다른 파일을 시도해주세요.")
                    else:
                        summary = summarize_paper(text, api_key)
                        final_title = title_input.strip() or summary.get("title") or "제목 미상"
                        db.insert_paper(user_id, final_title, source_filename, summary, text)
                        st.success(f"'{final_title}' 분석 완료 및 저장됨")

                        summary_row = dict(summary)
                        summary_row["title"] = final_title
                        summary_row["keywords"] = ", ".join(summary.get("keywords", []))

                        chips = ui.keyword_chips_html(summary_row["keywords"])
                        with st.container(border=True):
                            st.markdown(
                                f"""
                                <div class="pa-paper-title">{html.escape(final_title)}</div>
                                {ui.field_block_html(summary_row)}
                                <div>{chips}</div>
                                """,
                                unsafe_allow_html=True,
                            )
                            st.download_button(
                                "⬇️ 요약 다운로드 (.md)",
                                data=ui.build_markdown(summary_row),
                                file_name=f"{safe_filename(final_title)}.md",
                            )
                except Exception as e:
                    st.error(f"분석 중 오류가 발생했습니다: {e}")

elif page == "논문 목록 / 검색":
    st.markdown('<div class="pa-section-title">📚 논문 목록 / 검색</div>', unsafe_allow_html=True)
    query = st.text_input("검색어", placeholder="제목, 키워드, 요약 내용으로 검색...")
    rows = db.search_papers(user_id, query) if query.strip() else db.list_papers(user_id)

    if not rows:
        message = "검색 결과가 없습니다." if query.strip() else "저장된 논문이 없습니다. 먼저 업로드해주세요."
        emoji = "🔍" if query.strip() else "🗂️"
        st.markdown(
            f'<div class="pa-empty"><div class="pa-empty-emoji">{emoji}</div>{message}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.caption(f"총 {len(rows)}편")
        for row in rows:
            expand_key = f"expand_{row['id']}"
            if expand_key not in st.session_state:
                st.session_state[expand_key] = False

            chips = ui.keyword_chips_html(row["keywords"])
            if st.session_state[expand_key]:
                body_html = ui.field_block_html(row)
            else:
                purpose = row["purpose"] or ""
                preview = purpose[:140] + ("..." if len(purpose) > 140 else "")
                body_html = f'<div class="pa-field-text">{html.escape(preview)}</div>'

            meta = row["uploaded_at"]
            if row["source_filename"]:
                meta += " · " + html.escape(row["source_filename"])

            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="pa-paper-title">{html.escape(row['title'])}</div>
                    <div class="pa-paper-meta">{meta}</div>
                    {body_html}
                    <div>{chips}</div>
                    """,
                    unsafe_allow_html=True,
                )

                c1, c2, c3 = st.columns([1, 1, 1])
                with c1:
                    label = "접기" if st.session_state[expand_key] else "자세히 보기"
                    if st.button(label, key=f"toggle_{row['id']}", use_container_width=True):
                        st.session_state[expand_key] = not st.session_state[expand_key]
                        st.rerun()
                with c2:
                    st.download_button(
                        "다운로드",
                        data=ui.build_markdown(row),
                        file_name=f"{safe_filename(row['title'])}.md",
                        key=f"dl_{row['id']}",
                        use_container_width=True,
                    )
                with c3:
                    if st.button("삭제", key=f"delete_{row['id']}", use_container_width=True):
                        db.delete_paper(user_id, row["id"])
                        st.rerun()

elif page == "비교":
    st.markdown('<div class="pa-section-title">⚖️ 논문 비교</div>', unsafe_allow_html=True)
    rows = db.list_papers(user_id)
    if len(rows) < 2:
        st.markdown(
            '<div class="pa-empty"><div class="pa-empty-emoji">⚖️</div>'
            '비교하려면 최소 2편의 논문이 필요합니다.</div>',
            unsafe_allow_html=True,
        )
    else:
        options = {f"{r['title']} ({r['uploaded_at']})": r["id"] for r in rows}
        selected = st.multiselect("비교할 논문 선택 (최대 4편)", list(options.keys()))
        if len(selected) > 4:
            st.warning("가독성을 위해 최대 4편까지만 비교할 수 있어요. 처음 4편만 표시합니다.")
            selected = selected[:4]

        if len(selected) >= 2:
            selected_rows = [db.get_paper(user_id, options[s]) for s in selected]
            cols = st.columns(len(selected_rows))
            for col, row in zip(cols, selected_rows):
                with col:
                    st.markdown(
                        f"""
                        <div class="pa-card">
                            <div class="pa-paper-title">{html.escape(row['title'])}</div>
                            <div class="pa-paper-meta">{row['uploaded_at']}</div>
                            {ui.field_block_html(row)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        elif selected:
            st.info("2편 이상 선택해주세요.")
