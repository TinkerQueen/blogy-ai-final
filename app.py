"""
AI Blog Generator with SEO Score  ·  Powered by Groq
=====================================================
SETUP:
  1.  pip install -r requirements.txt
  2.  Create a .env file in the same folder:
          GROQ_API_KEY=gsk_...your_key_here
      OR export it in the terminal:
          export GROQ_API_KEY=gsk_...your_key_here
      OR paste it into the sidebar at runtime.
  3.  streamlit run app.py
"""

# ──────────────────────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────────────────────
import os
import re
import time
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ──────────────────────────────────────────────────────────────
# 0.  BASIC CONFIGURATION
# ──────────────────────────────────────────────────────────────
load_dotenv()   # reads GROQ_API_KEY from .env if it exists

st.set_page_config(
    page_title="AI Blog Generator with SEO Score",
    page_icon="✍️",
    layout="wide",
)

# ── Styling ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:wght@400;700&display=swap');

html, body, [class*="css"]          { font-family: 'Inter', sans-serif; }
.hero-title                         { font-family:'Lora',serif; font-size:2.3rem;
                                      font-weight:700; color:#111827; margin-bottom:0; }
.hero-sub                           { color:#6b7280; font-size:.95rem; margin-top:.2rem; }

.step-badge { display:inline-block; background:#dbeafe; color:#1d4ed8;
              border-radius:999px; padding:2px 14px; font-size:.75rem;
              font-weight:600; margin-bottom:6px; letter-spacing:.04em; }

.model-pill { display:inline-block; background:#dcfce7; color:#15803d;
              border-radius:999px; padding:2px 12px; font-size:.78rem; font-weight:600; }

.seo-card   { border-radius:14px; padding:1.4rem 1.8rem;
              text-align:center; margin-bottom:1rem; }
.seo-card.great { background:#d1fae5; border:2px solid #10b981; }
.seo-card.good  { background:#fef3c7; border:2px solid #f59e0b; }
.seo-card.poor  { background:#fee2e2; border:2px solid #ef4444; }
.seo-score-num  { font-size:3.8rem; font-weight:700; line-height:1; }
.seo-label      { font-size:.95rem; font-weight:500; margin-top:4px; }

.score-row { display:flex; justify-content:space-between; align-items:center;
             padding:6px 0; border-bottom:1px solid #f3f4f6; font-size:.88rem; }
.score-row:last-child { border-bottom:none; }
.score-pill { background:#e0e7ff; color:#3730a3; border-radius:999px;
              padding:1px 10px; font-size:.75rem; font-weight:600; }

hr { border:none; border-top:1px solid #e5e7eb; margin:1.2rem 0; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# 1.  GROQ MODEL CONFIGURATION
# ──────────────────────────────────────────────────────────────

# Available Groq models — fast inference on open-source LLMs
MODEL_OPTIONS = [
    "llama-3.3-70b-versatile",     # best quality
    "llama-3.1-8b-instant",        # fast & lightweight
    "mixtral-8x7b-32768",          # Mixtral MoE
    "gemma2-9b-it",                # Google Gemma 2
]

DEFAULT_MODEL = "llama-3.3-70b-versatile"


def init_groq(api_key: str, model_name: str):
    """
    Create a Groq client and validate the API key.
    Returns (client, model_name) or (None, "").
    """
    if not api_key or not api_key.strip():
        st.error("⚠️  No API key provided. Add it in the sidebar.")
        return None, ""

    try:
        client = Groq(api_key=api_key.strip())
        # Quick validation — list models to verify key works
        client.models.list()
        return client, model_name
    except Exception as exc:
        st.error(f"❌  Groq init failed: {exc}")
        return None, ""


# ──────────────────────────────────────────────────────────────
# 2.  CORE API CALL WRAPPER
# ──────────────────────────────────────────────────────────────

def call_groq(client: Groq, model: str, prompt: str, retries: int = 2) -> str:
    """
    Send a prompt to Groq and return the text.
    Retries up to `retries` times on transient errors.
    Raises RuntimeError on persistent failure.
    """
    last_error = None
    for attempt in range(retries + 1):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a professional blog writer and SEO expert."},
                    {"role": "user", "content": prompt},
                ],
                model=model,
                temperature=0.7,
                max_tokens=4096,
            )
            text = chat_completion.choices[0].message.content
            if not text:
                raise RuntimeError("Empty response from Groq.")
            return text.strip()
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(2 ** attempt)   # exponential back-off: 1s, 2s
    raise RuntimeError(f"Groq API error after {retries+1} attempts: {last_error}")


# ──────────────────────────────────────────────────────────────
# 3.  BLOG GENERATION PIPELINE
# ──────────────────────────────────────────────────────────────

def generate_outline(client: Groq, model: str, keyword: str) -> str:
    """Step 1 — Generate a structured blog outline with title + numbered headings."""
    prompt = f"""
You are an expert content strategist and SEO writer.

Create a detailed blog outline for the keyword: "{keyword}"

Format EXACTLY like this — no deviations:
Title: [Compelling SEO-optimised blog title that naturally contains the keyword]

1. Introduction
2. [Specific section heading]
3. [Specific section heading]
4. [Specific section heading]
5. [Specific section heading]
6. [Specific section heading]
7. Conclusion

Rules:
- The keyword "{keyword}" MUST appear in the title.
- Provide exactly 7 numbered headings (1-7).
- Make headings specific and descriptive, not generic.
- Output ONLY the outline. No explanations, no preamble.
"""
    return call_groq(client, model, prompt)


def expand_section(client: Groq, model: str, keyword: str, title: str, heading: str) -> str:
    """Step 2 — Write 2-3 paragraphs for a single section heading."""
    prompt = f"""
You are a professional blog writer specialising in SEO content.

Blog title  : "{title}"
Keyword     : "{keyword}"
This section: "{heading}"

Write 2-3 detailed, engaging paragraphs for this section.

Rules:
- Use the keyword "{keyword}" at least once, naturally.
- Friendly, clear, informative tone — no jargon.
- Flowing prose only — NO bullet points.
- Do NOT repeat the section heading at the start.
- Output ONLY the paragraphs.
"""
    return call_groq(client, model, prompt)


def generate_faq(client: Groq, model: str, keyword: str, title: str) -> str:
    """Step 3 — Generate an SEO-friendly FAQ block (5 Q&As)."""
    prompt = f"""
You are an SEO content expert.

Blog title: "{title}"
Keyword   : "{keyword}"

Write a FAQ section with exactly 5 questions and answers.

Format EXACTLY like this:
## Frequently Asked Questions (FAQ)

**Q1: [Question containing the keyword]**
A: [2-3 sentence informative answer]

**Q2: [Question]**
A: [Answer]

**Q3: [Question]**
A: [Answer]

**Q4: [Question]**
A: [Answer]

**Q5: [Question related to the keyword]**
A: [Answer]

Rules:
- Use "{keyword}" in at least Q1 and Q5.
- Answers must be accurate and genuinely helpful.
- Output ONLY the FAQ block — no preamble.
"""
    return call_groq(client, model, prompt)


def assemble_blog(outline: str, sections: list, faq: str) -> str:
    """
    Step 4 — Combine outline title, expanded section content, and FAQ
    into a single, well-formatted markdown blog post.
    """
    # Extract title from outline
    blog_title = "Blog Post"
    for line in outline.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("title:"):
            blog_title = stripped.split(":", 1)[1].strip()
            break

    # Extract numbered headings from outline
    heading_lines = [
        line.strip()
        for line in outline.splitlines()
        if re.match(r"^\d+\.", line.strip())
    ]

    # Build the post
    parts = [f"# {blog_title}\n"]
    for i, section in enumerate(sections):
        raw_heading = heading_lines[i] if i < len(heading_lines) else section["heading"]
        clean_heading = re.sub(r"^\d+\.\s*", "", raw_heading)
        parts.append(f"\n## {clean_heading}\n")
        parts.append(section["content"])

    parts.append(f"\n\n{faq}")
    return "\n".join(parts)


# ──────────────────────────────────────────────────────────────
# 4.  SEO SCORING ENGINE
# ──────────────────────────────────────────────────────────────

def calculate_seo_score(blog_text: str, keyword: str) -> dict:
    """
    Score the generated blog on 6 SEO criteria. Returns a dict with:
      - total      (int 0-100)
      - breakdown  (dict of criterion -> {earned, max, detail})
      - word_count (int)
    """
    scores   = {}
    kw_lower = keyword.lower()
    txt_low  = blog_text.lower()
    lines    = blog_text.splitlines()

    # 1. Keyword in title (10 pts)
    title_line = next((l for l in lines if l.startswith("# ")), "")
    kw_in_title = kw_lower in title_line.lower()
    scores["Keyword in Title"] = {
        "earned": 10 if kw_in_title else 0,
        "max": 10,
        "detail": "Found in H1 title" if kw_in_title else "Not in H1 title",
    }

    # 2. Keyword frequency / density (20 pts)
    word_count = len(blog_text.split())
    freq       = txt_low.count(kw_lower)
    density    = (freq / word_count * 100) if word_count else 0

    if   1.0 <= density <= 3.0:  kw_pts, kw_msg = 20, f"Density {density:.1f}% — ideal (1-3%)"
    elif 0.5 <= density <  1.0:  kw_pts, kw_msg = 12, f"Density {density:.1f}% — slightly low"
    elif 3.0 <  density <= 5.0:  kw_pts, kw_msg = 12, f"Density {density:.1f}% — slightly high"
    elif freq > 0:               kw_pts, kw_msg =  5, f"Only {freq} occurrence(s) — too sparse"
    else:                        kw_pts, kw_msg =  0, "Keyword not found in body"

    scores["Keyword Frequency"] = {"earned": kw_pts, "max": 20, "detail": kw_msg}

    # 3. Headings (20 pts)
    h2_count = sum(1 for l in lines if l.startswith("## "))
    if   h2_count >= 5: h_pts = 20
    elif h2_count >= 3: h_pts = 13
    elif h2_count >= 1: h_pts =  7
    else:               h_pts =  0

    scores["Use of H2 Headings"] = {
        "earned": h_pts,
        "max": 20,
        "detail": f"{h2_count} H2 heading(s) found",
    }

    # 4. FAQ section (15 pts)
    has_faq  = "faq" in txt_low or "frequently asked" in txt_low
    faq_qs   = len(re.findall(r"\*\*Q\d+:", blog_text))
    if   has_faq and faq_qs >= 4: faq_pts, faq_msg = 15, f"FAQ with {faq_qs} questions"
    elif has_faq:                  faq_pts, faq_msg =  8, f"FAQ present but only {faq_qs} question(s)"
    else:                          faq_pts, faq_msg =  0, "No FAQ section detected"

    scores["FAQ Section"] = {"earned": faq_pts, "max": 15, "detail": faq_msg}

    # 5. Word count (20 pts)
    if   word_count >= 1500: len_pts, len_msg = 20, f"{word_count} words — excellent"
    elif word_count >=  800: len_pts, len_msg = 14, f"{word_count} words — good"
    elif word_count >=  400: len_pts, len_msg =  8, f"{word_count} words — short"
    else:                    len_pts, len_msg =  0, f"{word_count} words — too short"

    scores["Content Length"] = {"earned": len_pts, "max": 20, "detail": len_msg}

    # 6. Readability / formatting (15 pts)
    fmt_pts, fmt_notes = 0, []

    if any(l.startswith("# ") for l in lines):
        fmt_pts += 5; fmt_notes.append("H1 title")

    if "**" in blog_text:
        fmt_pts += 5; fmt_notes.append("bold text")

    paras = [p.strip() for p in blog_text.split("\n\n") if p.strip() and not p.startswith("#")]
    if paras:
        avg_len = sum(len(p.split()) for p in paras) / len(paras)
        if avg_len <= 150:
            fmt_pts += 5; fmt_notes.append("good paragraph length")

    scores["Readability / Formatting"] = {
        "earned": fmt_pts,
        "max": 15,
        "detail": ", ".join(fmt_notes) or "Poor formatting",
    }

    total = sum(v["earned"] for v in scores.values())
    return {"total": total, "breakdown": scores, "word_count": word_count}


# ──────────────────────────────────────────────────────────────
# 5.  UI HELPERS
# ──────────────────────────────────────────────────────────────

def render_seo_score(result: dict) -> None:
    """Render the coloured score card + per-criterion breakdown."""
    total = result["total"]

    if   total >= 80: cls, emoji, label = "great", "🟢", "Excellent SEO"
    elif total >= 55: cls, emoji, label = "good",  "🟡", "Needs Improvement"
    else:             cls, emoji, label = "poor",  "🔴", "Poor SEO"

    st.markdown(f"""
    <div class="seo-card {cls}">
        <div class="seo-score-num">{total}<span style="font-size:1.4rem">/100</span></div>
        <div class="seo-label">{emoji} {label}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Score Breakdown**")
    for criterion, data in result["breakdown"].items():
        st.markdown(f"""
        <div class="score-row">
            <span>{criterion}
                <small style="color:#9ca3af"> — {data['detail']}</small>
            </span>
            <span class="score-pill">{data['earned']}/{data['max']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        f"<small style='color:#9ca3af'>Total word count: {result['word_count']}</small>",
        unsafe_allow_html=True,
    )


def seo_tips(result: dict) -> None:
    """Derive actionable improvement tips from the score breakdown."""
    bd   = result["breakdown"]
    tips = []

    if bd["Keyword in Title"]["earned"] < 10:
        tips.append("Add your keyword to the H1 title.")
    if bd["Keyword Frequency"]["earned"] < 15:
        tips.append("Use the keyword more naturally throughout the body.")
    if bd["Use of H2 Headings"]["earned"] < 15:
        tips.append("Add at least 5 H2 sub-headings.")
    if bd["FAQ Section"]["earned"] < 15:
        tips.append("Ensure the FAQ has at least 5 Q&A pairs.")
    if bd["Content Length"]["earned"] < 14:
        tips.append("Aim for 1500+ words for stronger ranking signals.")
    if bd["Readability / Formatting"]["earned"] < 10:
        tips.append("Add bold text and keep paragraphs under 150 words.")

    if not tips:
        st.success("🎉 Great job! Your blog is well-optimised.")
    else:
        st.markdown("**💡 Improvement Tips**")
        for t in tips:
            st.markdown(f"- {t}")


# ──────────────────────────────────────────────────────────────
# 6.  MAIN APP
# ──────────────────────────────────────────────────────────────

def main() -> None:

    # Page header
    st.markdown('<div class="hero-title">✍️ AI Blog Generator with SEO Score</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Powered by Groq · Lightning-fast inference on open-source LLMs</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        api_key_input = st.text_input(
            "Groq API Key",
            value=os.getenv("GROQ_API_KEY", ""),
            type="password",
            help="Get a free key at https://console.groq.com/keys",
        )
        st.caption("Key stays in your session — never stored.")

        st.markdown("---")
        selected_model = st.selectbox(
            "🤖  Model",
            options=MODEL_OPTIONS,
            index=0,
            help="Choose the Groq-hosted model to use for generation.",
        )

        st.markdown("---")
        st.markdown("**Common Fixes**")
        st.markdown("""
- **401 Unauthorized** → check your API key
- **Rate limit** → wait a moment, Groq has generous free-tier limits
- **ModuleNotFoundError** → run `pip install -r requirements.txt`
- **dotenv not loading** → `.env` must be in the same folder as `app.py`
        """)

    # Keyword input
    col_kw, _ = st.columns([3, 1])
    with col_kw:
        keyword = st.text_input(
            "🔑  Target Keyword",
            placeholder='e.g. "AI blog tool India"',
            help="Primary keyword for SEO targeting.",
        )

    generate_btn = st.button("🚀  Generate Blog", type="primary")

    # Generation pipeline
    if generate_btn:
        if not keyword.strip():
            st.warning("Please enter a keyword first.")
            st.stop()

        # Init Groq client
        client, model_name = init_groq(api_key_input, selected_model)
        if client is None:
            st.stop()

        # Show which model was selected
        st.sidebar.markdown(
            f"**Active model:** <span class='model-pill'>{model_name}</span>",
            unsafe_allow_html=True,
        )

        # Live-update containers
        status_bar      = st.empty()
        outline_expdr   = st.expander("📋  Step 1 — Blog Outline",     expanded=False)
        sections_expdr  = st.expander("📝  Step 2 — Expanded Sections", expanded=False)
        faq_expdr       = st.expander("❓  Step 3 — FAQ Section",       expanded=False)

        try:
            # Step 1: Outline
            status_bar.info("⏳  Step 1/4 — Generating blog outline…")
            with st.spinner("Thinking about structure…"):
                outline = generate_outline(client, model_name, keyword)
            with outline_expdr:
                st.code(outline, language=None)

            # Parse title + headings from outline
            blog_title = keyword
            for line in outline.splitlines():
                if line.strip().lower().startswith("title:"):
                    blog_title = line.split(":", 1)[1].strip()
                    break

            headings = [
                re.sub(r"^\d+\.\s*", "", l.strip())
                for l in outline.splitlines()
                if re.match(r"^\d+\.", l.strip())
            ]

            # Step 2: Expand sections
            status_bar.info(f"⏳  Step 2/4 — Writing {len(headings)} sections…")
            sections = []
            with sections_expdr:
                for i, heading in enumerate(headings, 1):
                    st.markdown(
                        f'<span class="step-badge">Section {i}/{len(headings)}</span>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"**{heading}**")
                    with st.spinner(f"Writing '{heading}'…"):
                        content = expand_section(client, model_name, keyword, blog_title, heading)
                    st.write(content)
                    st.divider()
                    sections.append({"heading": heading, "content": content})

            # Step 3: FAQ
            status_bar.info("⏳  Step 3/4 — Generating FAQ…")
            with st.spinner("Creating FAQ…"):
                faq = generate_faq(client, model_name, keyword, blog_title)
            with faq_expdr:
                st.markdown(faq)

            # Step 4: Assemble
            status_bar.info("⏳  Step 4/4 — Assembling final blog…")
            time.sleep(0.2)
            final_blog = assemble_blog(outline, sections, faq)
            seo_result = calculate_seo_score(final_blog, keyword)
            status_bar.success(f"✅  Done! Blog generated using **{model_name}**")

        except RuntimeError as exc:
            status_bar.error(f"❌  {exc}")
            st.markdown("""
**Troubleshooting:**
- Verify your API key in the sidebar
- Make sure your Groq account is active
- Check if you've hit the rate limit (wait a moment and retry)
            """)
            st.stop()

        # Output
        st.markdown("---")
        col_blog, col_seo = st.columns([2, 1], gap="large")

        with col_blog:
            st.subheader("📄  Generated Blog")
            st.markdown(final_blog)

            st.download_button(
                label="⬇️  Download Blog (.txt)",
                data=final_blog,
                file_name=f"{keyword.replace(' ', '_')}_blog.txt",
                mime="text/plain",
            )

        with col_seo:
            st.subheader("📊  SEO Score")
            render_seo_score(seo_result)
            st.markdown("---")
            seo_tips(seo_result)

    else:
        # Idle state
        st.info("👆  Enter a keyword and click **Generate Blog** to start.")
        st.markdown("""
**Pipeline overview:**
1. 📋  **Outline** — title + 7 structured headings
2. ✍️  **Sections** — 2-3 paragraphs per heading
3. ❓  **FAQ** — 5 keyword-rich Q&As
4. 📊  **SEO Score** — 6-criterion audit (0-100)
5. ⬇️  **Download** — full blog as `.txt`
        """)


# ──────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()