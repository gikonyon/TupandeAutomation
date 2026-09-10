import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & BRANDING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Tupande Automation & AI Platform | One Acre Fund",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling to Match One Acre Fund / Tupande Branding
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E5631;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #4C9A2A;
        margin-bottom: 25px;
    }
    .stMetric {
        background-color: #F4F7F4;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #1E5631;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🌾 Tupande Tech Suite")
    st.caption("AI, Automation & Engineering Proof-of-Concept")
    
    selected_module = st.radio(
        "Select Core Service Module:",
        [
            "🌾 1. Tupande Duka Credit Simulator",
            "🤖 2. AI Extension & Agronomic Assistant",
            "🛰️ 3. Regional Weather & Risk Analytics",
            "⚙️ 4. Deployment & Architecture (Git + Streamlit)"
        ]
    )
    
    st.divider()
    st.markdown("**Target Operating Regions:**")
    selected_region = st.selectbox("Active Focus Area", ["Kakamega", "Bungoma", "Trans Nzoia", "Narok"])
    st.caption(f"Showing operational data tuned for **{selected_region}**.")

# -----------------------------------------------------------------------------
# HEADER SECTION
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">Tupande Digital Agriculture Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Empowering Smallholder Farmers with Data-Driven Inputs, AI Extension & Automated Credit Workflows</div>', unsafe_allow_html=True)

# =============================================================================
# MODULE 1: TUPANDE DUKA INPUT CREDIT & REPAYMENT CALCULATOR
# =============================================================================
if selected_module == "🌾 1. Tupande Duka Credit Simulator":
    st.header("🌾 Tupande Duka Input Credit & Flexible Repayment Simulator")
    st.markdown("Model customized crop input bundles (seeds, crop protection, tree seedlings) and generate dynamic M-Pesa weekly repayment schedules tailored to farmer seasonal cash flows.")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("1. Configure Farmer Package")
        farm_size = st.slider("Farm Size (Acres)", min_value=0.5, max_value=10.0, value=1.5, step=0.5)
        crop_type = st.selectbox("Primary Target Crop", ["Maize (Hybrid)", "Beans (High Yield)", "Vegetables/Horticulture", "Mixed Farming"])
        
        st.markdown("**Select Input Add-ons:**")
        include_fertilizer = st.checkbox("Basal & Top-Dressing Fertilizer Package", value=True)
        include_trees = st.checkbox("Grevillea / Avocado Tree Seedlings (20 Units)", value=True)
        include_insurance = st.checkbox("Weather-Index Crop Yield Insurance", value=True)
        
        # Base unit pricing (KES)
        base_seed_cost = 4500 * farm_size
        fertilizer_cost = (7200 * farm_size) if include_fertilizer else 0
        tree_cost = 1800 if include_trees else 0
        insurance_cost = (850 * farm_size) if include_insurance else 0
        
        total_package_value = base_seed_cost + fertilizer_cost + tree_cost + insurance_cost
        
        st.divider()
        st.subheader("2. Repayment Terms")
        down_payment_pct = st.select_slider("Upfront Commitment Deposit (%)", options=[10, 15, 20, 25, 30], value=15)
        repayment_weeks = st.slider("Repayment Window (Weeks)", min_value=12, max_value=28, value=20, step=2)
        
        down_payment = total_package_value * (down_payment_pct / 100.0)
        financed_amount = total_package_value - down_payment
        weekly_installment = financed_amount / repayment_weeks

    with col2:
        st.subheader("Credit Summary & Repayment Schedule")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Package Value", f"KES {total_package_value:,.0f}")
        m2.metric("Upfront Deposit", f"KES {down_payment:,.0f}", delta=f"{down_payment_pct}%")
        m3.metric("Weekly M-Pesa Target", f"KES {weekly_installment:,.0f}")
        
        # Package Breakdown Chart
        breakdown_data = pd.DataFrame({
            "Component": ["Seeds", "Fertilizer", "Tree Seedlings", "Yield Insurance"],
            "Cost (KES)": [base_seed_cost, fertilizer_cost, tree_cost, insurance_cost]
        })
        breakdown_data = breakdown_data[breakdown_data["Cost (KES)"] > 0]
        
        fig_donut = px.pie(
            breakdown_data, 
            names="Component", 
            values="Cost (KES)", 
            title="Package Cost Breakdown",
            color_discrete_sequence=["#1E5631", "#4C9A2A", "#78B833", "#A8D865"],
            hole=0.4
        )
        fig_donut.update_layout(margin=dict(t=30, b=10, l=10, r=10), height=220)
        st.plotly_chart(fig_donut, use_container_width=True)
        
        # Amortization Table & Trajectory
        weeks = list(range(1, repayment_weeks + 1))
        remaining_balances = [financed_amount - (weekly_installment * w) for w in weeks]
        schedule_df = pd.DataFrame({
            "Week": weeks,
            "Payment (KES)": [round(weekly_installment, 2)] * repayment_weeks,
            "Remaining Balance (KES)": [max(0, round(b, 2)) for b in remaining_balances]
        })
        
        fig_line = px.line(
            schedule_df, 
            x="Week", 
            y="Remaining Balance (KES)", 
            title="Seasonal Loan Paydown Trajectory",
            markers=True
        )
        fig_line.update_traces(line_color="#1E5631")
        fig_line.update_layout(margin=dict(t=30, b=10, l=10, r=10), height=200)
        st.plotly_chart(fig_line, use_container_width=True)

    with st.expander("📋 View Full M-Pesa Installment Table"):
        st.dataframe(schedule_df, use_container_width=True)

# =============================================================================
# MODULE 2: AI AGRONOMIC & EXTENSION ASSISTANT (RAG BOT)
# =============================================================================
elif selected_module == "🤖 2. AI Extension & Agronomic Assistant":
    st.header("🤖 Tupande Smart Agronomic Extension Assistant")
    st.markdown("A Retrieval-Augmented Generation (RAG) assistant delivering localized agronomic advice, pest management instructions, and planting best practices.")
    
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.subheader("Ask the Agronomic Assistant")
        
        preset_query = st.selectbox(
            "Select a common farmer inquiry or type below:",
            [
                "Select a sample prompt...",
                "How do I control Fall Armyworm in my Kakamega maize plot naturally?",
                "When should I apply CAN fertilizer to top-dress my maize?",
                "What is the recommended seed spacing for hybrid maize in wet regions?",
                "How can I prepare soil with high acidity before planting beans?"
            ]
        )
        
        user_input = st.text_area(
            "Enter Agronomic Question / Field Observation:",
            value="" if preset_query == "Select a sample prompt..." else preset_query,
            placeholder="e.g., My maize leaves have small holes and caterpillar droppings. What should I do?",
            height=100
        )
        
        if st.button("Get Agronomic Guidance", type="primary"):
            if user_input.strip():
                with st.spinner("Analyzing agronomic knowledge base & regional field guidelines..."):
                    st.success("Analysis Complete — Verified Guidance Generated")
                    st.markdown("### 🌿 Recommended Action Plan")
                    
                    if "Armyworm" in user_input or "holes" in user_input:
                        st.warning("⚠️ **Diagnostic:** Fall Armyworm (*Spodoptera frugiperda*) infestation detected.")
                        st.markdown("""
                        **Immediate Steps for Smallholders:**
                        1. **Handpicking:** For minor plots, inspect crop whorls early morning and crush egg masses manually.
                        2. **Botanical Treatment:** Apply a small pinch of clean dry sand or wood ash into the leaf whorls to smother caterpillars.
                        3. **Bio-Pesticide Application:** If infestation exceeds 20% of plants, spray targeted biopesticides like *Bacillus thuringiensis* or Neem extracts during cool hours (5:00 PM - 7:00 PM).
                        4. **Prevention:** Practice crop rotation with non-host crops like sweet potatoes or cassava in subsequent seasons.
                        """)
                    elif "fertilizer" in user_input or "CAN" in user_input:
                        st.info("💡 **Diagnostic:** Fertilizer Timing Advisory.")
                        st.markdown("""
                        **CAN Top-Dressing Best Practices:**
                        1. **Timing:** Apply first top-dressing when maize is knee-high (approx. 2-3 weeks after germination, 18-24 days).
                        2. **Dosage:** Apply 1 bottle top (approx. 10g) per plant placed 5cm away from the stem in a ring or side-band.
                        3. **Soil Conditions:** Ensure soil is moist during application to prevent nitrogen volatility loss.
                        """)
                    else:
                        st.markdown("""
                        **General Agronomic Guidance:**
                        - Ensure proper spacing (75cm between rows, 25cm between plants for single seed planting).
                        - Integrate leguminous trees (*Calliandra*, *Sesbania*) along farm boundaries to restore nitrogen levels naturally.
                        - Consult your local Tupande Field Officer if crop discoloration persists past 14 days post-germination.
                        """)
            else:
                st.error("Please enter a question or select a prompt above.")

    with col_right:
        st.subheader("📚 Active Knowledge Base (RAG)")
        st.markdown("The AI queries localized Tupande technical manuals and agronomic research papers:")
        
        with st.expander("📖 Tupande Crop Protection Manual v4.2", expanded=True):
            st.caption("Covers Fall Armyworm thresholds, biological controls, and safe chemical handling.")
        with st.expander("📖 East Africa Smallholder Fertilizer Handbook"):
            st.caption("Soil NPK requirements, acidic soil remediation using agricultural lime in Western Kenya.")
        with st.expander("📖 Climate-Smart Agroforestry Guide"):
            st.caption("Intercropping paradigms, shade tree integration, and fodder tree management.")

# =============================================================================
# MODULE 3: REGIONAL WEATHER & YIELD RISK ANALYTICS
# =============================================================================
elif selected_module == "🛰️ 3. Regional Weather & Risk Analytics":
    st.header(f"🛰️ Regional Weather & Yield Risk Analytics — {selected_region}")
    st.markdown("Continuous monitoring of micro-climate patterns, soil moisture indicators, and satellite-derived vegetation index (NDVI) to protect farmer yields.")
    
    dates = [datetime.now() - timedelta(days=x) for x in range(60, 0, -1)]
    np.random.seed(42 if selected_region == "Kakamega" else 101)
    
    rainfall = np.random.gamma(shape=2, scale=3.5, size=60)
    soil_moisture = np.clip(np.cumsum(rainfall * 0.1) + 20, 15, 65)
    ndvi = np.clip(0.3 + (soil_moisture * 0.008) + np.sin(np.linspace(0, 3, 60)) * 0.15, 0.2, 0.85)
    
    df_weather = pd.DataFrame({
        "Date": dates,
        "Daily Rainfall (mm)": rainfall,
        "Soil Moisture (%)": soil_moisture,
        "Satellite NDVI Vigor": ndvi
    })
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("30-Day Total Rainfall", f"{df_weather['Daily Rainfall (mm)'].tail(30).sum():.1f} mm", delta="+12% vs Average")
    k2.metric("Avg Soil Moisture", f"{df_weather['Soil Moisture (%)'].iloc[-1]:.1f} %", delta="Optimal")
    k3.metric("Crop Health (NDVI)", f"{df_weather['Satellite NDVI Vigor'].iloc[-1]:.2f}", delta="Good Vigor")
    k4.metric("Drought Risk Level", "LOW", delta_color="normal")
    
    st.divider()
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Precipitation & Soil Moisture Trend")
        fig_rain = go.Figure()
        fig_rain.add_trace(go.Bar(x=df_weather["Date"], y=df_weather["Daily Rainfall (mm)"], name="Rainfall (mm)", marker_color="#78B833"))
        fig_rain.add_trace(go.Scatter(x=df_weather["Date"], y=df_weather["Soil Moisture (%)"], name="Soil Moisture (%)", yaxis="y2", line=dict(color="#1E5631", width=2)))
        
        fig_rain.update_layout(
            yaxis=dict(title="Rainfall (mm)"),
            yaxis2=dict(title="Soil Moisture (%)", overlaying="y", side="right"),
            legend=dict(x=0, y=1.1, orientation="h"),
            margin=dict(t=20, b=20, l=10, r=10),
            height=300
        )
        st.plotly_chart(fig_rain, use_container_width=True)

    with col_chart2:
        st.subheader("Satellite Crop Health Index (NDVI)")
        fig_ndvi = px.line(df_weather, x="Date", y="Satellite NDVI Vigor", title=f"Satellite Vegetation Vigor index ({selected_region})")
        fig_ndvi.add_hrect(y0=0.6, y1=0.85, fillcolor="green", opacity=0.1, line_width=0, annotation_text="Healthy Canopy Threshold")
        fig_ndvi.update_traces(line_color="#4C9A2A", width=2.5)
        fig_ndvi.update_layout(margin=dict(t=30, b=20, l=10, r=10), height=300)
        st.plotly_chart(fig_ndvi, use_container_width=True)

# =============================================================================
# MODULE 4: DEPLOYMENT & ARCHITECTURE (GIT + STREAMLIT.IO)
# =============================================================================
elif selected_module == "⚙️ 4. Deployment & Architecture (Git + Streamlit)":
    st.header("⚙️ Git + Streamlit.io Deployment Architecture")
    st.markdown("This entire demo application runs directly off a public/private GitHub repository connected seamlessly to **Streamlit Community Cloud (`streamlit.io`)**.")
    
    st.subheader("🏗️ System Architecture Flow")
    st.code("""
+-----------------------------------------------------------------------+
|                     1. GitHub Repository                              |
|  • app.py (Streamlit Code)                                            |
|  • requirements.txt (Dependencies: pandas, plotly, streamlit)         |
|  • .streamlit/config.toml (Branding & Palette)                        |
+-----------------------------------+-----------------------------------+
                                    |
                                    v  Automated Git Webhook / Push
+-----------------------------------------------------------------------+
|                     2. Streamlit.io Cloud Platform                    |
|  • Auto-detects updates on commit push                                |
|  • Secure Secrets Manager (API Keys for OpenAI / Gemini / M-Pesa)     |
|  • Free Web Hosting & SSL Certificate                                 |
+-----------------------------------+-----------------------------------+
                                    |
                                    v  Instant Global Web Access
+-----------------------------------------------------------------------+
|                     3. End-User Web Application                       |
|  • https://<your-app-name>.streamlit.app                              |
+-----------------------------------------------------------------------+
    """, language="text")

st.divider()
st.caption("🌾 Tupande Automation & AI Platform Demo | Developed for One Acre Fund Innovation Showcase")
