# 📊 Retention Intelligence Dashboard

> Executive-grade Streamlit dashboard for AI-powered customer retention risk scoring and strategic intervention planning.

🔗 **Live App**: https://sentiment-dashboard-f8agdbvg5epa4kt4etasaz.streamlit.app

---

##  Overview

This dashboard provides business leadership and customer success teams with a real-time retention intelligence interface. It translates raw behavioral signals into actionable, segment-specific retention strategies — no technical knowledge required.

---

##  Features

- **Customer Profiling** — Simple business-friendly intake form (no ML jargon)
- **AI Segmentation** — Classifies customers into one of 5 behavioral segments
- **Sentiment Detection** — Identifies customer tone (negative / neutral / positive)
- **Risk Scoring** — Computes a 0–100 retention risk score with urgency level
- **Action Plan** — Step-by-step intervention strategy tailored to the segment
- **Expected Outcome** — Projected results if the strategy is applied
- **Segment Portfolio** — Overview of all 5 customer segments and their risk levels
- **System Status** — Live API health check and model status

---

##  Customer Segments

| Segment | Name | Risk Level | Urgency |
|---|---|---|---|
| C0 | Satisfied Loyal Shoppers | 🟢 Low | Act within 30 days |
| C1 | Frustrated Complainers | 🟠 High | Act within 7 days |
| C2 | Neutral Browsers | 🟡 Medium | Act within 30 days |
| C3 | Impulsive Buyers | 🟠 High | Act within 7 days |
| C4 | Engaged Brand Advocates | 🔴 Critical | Act within 24 hours |

---

##  How It Works

Business User fills intake form
↓
Dashboard maps inputs to ML features
↓
Calls Live FastAPI endpoint (Render)
↓
Dual-head MLP returns segment + sentiment
↓
Dashboard renders risk score + action plan
---

##  Tech Stack

- **Frontend** — Streamlit 1.45.0
- **Charts** — Plotly
- **Backend** — FastAPI REST API (hosted on Render)
- **ML Model** — Dual-head MLP (PyTorch), trained on 100k reviews
- **Deployment** — Streamlit Cloud

---

##  Related

| Service | URL |
|---|---|
|  Live API | https://sentiment-api-8mdq.onrender.com/docs |
|  API Source Code | https://github.com/BennjimaTakwa/sentiment-api |
|  ML Notebooks | https://github.com/BennjimaTakwa/customer-retention-DL |

---

##  Project Structure
sentiment-dashboard/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
└── README.md
---

##  Authors

**Bennjimatakwa** · **MabroukYahya**  
Kaggle: https://www.kaggle.com/bennjimatakwa
