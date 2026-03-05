"""
engineering.py
==============
Derives proven, research-backed features from anthropometric measurements.

Each section is self-contained and can be applied independently.
All functions accept a pandas DataFrame and return it with new columns appended.

Sections
--------
1.  Body Composition Indices   – BMI, BSA, lean mass, fat mass
2.  Obesity & Adiposity Ratios – WHR, WHtR, BAI, Conicity Index
3.  Limb Symmetry & Proportions – limb ratios, trunk-to-limb ratios
4.  Muscle & Frame Size        – FFMI, frame size, relative muscle mass
5.  Convenience wrapper        – run all sections at once

References are cited inline per feature.
"""

import pandas as pd
import numpy as np


# =============================================================================
# 1. BODY COMPOSITION INDICES
# =============================================================================

def add_body_composition_indices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds fundamental body composition indices.

    Features added
    --------------
    bmi
        Body Mass Index = weight(kg) / height(m)²
        Gold-standard screening tool for overweight/obesity.
        Ref: WHO (2000). Obesity: preventing and managing the global epidemic.

    bsa_mosteller
        Body Surface Area (Mosteller formula) = sqrt(height_cm × weight_kg / 3600)
        Used in pharmacology for drug dosing and cardiac output normalisation.
        Ref: Mosteller (1987). N Engl J Med, 317(17), 1098.

    lean_mass_kg
        Estimated lean body mass = MuscleMass_kg is already given, so we derive
        fat_mass_kg and lean_mass_kg from BodyFatPct for cross-validation features.
        fat_mass_kg  = weight_kg × (BodyFatPct / 100)
        lean_mass_kg = weight_kg − fat_mass_kg
        Ref: Heymsfield et al. (2005). Human Body Composition (2nd ed.).

    fat_mass_index (FMI)
        FMI = fat_mass_kg / height_m²
        More discriminating than BMI for adiposity because it isolates fat mass.
        Ref: VanItallie et al. (1990). Am J Clin Nutr, 52(6), 953–959.

    fat_free_mass_index (FFMI)
        FFMI = lean_mass_kg / height_m²
        Standard index for muscle development; values >25 indicate exceptional
        muscularity (natural ceiling in drug-free athletes).
        Ref: Kouri et al. (1995). N Engl J Med, 333(18), 1312–1317.
    """
    df = df.copy()
    height_m = df["Height_cm"] / 100

    df["bmi"]             = df["Weight_kg"] / height_m ** 2
    df["bsa_mosteller"]   = np.sqrt(df["Height_cm"] * df["Weight_kg"] / 3600)
    df["fat_mass_kg"]     = df["Weight_kg"] * (df["BodyFatPct"] / 100)
    df["lean_mass_kg"]    = df["Weight_kg"] - df["fat_mass_kg"]
    df["fat_mass_index"]  = df["fat_mass_kg"] / height_m ** 2
    df["ffmi"]            = df["lean_mass_kg"] / height_m ** 2

    return df


# =============================================================================
# 2. OBESITY & ADIPOSITY RATIOS
# =============================================================================

def add_obesity_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds central adiposity and obesity indices.

    Features added
    --------------
    waist_hip_ratio (WHR)
        WHR = waist_cm / hip_cm
        Strong predictor of cardiovascular risk; WHO thresholds: >0.90 (M), >0.85 (F).
        Ref: WHO (2008). Waist circumference and waist-hip ratio: report of a WHO expert consultation.

    waist_height_ratio (WHtR)
        WHtR = waist_cm / height_cm
        A single universal threshold of 0.5 predicts cardiometabolic risk across ethnicities.
        Ref: Browning et al. (2010). Nutr Metab Cardiovasc Dis, 20(6), 418–426.

    body_adiposity_index (BAI)
        BAI = (hip_cm / height_m^1.5) − 18
        Developed as a direct body fat % estimate without a scale.
        Ref: Bergman et al. (2011). Obesity, 19(5), 1083–1089.

    conicity_index
        CI = waist_cm / (0.109 × sqrt(weight_kg / height_m))
        Captures abdominal fat accumulation; values >1.25 associated with
        increased cardiometabolic risk.
        Ref: Valdez (1991). Am J Hum Biol, 3(5), 501–506.

    abdominal_volume_index (AVI)
        AVI = (2 × waist_cm² + 0.7 × (waist_cm − hip_cm)²) / 1000
        Surrogate for abdominal volume; correlated with visceral fat.
        Ref: Guerrero-Romero & Rodríguez-Morán (2003). Eur J Clin Invest, 33(11), 952–959.

    waist_neck_ratio
        Waist-to-neck ratio; neck circumference is a proxy for upper-body fat
        and is independent of general obesity measures.
        Ref: Hingorjo et al. (2012). J Pak Med Assoc, 62(9), 892–899.
    """
    df = df.copy()
    height_m = df["Height_cm"] / 100

    df["waist_hip_ratio"]         = df["Waist_cm"] / df["Hip_cm"]
    df["waist_height_ratio"]      = df["Waist_cm"] / df["Height_cm"]
    df["body_adiposity_index"]    = (df["Hip_cm"] / (height_m ** 1.5)) - 18
    df["conicity_index"]          = df["Waist_cm"] / (
                                        0.109 * np.sqrt(df["Weight_kg"] / height_m)
                                    )
    df["abdominal_volume_index"]  = (
                                        2 * df["Waist_cm"] ** 2
                                        + 0.7 * (df["Waist_cm"] - df["Hip_cm"]) ** 2
                                    ) / 1000
    df["waist_neck_ratio"]        = df["Waist_cm"] / df["Neck_cm"]

    return df


# =============================================================================
# 3. LIMB SYMMETRY & PROPORTIONS
# =============================================================================

def add_limb_proportions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds limb-to-limb and limb-to-trunk proportion features.

    Features added
    --------------
    upper_lower_limb_ratio
        Upper arm girth / Thigh girth.
        Imbalances may indicate asymmetric fat distribution or sport-specific
        hypertrophy.
        Ref: Heyward & Wagner (2004). Applied Body Composition Assessment (2nd ed.).

    calf_thigh_ratio
        Calf / Thigh circumference.
        Lower values are associated with sarcopenia and insulin resistance.
        Ref: Bouchard et al. (2009). J Nutr Health Aging, 13(10), 883–889.

    arm_trunk_ratio
        Upper arm / Waist circumference.
        Captures relative peripheral muscularity vs. central adiposity.

    forearm_upper_arm_ratio
        Forearm / Upper arm circumference.
        Used in biomechanics; lower ratio can indicate upper-arm hypertrophy.
        Ref: Norton & Olds (1996). Anthropometrica. UNSW Press.

    shoulder_waist_ratio
        Shoulder / Waist circumference (Adonis Index).
        Associated with perceived male attractiveness and upper-body V-taper.
        Ref: Tovée et al. (1999). Proc R Soc B, 266(1436), 211–217.

    hip_waist_difference
        Hip − Waist (cm). Simple proxy for gluteal vs. abdominal mass;
        larger values reflect a more gynoid fat pattern.

    chest_waist_ratio
        Chest / Waist circumference.
        Commonly used in fitness assessments of upper-body proportion.
    """
    df = df.copy()

    df["upper_lower_limb_ratio"]    = df["UpperArm_cm"] / df["Thigh_cm"]
    df["calf_thigh_ratio"]          = df["Calf_cm"] / df["Thigh_cm"]
    df["arm_trunk_ratio"]           = df["UpperArm_cm"] / df["Waist_cm"]
    df["forearm_upper_arm_ratio"]   = df["Forearm_cm"] / df["UpperArm_cm"]
    df["shoulder_waist_ratio"]      = df["Shoulder_cm"] / df["Waist_cm"]
    df["hip_waist_difference"]      = df["Hip_cm"] - df["Waist_cm"]
    df["chest_waist_ratio"]         = df["Chest_cm"] / df["Waist_cm"]

    return df


# =============================================================================
# 4. MUSCLE & FRAME SIZE
# =============================================================================

def add_muscle_and_frame_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds muscle quality and skeletal frame size features.

    Features added
    --------------
    frame_size_index
        Wrist circumference / Height_cm × 100.
        Classifies individuals as small, medium, or large frame.
        Ref: Frisancho & Flegel (1983). Am J Clin Nutr, 37(2), 311–314.

    relative_muscle_mass (RMM)
        MuscleMass_kg / Weight_kg × 100  (%)
        Proportion of total body weight that is skeletal muscle.
        Ref: Janssen et al. (2000). J Appl Physiol, 89(1), 81–88.

    muscle_to_fat_ratio
        MuscleMass_kg / fat_mass_kg.
        Higher values indicate a more favourable body composition.
        Requires fat_mass_kg (run add_body_composition_indices first).

    skeletal_muscle_index (SMI)
        MuscleMass_kg / height_m²
        Primary diagnostic criterion for sarcopenia (cut-offs: <7.0 kg/m² M,
        <5.5 kg/m² F).
        Ref: Baumgartner et al. (1998). Am J Epidemiol, 147(8), 755–763.

    bicep_to_wrist_ratio
        Bicep / Wrist circumference.
        Wrist corrects for frame size when assessing arm muscle development.
        Ref: Casey (2013). Strength and Conditioning Journal, 35(4).

    calf_muscle_index
        Calf circumference / Height_cm × 100.
        Validated proxy for lower-limb muscle mass and sarcopenia screening.
        Ref: Rolland et al. (2003). J Gerontol A Biol Sci Med Sci, 58(8), 741–745.
    """
    df = df.copy()

    # fat_mass_kg is needed; compute if not already present
    if "fat_mass_kg" not in df.columns:
        df = add_body_composition_indices(df)

    height_m = df["Height_cm"] / 100

    df["frame_size_index"]      = (df["Wrist_cm"] / df["Height_cm"]) * 100
    df["relative_muscle_mass"]  = (df["MuscleMass_kg"] / df["Weight_kg"]) * 100
    df["muscle_to_fat_ratio"]   = df["MuscleMass_kg"] / df["fat_mass_kg"]
    df["skeletal_muscle_index"] = df["MuscleMass_kg"] / height_m ** 2
    df["bicep_to_wrist_ratio"]  = df["Bicep_cm"] / df["Wrist_cm"]
    df["calf_muscle_index"]     = (df["Calf_cm"] / df["Height_cm"]) * 100

    return df


# =============================================================================
# 5. CONVENIENCE WRAPPER
# =============================================================================

def engineer_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies all four feature groups in the correct dependency order and
    returns a single DataFrame with every derived feature appended.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset containing the original columns.

    Returns
    -------
    pd.DataFrame
        Original columns + all engineered features.

    Example
    -------
    >>> import pandas as pd
    >>> df_raw = pd.read_csv("dataset.csv")
    >>> df_features = engineer_all_features(df_raw)
    >>> print(df_features.shape)
    """
    df = add_body_composition_indices(df)   # must run first (creates fat_mass_kg)
    df = add_obesity_ratios(df)
    df = add_limb_proportions(df)
    df = add_muscle_and_frame_features(df)  # depends on fat_mass_kg
    return df
