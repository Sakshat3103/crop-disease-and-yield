"""
Crop Yield Dataset Synthesis & ML Regression Training Engine.
Generates empirical agronomic production records across 14 crops based on ICAR and FAO
yield equations, then trains and benchmarks 4 regression algorithms.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 14 Agricultural Crops with baseline potential (tons/ha), optimal conditions, and MSP (INR/ton)
CROP_YIELD_PROFILES = {
    "Rice": {
        "base_yield": 4.2, "yield_std": 0.8, "opt_rain": 200, "opt_temp": 26, "opt_ph": 6.5,
        "n_req": 90, "p_req": 45, "k_req": 45, "seasons": ["Kharif", "Summer"],
        "msp_per_ton": 22000
    },
    "Wheat": {
        "base_yield": 3.8, "yield_std": 0.6, "opt_rain": 85, "opt_temp": 19, "opt_ph": 6.8,
        "n_req": 110, "p_req": 50, "k_req": 40, "seasons": ["Rabi"],
        "msp_per_ton": 22750
    },
    "Maize": {
        "base_yield": 4.5, "yield_std": 0.9, "opt_rain": 110, "opt_temp": 24, "opt_ph": 6.5,
        "n_req": 100, "p_req": 50, "k_req": 40, "seasons": ["Kharif", "Rabi"],
        "msp_per_ton": 20900
    },
    "Cotton": {
        "base_yield": 2.2, "yield_std": 0.4, "opt_rain": 90, "opt_temp": 26, "opt_ph": 7.0,
        "n_req": 110, "p_req": 45, "k_req": 45, "seasons": ["Kharif"],
        "msp_per_ton": 66200
    },
    "Sugarcane": {
        "base_yield": 75.0, "yield_std": 12.0, "opt_rain": 220, "opt_temp": 28, "opt_ph": 6.8,
        "n_req": 160, "p_req": 65, "k_req": 90, "seasons": ["Whole Year"],
        "msp_per_ton": 3150
    },
    "Potato": {
        "base_yield": 24.0, "yield_std": 4.5, "opt_rain": 75, "opt_temp": 18, "opt_ph": 5.8,
        "n_req": 130, "p_req": 80, "k_req": 100, "seasons": ["Rabi"],
        "msp_per_ton": 15000
    },
    "Tomato": {
        "base_yield": 28.0, "yield_std": 5.0, "opt_rain": 80, "opt_temp": 23, "opt_ph": 6.3,
        "n_req": 120, "p_req": 70, "k_req": 90, "seasons": ["Kharif", "Rabi", "Summer"],
        "msp_per_ton": 18000
    },
    "Chickpea": {
        "base_yield": 1.4, "yield_std": 0.3, "opt_rain": 60, "opt_temp": 19, "opt_ph": 7.2,
        "n_req": 30, "p_req": 60, "k_req": 40, "seasons": ["Rabi"],
        "msp_per_ton": 54400
    },
    "Soybean": {
        "base_yield": 2.1, "yield_std": 0.4, "opt_rain": 110, "opt_temp": 25, "opt_ph": 6.6,
        "n_req": 40, "p_req": 70, "k_req": 50, "seasons": ["Kharif"],
        "msp_per_ton": 46000
    },
    "Groundnut": {
        "base_yield": 2.4, "yield_std": 0.45, "opt_rain": 85, "opt_temp": 27, "opt_ph": 6.5,
        "n_req": 35, "p_req": 55, "k_req": 45, "seasons": ["Kharif", "Summer"],
        "msp_per_ton": 63770
    },
    "Banana": {
        "base_yield": 48.0, "yield_std": 8.0, "opt_rain": 180, "opt_temp": 28, "opt_ph": 6.5,
        "n_req": 150, "p_req": 60, "k_req": 160, "seasons": ["Whole Year"],
        "msp_per_ton": 21000
    },
    "Apple": {
        "base_yield": 14.0, "yield_std": 2.8, "opt_rain": 120, "opt_temp": 16, "opt_ph": 6.0,
        "n_req": 60, "p_req": 40, "k_req": 90, "seasons": ["Whole Year"],
        "msp_per_ton": 55000
    },
    "Mustard": {
        "base_yield": 1.6, "yield_std": 0.3, "opt_rain": 50, "opt_temp": 18, "opt_ph": 7.0,
        "n_req": 70, "p_req": 40, "k_req": 35, "seasons": ["Rabi"],
        "msp_per_ton": 56500
    },
    "Barley": {
        "base_yield": 3.2, "yield_std": 0.5, "opt_rain": 60, "opt_temp": 18, "opt_ph": 7.2,
        "n_req": 65, "p_req": 35, "k_req": 30, "seasons": ["Rabi"],
        "msp_per_ton": 18500
    }
}

STATES = [
    "Punjab", "Uttar Pradesh", "Maharashtra", "Madhya Pradesh", 
    "Andhra Pradesh", "Karnataka", "Gujarat", "Tamil Nadu", "Haryana", "Bihar"
]


def generate_crop_yield_dataset(n_samples: int = 2800, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic empirical crop yield records respecting biological response curves.
    """
    np.random.seed(seed)
    crops = list(CROP_YIELD_PROFILES.keys())
    
    rows = []
    samples_per_crop = n_samples // len(crops)
    
    for crop in crops:
        p = CROP_YIELD_PROFILES[crop]
        for _ in range(samples_per_crop):
            season = np.random.choice(p["seasons"])
            state = np.random.choice(STATES)
            
            # Area in Hectares (0.5 to 45 ha)
            area = round(float(np.random.exponential(scale=5.0) + 0.5), 2)
            area = min(area, 50.0)
            
            # Weather variables around crop optimum with natural variance
            rainfall = max(20.0, float(np.random.normal(loc=p["opt_rain"], scale=40.0)))
            temp = float(np.clip(np.random.normal(loc=p["opt_temp"], scale=4.0), 10.0, 42.0))
            ph = float(np.clip(np.random.normal(loc=p["opt_ph"], scale=0.6), 4.5, 8.8))
            
            # Soil nutrients applied
            n_val = max(10.0, float(np.random.normal(loc=p["n_req"], scale=25.0)))
            p_val = max(5.0, float(np.random.normal(loc=p["p_req"], scale=18.0)))
            k_val = max(5.0, float(np.random.normal(loc=p["k_req"], scale=20.0)))
            
            # Biological Liebig Law factor (limiting nutrient response)
            n_ratio = min(n_val / p["n_req"], 1.25)
            p_ratio = min(p_val / p["p_req"], 1.25)
            k_ratio = min(k_val / p["k_req"], 1.25)
            nutrient_factor = (n_ratio * 0.4 + p_ratio * 0.3 + k_ratio * 0.3)
            
            # Environmental stress penalty
            rain_diff = abs(rainfall - p["opt_rain"]) / p["opt_rain"]
            rain_factor = max(0.4, 1.0 - (0.45 * rain_diff))
            
            temp_diff = abs(temp - p["opt_temp"]) / p["opt_temp"]
            temp_factor = max(0.45, 1.0 - (0.5 * temp_diff))
            
            ph_diff = abs(ph - p["opt_ph"])
            ph_factor = max(0.6, 1.0 - (0.15 * ph_diff))
            
            # Combined Yield (Tons/ha)
            yield_val = p["base_yield"] * (0.35 + 0.30 * nutrient_factor + 0.15 * rain_factor + 0.15 * temp_factor + 0.05 * ph_factor)
            # Add stochastic environmental variation
            yield_val += float(np.random.normal(0, p["yield_std"] * 0.25))
            yield_val = max(0.2, round(yield_val, 2))
            
            # Total production
            production = round(yield_val * area, 2)
            
            rows.append({
                "Crop": crop,
                "Season": season,
                "State": state,
                "Area_Hectares": area,
                "Rainfall_mm": round(rainfall, 1),
                "Temperature_C": round(temp, 1),
                "Soil_pH": round(ph, 2),
                "Nitrogen_kg_ha": round(n_val, 1),
                "Phosphorus_kg_ha": round(p_val, 1),
                "Potassium_kg_ha": round(k_val, 1),
                "Yield_ton_ha": yield_val,
                "Production_ton": production
            })
            
    df = pd.DataFrame(rows)
    return df


def train_and_save_yield_models(df: pd.DataFrame, models_dir: str) -> dict:
    """
    Train 4 regression models, evaluate, and serialize.
    """
    os.makedirs(models_dir, exist_ok=True)
    
    feature_cols = [
        "Crop", "Season", "Area_Hectares", "Rainfall_mm", 
        "Temperature_C", "Soil_pH", "Nitrogen_kg_ha", 
        "Phosphorus_kg_ha", "Potassium_kg_ha"
    ]
    target_col = "Yield_ton_ha"
    
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    
    cat_cols = ["Crop", "Season"]
    num_cols = ["Area_Hectares", "Rainfall_mm", "Temperature_C", "Soil_pH", "Nitrogen_kg_ha", "Phosphorus_kg_ha", "Potassium_kg_ha"]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
        ]
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "random_forest": {
            "name": "Random Forest Regressor",
            "model": RandomForestRegressor(n_estimators=100, max_depth=16, random_state=42, n_jobs=-1),
            "desc": "Ensemble of 100 regression trees modeling complex non-linear Liebig nutrient limits and weather interactions."
        },
        "gradient_boosting": {
            "name": "Gradient Boosting Regressor",
            "model": GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42),
            "desc": "Sequential boosting minimizing pseudo-residuals for high precision forecasting."
        },
        "decision_tree": {
            "name": "Decision Tree Regressor",
            "model": DecisionTreeRegressor(max_depth=10, random_state=42),
            "desc": "Hierarchical tree partitioning feature spaces into discrete yield bins."
        },
        "ridge_regression": {
            "name": "Ridge Regressor (L2 Linear)",
            "model": Ridge(alpha=10.0),
            "desc": "Regularized linear regression penalizing large coefficients across standardized factors."
        }
    }
    
    results = {}
    best_r2 = -1.0
    best_pipe = None
    best_key = None
    
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    print("\n" + "="*70)
    print("TRAINING AND EVALUATING CROP YIELD REGRESSION MODELS")
    print("="*70)
    
    for key, cfg in models.items():
        pipe = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", cfg["model"])
        ])
        
        # Train
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        
        r2 = float(r2_score(y_test, y_pred))
        mae = float(mean_absolute_error(y_test, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        cv_r2 = cross_val_score(pipe, X_train, y_train, cv=kf, scoring="r2")
        
        results[key] = {
            "display_name": cfg["name"],
            "description": cfg["desc"],
            "r2_score": round(r2, 4),
            "mae": round(mae, 4),
            "rmse": round(rmse, 4),
            "cv_mean": round(float(np.mean(cv_r2)), 4),
            "cv_std": round(float(np.std(cv_r2)), 4)
        }
        
        # Save individual model pipeline
        model_path = os.path.join(models_dir, f"yield_{key}.pkl")
        joblib.dump(pipe, model_path)
        
        print(f"[*] {cfg['name']}:")
        print(f"    - R² Score : {r2 * 100:.2f}%")
        print(f"    - MAE      : {mae:.3f} ton/ha")
        print(f"    - RMSE     : {rmse:.3f} ton/ha")
        print(f"    - 5-Fold CV: {np.mean(cv_r2) * 100:.2f}% (±{np.std(cv_r2)*100:.2f}%)")
        
        if r2 > best_r2:
            best_r2 = r2
            best_pipe = pipe
            best_key = key
            
    # Serialize best model
    best_path = os.path.join(models_dir, "yield_best_model.pkl")
    joblib.dump(best_pipe, best_path)
    print(f"\n[🏆] Best Yield Model: {models[best_key]['name']} (R²: {best_r2*100:.2f}%)")
    
    # Save metrics json
    metrics_summary = {
        "best_model_key": best_key,
        "best_model_name": models[best_key]["name"],
        "feature_names": feature_cols,
        "target": target_col,
        "supported_crops": sorted(list(CROP_YIELD_PROFILES.keys())),
        "seasons": ["Kharif", "Rabi", "Summer", "Whole Year"],
        "models": results
    }
    
    with open(os.path.join(models_dir, "yield_metrics.json"), "w") as f:
        json.dump(metrics_summary, f, indent=2)
        
    return metrics_summary


if __name__ == "__main__":
    data_dir = os.path.join(PROJECT_ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_file = os.path.join(data_dir, "crop_yield_production.csv")
    
    print("[*] Generating empirical crop yield dataset...")
    df_yield = generate_crop_yield_dataset(n_samples=2800)
    df_yield.to_csv(csv_file, index=False)
    print(f"[+] Saved {len(df_yield)} yield records to {csv_file}")
    
    train_and_save_yield_models(df_yield, os.path.join(PROJECT_ROOT, "models"))
