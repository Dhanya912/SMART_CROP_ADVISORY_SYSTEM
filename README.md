# 🌾 Smart Crop Advisory System — Full Project

**Multi-Agent Agentic AI for Sustainable Agriculture**
Yenepoya Institute of Technology, Moodbidri | Dept. of CSE

---

## Team
Dhanyashree | Mahe Riza | Khushi C S | Archana M Naik
Guide: Dr. Sangamesh C J

---

## Features
- ✅ User Register / Login / Session Management
- ✅ 7 AI Agents + Chatbot: Crop, Disease, Weather, Soil, Market, Policy, Report, **Chatbot**
- ✅ Random Forest crop recommendation — **now trained on the real `data/crop_recommendation.csv` dataset** (2,200 rows, 22 crops, ~90%+ accuracy)
- ✅ ResNet-50 CNN disease detection — demo-mode heuristic classifier, taxonomy auto-broadened to 39 classes from `data/plant_disease.csv`
- ✅ Real-time weather (OpenWeatherMap) with **dataset-grounded offline fallback** (`data/weather_advisory.csv`) instead of pure random mock
- ✅ Market prices computed from `data/market_prices.csv` (real per-crop min/avg/max + mandi lists), not a small hardcoded table
- ✅ Government schemes & MSP loaded live from `data/government_schemes.csv` + `data/government_msp.csv`
- ✅ **Full multi-language advisory reports — English, Kannada, Tamil, Hindi, Telugu** (on-screen + PDF), not just an English/Tamil bolt-on
- ✅ **Floating chatbot assistant** on every page — quick-reply chips + free text, answers using YOUR last saved advisory, in all 5 languages
- ✅ **PDF Download** of advisory report, with Indic-script font support
- ✅ Complete advisory history saved per user
- ✅ Searchable history table with detail modal
- ✅ User profile management

---

## What changed from the previous version

| Area | Before | Now |
|---|---|---|
| Crop model | `sklearn.make_classification` synthetic data | Trained on real `crop_recommendation.csv` (2,200 rows) |
| Weather fallback | Pure random mock | Grounded in `weather_advisory.csv` by state/city |
| Market prices | ~16 hardcoded price ranges | Computed live from `market_prices.csv` (3,000 rows) — also **fixed a bug** where market analysis always ran for a generic "general" crop instead of the actually recommended crop |
| Govt schemes / MSP | 6 hardcoded schemes, 13 MSP values | Loaded from `government_schemes.csv` (17 schemes) + `government_msp.csv` (26 crops) |
| Disease taxonomy | 11 hardcoded classes | Auto-broadened to 39 using `plant_disease.csv` |
| Language | English, or a bolted-on Tamil paragraph (in Helvetica — didn't actually render Tamil glyphs) | Full report + PDF in English/Kannada/Tamil/Hindi/Telugu with proper Indic font embedding |
| Chatbot | None | Floating assistant, rule-based (zero config) + optional Gemini upgrade, uses your last saved advisory as context |

**Scope note:** the advisory report + chatbot are fully localized. The rest of the site chrome (nav, dashboard, buttons, forms) stays in English — that's what was asked for and keeps the change manageable. Government scheme names/benefits are shown in their original English wording (sourced from your CSV) with translated field labels (Benefit/Eligibility/etc.) rather than machine-translating official scheme text.

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. (Recommended, one-time, needs internet) fetch Indic fonts for PDF export
```bash
python fetch_fonts.py
```
Without this, PDFs still generate correctly, but non-English scripts show a "please run fetch_fonts.py" notice instead of Kannada/Tamil/Hindi/Telugu glyphs.

### 3. (Optional) Set API keys
```bash
# Windows
set OPENWEATHER_API_KEY=your_key
set GEMINI_API_KEY=your_key

# Mac/Linux
export OPENWEATHER_API_KEY=your_key
export GEMINI_API_KEY=your_key
```
*System works fully without API keys — weather uses the dataset-grounded fallback, and the chatbot uses its built-in rule-based matcher instead of Gemini.*

### 4. Run
```bash
python app.py
```

### 5. Open browser
```
http://localhost:5000
```
Register → Dashboard → Get Advisory (pick your language) → Download PDF → View History → try the chat bubble bottom-right on any page.

---

## Project Structure
```
smart_crop_advisory/
├── app.py                  Flask app — all routes (+ /api/chat, /api/chat/chips)
├── database.py             SQLite3 — users, sessions, history
├── auth.py                 Login/session decorators
├── pdf_report.py           Multilingual PDF generation with ReportLab + Indic fonts
├── i18n.py                 Central translation module (labels, crop names, templates)
├── fetch_fonts.py          One-time Indic font downloader
├── requirements.txt
├── README.md
├── data/                   crop_recommendation.csv, weather_advisory.csv, market_prices.csv,
│                           government_schemes.csv, government_msp.csv, plant_disease.csv,
│                           soil_health.csv, advisory_log.csv, DATASET_README.md
├── fonts/                  Populated by fetch_fonts.py
├── agents/
│   ├── orchestrator.py     Coordinates 7 agents + chatbot (parallel where possible)
│   ├── crop_agent.py       Random Forest ML — trained on data/crop_recommendation.csv
│   ├── disease_agent.py    ResNet-50-style CNN (demo mode; extended taxonomy from CSV)
│   ├── weather_agent.py    OpenWeatherMap API + dataset-grounded fallback
│   ├── soil_agent.py       NPK/pH analysis + fertiliser plan (i18n)
│   ├── market_agent.py     Price stats from data/market_prices.csv + income estimator
│   ├── policy_agent.py     Govt schemes + MSP from data/*.csv
│   ├── report_agent.py     Full multilingual report assembly
│   └── chatbot_agent.py    Rule-based assistant + optional Gemini upgrade
├── models/                 crop_rf.pkl (auto-generated on first run)
├── data/cropai.db          (auto-created)
├── static/
│   ├── css/style.css       + chatbot widget styles (appended)
│   ├── js/main.js          Advisory form + report renderer + PDF
│   ├── js/dashboard.js     Individual agent testers
│   └── js/chatbot.js       Chat widget logic
└── templates/
    ├── base.html, landing.html, auth.html, dashboard.html,
    ├── advisory.html       Full advisory form (5-language selector)
    ├── history.html, profile.html
    └── partials/navbar.html   Includes the chatbot widget (shown on every logged-in page)
```

## API Endpoints
| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| POST | /api/auth/register | No | Register user |
| POST | /api/auth/login | No | Login |
| GET | /api/auth/me | No | Check session |
| PUT | /api/auth/profile | Yes | Update profile |
| POST | /api/full-advisory | Yes | Run all 7 agents + save |
| GET | /api/download-pdf/<id> | Yes | Download advisory as PDF |
| POST | /api/download-latest-pdf | Yes | Download in-memory report as PDF |
| POST | /api/recommend-crop | Yes | Crop agent only |
| POST | /api/detect-disease | Yes | Disease agent only |
| POST/GET | /api/weather | Yes | Weather agent only |
| POST | /api/soil-health | Yes | Soil agent only |
| POST | /api/market-prices | Yes | Market agent only |
| POST/GET | /api/policy | Yes | Policy agent only |
| POST | /api/chat | Yes | Chatbot — send a message, get a localized reply |
| GET | /api/chat/chips | Yes | Chatbot quick-reply suggestions in the given language |
| GET | /api/history | Yes | Past advisories list |
| GET | /api/history/<id> | Yes | Advisory detail |
| GET | /api/stats | Yes | User statistics |
| GET | /api/health | No | Server health check |

---

## Animated UI update (v2)

The interface now has a full motion layer. Nothing in the Python code, agents,
routes or data files was changed — only presentation.

**New files**
- `static/css/animations.css` — all keyframes, entrance, hover and loading styles
- `static/js/animations.js` — scroll reveal, number count-up, ripples, floating leaves,
  scroll progress bar, back-to-top button, drag-and-drop highlight, busy button states

**Changed file**
- `templates/base.html` — links the two files above (every page inherits them)

**What you'll see**
- Landing page: slow-shifting green gradient, glowing hero light, blur-in headline,
  shimmering gold text, drifting leaves, staggered feature strip, count-up statistics
- Auth: animated split panel, cascading bullets, pop-in card, focus glow on fields
- Dashboard: cards fade up one by one, lift on hover, icons tilt, stats count up
- Advisory: sections stagger in, drag-and-drop upload highlight, submit button busy state
- Report: score circle pops, confidence bars grow, action-plan items slide in
- History: rows cascade in, modal opens with blurred backdrop and rotating close button
- Global: page fade-in, scroll progress bar, back-to-top button, button ripples

**Accessibility** — all motion is disabled automatically for visitors with
"reduce motion" enabled in their operating system.

Run exactly as before: `pip install -r requirements.txt` then `python app.py`
