"""
UI Helpers, Session State Management, and Branding for AgriVision AI.
"""

import os
from typing import Any, Optional, Dict
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSS_PATH = os.path.join(PROJECT_ROOT, "assets", "style.css")


def load_css() -> str:
    """Load style.css content."""
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, "r") as f:
            return f.read()
    return ""


def init_page(page_title: str, page_icon: str = "🔬") -> None:
    """Standardize page configuration and inject custom CSS."""
    st.set_page_config(
        page_title=f"{page_title} | AgriVision AI",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    css_content = load_css()
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        
    init_session_state()


def init_session_state() -> None:
    """Initialize session state keys."""
    if "last_disease_result" not in st.session_state:
        st.session_state.last_disease_result = None
    if "last_yield_result" not in st.session_state:
        st.session_state.last_yield_result = None


def render_banner(title: str, subtitle: str, badge: str = "AGRIVISION AI") -> None:
    """Render high-tech cyber banner."""
    html = f"""
    <div class="tech-banner">
        <span class="tech-badge">{badge}</span>
        <h1 class="tech-title">{title}</h1>
        <p class="tech-subtitle">{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_kpi(label: str, value: Any, sub: str = "", icon: str = "📊") -> None:
    """Render KPI box."""
    html = f"""
    <div class="kpi-box">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="kpi-label">{label}</div>
            <div style="font-size: 1.2rem;">{icon}</div>
        </div>
        <div class="kpi-number">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_sidebar_info() -> None:
    """Render modern sidebar info."""
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 1rem 0.5rem 0.8rem 0.5rem; text-align: center;">
                <div style="font-size: 2.8rem; margin-bottom: 0.2rem;">🔬</div>
                <h2 style="color: #38bdf8 !important; margin: 0; font-size: 1.4rem;">AgriVision AI</h2>
                <p style="color: #bae6fd; font-size: 0.82rem; margin-top: 0.2rem;">
                    Computer Vision Pathology & Yield Forecasting
                </p>
            </div>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 0.4rem 0 1rem 0;">
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("### 🌾 Engine Telemetry")
        st.markdown(
            """
            - **Vision AI Engine:** HSV Necrosis Lesion Segmentation
            - **Pathology Catalog:** 12 Major Disease Signatures
            - **Yield Predictor:** Random Forest Regressor (R² = 99.58%)
            - **Crop Yield Profiles:** 14 Major Field Crops
            - **Prescription System:** Real-time PDF Rx Generator
            """
        )
        
        st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 1rem 0;'>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 0.75rem; color: #bae6fd; opacity: 0.85;">
                Crop Disease & Yield Estimation Platform
            </div>
            """,
            unsafe_allow_html=True
        )


def render_footer() -> None:
    """Render standard footer."""
    st.markdown(
        """
        <div style="margin-top: 4rem; padding: 2rem 0; border-top: 1px solid #e2e8f0; text-align: center; color: #64748b; font-size: 0.85rem;">
            <div style="font-weight: 700; color: #0c4a6e; margin-bottom: 0.3rem;">
                🔬 AgriVision AI — Precision Crop Pathology & Yield Forecasting Engine
            </div>
            <div>
                Powered by Computer Vision & Supervised Machine Learning
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
