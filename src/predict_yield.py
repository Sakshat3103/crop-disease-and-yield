"""
Yield Prediction Inference Engine for AgriVision AI.
Predicts crop yield per hectare, calculates gross farm production, estimates market revenue,
and identifies agronomic limiting factors to suggest actionable yield boosts.
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.yield_data_generator import CROP_YIELD_PROFILES


class CropYieldPredictor:
    """
    Inference and agronomic advisory wrapper for crop yield regression models.
    """
    
    def __init__(self, models_dir: Optional[str] = None):
        if models_dir is None:
            models_dir = os.path.join(PROJECT_ROOT, "models")
        self.models_dir = models_dir
        self._loaded_models: Dict[str, Any] = {}
        
    def load_model(self, model_key: str = "yield_best_model") -> Any:
        """Load trained regression pipeline with caching."""
        if model_key in self._loaded_models:
            return self._loaded_models[model_key]
            
        filename = f"{model_key}.pkl" if not model_key.endswith(".pkl") else model_key
        path = os.path.join(self.models_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model artifact not found at '{path}'.")
            
        model = joblib.load(path)
        self._loaded_models[model_key] = model
        return model

    def estimate_yield(
        self,
        inputs: Dict[str, Any],
        model_key: str = "yield_best_model"
    ) -> Dict[str, Any]:
        """
        Estimate crop yield, gross production, market value, and agronomic optimization advice.
        
        Args:
            inputs: Dict with keys: Crop, Season, Area_Hectares, Rainfall_mm, 
                    Temperature_C, Soil_pH, Nitrogen_kg_ha, Phosphorus_kg_ha, Potassium_kg_ha
            model_key: Key of model to use.
            
        Returns:
            Structured dictionary of yield predictions and advisory details.
        """
        crop = inputs["Crop"]
        if crop not in CROP_YIELD_PROFILES:
            raise ValueError(f"Crop '{crop}' is not currently in supported yield profiles.")
            
        crop_prof = CROP_YIELD_PROFILES[crop]
        
        # Format input DataFrame matching training columns
        feature_cols = [
            "Crop", "Season", "Area_Hectares", "Rainfall_mm", 
            "Temperature_C", "Soil_pH", "Nitrogen_kg_ha", 
            "Phosphorus_kg_ha", "Potassium_kg_ha"
        ]
        input_df = pd.DataFrame([{col: inputs[col] for col in feature_cols}])
        
        # Inference
        pipeline = self.load_model(model_key)
        raw_pred = pipeline.predict(input_df)[0]
        
        # Enforce physical non-negativity
        yield_per_ha = max(0.1, round(float(raw_pred), 2))
        area = float(inputs["Area_Hectares"])
        total_ton = round(yield_per_ha * area, 2)
        total_quintals = round(total_ton * 10, 2)
        
        # Market Value in INR (MSP-based)
        msp = crop_prof.get("msp_per_ton", 20000)
        est_revenue = round(total_ton * msp, 0)
        
        # Benchmark efficiency
        base_pot = crop_prof["base_yield"]
        efficiency = min(100.0, round((yield_per_ha / (base_pot * 1.15)) * 100, 1))
        
        # Identify Limiting Factors & Generate Agronomic Guidance
        limiting_factors: List[str] = []
        actionable_tips: List[str] = []
        
        # Nitrogen Check
        n_in = float(inputs["Nitrogen_kg_ha"])
        if n_in < crop_prof["n_req"] * 0.8:
            defic = round(crop_prof["n_req"] - n_in, 1)
            limiting_factors.append(f"Nitrogen deficiency (Current: {n_in} kg/ha vs. Target: {crop_prof['n_req']} kg/ha).")
            actionable_tips.append(f"Top-dress with approximately {defic * 2.17:.0f} kg/ha of Urea in split applications during vegetative tillering.")
            
        # Phosphorus Check
        p_in = float(inputs["Phosphorus_kg_ha"])
        if p_in < crop_prof["p_req"] * 0.8:
            limiting_factors.append(f"Sub-optimal Phosphorus (Current: {p_in} kg/ha vs. Target: {crop_prof['p_req']} kg/ha).")
            actionable_tips.append("Apply basal Diammonium Phosphate (DAP) or Single Super Phosphate (SSP) during seedbed preparation to foster root expansion.")

        # Potassium Check
        k_in = float(inputs["Potassium_kg_ha"])
        if k_in < crop_prof["k_req"] * 0.8:
            limiting_factors.append(f"Potassium deficit (Current: {k_in} kg/ha vs. Target: {crop_prof['k_req']} kg/ha).")
            actionable_tips.append("Incorporate Muriate of Potash (MOP) to enhance stalk rigidity, grain fill weight, and drought resilience.")
            
        # Rainfall / Moisture Check
        rain_in = float(inputs["Rainfall_mm"])
        if rain_in < crop_prof["opt_rain"] * 0.75:
            limiting_factors.append(f"Moisture stress: Seasonal rainfall ({rain_in} mm) is substantially below the crop's ideal demand ({crop_prof['opt_rain']} mm).")
            actionable_tips.append("Deploy scheduled drip or sprinkler micro-irrigation at critical stages (flowering and grain-filling) to recover up to 20-30% yield loss.")
        elif rain_in > crop_prof["opt_rain"] * 1.4:
            limiting_factors.append(f"Excess water risk: Rainfall ({rain_in} mm) is higher than optimum ({crop_prof['opt_rain']} mm).")
            actionable_tips.append("Ensure proper furrow drainage and bed elevation to prevent waterlogging and root hypoxia.")
            
        # Soil pH Check
        ph_in = float(inputs["Soil_pH"])
        if ph_in < crop_prof["opt_ph"] - 0.7:
            limiting_factors.append(f"Acidic soil stress (pH {ph_in} vs. optimum {crop_prof['opt_ph']}).")
            actionable_tips.append("Apply agricultural lime (calcium carbonate) or dolomite to neutralize soil acidity and unlock fixed nutrients.")
        elif ph_in > crop_prof["opt_ph"] + 0.7:
            limiting_factors.append(f"Alkaline soil stress (pH {ph_in} vs. optimum {crop_prof['opt_ph']}).")
            actionable_tips.append("Incorporate agricultural gypsum and organic farmyard manure (FYM) to remediate sodic alkalinity.")

        if not limiting_factors:
            limiting_factors.append("Optimal balance: Environmental parameters align very closely with maximum yield potential.")
            actionable_tips.append("Maintain current management practices and practice preventative disease scouting.")
            
        return {
            "crop": crop,
            "season": inputs["Season"],
            "area_hectares": area,
            "area_acres": round(area * 2.471, 2),
            "predicted_yield_ton_ha": yield_per_ha,
            "predicted_yield_quintal_ha": round(yield_per_ha * 10, 2),
            "total_production_ton": total_ton,
            "total_production_quintals": total_quintals,
            "msp_per_ton": msp,
            "estimated_revenue_inr": est_revenue,
            "efficiency_percentage": efficiency,
            "limiting_factors": limiting_factors,
            "actionable_tips": actionable_tips,
            "model_used": model_key
        }


if __name__ == "__main__":
    predictor = CropYieldPredictor()
    test_input = {
        "Crop": "Rice",
        "Season": "Kharif",
        "Area_Hectares": 5.0,
        "Rainfall_mm": 180.0,
        "Temperature_C": 26.0,
        "Soil_pH": 6.5,
        "Nitrogen_kg_ha": 95.0,
        "Phosphorus_kg_ha": 45.0,
        "Potassium_kg_ha": 40.0
    }
    res = predictor.estimate_yield(test_input)
    print("Yield estimate test result:\n", res)
