"""
Crop Yield Estimation & Forecasting Page — AgriVision AI.
Supervised machine learning regression estimating yield per hectare,
gross farm harvest volume, MSP-based revenue projections, and limiting factor optimization.
"""

import os
import sys
import pandas as pd
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.predict_yield import CropYieldPredictor, CROP_YIELD_PROFILES
from utils.visualizations import (
    plot_yield_efficiency_gauge,
    plot_rainfall_yield_sensitivity
)
from utils.generate_prescription_pdf import create_prescription_pdf
from utils.helpers import init_page, render_banner, render_kpi, render_sidebar_info, render_footer

init_page("Yield Estimation", "🚜")
render_sidebar_info()

render_banner(
    title="Predictive Crop Yield Estimation",
    subtitle="Forecast crop harvest volume, evaluate nutrient limitations according to Liebig's Law, and calculate gross market returns using trained Random Forest regression pipelines.",
    badge="MACHINE LEARNING REGRESSION"
)

predictor = CropYieldPredictor()
all_crops = sorted(list(CROP_YIELD_PROFILES.keys()))

# Model Switcher
m_col1, m_col2 = st.columns([2, 1])
with m_col1:
    model_map = {
        "yield_best_model": "🏆 Best Model: Random Forest Regressor (R² = 99.58%)",
        "yield_gradient_boosting": "⚡ Gradient Boosting Regressor (R² = 99.56%)",
        "yield_decision_tree": "🌿 Decision Tree Regressor (R² = 99.43%)",
        "yield_ridge_regression": "📐 Ridge Linear Regressor (R² = 99.03%)"
    }
    selected_model = st.selectbox(
        "Select Machine Learning Regression Algorithm:",
        options=list(model_map.keys()),
        format_func=lambda k: model_map[k]
    )

with m_col2:
    unit_mode = st.radio("Farm Area Unit:", options=["Hectares", "Acres"], horizontal=True)

# Farm Input Parameters Form
st.markdown("### 📋 Enter Farm Soil, Area & Climate Parameters")

with st.container():
    f_c1, f_c2 = st.columns(2)
    
    with f_c1:
        st.markdown(
            """
            <div style="background: #e0f2fe; padding: 0.8rem 1rem; border-radius: 8px; border-left: 4px solid #0284c7; margin-bottom: 1rem;">
                <strong style="color: #0369a1;">🌾 Crop Variety & Farm Land Dimension</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        selected_crop = st.selectbox("Select Crop Variety:", options=all_crops, index=0)
        crop_cfg = CROP_YIELD_PROFILES[selected_crop]
        
        selected_season = st.selectbox("Cropping Season:", options=crop_cfg["seasons"])
        
        if unit_mode == "Hectares":
            area_val = st.number_input("Cultivated Land Area (Hectares):", min_value=0.2, max_value=100.0, value=3.0, step=0.5)
            area_ha = float(area_val)
        else:
            area_val = st.number_input("Cultivated Land Area (Acres):", min_value=0.5, max_value=250.0, value=7.5, step=1.0)
            area_ha = float(area_val) / 2.471
            
        ph_val = st.slider("Soil pH:", min_value=4.0, max_value=9.0, value=float(crop_cfg["opt_ph"]), step=0.1)

    with f_c2:
        st.markdown(
            """
            <div style="background: #f0fdf4; padding: 0.8rem 1rem; border-radius: 8px; border-left: 4px solid #10b981; margin-bottom: 1rem;">
                <strong style="color: #065f46;">⛅ Environmental Weather & Soil NPK Nutrients</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        rain_val = st.slider(
            "Seasonal Rainfall (mm):",
            min_value=20.0, max_value=350.0,
            value=float(crop_cfg["opt_rain"]), step=5.0
        )
        
        temp_val = st.slider(
            "Mean Ambient Temperature (°C):",
            min_value=10.0, max_value=42.0,
            value=float(crop_cfg["opt_temp"]), step=0.5
        )
        
        npk_c1, npk_c2, npk_c3 = st.columns(3)
        with npk_c1:
            n_val = st.number_input("Nitrogen (N) kg/ha:", min_value=10.0, max_value=250.0, value=float(crop_cfg["n_req"]), step=5.0)
        with npk_c2:
            p_val = st.number_input("Phosphorus (P) kg/ha:", min_value=5.0, max_value=150.0, value=float(crop_cfg["p_req"]), step=5.0)
        with npk_c3:
            k_val = st.number_input("Potassium (K) kg/ha:", min_value=5.0, max_value=200.0, value=float(crop_cfg["k_req"]), step=5.0)

st.markdown("<br>", unsafe_allow_html=True)
estimate_btn = st.button("🚀 Estimate Crop Yield & Production", use_container_width=True, type="primary")

# Execute Forecasting
if estimate_btn or st.session_state.get("last_yield_result") is not None:
    current_inputs = {
        "Crop": selected_crop,
        "Season": selected_season,
        "Area_Hectares": area_ha,
        "Rainfall_mm": float(rain_val),
        "Temperature_C": float(temp_val),
        "Soil_pH": float(ph_val),
        "Nitrogen_kg_ha": float(n_val),
        "Phosphorus_kg_ha": float(p_val),
        "Potassium_kg_ha": float(k_val)
    }
    
    with st.spinner("Running regression model pipeline and calculating yield equations..."):
        res = predictor.estimate_yield(current_inputs, model_key=selected_model)
        st.session_state.last_yield_result = res

    st.markdown("<hr style='border-color: #e2e8f0; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    st.markdown("## 📊 Yield Forecast & Production Returns")
    
    # KPI Highlights
    y_k1, y_k2, y_k3, y_k4 = st.columns(4)
    with y_k1:
        render_kpi("Predicted Yield", f"{res['predicted_yield_ton_ha']} Ton/ha", f"{res['predicted_yield_quintal_ha']} Quintals / ha", "🌾")
    with y_k2:
        render_kpi("Gross Production", f"{res['total_production_ton']} Tons", f"{res['total_production_quintals']} Quintals total", "⚖️")
    with y_k3:
        render_kpi("Estimated Market Value", f"₹ {res['estimated_revenue_inr']:,.0f}", f"At MSP ₹{res['msp_per_ton']:,}/ton", "💰")
    with y_k4:
        render_kpi("Yield Potential Efficiency", f"{res['efficiency_percentage']}%", "Of genetic maximum potential", "📈")

    st.markdown("<br>", unsafe_allow_html=True)

    # Detailed Visual Analysis Row
    col_gauge, col_curve = st.columns([1.2, 1.8])
    
    with col_gauge:
        fig_eff = plot_yield_efficiency_gauge(res["efficiency_percentage"], selected_crop)
        st.plotly_chart(fig_eff, use_container_width=True)
        
    with col_curve:
        fig_sens = plot_rainfall_yield_sensitivity(current_inputs, predictor.estimate_yield)
        st.plotly_chart(fig_sens, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Agronomic Limiting Factor Analysis & Actionable Advisory
    st.markdown("### 🔬 Agronomic Limiting Factors & Optimization Protocol")
    
    adv_c1, adv_c2 = st.columns(2)
    
    with adv_c1:
        st.markdown(
            f"""
            <div class="tech-card tech-card-cyan">
                <h4 style="color: #0369a1; margin-top: 0;">⚠️ Identified Soil & Weather Limiting Factors</h4>
                <ul style="color: #334155; line-height: 1.6; font-size: 0.95rem;">
                    {''.join([f'<li style="margin-bottom: 0.5rem;">{f}</li>' for f in res['limiting_factors']])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with adv_c2:
        st.markdown(
            f"""
            <div class="tech-card tech-card-emerald">
                <h4 style="color: #065f46; margin-top: 0;">💡 Actionable Yield Optimization Steps (+15-25% Boost)</h4>
                <ul style="color: #334155; line-height: 1.6; font-size: 0.95rem;">
                    {''.join([f'<li style="margin-bottom: 0.5rem;">{t}</li>' for t in res['actionable_tips']])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Export Report Button
    st.markdown("### 📄 Export Full Agronomic Field Report")
    
    dummy_disease = st.session_state.get("last_disease_result", {
        "crop": selected_crop,
        "disease_name": "Healthy Foliage (Baseline Inspection)",
        "pathogen": "None",
        "pathogen_type": "Healthy",
        "infection_area_pct": 0.0,
        "severity_tier": "Healthy",
        "confidence_pct": 98.0,
        "symptoms": "Foliage in robust physiological condition.",
        "chemical_treatment": ["None required."],
        "organic_control": ["Maintain balanced bio-fertilizers."],
        "prevention": ["Routine visual monitoring."]
    })
    
    pdf_bytes = create_prescription_pdf(dummy_disease, res)
    
    p_b1, p_b2, _ = st.columns([1.5, 1.5, 2])
    with p_b1:
        st.download_button(
            label="📥 Download Yield & Advisory PDF",
            data=pdf_bytes,
            file_name=f"Harvest_Yield_Report_{selected_crop}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

render_footer()
