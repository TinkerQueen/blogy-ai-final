# 🚀 Blogy — AI Blog Automation Platform

An advanced AI-powered blog generation engine that transforms a single keyword into a fully structured, SEO-optimized blog using a **7-step intelligent pipeline**.

Built with Groq API for ultra-fast inference and a modular backend architecture.

---

## 🧠 Core Features

- ✨ AI-powered blog generation using Groq (LLaMA / Mixtral models)
- ⚙️ 7-step automated SEO pipeline:
  1. Keyword Clustering (LSI + long-tail)
  2. SERP Gap Analysis
  3. Blog Outline Generation
  4. Full Blog Content (1500–2000 words)
  5. FAQ + JSON-LD Schema
  6. CTA Generation
  7. SEO Validation Report
- 📊 Advanced SEO scoring engine (0–100)
- 📍 GEO optimization (location-based content)
- 🧩 Modular backend architecture
- 🎨 Custom frontend (React + Vite + Tailwind)

---

## ⚙️ Tech Stack

### 🖥️ Frontend
- React (Vite)
- Tailwind CSS
- TypeScript

### ⚙️ Backend
- Python
- Streamlit (for prototyping)
- Modular pipeline architecture

### 🤖 AI
- Groq API
- Models:
  - llama-3.3-70b-versatile
  - mixtral-8x7b
  - gemma2-9b

---

## 🧩 System Architecture
User Input (Keyword)
↓
Step 1: Keyword Cluster (LSI keywords)
↓
Step 2: SERP Gap Analysis
↓
Step 3: SEO Blog Outline
↓
Step 4: Full Blog Generation
↓
Step 5: FAQ + Schema Markup
↓
Step 6: CTA Generation
↓
Step 7: SEO Validation Engine
↓
Final Blog + SEO Score


---

## 📊 SEO Validation Engine

The system evaluates blog quality using:

- Keyword in title
- Keyword density (1–2.5%)
- H2 structure & keyword placement
- Featured snippet optimization
- LSI keyword usage
- GEO signals (India-based context)
- FAQ completeness
- CTA presence
- Content length
- Naturalness score

---

## 📦 Installation

### 1. Clone repo
```
git clone https://github.com/TinkerQueen/DTU-project.git
cd DTU-project
```
### Backend setup:
```
pip install -r requirements.txt
```
### Create .env file:
```
GROQ_API_KEY=your_api_key_here
```
### Run backend:
```
python -m streamlit run app.py
```
### Frontend setup
```
cd frontend
npm install
npm run dev
```
## ▶️ Usage
Enter a keyword

Select:

Model

Location

Tone

Click Generate Blog

Get:

Full blog

FAQ + schema

SEO score

## 🧪 Example
Input:

AI blog tools India
Output:

1500+ word blog

SEO score (e.g. 82/100)

Structured content + FAQ + CTA

## 🏁 Conclusion
Blogy is not just a content generator — it is a complete SEO-aware content automation system that combines AI generation with structured optimization logic.
