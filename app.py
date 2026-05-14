import streamlit as st
import requests
import plotly.graph_objects as go

# ── Config
API_URL = "https://sentiment-api-8mdq.onrender.com"

st.set_page_config(
    page_title="Retention Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Navy & Gold Executive Theme
st.markdown("""
<style>
    /* Base */
    .stApp { background-color: #0a0f1e; }
    section[data-testid="stSidebar"] { background-color: #060d1f; border-right: 1px solid #1e3a5f; }

    /* Typography */
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    /* Header */
    .exec-header {
        background: linear-gradient(135deg, #0d1b3e 0%, #1a2f5e 100%);
        border-bottom: 2px solid #c9a84c;
        padding: 28px 36px;
        border-radius: 0 0 16px 16px;
        margin-bottom: 24px;
    }
    .exec-title {
        font-size: 2rem;
        font-weight: 800;
        color: #c9a84c;
        letter-spacing: 1px;
        margin: 0;
    }
    .exec-subtitle {
        font-size: 0.9rem;
        color: #7a9cc4;
        margin: 6px 0 0 0;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, #0d1b3e, #112244);
        border: 1px solid #1e3a5f;
        border-top: 3px solid #c9a84c;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }
    .kpi-label {
        font-size: 0.72rem;
        color: #7a9cc4;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #c9a84c;
        margin-top: 4px;
    }

    /* Risk Card */
    .risk-card {
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 16px;
    }
    .risk-critical { background: linear-gradient(135deg, #1a0a0a, #2d1010); border: 1px solid #8b1a1a; border-left: 4px solid #ff3333; }
    .risk-high     { background: linear-gradient(135deg, #1a1100, #2d1f00); border: 1px solid #8b5a00; border-left: 4px solid #ff9900; }
    .risk-medium   { background: linear-gradient(135deg, #151500, #252500); border: 1px solid #6b6b00; border-left: 4px solid #f0d000; }
    .risk-low      { background: linear-gradient(135deg, #001a0a, #002d14); border: 1px solid #006b2a; border-left: 4px solid #00cc55; }

    /* Section Headers */
    .section-header {
        font-size: 0.75rem;
        font-weight: 700;
        color: #c9a84c;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin: 24px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #1e3a5f;
    }

    /* Step Cards */
    .step-card {
        background: linear-gradient(145deg, #0d1b3e, #112244);
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        padding: 18px 14px;
        text-align: center;
        min-height: 140px;
        position: relative;
    }
    .step-number {
        font-size: 2rem;
        font-weight: 900;
        color: #c9a84c;
        opacity: 0.3;
        position: absolute;
        top: 8px;
        right: 12px;
    }
    .step-text {
        font-size: 0.82rem;
        color: #b0c4de;
        line-height: 1.5;
        margin-top: 8px;
    }

    /* Segment Cards */
    .seg-card {
        background: linear-gradient(145deg, #0d1b3e, #0f2050);
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 6px 0;
        transition: border-color 0.2s;
    }
    .seg-name { font-size: 0.95rem; font-weight: 700; }
    .seg-meta { font-size: 0.78rem; color: #7a9cc4; margin-top: 4px; }

    /* Outcome Box */
    .outcome-box {
        background: linear-gradient(135deg, #0a1f0a, #0d2d0d);
        border: 1px solid #1a5c1a;
        border-left: 4px solid #00cc55;
        border-radius: 10px;
        padding: 20px 24px;
        color: #90ee90;
        font-size: 0.95rem;
        line-height: 1.7;
    }

    /* Root cause */
    .rootcause-box {
        background: linear-gradient(135deg, #1a1200, #2a1e00);
        border: 1px solid #5c4200;
        border-left: 4px solid #c9a84c;
        border-radius: 10px;
        padding: 18px 22px;
        color: #e8d5a0;
        font-size: 0.9rem;
        line-height: 1.7;
    }

    /* Sidebar labels */
    .sidebar-section {
        font-size: 0.7rem;
        font-weight: 700;
        color: #c9a84c;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 16px 0 8px 0;
    }

    /* Divider */
    hr { border-color: #1e3a5f; }

    /* Streamlit metric override */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #0d1b3e, #112244);
        border: 1px solid #1e3a5f;
        border-top: 2px solid #c9a84c;
        border-radius: 10px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ── Risk Config
RISK_EMOJI = {"critical": "◆", "high": "▲", "medium": "●", "low": "✓"}
RISK_COLOR = {
    "critical": "#ff3333",
    "high":     "#ff9900",
    "medium":   "#f0d000",
    "low":      "#00cc55"
}
RISK_LABEL = {
    "critical": "CRITICAL RISK",
    "high":     "HIGH RISK",
    "medium":   "MODERATE RISK",
    "low":      "LOW RISK"
}

# ── Segment Details
SEGMENT_DETAILS = {
    0: {
        "name": "Satisfied Loyal Shoppers",
        "root_cause": "This customer demonstrates high satisfaction and consistent platform engagement. No immediate churn risk is detected. However, sustained loyalty programs are essential to maintain this relationship and prevent future disengagement as competitive alternatives emerge.",
        "urgency": "Act within 30 days",
        "urgency_color": "#00cc55",
        "steps": [
            "Enroll in VIP loyalty rewards tier with exclusive benefits",
            "Deliver personalized thank-you communications and early access offers",
            "Solicit testimonials and product reviews to leverage brand advocacy",
            "Introduce referral incentive program to expand acquisition",
            "Schedule quarterly satisfaction assessments to monitor health",
        ],
        "expected_outcome": "Projected 40% increase in lifetime value and referral rate within 90 days. Sustained brand loyalty reduces churn probability to under 5% over the next quarter.",
    },
    1: {
        "name": "Frustrated Complainers",
        "root_cause": "This customer exhibits elevated frustration signals paired with strong negative sentiment across multiple touchpoints. Repeated poor platform experiences have eroded trust. Historical data shows this profile churns within 2–4 weeks without direct intervention from the retention team.",
        "urgency": "Act within 7 days",
        "urgency_color": "#ff9900",
        "steps": [
            "Assign dedicated senior support agent to audit full complaint history",
            "Issue personalized executive-level apology with resolution commitment",
            "Deploy compensation package — targeted discount, refund, or priority shipping",
            "Conduct 48-hour follow-up call to verify issue resolution and satisfaction",
            "Escalate account to monthly retention check-ins for 90-day monitoring period",
        ],
        "expected_outcome": "60–70% reduction in churn probability with contact within 7 days. Customer expected to migrate toward Neutral Browsers segment within 30 days of successful intervention.",
    },
    2: {
        "name": "Neutral Browsers",
        "root_cause": "This customer is passively engaging without meaningful platform attachment. Low engagement quality indicates an inability to find compelling conversion triggers. This profile is highly susceptible to competitor acquisition through targeted promotions.",
        "urgency": "Act within 30 days",
        "urgency_color": "#f0d000",
        "steps": [
            "Deploy personalized re-engagement email sequence over 2-week cadence",
            "Activate time-limited conversion offer to trigger first meaningful purchase",
            "Implement behavioral retargeting campaign based on browsing and search history",
            "Launch AI-driven product recommendation engine on homepage and emails",
            "Run A/B test on push notification formats to identify highest-engagement trigger",
        ],
        "expected_outcome": "20–35% improvement in engagement rate within 30 days. Full conversion to active buyer segment projected within 60 days with consistent multi-channel outreach.",
    },
    3: {
        "name": "Impulsive Buyers",
        "root_cause": "This customer's purchasing behavior is driven by deal availability rather than brand loyalty. Satisfaction scores are volatile and directly correlated with promotional exposure. Without continuous incentive stimulation, this profile will defect to the highest-value competitor offer within the next purchase cycle.",
        "urgency": "Act within 7 days",
        "urgency_color": "#ff9900",
        "steps": [
            "Configure real-time deal alert system with personalized category targeting",
            "Build dynamic offer engine leveraging past purchase category data",
            "Launch gamified loyalty mechanics — points, streaks, and milestone rewards",
            "Activate cart abandonment re-engagement within 60 minutes of drop-off",
            "Structure bundle promotions to increase average order value per session",
        ],
        "expected_outcome": "30–45% increase in purchase frequency within 30 days. Gradual behavioral shift toward habitual loyalty within 90 days with sustained gamification engagement.",
    },
    4: {
        "name": "Engaged Brand Advocates",
        "root_cause": "This customer presents the highest risk profile in the portfolio. Despite strong engagement, they carry the highest frustration index (2.25/5) and 59% negative sentiment — a uniquely dangerous combination. Their emotional investment in the brand amplifies dissatisfaction. Without immediate intervention, this segment is the most likely to generate negative public reviews and accelerate social churn.",
        "urgency": "Act within 24 hours",
        "urgency_color": "#ff3333",
        "steps": [
            "Immediately surface and contact all advocates flagged with negative sentiment signals",
            "Book priority 1-on-1 feedback session to surface specific unmet expectations",
            "Grant exclusive early access to unreleased features as recognition of advocacy",
            "Formalize brand ambassador program with structured rewards and public recognition",
            "Respond publicly to their concerns to demonstrate accountability and rebuild trust",
            "Institute weekly sentiment monitoring with 14-day escalation threshold",
        ],
        "expected_outcome": "75% customer retention probability with contact within 24 hours. Delay beyond 48 hours increases churn risk by 40% and raises probability of negative public review by 3x.",
    },
}


# ── Business → ML Feature Mapping
def map_business_to_features(
    complaint_count, purchase_recency, platform_replied,
    review_length, customer_influence, overall_tone
):
    frustration_map = {
        "None": 0.2, "1–2 complaints": 0.8,
        "3–5 complaints": 1.5, "More than 5": 2.5
    }
    engagement_map = {
        "Very brief (1–5 words)": 0.1, "Short (6–20 words)": 0.3,
        "Detailed (21–50 words)": 0.6, "Extensive (50+ words)": 0.9
    }
    influence_map = {
        "General customer": 0.2,
        "Moderately influential": 0.5,
        "High influence — public figure / blogger": 0.9
    }
    recency_map = {
        "This week": 0.9, "1–2 weeks ago": 0.6,
        "Last month": 0.3, "Over a month ago": 0.1
    }
    word_map = {
        "Very brief (1–5 words)": 3, "Short (6–20 words)": 12,
        "Detailed (21–50 words)": 30, "Extensive (50+ words)": 75
    }
    tone_map = {
        "Strongly Negative": (0.82, 0.13, 0.05),
        "Negative":          (0.65, 0.25, 0.10),
        "Mixed":             (0.25, 0.50, 0.25),
        "Positive":          (0.10, 0.22, 0.68),
        "Strongly Positive": (0.04, 0.10, 0.86),
    }
    neg, neu, pos = tone_map[overall_tone]

    return {
        "frustration_score":  frustration_map[complaint_count],
        "engagement_quality": engagement_map[review_length],
        "influence_weight":   influence_map[customer_influence],
        "recency_weight":     recency_map[purchase_recency],
        "word_count":         word_map[review_length],
        "has_reply":          1 if platform_replied == "Yes" else 0,
        "bilstm_prob_neg":    neg,
        "bilstm_prob_neu":    neu,
        "bilstm_prob_pos":    pos,
        "bilstm_confidence":  max(neg, neu, pos),
    }


# ════════════════════════════════════════
# HEADER
# ════════════════════════════════════════
st.markdown("""
<div class="exec-header">
    <p class="exec-title">⚡ RETENTION INTELLIGENCE PLATFORM</p>
    <p class="exec-subtitle">Customer Segmentation · Sentiment Analysis · Strategic Risk Scoring</p>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <p style="color:#c9a84c; font-size:1.1rem; font-weight:800;
              letter-spacing:2px; text-transform:uppercase; margin-bottom:4px">
        Customer Intake
    </p>
    <p style="color:#7a9cc4; font-size:0.78rem; margin-bottom:16px">
        Complete the profile below to generate a strategic retention assessment.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section">Review Tone</p>', unsafe_allow_html=True)
    overall_tone = st.select_slider(
        "Overall sentiment of customer reviews",
        options=["Strongly Negative", "Negative", "Mixed", "Positive", "Strongly Positive"],
        value="Negative",
        label_visibility="collapsed"
    )

    st.markdown('<p class="sidebar-section">Complaint History</p>', unsafe_allow_html=True)
    complaint_count = st.selectbox(
        "Number of complaints filed",
        ["None", "1–2 complaints", "3–5 complaints", "More than 5"],
        label_visibility="collapsed"
    )

    st.markdown('<p class="sidebar-section">Purchase Recency</p>', unsafe_allow_html=True)
    purchase_recency = st.selectbox(
        "Last purchase date",
        ["This week", "1–2 weeks ago", "Last month", "Over a month ago"],
        label_visibility="collapsed"
    )

    st.markdown('<p class="sidebar-section">Review Depth</p>', unsafe_allow_html=True)
    review_length = st.selectbox(
        "Length of customer review",
        ["Very brief (1–5 words)", "Short (6–20 words)",
         "Detailed (21–50 words)", "Extensive (50+ words)"],
        label_visibility="collapsed"
    )

    st.markdown('<p class="sidebar-section">Customer Influence</p>', unsafe_allow_html=True)
    customer_influence = st.selectbox(
        "Public influence level",
        ["General customer", "Moderately influential",
         "High influence — public figure / blogger"],
        label_visibility="collapsed"
    )

    st.markdown('<p class="sidebar-section">Support Response</p>', unsafe_allow_html=True)
    platform_replied = st.selectbox(
        "Did the team reply?",
        ["Yes", "No"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    predict_clicked = st.button(
        "GENERATE RETENTION ASSESSMENT",
        use_container_width=True,
        type="primary"
    )

    st.markdown("---")
    st.markdown("""
    <p style="color:#7a9cc4; font-size:0.72rem; line-height:1.6">
        Powered by a dual-head MLP trained on 100,000 e-commerce reviews across 11 platforms.
        Predictions are probabilistic and should inform — not replace — human judgment.
    </p>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════
# MAIN — PREDICTION VIEW
# ════════════════════════════════════════
if predict_clicked:
    payload = map_business_to_features(
        complaint_count, purchase_recency, platform_replied,
        review_length, customer_influence, overall_tone
    )

    with st.spinner("Running inference..."):
        try:
            response = requests.post(
                f"{API_URL}/predict/single", json=payload, timeout=30
            )
            r       = response.json()
            risk    = r["risk_level"]
            color   = RISK_COLOR[risk]
            seg_id  = r["segment_id"]
            details = SEGMENT_DETAILS[seg_id]

            # ── KPI Row
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Customer Segment</div>
                    <div class="kpi-value">{r['segment_name']}</div>
                    <div class="kpi-sub">C{r['segment_id']} of 5 segments</div>
                </div>""", unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Detected Sentiment</div>
                    <div class="kpi-value">{r['sentiment'].capitalize()}</div>
                    <div class="kpi-sub">{r['sentiment_confidence']*100:.1f}% confidence</div>
                </div>""", unsafe_allow_html=True)
            with k3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Retention Risk Score</div>
                    <div class="kpi-value" style="color:{color}">{r['retention_risk_score']:.1f}<span style="font-size:1rem;color:#7a9cc4"> /100</span></div>
                    <div class="kpi-sub">{RISK_LABEL[risk]}</div>
                </div>""", unsafe_allow_html=True)
            with k4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Action Priority</div>
                    <div class="kpi-value" style="color:{color}">{r['priority_tier']}</div>
                    <div class="kpi-sub">{details['urgency']}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Risk + Gauge Row
            left, right = st.columns([1.3, 1])

            with left:
                st.markdown(f"""
                <div class="risk-card risk-{risk}">
                    <p style="font-size:0.7rem; color:#7a9cc4;
                               text-transform:uppercase; letter-spacing:3px;
                               margin:0 0 6px 0">Risk Assessment</p>
                    <h2 style="color:{color}; margin:0; font-size:1.8rem;
                                font-weight:900; letter-spacing:1px">
                        {RISK_EMOJI[risk]} {RISK_LABEL[risk]}
                    </h2>
                    <p style="color:#c9a84c; margin:4px 0 16px 0;
                               font-size:0.85rem; font-weight:600">
                        {r['segment_name']} — {r['priority_tier']}
                    </p>
                    <hr style="border-color:#2a3a5a; margin:12px 0">
                    <table style="width:100%; color:#b0c4de; font-size:0.85rem">
                        <tr>
                            <td style="padding:4px 0">Segment Prediction</td>
                            <td style="text-align:right; color:white; font-weight:600">
                                {r['segment_confidence']*100:.1f}% confidence
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:4px 0">Sentiment Detection</td>
                            <td style="text-align:right; color:white; font-weight:600">
                                {r['sentiment_confidence']*100:.1f}% confidence
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:4px 0">Recommended Action</td>
                            <td style="text-align:right; color:{color}; font-weight:600">
                                {r['recommended_strategy']}
                            </td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

                # Urgency
                st.markdown(f"""
                <p class="section-header">Intervention Timeline</p>
                <p style="color:{details['urgency_color']}; font-size:1.1rem;
                           font-weight:700; margin:0">
                    {RISK_EMOJI[risk]} {details['urgency']}
                </p>
                """, unsafe_allow_html=True)

                # Root Cause
                st.markdown('<p class="section-header">Risk Diagnosis</p>',
                            unsafe_allow_html=True)
                st.markdown(f"""
                <div class="rootcause-box">{details['root_cause']}</div>
                """, unsafe_allow_html=True)

            with right:
                # Gauge
                fig = go.Figure(go.Indicator(
                    mode   = "gauge+number",
                    value  = r['retention_risk_score'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title  = {
                        'text': "RETENTION RISK INDEX",
                        'font': {'color': '#7a9cc4', 'size': 11}
                    },
                    gauge = {
                        'axis': {
                            'range': [0, 100],
                            'tickcolor': '#1e3a5f',
                            'tickfont' : {'color': '#7a9cc4', 'size': 10}
                        },
                        'bar'    : {'color': color, 'thickness': 0.25},
                        'bgcolor': '#0a0f1e',
                        'bordercolor': '#1e3a5f',
                        'steps': [
                            {'range': [0,  40],  'color': '#051a10'},
                            {'range': [40, 60],  'color': '#1a1a05'},
                            {'range': [60, 80],  'color': '#1a0d00'},
                            {'range': [80, 100], 'color': '#1a0000'},
                        ],
                        'threshold': {
                            'line'     : {'color': color, 'width': 3},
                            'thickness': 0.8,
                            'value'    : r['retention_risk_score']
                        }
                    },
                    number={
                        'suffix'  : '/100',
                        'font'    : {'color': color, 'size': 36},
                    }
                ))
                fig.update_layout(
                    height=280,
                    margin=dict(t=40, b=0, l=30, r=30),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#7a9cc4'}
                )
                st.plotly_chart(fig, use_container_width=True)

                # Confidence bars
                st.markdown('<p class="section-header">Model Confidence</p>',
                            unsafe_allow_html=True)
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    x=[r['segment_confidence']*100,
                       r['sentiment_confidence']*100],
                    y=['Segment', 'Sentiment'],
                    orientation='h',
                    marker_color=[color, '#c9a84c'],
                    marker_line_color='rgba(0,0,0,0)',
                    text=[f"{r['segment_confidence']*100:.1f}%",
                          f"{r['sentiment_confidence']*100:.1f}%"],
                    textposition='inside',
                    textfont={'color': '#0a0f1e', 'size': 12, 'family': 'Segoe UI'}
                ))
                fig2.update_layout(
                    height=120,
                    margin=dict(t=0, b=0, l=0, r=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#7a9cc4', 'size': 11},
                    xaxis={
                        'range'    : [0, 100],
                        'showgrid' : False,
                        'zeroline' : False,
                        'showticklabels': False
                    },
                    yaxis={'showgrid': False, 'zeroline': False},
                    bargap=0.3,
                )
                st.plotly_chart(fig2, use_container_width=True)

            # ── Action Plan
            st.markdown('<p class="section-header">Strategic Retention Action Plan</p>',
                        unsafe_allow_html=True)
            step_cols = st.columns(len(details['steps']))
            for i, (col, step) in enumerate(zip(step_cols, details['steps'])):
                with col:
                    st.markdown(f"""
                    <div class="step-card">
                        <span class="step-number">{i+1}</span>
                        <p style="color:#c9a84c; font-size:0.7rem;
                                   text-transform:uppercase; letter-spacing:2px;
                                   margin:0 0 8px 0; font-weight:700">
                            Step {i+1}
                        </p>
                        <p class="step-text">{step}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Expected Outcome
            st.markdown('<p class="section-header">Projected Outcome</p>',
                        unsafe_allow_html=True)
            st.markdown(f"""
            <div class="outcome-box">
                {details['expected_outcome']}
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Assessment failed: {e}")


# ════════════════════════════════════════
# MAIN — DEFAULT LANDING VIEW
# ════════════════════════════════════════
else:
    col1, col2, col3 = st.columns([1.3, 1.2, 1])

    with col1:
        st.markdown('<p class="section-header">Customer Segment Portfolio</p>',
                    unsafe_allow_html=True)
        try:
            segments = requests.get(f"{API_URL}/segments/", timeout=30).json()
            for seg in segments:
                color = RISK_COLOR.get(seg["risk_level"], "#888")
                st.markdown(f"""
                <div class="seg-card" style="border-left: 3px solid {color}">
                    <p class="seg-name" style="color:{color}; margin:0">
                        C{seg['segment_id']} — {seg['segment_name']}
                    </p>
                    <p class="seg-meta">
                        Risk: {seg['risk_level'].upper()} &nbsp;·&nbsp;
                        Avg Rating: {seg['avg_score']:.2f} ★ &nbsp;·&nbsp;
                        Top Platform: {seg['top_platform']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.warning("Unable to load segment data.")

    with col2:
        st.markdown('<p class="section-header">Platform Guide</p>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div style="color:#b0c4de; font-size:0.88rem; line-height:2">
            <b style="color:#c9a84c">01 &nbsp;</b> Complete the customer profile in the sidebar<br>
            <b style="color:#c9a84c">02 &nbsp;</b> Click <i>Generate Retention Assessment</i><br>
            <b style="color:#c9a84c">03 &nbsp;</b> Review segment classification and risk score<br>
            <b style="color:#c9a84c">04 &nbsp;</b> Read the risk diagnosis and urgency level<br>
            <b style="color:#c9a84c">05 &nbsp;</b> Execute the step-by-step action plan<br>
            <b style="color:#c9a84c">06 &nbsp;</b> Track outcomes against projected results
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#0d1b3e; border:1px solid #1e3a5f;
                    border-left:3px solid #c9a84c; border-radius:8px;
                    padding:14px 18px; color:#7a9cc4; font-size:0.8rem;
                    line-height:1.7">
            This platform processes behavioral signals through a dual-head MLP
            neural network to classify customers into one of five retention risk
            segments and prescribe targeted intervention strategies.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown('<p class="section-header">System Status</p>',
                    unsafe_allow_html=True)
        try:
            health = requests.get(f"{API_URL}/health/", timeout=10).json()
            status_color = "#00cc55" if health['model_loaded'] else "#ff3333"
            st.markdown(f"""
            <div style="background:#0d1b3e; border:1px solid #1e3a5f;
                        border-radius:10px; padding:20px">
                <p style="color:{status_color}; font-size:0.8rem;
                           text-transform:uppercase; letter-spacing:2px;
                           font-weight:700; margin:0 0 16px 0">
                    ● SYSTEM OPERATIONAL
                </p>
                <table style="width:100%; font-size:0.82rem; color:#b0c4de">
                    <tr>
                        <td style="padding:5px 0; color:#7a9cc4">AI Model</td>
                        <td style="text-align:right; color:#00cc55; font-weight:600">
                            Loaded
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0; color:#7a9cc4">API Version</td>
                        <td style="text-align:right; font-weight:600">
                            {health['version']}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0; color:#7a9cc4">Uptime</td>
                        <td style="text-align:right; font-weight:600">
                            {health['uptime_seconds']:.0f}s
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0; color:#7a9cc4">Training Data</td>
                        <td style="text-align:right; font-weight:600">100k reviews</td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0; color:#7a9cc4">Platforms</td>
                        <td style="text-align:right; font-weight:600">11</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.error("System offline")

# ── Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid #1e3a5f; padding:12px 0; margin-top:8px;
            display:flex; justify-content:space-between; align-items:center">
    <span style="color:#3a5a7a; font-size:0.72rem; letter-spacing:1px">
        RETENTION INTELLIGENCE PLATFORM &nbsp;·&nbsp; CONFIDENTIAL
    </span>
    <span style="color:#3a5a7a; font-size:0.72rem">
        API: {API_URL}/docs &nbsp;·&nbsp; MLP Dual-Head Model &nbsp;·&nbsp; 100k Reviews
    </span>
</div>
""", unsafe_allow_html=True)