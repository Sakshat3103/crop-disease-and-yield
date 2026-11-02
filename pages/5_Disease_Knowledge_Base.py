"""
Disease Knowledge Base & Spray Advisory — AgriVision AI.
Comprehensive phytopathological encyclopedia containing scientific profiles,
symptoms, environmental risk factors, chemical dosages, and organic remedies.
"""

import os
import sys
import pandas as pd
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.disease_data import DISEASE_CATALOG, get_disease_profile, list_all_diseases
from utils.helpers import init_page, render_banner, render_sidebar_info, render_footer

init_page("Disease Knowledge Base", "📚")
render_sidebar_info()

render_banner(
    title="Phytopathological Disease Knowledge Base",
    subtitle="Verified agronomic encyclopedia containing pathogen classifications, diagnostic symptoms, chemical spray dosages, and biological pest controls.",
    badge="AGRONOMIC ENCYCLOPEDIA"
)

all_diseases = list_all_diseases()
crops = ["All Crops", "Rice", "Potato", "Tomato", "Corn (Maize)", "Apple", "Cotton"]

c_f1, c_f2 = st.columns([1, 2])
with c_f1:
    selected_crop_filter = st.selectbox("Filter Diseases by Host Crop:", options=crops)

filtered_keys = []
for k in all_diseases:
    prof = DISEASE_CATALOG[k]
    if selected_crop_filter == "All Crops":
        filtered_keys.append(k)
    elif selected_crop_filter.split()[0].lower() in prof["crop"].lower():
        filtered_keys.append(k)

with c_f2:
    selected_disease_key = st.selectbox(
        "Select Specific Disease to Inspect:",
        options=filtered_keys if filtered_keys else all_diseases,
        format_func=lambda k: f"{DISEASE_CATALOG[k]['icon']} {DISEASE_CATALOG[k]['crop']} — {DISEASE_CATALOG[k]['disease_name']}"
    )

dis_info = get_disease_profile(selected_disease_key)

if dis_info:
    # Disease Profile Header Card
    st.markdown(
        f"""
        <div class="tech-card tech-card-cyan" style="background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%); margin-top: 1rem;">
            <div style="display: flex; align-items: center; gap: 1.2rem; flex-wrap: wrap;">
                <div style="font-size: 3.8rem;">{dis_info['icon']}</div>
                <div>
                    <span class="tech-badge" style="background: #0c4a6e;">{dis_info['type'].upper()} PATHOLOGY</span>
                    <h2 style="color: #0c4a6e; margin: 0.2rem 0; font-size: 2.2rem;">{dis_info['disease_name']}</h2>
                    <div style="color: #0284c7; font-style: italic; font-size: 1.1rem; font-weight: 500;">
                        Host: {dis_info['crop']} &nbsp;|&nbsp; Pathogen: {dis_info['pathogen']}
                    </div>
                </div>
            </div>
            <p style="color: #334155; font-size: 1rem; line-height: 1.6; margin-top: 1rem;">
                <strong>Diagnostic Foliar Symptoms:</strong> {dis_info['symptoms']}
            </p>
            <div style="background: #e0f2fe; padding: 0.6rem 1rem; border-radius: 8px; font-size: 0.9rem; color: #0369a1; margin-top: 0.5rem;">
                <strong>High-Risk Environmental Conditions:</strong> {dis_info['risk_factors']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Treatment Cards
    t_c1, t_c2 = st.columns(2)
    
    with t_c1:
        st.markdown(
            f"""
            <div class="tech-card tech-card-danger">
                <h4 style="color: #991b1b; margin-top: 0;">🧪 Recommended Chemical Fungicides & Bactericides</h4>
                <ul style="color: #334155; line-height: 1.6; font-size: 0.95rem;">
                    {''.join([f'<li style="margin-bottom: 0.6rem;">{c}</li>' for c in dis_info['chemical_treatment']])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with t_c2:
        st.markdown(
            f"""
            <div class="tech-card tech-card-emerald">
                <h4 style="color: #065f46; margin-top: 0;">🌿 Biological & Organic Control Protocols</h4>
                <p style="font-weight: 600; color: #047857; margin-bottom: 0.3rem;">Organic Formulations:</p>
                <ul style="color: #334155; font-size: 0.95rem; line-height: 1.5; margin-bottom: 0.8rem;">
                    {''.join([f'<li>{o}</li>' for o in dis_info['organic_control']])}
                </ul>
                <p style="font-weight: 600; color: #047857; margin-bottom: 0.3rem;">Cultural Preventative Management:</p>
                <ul style="color: #334155; font-size: 0.95rem; line-height: 1.5;">
                    {''.join([f'<li>{p}</li>' for p in dis_info['prevention']])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# Master Reference Matrix
with st.expander("📋 Browse Complete Plant Pathology Reference Matrix"):
    rows = []
    for k in all_diseases:
        d = DISEASE_CATALOG[k]
        rows.append({
            "Host Crop": d["crop"],
            "Disease Name": d["disease_name"],
            "Pathogen": d["pathogen"],
            "Type": d["type"],
            "First-Line Chemical Spray": d["chemical_treatment"][0] if d["chemical_treatment"] else "None",
            "Key Risk Trigger": d["risk_factors"].split(",")[0]
        })
    df_matrix = pd.DataFrame(rows)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)

render_footer()
