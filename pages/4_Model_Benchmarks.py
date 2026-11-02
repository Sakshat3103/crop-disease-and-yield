"""
Model Benchmarks & Performance Page — AgriVision AI.
Empirical evaluation metrics, cross-validation scores,
R² comparisons, error distributions, and theoretical algorithm breakdowns.
"""

import os
import sys
import json
import pandas as pd
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.visualizations import (
    plot_yield_model_comparison,
    plot_crop_yield_distributions
)
from utils.helpers import init_page, render_banner, render_sidebar_info, render_footer

init_page("Model Benchmarks", "📈")
render_sidebar_info()

render_banner(
    title="Machine Learning & Vision Benchmarks",
    subtitle="Statistical validation and comparative empirical metrics for regression yield forecasting algorithms and computer vision pathology diagnostics.",
    badge="STATISTICAL BENCHMARKS"
)

# Load yield metrics
metrics_path = os.path.join(PROJECT_ROOT, "models", "yield_metrics.json")
data_path = os.path.join(PROJECT_ROOT, "data", "crop_yield_production.csv")

if not os.path.exists(metrics_path):
    st.error("Yield metrics not found. Please train models.")
    st.stop()

with open(metrics_path, "r") as f:
    data = json.load(f)

models_dict = data.get("models", {})
best_key = data.get("best_model_key", "random_forest")
best_info = models_dict.get(best_key, {})

# Top Banner for Top Model
st.markdown(
    f"""
    <div class="tech-card tech-card-emerald" style="background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <span class="tech-badge" style="background: #10b981;">🏆 TOP REGRESSION BENCHMARK</span>
                <h2 style="color: #064e3b; margin: 0.4rem 0 0.2rem 0; font-size: 2rem;">
                    {best_info.get('display_name', 'Random Forest Regressor')}
                </h2>
                <p style="color: #475569; max-width: 780px; font-size: 0.95rem; margin: 0;">
                    {best_info.get('description', '')}
                </p>
            </div>
            <div style="text-align: right; background: #ffffff; padding: 1rem 1.5rem; border-radius: 12px; border: 1px solid #d1fae5; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <div style="font-size: 0.85rem; color: #64748b; font-weight: 600;">COEFFICIENT OF DETERMINATION</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #059669;">R² {best_info.get('r2_score', 0)*100:.2f}%</div>
                <div style="font-size: 0.8rem; color: #065f46; font-weight: 600;">MAE: {best_info.get('mae', 0):.3f} ton/ha</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Performance Metrics Table
st.markdown("### 📊 Regression Model Performance Comparison Table")

table_rows = []
for k, m in models_dict.items():
    table_rows.append({
        "Algorithm": m.get("display_name", k),
        "R² Score (%)": round(m["r2_score"] * 100, 2),
        "Mean Absolute Error (MAE)": f"{m['mae']} ton/ha",
        "Root Mean Squared Error (RMSE)": f"{m['rmse']} ton/ha",
        "5-Fold CV R² (Mean ± Std)": f"{m['cv_mean']*100:.2f}% ± {m['cv_std']*100:.2f}%"
    })

df_metrics = pd.DataFrame(table_rows).sort_values(by="R² Score (%)", ascending=False).reset_index(drop=True)
st.dataframe(df_metrics, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# Grouped Bar Chart
st.markdown("### 📈 Comparative R² Score Chart")
fig_bars = plot_yield_model_comparison(models_dict)
st.plotly_chart(fig_bars, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Empirical Crop Yield Distributions
if os.path.exists(data_path):
    st.markdown("### 🌾 Empirical Yield Distribution by Crop Class")
    df_yield = pd.read_csv(data_path)
    fig_dist = plot_crop_yield_distributions(df_yield)
    st.plotly_chart(fig_dist, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Vision Pathology Engine Architecture
st.markdown("### 🔬 Computer Vision Foliage Diagnostic Specifications")

cv_c1, cv_c2 = st.columns(2)

with cv_c1:
    st.markdown(
        """
        <div class="tech-card tech-card-cyan">
            <h4 style="color: #0369a1; margin-top: 0;">Vision Processing Pipeline</h4>
            <ul style="color: #334155; font-size: 0.9rem; line-height: 1.6;">
                <li><strong>Color Space Transformation:</strong> RGB input normalized to HSV & ExG (Excess Green: <code>2*G - R - B</code>).</li>
                <li><strong>Tissue vs. Background Segmentation:</strong> Isolates active plant foliage from background noise.</li>
                <li><strong>Necrosis Thresholding:</strong> High red/low blue spectrum clustering identifies dead leaf tissue.</li>
                <li><strong>Infection Area Quantification:</strong> Evaluates exact ratio of necrotic pixels against total leaf canopy area.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with cv_c2:
    st.markdown(
        """
        <div class="tech-card tech-card-cyan">
            <h4 style="color: #0369a1; margin-top: 0;">Diagnostic Severity Calibration</h4>
            <table style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #e2e8f0; font-weight: 600;"><td>Severity Tier</td><td>Infection Area (%)</td><td>Action Required</td></tr>
                <tr><td style="color: #10b981; font-weight: 600;">Healthy</td><td>&lt; 2.0%</td><td>Standard maintenance</td></tr>
                <tr><td style="color: #f59e0b; font-weight: 600;">Mild</td><td>2.0% - 10.0%</td><td>Prophylactic organic spray</td></tr>
                <tr><td style="color: #f97316; font-weight: 600;">Moderate</td><td>10.0% - 25.0%</td><td>Targeted systemic fungicide</td></tr>
                <tr><td style="color: #ef4444; font-weight: 600;">Severe</td><td>&gt; 25.0%</td><td>Immediate curative chemical spray</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

render_footer()
