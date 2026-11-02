"""
Phytopathological Disease Knowledge Base.
Contains verified scientific profiles, pathogen data, visual symptoms,
chemical treatments, organic controls, and preventative practices.
"""

from typing import Dict, Any, Optional

DISEASE_CATALOG: Dict[str, Dict[str, Any]] = {
    "Rice___Bacterial_Blight": {
        "crop": "Rice",
        "disease_name": "Bacterial Leaf Blight",
        "pathogen": "Xanthomonas oryzae pv. oryzae",
        "type": "Bacterial",
        "symptoms": "Water-soaked stripes along leaf margins progressing into wavy yellow to straw-white necrotic lesions. Bacterial ooze drops may form on young lesions during humid mornings.",
        "risk_factors": "High humidity (85-95%), ambient temperatures between 25-34°C, deep waterlogging, and excessive nitrogen fertilizer.",
        "chemical_treatment": [
            "Spray Copper Oxychloride 50 WP @ 2.5 g/L + Streptocycline @ 0.1 g/L (100 ppm) of water at early appearance.",
            "Secondary spray of Kresoxim-methyl 44.3 SC @ 1 mL/L if fungal co-infections are suspected."
        ],
        "organic_control": [
            "Foliar spray of fresh Cow Dung Extract (20%) or Panchagavya (3%) at 10-day intervals.",
            "Apply seed treatment with Pseudomonas fluorescens @ 10 g/kg seed."
        ],
        "prevention": [
            "Avoid excessive split applications of Nitrogen fertilizer.",
            "Maintain intermittent field drainage; do not allow standing water to circulate between fields.",
            "Grow resistant cultivars (e.g. IR64, Improved Samba Mahsuri)."
        ],
        "icon": "🌾"
    },
    "Rice___Brown_Spot": {
        "crop": "Rice",
        "disease_name": "Brown Spot Disease",
        "pathogen": "Bipolaris oryzae (Cochliobolus miyabeanus)",
        "type": "Fungal",
        "symptoms": "Oval or circular brown lesions with gray or whitish centers and distinct yellow chlorotic halos distributed uniformly across leaf blades.",
        "risk_factors": "Nutrient-deficient soils (especially low Potassium and Silicon), drought stress, and intermittent rainfall.",
        "chemical_treatment": [
            "Spray Mancozeb 75 WP @ 2 g/L or Propiconazole 25 EC @ 1 mL/L upon first detection.",
            "Spray Edifenphos 50 EC @ 1 mL/L during panicle initiation."
        ],
        "organic_control": [
            "Foliar spray with Neem oil (3%) or garlic bulb extract (5%).",
            "Seed treatment with Trichoderma viride @ 4 g/kg seed."
        ],
        "prevention": [
            "Ensure balanced fertilization; do not starve the crop of Potassium and Micronutrients.",
            "Pre-treat seeds with hot water (52-54°C for 10 minutes) before nursery sowing."
        ],
        "icon": "🌾"
    },
    "Rice___Leaf_Blast": {
        "crop": "Rice",
        "disease_name": "Rice Blast (Leaf Blast)",
        "pathogen": "Magnaporthe oryzae (Pyricularia oryzae)",
        "type": "Fungal",
        "symptoms": "Spindle-shaped (elliptical) lesions with pointed ends, gray centers, and brown margins. Lesions rapidly coalesce to kill entire leaf blades in blast epidemics.",
        "risk_factors": "High relative humidity (>90%), dew condensation on leaves for over 8 hours, and night temperatures below 20°C.",
        "chemical_treatment": [
            "Foliar application of Tricyclazole 75 WP @ 0.6 g/L of water at the nursery or tillering stage.",
            "Alternative spray: Isoprothiolane 40 EC @ 1.5 mL/L or Kasugamycin 3 SL @ 2 mL/L."
        ],
        "organic_control": [
            "Seed coating with Pseudomonas fluorescens (Pf1) @ 10 g/kg.",
            "Spray fermented buttermilk (5%) or seaweed kelp extract."
        ],
        "prevention": [
            "Avoid excessive basal or top-dressed Nitrogen.",
            "Maintain flooded water layer during cold nights to protect plant crowns."
        ],
        "icon": "🌾"
    },
    "Potato___Early_Blight": {
        "crop": "Potato",
        "disease_name": "Early Blight",
        "pathogen": "Alternaria solani",
        "type": "Fungal",
        "symptoms": "Dark brown to black angular spots on older foliage featuring concentric target-board rings. Yellowing surrounds the necrotic patches as leaves wither.",
        "risk_factors": "Alternating wet and dry spells, warm temperatures (24-29°C), and aging crop canopies under nutrient stress.",
        "chemical_treatment": [
            "Spray Chlorothalonil 75 WP @ 2 g/L or Mancozeb 75 WP @ 2.5 g/L upon observing lower leaf spotting.",
            "Systemic option: Azoxystrobin 23 SC @ 1 mL/L or Difenoconazole 25 EC @ 0.5 mL/L."
        ],
        "organic_control": [
            "Bordeaux mixture (1%) preventative spray.",
            "Foliar spray with Bacillus subtilis culture or copper soap solution."
        ],
        "prevention": [
            "Practice 3-year crop rotation with non-solanaceous crops.",
            "Mulch beds to prevent soil spores from splashing onto lower leaves."
        ],
        "icon": "🥔"
    },
    "Potato___Late_Blight": {
        "crop": "Potato",
        "disease_name": "Late Blight",
        "pathogen": "Phytophthora infestans",
        "type": "Oomycete / Fungal-like",
        "symptoms": "Rapidly expanding water-soaked blackish lesions starting from leaf tips and margins. In humid conditions, white fluffy mold sporulation appears on the leaf underside.",
        "risk_factors": "High humidity (>90%), cool temperatures (15-20°C), dense fog, and prolonged leaf wetness.",
        "chemical_treatment": [
            "Prophylactic: Mancozeb 75 WP @ 2.5 g/L before onset of overcast foggy weather.",
            "Curative: Metalaxyl 8% + Mancozeb 64% WP @ 2.5 g/L or Cymoxanil 8% + Mancozeb 64% @ 2 g/L."
        ],
        "organic_control": [
            "Copper hydroxide (Kocide) @ 2 g/L at weekly intervals.",
            "Strict destruction and burning of infected potato haulms."
        ],
        "prevention": [
            "Plant certified disease-free seed tubers.",
            "Earth up rows deeply to prevent sporangia from washing down into developing tubers."
        ],
        "icon": "🥔"
    },
    "Tomato___Early_Blight": {
        "crop": "Tomato",
        "disease_name": "Early Blight",
        "pathogen": "Alternaria linariae (Alternaria solani)",
        "type": "Fungal",
        "symptoms": "Concentric dark brown rings resembling a bullseye on mature lower leaves. Tissue around lesions turns yellow, leading to premature defoliation and sunscald on fruits.",
        "risk_factors": "Warm damp conditions (24-30°C), heavy morning dew, and splash irrigation.",
        "chemical_treatment": [
            "Spray Mancozeb 75 WP @ 2 g/L or Copper Oxychloride 50 WP @ 2.5 g/L.",
            "Curative: Tebuconazole 25.9 EC @ 1 mL/L."
        ],
        "organic_control": [
            "Foliar sprays of Trichoderma harzianum @ 5 g/L.",
            "Apply baking soda solution (1 tbsp baking soda + 1 tsp horticultural oil per gallon)."
        ],
        "prevention": [
            "Stake and prune lower sucker branches to keep foliage at least 30 cm above soil.",
            "Switch to drip irrigation to keep tomato foliage dry."
        ],
        "icon": "🍅"
    },
    "Tomato___Late_Blight": {
        "crop": "Tomato",
        "disease_name": "Late Blight",
        "pathogen": "Phytophthora infestans",
        "type": "Oomycete / Water Mold",
        "symptoms": "Large, irregular oily dark green to purplish-brown lesions on leaves and stems. White downy sporulation develops on undersides during wet weather.",
        "risk_factors": "Cool overcast days (15-22°C) combined with prolonged leaf wetness (>10 hours).",
        "chemical_treatment": [
            "Dimethomorph 50 WP @ 1 g/L or Famoxadone 16.6% + Cymoxanil 22.1% SC @ 1 mL/L.",
            "Protective spray with Chlorothalonil 75 WP @ 2 g/L."
        ],
        "organic_control": [
            "Copper octanoate (copper soap) sprays every 7 days during high-risk cool weather.",
            "Immediate removal and bagging of infected vine sections."
        ],
        "prevention": [
            "Ensure wide plant spacing for vigorous air circulation.",
            "Avoid planting adjacent to potato fields."
        ],
        "icon": "🍅"
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "disease_name": "Leaf Mold",
        "pathogen": "Passalora fulva (Cladosporium fulvum)",
        "type": "Fungal",
        "symptoms": "Pale green or yellowish spots with diffuse margins on upper leaf surfaces; velvety olive-green to grayish fungal velvety mold on the corresponding leaf undersides.",
        "risk_factors": "Relative humidity >85% and warm temperatures (21-27°C), typical in polyhouses and greenhouse tunnels.",
        "chemical_treatment": [
            "Spray Difenoconazole 25 EC @ 0.5 mL/L or Azoxystrobin 23 SC @ 1 mL/L.",
            "Copper Oxychloride @ 2.5 g/L."
        ],
        "organic_control": [
            "Sulfur-based fungicides or bio-fungicide Bacillus amyloliquefaciens.",
            "Increase ventilation fans in covered greenhouse tunnels."
        ],
        "prevention": [
            "Dramatically reduce indoor greenhouse relative humidity by increasing venting.",
            "Prune inner suckers to improve sunlight penetration."
        ],
        "icon": "🍅"
    },
    "Corn___Common_Rust": {
        "crop": "Corn (Maize)",
        "disease_name": "Common Rust",
        "pathogen": "Puccinia sorghi",
        "type": "Fungal (Basidiomycete)",
        "symptoms": "Golden-brown to cinnamon-brown powdery pustules (uredinia) scattered across both upper and lower leaf surfaces. Pustules rupture the epidermis to release powdery spores.",
        "risk_factors": "Cool temperatures (16-25°C), high relative humidity (>95%), and heavy overnight dews.",
        "chemical_treatment": [
            "Spray Pyraclostrobin 20% WG @ 1 g/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 mL/L.",
            "Mancozeb 75 WP @ 2.5 g/L at initial pustule emergence."
        ],
        "organic_control": [
            "Foliar spray with sulfur dust (20 kg/ha) or neem seed kernel extract (NSKE 5%).",
            "Plant rust-tolerant hybrid maize lines."
        ],
        "prevention": [
            "Plant early in the season to avoid peak fungal spore migrations.",
            "Deep plow crop residue to bury overwintering teliospores."
        ],
        "icon": "🌽"
    },
    "Apple___Apple_Scab": {
        "crop": "Apple",
        "disease_name": "Apple Scab",
        "pathogen": "Venturia inaequalis",
        "type": "Fungal (Ascomycete)",
        "symptoms": "Dull olive-green to velvety brown-black spots on leaves and young fruit. Lesions become corky, scabbed, and can cause severe leaf deformation and premature drop.",
        "risk_factors": "Spring rainfall events with continuous leaf wetness at 10-24°C during bud break.",
        "chemical_treatment": [
            "Spray Captan 50 WP @ 2 g/L or Dodine 65 WP @ 1 g/L during pink bud and petal fall stages.",
            "Post-infection systemic: Myclobutanil 10 WP @ 0.5 g/L."
        ],
        "organic_control": [
            "Lime sulfur spray during late dormancy before bud swell.",
            "Shred and rake fallen autumn leaves to eliminate overwintering pseudothecia."
        ],
        "prevention": [
            "Prune apple canopies annually into open-center or modified central leader systems.",
            "Apply urea (5%) spray to orchard floor in late autumn to speed leaf decomposition."
        ],
        "icon": "🍏"
    },
    "Cotton___Bacterial_Blight": {
        "crop": "Cotton",
        "disease_name": "Bacterial Blight (Blackarm)",
        "pathogen": "Xanthomonas citri pv. malvacearum",
        "type": "Bacterial",
        "symptoms": "Angular water-soaked spots bounded by leaf veins ('Angular Leaf Spot'). As lesions mature, they turn dark brown to black and spread down petioles and stems ('Blackarm').",
        "risk_factors": "Warm rainy weather (28-35°C), wind-driven rainstorms, and sprinkler irrigation.",
        "chemical_treatment": [
            "Spray Copper Oxychloride 50 WP @ 2.5 g/L + Streptocycline @ 0.1 g/L.",
            "Repeat after 12-15 days if rainfall continues."
        ],
        "organic_control": [
            "Seed delinting with concentrated sulfuric acid (H2SO4 @ 100 mL/kg seed).",
            "Seed treatment with Pseudomonas fluorescens @ 10 g/kg."
        ],
        "prevention": [
            "Use certified acid-delinted seeds to destroy seed-coat bacterial reservoirs.",
            "Destroy and bury previous cotton stubble."
        ],
        "icon": "🪴"
    },
    "Healthy___Foliage": {
        "crop": "General / All Crops",
        "disease_name": "Healthy Leaf Foliage",
        "pathogen": "None (No Pathological Infection)",
        "type": "Healthy Plant Tissue",
        "symptoms": "Uniform deep green coloration, intact epidermal cell structure, crisp venation, and completely clean leaf blade with zero necrotic lesions or chlorotic spotting.",
        "risk_factors": "N/A — Optimal vegetative state.",
        "chemical_treatment": [
            "No chemical fungicides or bactericides required.",
            "Continue standard balanced nutritional maintenance."
        ],
        "organic_control": [
            "Apply preventative seaweed extract or humic acid foliar nourishment.",
            "Maintain soil biodiversity with compost tea or mycorrhizae."
        ],
        "prevention": [
            "Continue periodic field monitoring.",
            "Maintain optimal irrigation and balanced NPK fertility."
        ],
        "icon": "🌿"
    }
}


def get_disease_profile(disease_key: str) -> Optional[Dict[str, Any]]:
    """Retrieve full diagnostic profile for a disease key."""
    return DISEASE_CATALOG.get(disease_key, None)


def list_all_diseases() -> list:
    """Return sorted list of all supported disease identifiers."""
    return sorted(list(DISEASE_CATALOG.keys()))
