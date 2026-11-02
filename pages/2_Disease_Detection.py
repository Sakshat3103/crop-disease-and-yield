"""
Crop Disease Detection & Diagnosis Page — AgriVision AI.
Computer Vision analysis of leaf foliage, lesion segmentation heatmap,
severity quantification, chemical prescription, and organic remedies.
"""

import os
import sys
from PIL import Image
import pandas as pd
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.vision_disease_detector import LeafDiseaseVisionDetector
from utils.visualizations import (
    plot_disease_severity_gauge,
    plot_tissue_composition_donut
)
from utils.generate_prescription_pdf import create_prescription_pdf
from utils.helpers import init_page, render_banner, render_kpi, render_sidebar_info, render_footer

init_page("Crop Disease Detection", "🍃")
render_sidebar_info()

render_banner(
    title="Crop Disease Detection & Visual Diagnosis",
    subtitle="Upload a leaf image or select a verified pathology sample to isolate necrotic lesions, quantify infection severity, and receive chemical and biological treatment prescriptions.",
    badge="COMPUTER VISION PATHOLOGY"
)

detector = LeafDiseaseVisionDetector()
SAMPLE_DIR = os.path.join(PROJECT_ROOT, "sample_images")

# Sample Image Registry
SAMPLES = {
    "Select from preloaded demo gallery...": None,
    "🌾 Rice — Bacterial Leaf Blight": ("rice_bacterial_blight.png", "Rice"),
    "🥔 Potato — Early Blight (Concentric Target Rings)": ("potato_early_blight.png", "Potato"),
    "🥔 Potato — Late Blight (Water-Soaked Necrosis)": ("potato_late_blight.png", "Potato"),
    "🍅 Tomato — Leaf Mold (Velvety Chlorotic Spots)": ("tomato_leaf_mold.png", "Tomato"),
    "🌽 Corn (Maize) — Common Rust (Powdery Pustules)": ("corn_common_rust.png", "Corn"),
    "🍏 Apple — Apple Scab (Olive-Brown Scabs)": ("apple_scab.png", "Apple"),
    "🌿 Healthy Foliage (Clean Uninfected Leaf)": ("healthy_leaf.png", "General")
}

# Image Input Mode
c_in1, c_in2 = st.columns([1.5, 1.5])

with c_in1:
    uploaded_file = st.file_uploader(
        "Upload Leaf Photograph (JPG, PNG, WEBP):",
        type=["jpg", "jpeg", "png", "webp"],
        help="Capture an in-focus photo of an individual leaf under clear lighting."
    )

with c_in2:
    selected_sample = st.selectbox(
        "Or Pick a Preloaded Pathology Test Leaf:",
        options=list(SAMPLES.keys())
    )

crop_options = ["Auto-Detect Crop Context", "Rice", "Potato", "Tomato", "Corn (Maize)", "Apple", "Cotton"]
crop_selection = st.selectbox("Crop Context (Helps refine pathogen signature):", options=crop_options)
crop_hint = None if crop_selection.startswith("Auto") else crop_selection.split()[0]

# Determine which image to process
active_image = None
if uploaded_file is not None:
    active_image = Image.open(uploaded_file)
elif selected_sample and SAMPLES[selected_sample] is not None:
    file_name, def_hint = SAMPLES[selected_sample]
    sample_path = os.path.join(SAMPLE_DIR, file_name)
    if os.path.exists(sample_path):
        active_image = Image.open(sample_path)
        if crop_hint is None:
            crop_hint = def_hint

if active_image is not None:
    st.markdown("<hr style='border-color: #e2e8f0; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    with st.spinner("Analyzing foliar color spaces, segmenting necrotic lesions, and classifying pathogen..."):
        diag = detector.analyze_leaf_image(active_image, crop_hint=crop_hint)
        st.session_state.last_disease_result = diag

    # Main Visual Inspection Split
    st.markdown("### 🔬 Computer Vision Foliage Inspection")
    
    img_col1, img_col2 = st.columns(2)
    with img_col1:
        st.markdown(
            """
            <div class="img-inspect-box">
                <div style="font-weight: 700; color: #0c4a6e; margin-bottom: 0.5rem;">Original Captured Leaf</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.image(diag["original_image"], use_container_width=True)

    with img_col2:
        st.markdown(
            """
            <div class="img-inspect-box" style="border-color: #f59e0b; background: #fffbeb;">
                <div style="font-weight: 700; color: #b45309; margin-bottom: 0.5rem;">AI Segmented Lesion Heatmap (Highlighted Infected Tissue)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.image(diag["annotated_image"], use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Diagnostic Findings Card
    st.markdown("### 📋 Phytopathological Diagnostic Findings")
    
    res_c1, res_c2, res_c3 = st.columns([1.5, 1, 1])
    
    with res_c1:
        st.markdown(
            f"""
            <div class="tech-card" style="border-left: 5px solid {diag['severity_color']}; height: 100%;">
                <span class="tech-badge" style="background: {diag['severity_color']};">{diag['severity_tier'].upper()}</span>
                <div style="font-size: 2.8rem; margin: 0.3rem 0;">{diag['icon']}</div>
                <h2 style="color: #0c4a6e; margin: 0.2rem 0; font-size: 2rem;">{diag['disease_name']}</h2>
                <div style="color: #0284c7; font-style: italic; font-weight: 600; font-size: 1.05rem; margin-bottom: 0.8rem;">
                    Pathogen: {diag['pathogen']} ({diag['pathogen_type']})
                </div>
                <p style="color: #334155; font-size: 0.95rem; line-height: 1.5;">
                    <strong>Observed Symptoms:</strong> {diag['symptoms']}
                </p>
                <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">
                    <strong>High-Risk Weather Triggers:</strong> {diag['risk_factors']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with res_c2:
        fig_sev = plot_disease_severity_gauge(diag["infection_area_pct"], diag["severity_tier"])
        st.plotly_chart(fig_sev, use_container_width=True)
        
    with res_c3:
        fig_donut = plot_tissue_composition_donut(diag["infection_area_pct"])
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Actionable Treatment Prescription
    st.markdown("### 💊 Agronomic Treatment Protocol & Chemical Spray Advisory")
    
    rx_col1, rx_col2 = st.columns(2)
    
    with rx_col1:
        st.markdown(
            f"""
            <div class="tech-card tech-card-danger">
                <h4 style="color: #991b1b; margin-top: 0;">🧪 Immediate Chemical Intervention</h4>
                <ul style="color: #334155; line-height: 1.6; font-size: 0.95rem;">
                    {''.join([f'<li style="margin-bottom: 0.5rem;">{c}</li>' for c in diag['chemical_treatment']])}
                </ul>
                <div style="font-size: 0.8rem; color: #64748b; font-style: italic; margin-top: 0.8rem;">
                    Always follow manufacturer pre-harvest intervals (PHI) and wear protective gloves and mask during spray application.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with rx_col2:
        st.markdown(
            f"""
            <div class="tech-card tech-card-emerald">
                <h4 style="color: #065f46; margin-top: 0;">🌿 Biological, Organic & Cultural Control</h4>
                <p style="font-weight: 600; color: #047857; margin-bottom: 0.3rem;">Organic Treatments:</p>
                <ul style="color: #334155; font-size: 0.95rem; line-height: 1.5; margin-bottom: 0.8rem;">
                    {''.join([f'<li>{o}</li>' for o in diag['organic_control']])}
                </ul>
                <p style="font-weight: 600; color: #047857; margin-bottom: 0.3rem;">Preventative Cultural Measures:</p>
                <ul style="color: #334155; font-size: 0.95rem; line-height: 1.5;">
                    {''.join([f'<li>{p}</li>' for p in diag['prevention']])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Generate Field Prescription PDF Button
    st.markdown("### 📄 Export Printable Field Prescription")
    
    dummy_yield = st.session_state.get("last_yield_result", {
        "crop": diag["crop"],
        "area_hectares": 2.5,
        "area_acres": 6.18,
        "predicted_yield_ton_ha": 4.2,
        "predicted_yield_quintal_ha": 42.0,
        "total_production_ton": 10.5,
        "total_production_quintals": 105.0,
        "efficiency_percentage": 88.0,
        "msp_per_ton": 22000,
        "estimated_revenue_inr": 231000
    })
    
    pdf_bytes = create_prescription_pdf(diag, dummy_yield)
    
    p_c1, p_c2, _ = st.columns([1.5, 1.5, 2])
    with p_c1:
        st.download_button(
            label="📥 Download Field Prescription (PDF)",
            data=pdf_bytes,
            file_name=f"Prescription_{diag['crop']}_{diag['disease_name'].replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

else:
    st.info("👆 Please upload a leaf image above or select a preloaded test specimen from the dropdown.")

render_footer()
