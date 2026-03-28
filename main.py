import os
import re
import time
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Blogy AI API")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── GROQ CONFIG ──────────────────────────────────────────────
client = None
if os.getenv("GROQ_API_KEY"):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── REQUEST MODELS ───────────────────────────────────────────
class BaseRequest(BaseModel):
    keyword: str
    location: str = "India"
    tone: str = "Professional"
    model: str = "llama-3.3-70b-versatile"
    api_key: Optional[str] = None

class OutlineRequest(BaseRequest):
    cluster: str = ""
    serp: str = ""

class FullBlogRequest(BaseRequest):
    outline: str = ""
    cluster: str = ""

class FaqRequest(BaseRequest):
    title: str = ""

class SeoReportRequest(BaseRequest):
    blog_text: str = ""
    cluster: str = ""

# ── HELPERS ───────────────────────────────────────────────────
def call_groq(model: str, prompt: str, user_api_key: Optional[str] = None) -> str:
    if user_api_key:
        target_client = Groq(api_key=user_api_key)
    else:
        target_client = client

    if not target_client:
        raise HTTPException(status_code=401, detail="Groq API key missing. Set GROQ_API_KEY in .env or provide one.")

    try:
        chat_completion = target_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a world-class SEO blog writer and content strategist for Blogy, India's leading AI blog automation platform."},
                {"role": "user", "content": prompt},
            ],
            model=model,
            temperature=0.7,
            max_tokens=4096,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")

# ── ENDPOINTS ─────────────────────────────────────────────────

@app.post("/api/keyword-cluster")
async def keyword_cluster(req: BaseRequest):
    prompt = f"""Generate a keyword cluster of 6-8 semantically related LSI keywords for "{req.keyword}" in "{req.location}". Include long-tail variants and location-modified terms. Output as a numbered list only."""
    result = call_groq(req.model, prompt, req.api_key)
    return {"result": result}

@app.post("/api/serp-gap")
async def serp_gap(req: BaseRequest):
    prompt = f"""Perform a SERP gap analysis for "{req.keyword}" in "{req.location}". Identify 4 typical competitor H2s and 3 unique content gaps. Format: ## Competitor Headings \n 1... ## SERP Gap Angles \n 1..."""
    result = call_groq(req.model, prompt, req.api_key)
    return {"result": result}

@app.post("/api/outline")
async def outline(req: OutlineRequest):
    prompt = f"Create a detailed blog outline for '{req.keyword}' in '{req.location}' with tone '{req.tone}'. Use these LSI keywords: {req.cluster}. Incorporate these SERP gaps: {req.serp}. Title, Meta Description, H1, and exactly 7 H2s (last one FAQ). Output outline only."
    result = call_groq(req.model, prompt, req.api_key)
    return {"result": result}

@app.post("/api/full-blog")
async def full_blog(req: FullBlogRequest):
    prompt = f"Write a 1,500-2,000 word blog for '{req.keyword}' using this outline: {req.outline}. Incorporate 3 keywords from: {req.cluster}. Include a featured snippet definition (40-60 words) first. Use markdown. Skip FAQ."
    result = call_groq(req.model, prompt, req.api_key)
    return {"result": result}

@app.post("/api/faq")
async def faq(req: FaqRequest):
    prompt = f"Write 5 Q&A pairs for '{req.keyword}' (title: {req.title}) and a JSON-LD FAQ schema. Output FAQ markdown, then '---', then JSON-LD in a code block."
    result = call_groq(req.model, prompt, req.api_key)
    return {"result": result}

@app.post("/api/cta")
async def cta(req: BaseRequest):
    prompt = f"Write a 3-sentence conversion CTA for Blogy using the keyword '{req.keyword}'. Persuasive and natural. Output only sentences."
    result = call_groq(req.model, prompt, req.api_key)
    return {"result": result}

@app.post("/api/seo-report")
async def seo_report(req: SeoReportRequest):
    kw_lower = req.keyword.lower()
    txt_low = req.blog_text.lower()
    words = req.blog_text.split()
    word_count = len(words)

    score = 70
    if kw_lower in txt_low: score += 10
    if word_count > 1000: score += 10
    if "faq" in txt_low: score += 10

    density = round((txt_low.count(kw_lower) / word_count * 100), 2) if word_count else 0

    return {
        "score": min(score, 100),
        "word_count": word_count,
        "density": density,
        "suggestions": [
            "Add more context to H2s",
            "Increase keyword usage in conclusion",
            "Add internal linking to related topics",
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
