"""
Plotly Interactive Visualizations for AgriVision AI.
Provides charts for Yield Estimation, Model Benchmarking,
and Disease Severity Quantification.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# High-Tech Modern AgriTheme
NAVY_THEME = {
    "font": {"family": "Inter, -apple-system, sans-serif", "color": "#0f172a"},
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)"
}


def plot_yield_model_comparison(metrics_dict: Dict[str, Dict[str, Any]]) -> go.Figure:
    """Grouped bar chart comparing regression models by R² score and MAE."""
    models = []
    r2_scores = []
    maes = []
    
    for k, v in metrics_dict.items():
        models.append(v.get("display_name", k))
        r2_scores.append(v["r2_score"] * 100)
        maes.append(v["mae"])
        
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="R² Score (%)",
        x=models,
        y=r2_scores,
        marker_color="#0284c7",
        text=[f"{val:.2f}%" for val in r2_scores],
        textposition="auto"
    ))
    
    fig.update_layout(
        title="<b>Crop Yield Regression Algorithm Comparison (R² Score %)</b>",
        yaxis={"title": "R² Score (%)", "range": [95, 100.5], "gridcolor": "#e2e8f0"},
        xaxis={"title": "Regression Model"},
        **NAVY_THEME
    )
    return fig


def plot_yield_efficiency_gauge(efficiency_pct: float, crop_name: str) -> go.Figure:
    """Speedometer gauge indicating farm yield efficiency against maximum crop potential."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=efficiency_pct,
        number={"suffix": "%", "font": {"size": 36, "color": "#0369a1"}},
        title={"text": f"<b>Yield Efficiency ({crop_name})</b>", "font": {"size": 18, "color": "#0f172a"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#64748b"},
            "bar": {"color": "#0284c7"},
            "bgcolor": "#f8fafc",
            "borderwidth": 1,
            "bordercolor": "#cbd5e1",
            "steps": [
                {"range": [0, 50], "color": "#fee2e2"},
                {"range": [50, 75], "color": "#fef3c7"},
                {"range": [75, 100], "color": "#e0f2fe"}
            ],
            "threshold": {
                "line": {"color": "#0c4a6e", "width": 4},
                "thickness": 0.8,
                "value": efficiency_pct
            }
        }
    ))
    fig.update_layout(height=250, margin={"l": 20, "r": 20, "t": 30, "b": 10}, **NAVY_THEME)
    return fig


def plot_disease_severity_gauge(infection_pct: float, severity_tier: str) -> go.Figure:
    """Speedometer gauge indicating percentage of foliage infected by lesions."""
    # Determine bar color based on tier
    if infection_pct < 2.0:
        bar_color = "#10b981"
    elif infection_pct <= 10.0:
        bar_color = "#f59e0b"
    elif infection_pct <= 25.0:
        bar_color = "#f97316"
    else:
        bar_color = "#ef4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=infection_pct,
        number={"suffix": "%", "font": {"size": 36, "color": bar_color}},
        title={"text": f"<b>Infection Severity ({severity_tier.split()[0]})</b>", "font": {"size": 18, "color": "#0f172a"}},
        gauge={
            "axis": {"range": [0, 60], "tickwidth": 1, "tickcolor": "#64748b"},
            "bar": {"color": bar_color},
            "bgcolor": "#f8fafc",
            "borderwidth": 1,
            "bordercolor": "#cbd5e1",
            "steps": [
                {"range": [0, 2], "color": "#d1fae5"},
                {"range": [2, 10], "color": "#fef3c7"},
                {"range": [10, 25], "color": "#ffedd5"},
                {"range": [25, 60], "color": "#fee2e2"}
            ],
            "threshold": {
                "line": {"color": "#991b1b", "width": 4},
                "thickness": 0.8,
                "value": infection_pct
            }
        }
    ))
    fig.update_layout(height=250, margin={"l": 20, "r": 20, "t": 30, "b": 10}, **NAVY_THEME)
    return fig


def plot_tissue_composition_donut(infection_pct: float) -> go.Figure:
    """Donut chart illustrating healthy vs. infected tissue ratios."""
    healthy_pct = max(0.0, 100.0 - infection_pct)
    labels = ["Healthy Foliage", "Infected Lesion Tissue"]
    values = [healthy_pct, infection_pct]
    colors = ["#10b981", "#ef4444" if infection_pct > 10 else "#f59e0b"]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker_colors=colors,
        textinfo="label+percent"
    )])
    fig.update_layout(
        title="<b>Leaf Surface Tissue Composition</b>",
        showlegend=False,
        height=260,
        margin={"l": 10, "r": 10, "t": 35, "b": 10},
        **NAVY_THEME
    )
    return fig


def plot_rainfall_yield_sensitivity(base_inputs: Dict[str, Any], predictor_func) -> go.Figure:
    """Simulate and plot how varying seasonal rainfall affects predicted yield."""
    current_rain = float(base_inputs["Rainfall_mm"])
    rain_range = np.linspace(max(20.0, current_rain - 100.0), current_rain + 100.0, 15)
    
    sim_yields = []
    for r in rain_range:
        sim_input = base_inputs.copy()
        sim_input["Rainfall_mm"] = r
        res = predictor_func(sim_input)
        sim_yields.append(res["predicted_yield_ton_ha"])
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rain_range,
        y=sim_yields,
        mode="lines+markers",
        line={"color": "#0284c7", "width": 3},
        marker={"size": 6, "color": "#0369a1"},
        name="Yield Response"
    ))
    
    # Highlight current user rainfall
    current_res = predictor_func(base_inputs)
    fig.add_trace(go.Scatter(
        x=[current_rain],
        y=[current_res["predicted_yield_ton_ha"]],
        mode="markers",
        marker={"size": 12, "color": "#ef4444", "symbol": "star"},
        name="Your Current Farm Point"
    ))
    
    fig.update_layout(
        title="<b>Rainfall vs. Yield Sensitivity Response Curve</b>",
        xaxis={"title": "Seasonal Rainfall (mm)", "gridcolor": "#e2e8f0"},
        yaxis={"title": "Predicted Yield (Tons / Hectare)", "gridcolor": "#e2e8f0"},
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": 0.5},
        height=320,
        **NAVY_THEME
    )
    return fig


def plot_crop_yield_distributions(df: pd.DataFrame) -> go.Figure:
    """Boxplot displaying historical yield spread across all 14 crops."""
    fig = px.box(
        df,
        x="Crop",
        y="Yield_ton_ha",
        color="Crop",
        labels={"Yield_ton_ha": "Yield (Tons / Hectare)", "Crop": "Crop Variety"}
    )
    fig.update_layout(
        title="<b>Empirical Yield Distributions by Crop Variety (Tons/ha)</b>",
        xaxis={"tickangle": -45},
        showlegend=False,
        **NAVY_THEME
    )
    return fig
