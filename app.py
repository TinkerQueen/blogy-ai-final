"""
AI Blog Generator with SEO Score
=================================
A Streamlit app that uses Google Gemini API to generate full SEO-optimized blogs.

Setup:
    1. Install dependencies:
       pip install streamlit google-generativeai python-dotenv

    2. Set your Gemini API key:
       Option A - .env file:   GEMINI_API_KEY=your_key_here
       Option B - Environment: export GEMINI_API_KEY=your_key_here
       Option C - Enter it in the Streamlit sidebar at runtime

    3. Run the app:
       streamlit run app.py
"""

import os
import re
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# 0.  CONFIGURATION & PAGE SETUP
# ─────────────────────────────────────────────
load_dotenv()  # Load .env file if present

st.set_page_config(
    page_title="AI Blog Generator with SEO Score",
    page_icon="✍️",
    layout="wide",
)

# ── Custom CSS for a clean, modern look ──────
st.markdown("""
<style>
    /* Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@400;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Hero title */
    .hero-title {
        font-family: 'Merriweather', serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0;
    }
    .hero-sub {
        color: #6b7280;
        font-size: 1rem;
        margin-top: 0.25rem;
    }

    /* Step badges */
    .step-badge {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        border-radius: 999px;
        padding: 2px 14px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 8px;
        letter-spacing: 0.04em;
    }

    /* SEO Score card */
    .seo-card {
        border-radius: 16px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .seo-card.great  { background: #d1fae5; border: 2px solid #10b981; }
    .seo-card.good   { background: #fef3c7; border: 2px solid #f59e0b; }
    .seo-card.poor   { background: #fee2e2; border: 2px solid #ef4444; }
    .seo-score-num {
        font-size: 4rem;
        font-weight: 700;
        line-height: 1;
    }
    .seo-label { font-size: 1rem; font-weight: 500; margin-top: 4px; }

    /* Individual score row */
    .score-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid #f3f4f6;
        font-size: 0.9rem;
    }
    .score-row:last-child { border-bottom: none; }
    .score-pill {
        background: #e0e7ff;
        color: #3730a3;
        border-radius: 999px;
        padding: 1px 10px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* Blog content area */
    .blog-box {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 2rem;
        font-family: 'Merriweather', serif;
        font-size: 0.95rem;
        line-height: 1.9;
        color: #1f2937;
        white-space: pre-wrap;
        word-break: break-word;
        max-height: 600px;
        overflow-y: auto;
    }

    /* Divider */
    hr { border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 1.  GEMINI API INITIALISATION
# ─────────────────────────────────────────────

def init_gemini(api_key: str) -> genai.GenerativeModel | None:
    """
    Configure the Gemini client and return a GenerativeModel instance.
    Returns None and shows an error if the key is missing or invalid.
    """
    if not api_key:
        st.error("⚠️  No API key provided. Enter your Gemini API key in the sidebar.")
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model
    except Exception as exc:
        st.error(f"❌  Failed to initialise Gemini: {exc}")
        return None


def call_gemini(model: genai.GenerativeModel, prompt: str) -> str:
    """
    Send a prompt to Gemini and return the text response.
    Raises RuntimeError on API failure so callers can surface it clearly.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        raise RuntimeError(f"Gemini API error: {exc}") from exc


# ─────────────────────────────────────────────
# 2.  BLOG GENERATION PIPELINE — STEP FUNCTIONS
# ─────────────────────────────────────────────

def generate_outline(model: genai.GenerativeModel, keyword: str) -> str:
    """
    Step 1 — Ask Gemini to produce a structured blog outline (headings).
    Returns the raw outline text.
    """
    prompt = f"""
You are an expert content strategist and SEO writer.

Create a detailed blog outline for the keyword: "{keyword}"

Format the outline exactly like this:
Title: [Compelling SEO-optimised blog title containing the keyword]

1. Introduction
2. [Section heading]
3. [Section heading]
4. [Section heading]
5. [Section heading]
6. [Section heading]
7. Conclusion

Rules:
- Include the exact keyword naturally in the title.
- Provide 5–7 meaningful section headings (numbered 1–7).
- Make headings specific and informative, not generic.
- Output ONLY the outline — no extra commentary.
"""
    return call_gemini(model, prompt)


def expand_section(model: genai.GenerativeModel, keyword: str, title: str, heading: str) -> str:
    """
    Step 2 — Expand a single section heading into detailed paragraph content.
    Returns the expanded text for that section.
    """
    prompt = f"""
You are a professional blog writer specialising in SEO content.

Blog title : "{title}"
Target keyword : "{keyword}"
Section heading: "{heading}"

Write 2–3 detailed, engaging paragraphs for this section.

Rules:
- Use the keyword "{keyword}" naturally at least once.
- Write in a clear, friendly, informative tone.
- Do NOT use bullet points — write in flowing prose.
- Do NOT repeat the section heading in your answer.
- Output ONLY the paragraphs, no extra labels.
"""
    return call_gemini(model, prompt)


def generate_faq(model: genai.GenerativeModel, keyword: str, title: str) -> str:
    """
    Step 3 — Generate a structured FAQ section for the blog.
    Returns the FAQ block as a string.
    """
    prompt = f"""
You are an SEO content expert.

Blog title : "{title}"
Target keyword : "{keyword}"

Generate a FAQ section with exactly 5 questions and detailed answers related to the keyword.

Format:
## Frequently Asked Questions (FAQ)

**Q1: [Question]**
A: [Detailed answer in 2–3 sentences]

**Q2: [Question]**
A: [Detailed answer]

...and so on up to Q5.

Rules:
- Use the keyword "{keyword}" in at least 2 questions.
- Answers must be accurate, informative, and helpful.
- Output ONLY the FAQ block — no extra text.
"""
    return call_gemini(model, prompt)


def assemble_blog(outline: str, sections: list[dict], faq: str) -> str:
    """
    Step 4 — Combine outline title, expanded sections, and FAQ into one final blog.
    Returns the complete blog string.
    """
    # Extract the title line from the outline
    title_line = ""
    for line in outline.splitlines():
        if line.lower().startswith("title:"):
            title_line = line.replace("Title:", "").replace("title:", "").strip()
            break

    # Extract numbered headings from outline
    heading_lines = [
        line.strip()
        for line in outline.splitlines()
        if re.match(r"^\d+\.", line.strip())
    ]

    # Build the blog
    blog_parts = [f"# {title_line}\n"]

    for i, section in enumerate(sections):
        heading = heading_lines[i] if i < len(heading_lines) else section["heading"]
        # Remove leading number+dot from heading for display
        clean_heading = re.sub(r"^\d+\.\s*", "", heading)
        blog_parts.append(f"\n## {clean_heading}\n")
        blog_parts.append(section["content"])

    blog_parts.append(f"\n\n{faq}")

    return "\n".join(blog_parts)


# ─────────────────────────────────────────────
# 3.  SEO SCORING SYSTEM
# ─────────────────────────────────────────────

def calculate_seo_score(blog_text: str, keyword: str) -> dict:
    """
    Evaluate the blog against 6 SEO criteria and return a score breakdown dict.

    Criteria                        Max points
    ─────────────────────────────── ──────────
    Keyword in title                    10
    Keyword frequency in body           20
    Use of headings (## markers)        20
    FAQ section present                 15
    Content length > 800 words          20
    Readability / basic formatting      15
    ─────────────────────────────── ──────────
    Total                              100
    """
    scores = {}
    kw_lower = keyword.lower()
    text_lower = blog_text.lower()
    lines = blog_text.splitlines()

    # ── Criterion 1: Keyword in title (10 pts) ──────────────────
    title_line = next((l for l in lines if l.startswith("# ")), "")
    scores["Keyword in Title"] = {
        "earned": 10 if kw_lower in title_line.lower() else 0,
        "max": 10,
        "detail": "Keyword found in H1 title" if kw_lower in title_line.lower()
                  else "Keyword missing from H1 title",
    }

    # ── Criterion 2: Keyword frequency (20 pts) ─────────────────
    freq = text_lower.count(kw_lower)
    word_count = len(blog_text.split())
    density = (freq / word_count * 100) if word_count else 0
    # Target density: 1–3 % = full marks; 0.5–1 % or 3–5 % = half marks
    if 1.0 <= density <= 3.0:
        kw_pts = 20
        kw_detail = f"Keyword density {density:.1f}% — ideal range (1–3%)"
    elif 0.5 <= density < 1.0 or 3.0 < density <= 5.0:
        kw_pts = 12
        kw_detail = f"Keyword density {density:.1f}% — acceptable but not optimal"
    elif freq > 0:
        kw_pts = 5
        kw_detail = f"Keyword appears only {freq} time(s) — too sparse"
    else:
        kw_pts = 0
        kw_detail = "Keyword not found in content"
    scores["Keyword Frequency"] = {"earned": kw_pts, "max": 20, "detail": kw_detail}

    # ── Criterion 3: Headings (## markers) (20 pts) ─────────────
    h2_count = sum(1 for l in lines if l.startswith("## "))
    if h2_count >= 5:
        h_pts = 20
    elif h2_count >= 3:
        h_pts = 13
    elif h2_count >= 1:
        h_pts = 7
    else:
        h_pts = 0
    scores["Use of Headings"] = {
        "earned": h_pts,
        "max": 20,
        "detail": f"{h2_count} H2 heading(s) found",
    }

    # ── Criterion 4: FAQ presence (15 pts) ──────────────────────
    has_faq = "faq" in text_lower or "frequently asked" in text_lower
    faq_q_count = len(re.findall(r"\*\*Q\d+:", blog_text))
    if has_faq and faq_q_count >= 4:
        faq_pts = 15
        faq_detail = f"FAQ section with {faq_q_count} questions"
    elif has_faq:
        faq_pts = 8
        faq_detail = "FAQ section present but incomplete"
    else:
        faq_pts = 0
        faq_detail = "No FAQ section detected"
    scores["FAQ Section"] = {"earned": faq_pts, "max": 15, "detail": faq_detail}

    # ── Criterion 5: Content length > 800 words (20 pts) ────────
    if word_count >= 1500:
        len_pts = 20
    elif word_count >= 800:
        len_pts = 14
    elif word_count >= 400:
        len_pts = 8
    else:
        len_pts = 0
    scores["Content Length"] = {
        "earned": len_pts,
        "max": 20,
        "detail": f"{word_count} words",
    }

    # ── Criterion 6: Readability / basic formatting (15 pts) ────
    fmt_pts = 0
    fmt_notes = []
    # Has a title (H1)
    if any(l.startswith("# ") for l in lines):
        fmt_pts += 5
        fmt_notes.append("H1 title ✓")
    # Has bold text (**text**)
    if "**" in blog_text:
        fmt_pts += 5
        fmt_notes.append("bold text ✓")
    # Average paragraph length ≤ 150 words (readable chunks)
    paragraphs = [p.strip() for p in blog_text.split("\n\n") if p.strip() and not p.startswith("#")]
    if paragraphs:
        avg_para_len = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
        if avg_para_len <= 150:
            fmt_pts += 5
            fmt_notes.append("paragraph length ✓")
    scores["Readability / Formatting"] = {
        "earned": fmt_pts,
        "max": 15,
        "detail": ", ".join(fmt_notes) if fmt_notes else "Poor formatting",
    }

    # ── Total ────────────────────────────────────────────────────
    total = sum(v["earned"] for v in scores.values())
    return {"total": total, "breakdown": scores, "word_count": word_count}


# ─────────────────────────────────────────────
# 4.  STREAMLIT UI
# ─────────────────────────────────────────────

def render_seo_score(result: dict) -> None:
    """Render the SEO score card and breakdown table."""
    total = result["total"]

    # Colour coding
    if total >= 80:
        card_cls, emoji, label = "great", "🟢", "Excellent SEO"
    elif total >= 55:
        card_cls, emoji, label = "good", "🟡", "Needs Improvement"
    else:
        card_cls, emoji, label = "poor", "🔴", "Poor SEO"

    st.markdown(f"""
    <div class="seo-card {card_cls}">
        <div class="seo-score-num">{total}<span style="font-size:1.5rem">/100</span></div>
        <div class="seo-label">{emoji} {label}</div>
    </div>
    """, unsafe_allow_html=True)

    # Breakdown
    st.markdown("**Score Breakdown**")
    for criterion, data in result["breakdown"].items():
        st.markdown(f"""
        <div class="score-row">
            <span>{criterion} <small style="color:#9ca3af">— {data['detail']}</small></span>
            <span class="score-pill">{data['earned']}/{data['max']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<small style='color:#9ca3af'>Word count: {result['word_count']}</small>",
                unsafe_allow_html=True)


def main() -> None:
    # ── Header ───────────────────────────────────────────────────
    st.markdown('<div class="hero-title">✍️ AI Blog Generator with SEO Score</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Powered by Google Gemini · Generate full SEO-optimised blog posts in seconds</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Sidebar: API Key ─────────────────────────────────────────
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key_input = st.text_input(
            "Gemini API Key",
            value=os.getenv("GEMINI_API_KEY", ""),
            type="password",
            help="Get your key from https://aistudio.google.com/app/apikey",
        )
        st.caption("Your key is never stored — it lives only in your browser session.")
        st.markdown("---")
        st.markdown("**How to get a free API key:**")
        st.markdown("1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)")
        st.markdown("2. Sign in with Google")
        st.markdown("3. Click **Create API Key**")
        st.markdown("4. Paste it above ↑")

    # ── Input Section ─────────────────────────────────────────────
    col_input, col_spacer = st.columns([3, 1])
    with col_input:
        keyword = st.text_input(
            "🔑  Target Keyword",
            placeholder='e.g. "AI blog tool India"',
            help="The primary keyword your blog should rank for.",
        )

    generate_btn = st.button("🚀  Generate Blog", type="primary", use_container_width=False)

    # ── Generation Pipeline ───────────────────────────────────────
    if generate_btn:
        if not keyword.strip():
            st.warning("Please enter a keyword before generating.")
            st.stop()

        model = init_gemini(api_key_input)
        if model is None:
            st.stop()

        # Containers for section-wise live display
        status_bar     = st.empty()
        outline_expdr  = st.expander("📋  Blog Outline", expanded=False)
        sections_expdr = st.expander("📝  Expanded Sections", expanded=False)
        faq_expdr      = st.expander("❓  FAQ Section", expanded=False)

        try:
            # ── Step 1: Outline ──────────────────────────────────
            status_bar.info("⏳  Step 1/4 — Generating blog outline…")
            with st.spinner("Generating outline…"):
                outline = generate_outline(model, keyword)
            with outline_expdr:
                st.code(outline, language=None)

            # Extract title from outline for subsequent steps
            blog_title = keyword  # fallback
            for line in outline.splitlines():
                if line.lower().startswith("title:"):
                    blog_title = line.split(":", 1)[1].strip()
                    break

            # Extract numbered headings
            headings = [
                re.sub(r"^\d+\.\s*", "", l.strip())
                for l in outline.splitlines()
                if re.match(r"^\d+\.", l.strip())
            ]

            # ── Step 2: Expand each section ─────────────────────
            status_bar.info(f"⏳  Step 2/4 — Expanding {len(headings)} sections…")
            sections = []
            with sections_expdr:
                for i, heading in enumerate(headings):
                    st.markdown(f'<span class="step-badge">Section {i+1}/{len(headings)}</span>', unsafe_allow_html=True)
                    st.markdown(f"**{heading}**")
                    with st.spinner(f"Writing '{heading}'…"):
                        content = expand_section(model, keyword, blog_title, heading)
                    st.write(content)
                    st.divider()
                    sections.append({"heading": heading, "content": content})

            # ── Step 3: FAQ ──────────────────────────────────────
            status_bar.info("⏳  Step 3/4 — Generating FAQ section…")
            with st.spinner("Generating FAQ…"):
                faq = generate_faq(model, keyword, blog_title)
            with faq_expdr:
                st.markdown(faq)

            # ── Step 4: Assemble full blog ───────────────────────
            status_bar.info("⏳  Step 4/4 — Assembling final blog…")
            time.sleep(0.3)  # tiny pause for UX
            final_blog = assemble_blog(outline, sections, faq)

            # ── SEO Scoring ──────────────────────────────────────
            seo_result = calculate_seo_score(final_blog, keyword)

            status_bar.success("✅  Blog generated successfully!")

        except RuntimeError as exc:
            status_bar.error(f"❌  {exc}")
            st.stop()

        # ── Output Layout ─────────────────────────────────────────
        st.markdown("---")
        col_blog, col_seo = st.columns([2, 1], gap="large")

        with col_blog:
            st.subheader("📄  Generated Blog")
            st.markdown(f'<div class="blog-box">{final_blog}</div>', unsafe_allow_html=True)

            # Download button
            st.download_button(
                label="⬇️  Download Blog (.txt)",
                data=final_blog,
                file_name=f"{keyword.replace(' ', '_')}_blog.txt",
                mime="text/plain",
            )

        with col_seo:
            st.subheader("📊  SEO Score")
            render_seo_score(seo_result)

            # Tips
            st.markdown("---")
            st.markdown("**💡 Quick Tips**")
            tips = []
            bd = seo_result["breakdown"]
            if bd["Keyword in Title"]["earned"] < 10:
                tips.append("Add the keyword to your title.")
            if bd["Keyword Frequency"]["earned"] < 15:
                tips.append("Use the keyword more naturally throughout.")
            if bd["Use of Headings"]["earned"] < 15:
                tips.append("Add more H2/H3 subheadings.")
            if bd["FAQ Section"]["earned"] < 15:
                tips.append("Expand FAQ to at least 5 Q&As.")
            if bd["Content Length"]["earned"] < 15:
                tips.append("Aim for 1 500+ words for best ranking.")
            if not tips:
                tips.append("Great job! Your blog is well-optimised. 🎉")
            for t in tips:
                st.markdown(f"- {t}")

    # ── Footer hint when idle ─────────────────────────────────────
    else:
        st.info("👆  Enter a keyword and click **Generate Blog** to get started.")
        st.markdown("""
        **What this tool does:**
        1. 📋  Generates a structured blog outline from your keyword
        2. ✍️  Expands each section into full paragraphs
        3. ❓  Appends an SEO-friendly FAQ section
        4. 📊  Scores your blog on 6 SEO criteria (0–100)
        5. ⬇️  Lets you download the final article
        """)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()