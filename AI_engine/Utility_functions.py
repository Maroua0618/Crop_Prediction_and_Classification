
import pandas as pd

def get_crop_requirements(file_path=None):
    """
    Generate sample crop requirements if data file isn't available or has errors
    """


    df = pd.read_csv(file_path)


    if 'label' in df.columns:

        features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        crop_stats = df.groupby('label')[features].agg(['min', 'max'])
        df = df[features + ['label']].rename(columns={'label': 'Crop_Type'})
        profiles = {}
        for crop in df['Crop_Type'].unique():
            crop_data = df[df['Crop_Type'] == crop]
            profiles[crop] = {f: crop_data[f].mean() for f in features}
        crop_requirements = {}
        for crop in crop_stats.index:
            feature_ranges = {}
            for feature in features:
                        min_val = crop_stats.loc[crop, (feature, 'min')]
                        max_val = crop_stats.loc[crop, (feature, 'max')]
                        feature_ranges[feature] = (round(min_val, 1), round(max_val, 1))
            crop_requirements[crop] = feature_ranges

        return crop_requirements,df, features, profiles

agricultural_practices_effects = {
    "add_organic_matter": {
        "unit": "tonnes/ha",
        "effects": {
            "N": {
                "effect_per_unit": 0.055,  # % total N increase per tonne/ha of compost
                "notes": "4.5 t/ha compost increases total N by ~0.25 percentage points"
            },
            "P": {
                "effect_per_unit": 8.5,  # % increase in available P per tonne/ha of compost
                "notes": "4.5 t/ha compost increases available P by ~38.5%"
            },
            "K": {
                "effect_per_unit": 4.17,  # ppm K increase per % SOM increase
                "notes": "2.4% SOM increase raises soil K by ~100 ppm; 10 t/ha adds ~100-200 kg K₂O"
            },
            "humidity": {  # Changed from moisture to match feature naming in dataset
                "effect_per_unit": 3.8,  # % soil moisture increase per tonne/ha of compost
                "notes": "4.5 t/ha compost increases soil moisture by ~17%"
            },
            "ph": {  # Changed from pH to match feature naming in dataset
                "effect_per_unit": 0.017,  # pH unit increase per tonne/ha of compost (over 3 years)
                "notes": "15-45 t/ha compost over 3 years raises pH by 0.5-0.75 units"
            }
        }
    },

    "irrigation_frequency": {
        "unit": "days_between_irrigation",
        "effects": {
            "N": {
                "effect_per_unit": 0.017,  # % increase in available N per additional day between irrigation events
                "notes": "9-day vs 3-day interval showed ~10% higher soil N; 10% ÷ 6 days ≈ 1.7% per day"
            },
            "P": {
                "effect_per_unit": 0.007,  # % increase in available P per day (optimal around 7-day interval)
                "notes": "7-day interval optimal for P availability, showing ~4% higher P than 3-day"
            },
            "K": {
                "effect_per_unit": 0.026,  # % increase in available K per additional day between irrigation
                "notes": "9-day vs 3-day interval showed ~10_23% higher soil K; Average:16% ÷ 6 days ≈ 2.6% per day"
            },
            "humidity": {  # Changed from moisture to match feature naming
                "effect_per_unit": -0.03,  # fractional decrease in average moisture per additional day between irrigation
                "notes": "Less frequent irrigation reduces average soil moisture by ~3% per additional day"
            }
        }
    },

    "apply_N_fertilizer": {
        "unit": "kg N/ha",
        "effects": {
            "N": {
                "effect_per_unit": 0.375,  # ppm soil nitrate-N increase per kg N/ha applied
                "notes": "100 kg N/ha increases soil nitrate by ~25_50 ppm in top 30 cm (varies by soil)"
            }
        }
    },

    "apply_P_fertilizer": {
        "unit": "kg P₂O₅/ha",
        "effects": {
            "P": {
                "effect_per_unit": 0.2,  # ppm increase in soil-test P per kg P₂O₅/ha
                "notes": "50 kg P₂O₅/ha increases soil-test P by ~10 ppm (varies by soil fixation capacity)"
            }
        }
    },

    "apply_K_fertilizer": {
        "unit": "kg K₂O/ha",
        "effects": {
            "K": {
                "effect_per_unit": 0.4,  # ppm increase in soil-test K per kg K₂O/ha
                "notes": "100 kg K₂O/ha increases soil-test K by ~50 ppm (varies by soil CEC)"
            }
        }
    }
}



