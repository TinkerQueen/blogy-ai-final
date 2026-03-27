"""
Blogy — AI Blog Automation Platform  ·  Powered by Groq
========================================================
SETUP:
  1.  pip install -r requirements.txt
  2.  Create a .env file in the same folder:
          GROQ_API_KEY=gsk_...your_key_here
      OR paste it into the sidebar at runtime.
  3.  streamlit run app.py
"""

# ──────────────────────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────────────────────
import os
import re
import json
import time
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ──────────────────────────────────────────────────────────────
# 0.  BASIC CONFIGURATION
# ──────────────────────────────────────────────────────────────
load_dotenv()

st.set_page_config(
    page_title="Blogy — AI Blog Automation",
    page_icon="✍️",
    layout="wide",
)

# ── Styling ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:wght@400;700&display=swap');

html, body, [class*="css"]          { font-family: 'Inter', sans-serif; }
.hero-title                         { font-family:'Lora',serif; font-size:2.4rem;
                                      font-weight:700;
                                      background: linear-gradient(135deg, #6366f1, #ec4899);
                                      -webkit-background-clip: text;
                                      -webkit-text-fill-color: transparent;
                                      margin-bottom:0; }
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

.report-field { display:flex; justify-content:space-between; padding:5px 0;
                border-bottom:1px solid #f3f4f6; font-size:.87rem; }
.report-field:last-child { border-bottom:none; }
.report-val { font-weight:600; color:#1d4ed8; }

hr { border:none; border-top:1px solid #e5e7eb; margin:1.2rem 0; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# 1.  GROQ MODEL CONFIGURATION
# ──────────────────────────────────────────────────────────────
MODEL_OPTIONS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]
DEFAULT_MODEL = "llama-3.3-70b-versatile"

TONE_OPTIONS = ["Professional", "Conversational", "Authoritative"]


def init_groq(api_key: str, model_name: str):
    if not api_key or not api_key.strip():
        st.error("⚠️  No API key provided. Add it in the sidebar.")
        return None, ""
    try:
        client = Groq(api_key=api_key.strip())
        client.models.list()
        return client, model_name
    except Exception as exc:
        st.error(f"❌  Groq init failed: {exc}")
        return None, ""


# ──────────────────────────────────────────────────────────────
# 2.  CORE API CALL WRAPPER
# ──────────────────────────────────────────────────────────────
def call_groq(client: Groq, model: str, prompt: str, retries: int = 2) -> str:
    last_error = None
    for attempt in range(retries + 1):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a world-class SEO blog writer and content strategist for Blogy, India's leading AI blog automation platform."},
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
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Groq API error after {retries+1} attempts: {last_error}")


# ──────────────────────────────────────────────────────────────
# 3.  PIPELINE STEP FUNCTIONS
# ──────────────────────────────────────────────────────────────

def step1_keyword_cluster(client, model, keyword, location):
    """Step 1 — Generate keyword cluster with LSI keywords."""
    prompt = f"""
You are an expert SEO keyword researcher.

Primary keyword: "{keyword}"
Target location: "{location}"

Generate a keyword cluster of 6-8 semantically related LSI keywords for the primary keyword.

Requirements:
- Include long-tail variants (3-5 word phrases)
- Include question-based keywords (e.g. "how to...", "what is...")
- Include location-modified terms using "{location}"
- Each keyword should be something people actually search for

Output as a numbered list, one keyword per line. No explanations, no preamble.
"""
    return call_groq(client, model, prompt)


def step2_serp_gap(client, model, keyword, location):
    """Step 2 — SERP gap & competitor structure analysis."""
    prompt = f"""
You are an expert SEO analyst.

Primary keyword: "{keyword}"
Target location: "{location}"

Perform a simulated SERP analysis:

PART A — List 4 typical H2 headings that top-ranking competitor articles would use for this keyword. Label them "Competitor Headings".

PART B — Identify 3 unique angles or H2 headings that competitors likely MISS. These should be genuine content gaps that would differentiate a blog post. Label them "SERP Gap Angles".

Format:
## Competitor Headings
1. ...
2. ...
3. ...
4. ...

## SERP Gap Angles
1. ...
2. ...
3. ...

Output ONLY the above — no preamble, no explanations.
"""
    return call_groq(client, model, prompt)


def step3_outline(client, model, keyword, location, tone, keyword_cluster, serp_gap):
    """Step 3 — Blog outline incorporating SERP gaps."""
    prompt = f"""
You are a content strategist for Blogy, India's leading AI blog automation platform.

Primary keyword: "{keyword}"
Target location: "{location}"
Blog tone: {tone}
Keyword cluster: {keyword_cluster}
SERP gap analysis: {serp_gap}

Create a detailed blog outline:

Rules:
- Title: SEO-optimized, contains the primary keyword, MAX 65 characters
- Meta Description: MAX 155 characters, contains keyword, includes a CTA
- H1: Same as the title
- Exactly 7 H2 headings — at least 2 must come from the SERP Gap Angles
- The last H2 MUST be "Frequently Asked Questions"
- Headings should feel natural and incorporate LSI keywords where appropriate

Format EXACTLY like this:
Title: [title]
Meta Description: [meta description]
H1: [same as title]

1. [H2 heading]
2. [H2 heading]
3. [H2 heading]
4. [H2 heading]
5. [H2 heading]
6. [H2 heading]
7. Frequently Asked Questions

Output ONLY the outline. No explanations.
"""
    return call_groq(client, model, prompt)


def step4_full_blog(client, model, keyword, location, tone, outline, keyword_cluster):
    """Step 4 — Generate the full blog post (1,500-2,000 words)."""
    prompt = f"""
You are a professional blog writer for Blogy, an AI blog automation platform based in {location}.

Primary keyword: "{keyword}"
Target location: "{location}"
Blog tone: {tone}
Keyword cluster (use at least 3 of these naturally): {keyword_cluster}
Outline to follow: {outline}

Write the COMPLETE blog post following these STRICT rules:

1. Word count: 1,500-2,000 words
2. Include the primary keyword "{keyword}" in:
   - The title (H1)
   - The first 100 words
   - At least 3 of the H2 headings
   - The conclusion
3. Keyword density: 1-2.5% (use the keyword naturally, not stuffed)
4. The FIRST PARAGRAPH must be a concise 40-60 word definition/answer — this is optimized for Google's featured snippet
5. Use **bold text** for key terms and important phrases
6. Include at least one {location}-specific statistic, example, or reference (GEO signal)
7. End each section with a natural transition sentence leading to the next section
8. Each paragraph: 60-120 words max
9. Use markdown formatting: # for H1, ## for H2
10. Do NOT include the FAQ section — that will be generated separately
11. Write only sections 1-6 from the outline (skip the FAQ heading)

Output ONLY the blog post in markdown. No preamble.
"""
    return call_groq(client, model, prompt)


def step5_faq(client, model, keyword, location, title):
    """Step 5 — Generate FAQ section + JSON-LD schema."""
    prompt = f"""
You are an SEO expert for Blogy.

Blog title: "{title}"
Primary keyword: "{keyword}"
Target location: "{location}"

Write a FAQ section with exactly 5 question-and-answer pairs.

Rules:
- Q1 MUST contain the primary keyword "{keyword}"
- Each answer: 40-80 words, conversational, factually grounded
- At least one answer should mention {location}
- Format for display:

## Frequently Asked Questions

**Q1: [Question containing the keyword]**
A: [Answer]

**Q2: [Question]**
A: [Answer]

**Q3: [Question]**
A: [Answer]

**Q4: [Question]**
A: [Answer]

**Q5: [Question]**
A: [Answer]

---

Now ALSO output the FAQ Schema JSON-LD block separately, wrapped in a code block labeled ```json.
The JSON-LD must use "@type": "FAQPage" with "mainEntity" containing each Q&A as a "Question" type.

Output the FAQ markdown FIRST, then a separator "---", then the JSON-LD code block. No other text.
"""
    return call_groq(client, model, prompt)


def step6_cta(client, model, keyword):
    """Step 6 — Generate CTA section."""
    prompt = f"""
You are a conversion copywriter for Blogy — India's leading AI blog automation platform.

Primary keyword: "{keyword}"

Write a 3-sentence closing CTA paragraph that:
1. References "Blogy" by name
2. Uses urgency or value language (e.g. "Don't miss out", "Transform your content strategy")
3. Contains one strong action verb (Start, Try, Discover, Unlock, etc.)

Keep it punchy, persuasive, and natural. Output ONLY the 3 sentences. No heading, no preamble.
"""
    return call_groq(client, model, prompt)


# ──────────────────────────────────────────────────────────────
# 4.  SEO VALIDATION ENGINE
# ──────────────────────────────────────────────────────────────

def step7_seo_report(blog_text: str, keyword: str, lsi_keywords: list) -> dict:
    """
    Step 7 — Compute a structured SEO validation report.
    Pure Python, no API call needed.
    """
    kw_lower  = keyword.lower()
    txt_low   = blog_text.lower()
    lines     = blog_text.splitlines()
    words     = blog_text.split()
    word_count = len(words)

    # --- Keyword in title ---
    title_line = next((l for l in lines if l.startswith("# ")), "")
    kw_in_title = kw_lower in title_line.lower()

    # --- Keyword density ---
    freq    = txt_low.count(kw_lower)
    density = (freq / word_count * 100) if word_count else 0

    # --- H2 count ---
    h2_lines = [l for l in lines if l.startswith("## ")]
    h2_count = len(h2_lines)

    # --- Keyword in H2s ---
    kw_h2_count = sum(1 for h in h2_lines if kw_lower in h.lower())

    # --- Featured snippet paragraph (first real paragraph) ---
    first_para = ""
    in_content = False
    for l in lines:
        stripped = l.strip()
        if stripped.startswith("# "):
            in_content = True
            continue
        if in_content and stripped and not stripped.startswith("#"):
            first_para = stripped
            break
    first_para_wc = len(first_para.split()) if first_para else 0
    snippet_ok = 30 <= first_para_wc <= 70

    # --- LSI keywords used ---
    lsi_used = [kw for kw in lsi_keywords if kw.lower() in txt_low]

    # --- GEO signal ---
    geo_terms = ["india", "indian", "bharat", "mumbai", "delhi", "bangalore",
                 "bengaluru", "hyderabad", "chennai", "kolkata", "pune",
                 "₹", "crore", "lakh"]
    geo_present = any(term in txt_low for term in geo_terms)

    # --- FAQ count ---
    faq_count = len(re.findall(r"\*\*Q\d+:", blog_text))

    # --- CTA present ---
    cta_present = "blogy" in txt_low

    # --- Bold text usage ---
    bold_count = len(re.findall(r"\*\*[^*]+\*\*", blog_text))

    # --- Naturalness score (1-10) ---
    paragraphs = [p.strip() for p in blog_text.split("\n\n")
                  if p.strip() and not p.strip().startswith("#")]
    if paragraphs:
        lengths = [len(p.split()) for p in paragraphs]
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        std_dev = variance ** 0.5
        # Good variance = 10-40 std dev
        if 10 <= std_dev <= 40:
            nat_score = 8
        elif 5 <= std_dev < 10 or 40 < std_dev <= 60:
            nat_score = 6
        else:
            nat_score = 4

        # Bonus for reasonable paragraph lengths
        reasonable = sum(1 for l in lengths if 40 <= l <= 130)
        ratio = reasonable / len(lengths)
        if ratio >= 0.7:
            nat_score = min(10, nat_score + 2)
        elif ratio >= 0.4:
            nat_score = min(10, nat_score + 1)
    else:
        nat_score = 3

    # --- SEO Score calculation ---
    score = 0
    score += 10 if kw_in_title else 0
    if 1.0 <= density <= 2.5:
        score += 15
    elif 0.5 <= density < 1.0 or 2.5 < density <= 4.0:
        score += 8
    elif freq > 0:
        score += 3

    if h2_count >= 6:
        score += 12
    elif h2_count >= 4:
        score += 8
    elif h2_count >= 2:
        score += 4

    score += min(kw_h2_count * 3, 9)  # up to 9 pts for keyword in H2s

    score += 8 if snippet_ok else 0

    score += min(len(lsi_used) * 3, 12)  # up to 12 pts

    score += 8 if geo_present else 0

    if faq_count >= 5:
        score += 10
    elif faq_count >= 3:
        score += 6

    score += 6 if cta_present else 0

    if word_count >= 1500:
        score += 10
    elif word_count >= 800:
        score += 6
    elif word_count >= 400:
        score += 3

    # --- Suggestions ---
    suggestions = []
    if not kw_in_title:
        suggestions.append("Add the primary keyword to the H1 title.")
    if density < 1.0:
        suggestions.append(f"Keyword density is {density:.1f}% — increase natural usage of \"{keyword}\".")
    elif density > 2.5:
        suggestions.append(f"Keyword density is {density:.1f}% — reduce usage to avoid over-optimization.")
    if not snippet_ok:
        suggestions.append(f"First paragraph is {first_para_wc} words — aim for 40-60 words for featured snippet eligibility.")
    if not geo_present:
        suggestions.append("Add an India-specific statistic or example for stronger GEO signals.")
    if len(lsi_used) < 3:
        suggestions.append("Use more LSI keywords from the cluster to strengthen topical relevance.")
    if h2_count < 6:
        suggestions.append("Add more H2 sub-headings to improve content structure.")
    if faq_count < 5:
        suggestions.append("Ensure the FAQ section has at least 5 Q&A pairs.")
    if bold_count < 5:
        suggestions.append("Use more **bold text** to highlight key terms for scannability.")
    if word_count < 1500:
        suggestions.append(f"Word count is {word_count} — aim for 1,500+ words for stronger ranking.")
    # Trim to 3
    suggestions = suggestions[:3]
    if not suggestions:
        suggestions = ["Your blog is well-optimized! Consider A/B testing headlines for CTR."]

    return {
        "kw_in_title": kw_in_title,
        "density": round(density, 2),
        "word_count": word_count,
        "h2_count": h2_count,
        "kw_in_h2s": kw_h2_count,
        "snippet_ok": snippet_ok,
        "first_para_wc": first_para_wc,
        "lsi_used": lsi_used,
        "geo_present": geo_present,
        "faq_count": faq_count,
        "cta_present": cta_present,
        "score": min(score, 100),
        "naturalness": nat_score,
        "suggestions": suggestions,
    }


# ──────────────────────────────────────────────────────────────
# 5.  UI HELPERS
# ──────────────────────────────────────────────────────────────

def render_seo_report(report: dict) -> None:
    """Render the SEO validation report as a visual card."""
    total = report["score"]

    if total >= 80:
        cls, emoji, label = "great", "🟢", "Excellent SEO"
    elif total >= 55:
        cls, emoji, label = "good", "🟡", "Needs Improvement"
    else:
        cls, emoji, label = "poor", "🔴", "Poor SEO"

    st.markdown(f"""
    <div class="seo-card {cls}">
        <div class="seo-score-num">{total}<span style="font-size:1.4rem">/100</span></div>
        <div class="seo-label">{emoji} {label}</div>
    </div>
    """, unsafe_allow_html=True)

    fields = [
        ("Keyword in Title", "YES" if report["kw_in_title"] else "NO"),
        ("Keyword Density", f"{report['density']}%"),
        ("Word Count", str(report["word_count"])),
        ("H2 Headings", str(report["h2_count"])),
        ("Keyword in H2s", str(report["kw_in_h2s"])),
        ("Featured Snippet Para", f"{'YES' if report['snippet_ok'] else 'NO'} ({report['first_para_wc']} words)"),
        ("LSI Keywords Used", str(len(report["lsi_used"]))),
        ("GEO Signal", "YES" if report["geo_present"] else "NO"),
        ("FAQ Count", str(report["faq_count"])),
        ("CTA Present", "YES" if report["cta_present"] else "NO"),
        ("Naturalness Score", f"{report['naturalness']}/10"),
    ]

    st.markdown("**📋 SEO Validation Report**")
    for label_text, value in fields:
        color = "#15803d" if value.startswith("YES") or value.startswith("8") or value.startswith("9") or value.startswith("10") else "#1d4ed8"
        st.markdown(f"""
        <div class="report-field">
            <span>{label_text}</span>
            <span class="report-val" style="color:{color}">{value}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**💡 Improvement Suggestions**")
    for s in report["suggestions"]:
        st.markdown(f"- {s}")


def parse_lsi_keywords(cluster_text: str) -> list:
    """Extract individual keywords from the numbered cluster list."""
    keywords = []
    for line in cluster_text.splitlines():
        line = line.strip()
        match = re.match(r"^\d+[\.\)]\s*(.+)", line)
        if match:
            kw = match.group(1).strip().strip('"').strip("'")
            keywords.append(kw)
    return keywords


def extract_title(outline: str) -> str:
    """Extract the title from the outline."""
    for line in outline.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("title:"):
            return stripped.split(":", 1)[1].strip()
    return "Blog Post"


def extract_meta_desc(outline: str) -> str:
    """Extract the meta description from the outline."""
    for line in outline.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("meta description:"):
            return stripped.split(":", 1)[1].strip()
    return ""


def split_faq_and_schema(faq_response: str) -> tuple:
    """Split the FAQ response into markdown and JSON-LD schema."""
    # Try to find JSON block
    json_match = re.search(r"```json\s*\n(.*?)```", faq_response, re.DOTALL)
    if json_match:
        schema_str = json_match.group(1).strip()
        faq_md = faq_response[:json_match.start()].strip()
        # Clean trailing separators
        faq_md = re.sub(r"\n---\s*$", "", faq_md).strip()
        return faq_md, schema_str
    return faq_response, ""


# ──────────────────────────────────────────────────────────────
# 6.  MAIN APP
# ──────────────────────────────────────────────────────────────

def main() -> None:

    # Page header
    st.markdown('<div class="hero-title">✍️ Blogy — AI Blog Automation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">India\'s leading AI blog platform · 7-step SEO pipeline · Powered by Groq</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────
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
            help="Choose the Groq-hosted model to use.",
        )

        st.markdown("---")
        target_location = st.text_input(
            "📍  Target Location",
            value="India",
            help="Location for GEO-optimized content.",
        )

        blog_tone = st.selectbox(
            "🎨  Blog Tone",
            options=TONE_OPTIONS,
            index=0,
            help="Sets the writing style for the generated blog.",
        )

        st.markdown("---")
        st.markdown("**Common Fixes**")
        st.markdown("""
- **401 Unauthorized** → check your API key
- **Rate limit** → wait a moment, Groq has generous free-tier limits
- **ModuleNotFoundError** → run `pip install -r requirements.txt`
        """)

    # ── Main area inputs ──────────────────────────────────────
    col_kw, _ = st.columns([3, 1])
    with col_kw:
        keyword = st.text_input(
            "🔑  Primary Keyword",
            placeholder='e.g. "AI content writing tools India"',
            help="Primary keyword for the 7-step SEO blog pipeline.",
        )

    generate_btn = st.button("🚀  Generate Blog", type="primary")

    # ── Generation pipeline ───────────────────────────────────
    if generate_btn:
        if not keyword.strip():
            st.warning("Please enter a keyword first.")
            st.stop()

        client, model_name = init_groq(api_key_input, selected_model)
        if client is None:
            st.stop()

        st.sidebar.markdown(
            f"**Active model:** <span class='model-pill'>{model_name}</span>",
            unsafe_allow_html=True,
        )

        # Live-update containers
        status_bar = st.empty()
        step1_exp = st.expander("🔍  Step 1 — Keyword Cluster", expanded=False)
        step2_exp = st.expander("📊  Step 2 — SERP Gap Analysis", expanded=False)
        step3_exp = st.expander("📋  Step 3 — Blog Outline", expanded=False)
        step4_exp = st.expander("✍️  Step 4 — Full Blog Content", expanded=False)
        step5_exp = st.expander("❓  Step 5 — FAQ Section", expanded=False)
        step6_exp = st.expander("📣  Step 6 — CTA Section", expanded=False)

        try:
            # ── Step 1: Keyword Cluster ───────────────────────
            status_bar.info("⏳  Step 1/7 — Generating keyword cluster…")
            with st.spinner("Researching LSI keywords…"):
                cluster_text = step1_keyword_cluster(client, model_name, keyword, target_location)
            with step1_exp:
                st.markdown(cluster_text)
            lsi_keywords = parse_lsi_keywords(cluster_text)

            # ── Step 2: SERP Gap Analysis ─────────────────────
            status_bar.info("⏳  Step 2/7 — Analyzing SERP gaps…")
            with st.spinner("Simulating competitor analysis…"):
                serp_gap = step2_serp_gap(client, model_name, keyword, target_location)
            with step2_exp:
                st.markdown(serp_gap)

            # ── Step 3: Outline ───────────────────────────────
            status_bar.info("⏳  Step 3/7 — Creating blog outline…")
            with st.spinner("Structuring the outline…"):
                outline = step3_outline(client, model_name, keyword, target_location, blog_tone, cluster_text, serp_gap)
            with step3_exp:
                st.code(outline, language=None)

            blog_title = extract_title(outline)
            meta_desc = extract_meta_desc(outline)

            # ── Step 4: Full Blog ─────────────────────────────
            status_bar.info("⏳  Step 4/7 — Writing full blog post (this takes a moment)…")
            with st.spinner("Crafting 1,500-2,000 words…"):
                blog_body = step4_full_blog(client, model_name, keyword, target_location, blog_tone, outline, cluster_text)
            with step4_exp:
                st.markdown(blog_body)

            # ── Step 5: FAQ + Schema ──────────────────────────
            status_bar.info("⏳  Step 5/7 — Generating FAQ & schema…")
            with st.spinner("Building FAQ section…"):
                faq_raw = step5_faq(client, model_name, keyword, target_location, blog_title)
            faq_md, faq_schema = split_faq_and_schema(faq_raw)
            with step5_exp:
                st.markdown(faq_md)

            # ── Step 6: CTA ───────────────────────────────────
            status_bar.info("⏳  Step 6/7 — Writing CTA…")
            with st.spinner("Crafting the call-to-action…"):
                cta_text = step6_cta(client, model_name, keyword)
            with step6_exp:
                st.markdown(cta_text)

            # ── Step 7: Assemble & Score ──────────────────────
            status_bar.info("⏳  Step 7/7 — Running SEO validation…")
            time.sleep(0.3)

            # Assemble final blog
            final_blog = blog_body.strip()
            final_blog += f"\n\n{faq_md}"
            final_blog += f"\n\n---\n\n{cta_text}"

            seo_report = step7_seo_report(final_blog, keyword, lsi_keywords)

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

        # ── Output ────────────────────────────────────────────
        st.markdown("---")
        col_blog, col_seo = st.columns([2, 1], gap="large")

        with col_blog:
            st.subheader("📄  Generated Blog")

            if meta_desc:
                st.markdown(
                    f"<small style='color:#6b7280'><b>Meta Description:</b> {meta_desc}</small>",
                    unsafe_allow_html=True,
                )

            st.markdown(final_blog)

            st.download_button(
                label="⬇️  Download Blog (.txt)",
                data=final_blog,
                file_name=f"{keyword.replace(' ', '_')}_blog.txt",
                mime="text/plain",
            )

        with col_seo:
            st.subheader("📊  SEO Validation Report")
            render_seo_report(seo_report)

            if faq_schema:
                st.markdown("---")
                st.subheader("🔗  FAQ JSON-LD Schema")
                st.code(faq_schema, language="json")

    else:
        # Idle state
        st.info("👆  Enter a keyword and click **Generate Blog** to start.")
        st.markdown("""
**Blogy 7-Step Pipeline:**
1. 🔍  **Keyword Cluster** — 6-8 LSI & long-tail keywords
2. 📊  **SERP Gap Analysis** — competitor headings & content gaps
3. 📋  **Blog Outline** — title, meta description, 7 H2s
4. ✍️  **Full Blog** — 1,500-2,000 word SEO-optimized post
5. ❓  **FAQ Section** — 5 Q&As + JSON-LD schema
6. 📣  **CTA Section** — conversion-focused closing
7. 📊  **SEO Report** — full validation with score & tips
        """)


# ──────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()