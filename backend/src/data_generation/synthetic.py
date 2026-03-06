"""
synthetic.py
===========
Generate synthetic body measurements data grounded in real measured population data.

Distribution parameters are sourced from:
  - NHANES 2021-2023 (Fryar et al., 2025, Vital Health Stat Series 3 No. 50)
    CDC National Center for Health Statistics - the most recent nationally
    representative measured (not self-reported) U.S. adult anthropometric data.
  - NHANES 2015-2018 for measurements not in the 2021-2023 release
    (mid-arm circumference, upper arm length, hip circumference by age).

Key facts from NHANES 2021-2023 (measured adults 20+):
  Men:   height ~175.2 cm, weight ~90.3 kg, waist ~103.1 cm, hip ~107.5 cm
  Women: height ~161.3 cm, weight ~77.9 kg, waist  ~97.9 cm, hip ~109.8 cm

Age-specific means are used per decade (20-29, 30-39, 40-49, 50-59, 60-69, 70+)
since NHANES shows clear trends: weight and waist rise through midlife, height
dips slightly at older ages.

Standard deviations are derived from NHANES percentile spreads (p15-p85 ~ +/-1 SD).
Where NHANES only publishes SE (standard error of mean), SD is estimated from
the published percentile spread across the full distribution.

Dirty data characteristics retained:
  - Missing values (~4% per field)
  - Outliers: elite athletes, obesity Class III, measurement anomalies (~3.5%)
  - Unit entry errors: inches entered instead of cm, lbs instead of kg (~1.5%)
  - Digit transposition errors (~2%)
  - Lazy rounding to nearest 5 (~15%)
  - Right-skewed weight via lognormal noise
  - Inconsistent sex label encoding (M/Male/male/MALE)
  - Near-duplicate records (~2%)
"""

import random
import numpy as np
from typing import Dict, Optional


# ---------------------------------------------------------------------------
# AGE-STRATIFIED NHANES 2021-2023 DISTRIBUTIONS
# ---------------------------------------------------------------------------
# Format: {age_decade: (mean, std)}
# SD estimated from NHANES percentile tables (p15 ~ mean-1SD, p85 ~ mean+1SD).
# ---------------------------------------------------------------------------

# HEIGHT (cm) - NHANES Table 7 (2021-2023)
HEIGHT_BY_AGE = {
    'M': {
        '20s':    (176.4, 7.1),
        '30s':    (176.3, 7.0),
        '40s':    (175.8, 7.2),
        '50s':    (175.0, 7.3),
        '60s':    (173.6, 7.2),
        '70plus': (171.2, 7.5),
    },
    'F': {
        '20s':    (162.5, 6.5),
        '30s':    (162.0, 6.6),
        '40s':    (161.8, 6.6),
        '50s':    (161.0, 6.7),
        '60s':    (160.5, 6.8),
        '70plus': (157.0, 7.0),
    },
}

# WEIGHT (kg) - NHANES Table 3 (2021-2023)
# Weight rises through 40s-50s then drops slightly at older ages.
WEIGHT_BY_AGE = {
    'M': {
        '20s':    (85.0,  19.0),
        '30s':    (90.5,  20.0),
        '40s':    (93.5,  20.5),
        '50s':    (93.0,  20.0),
        '60s':    (91.0,  19.5),
        '70plus': (84.5,  17.5),
    },
    'F': {
        '20s':    (71.5,  19.5),
        '30s':    (77.5,  21.0),
        '40s':    (81.0,  22.0),
        '50s':    (82.5,  22.0),
        '60s':    (80.5,  20.5),
        '70plus': (73.0,  18.0),
    },
}

# WAIST (cm) - NHANES Table 12 (2021-2023)
# Men avg ~103.1 cm, Women avg ~97.9 cm (measured at iliac crest).
WAIST_BY_AGE = {
    'M': {
        '20s':    (96.5,  14.5),
        '30s':    (102.0, 14.5),
        '40s':    (105.5, 14.0),
        '50s':    (106.5, 13.5),
        '60s':    (106.0, 13.0),
        '70plus': (103.5, 13.0),
    },
    'F': {
        '20s':    (89.5,  16.0),
        '30s':    (96.0,  16.5),
        '40s':    (100.0, 16.0),
        '50s':    (102.5, 16.0),
        '60s':    (103.0, 15.5),
        '70plus': (101.0, 15.0),
    },
}

# HIP (cm) - NHANES Table 14 (2021-2023)
# Women avg ~109.8 cm, Men avg ~107.5 cm.
HIP_BY_AGE = {
    'M': {
        '20s':    (103.5, 10.0),
        '30s':    (107.0, 10.5),
        '40s':    (109.0, 10.5),
        '50s':    (109.5, 10.0),
        '60s':    (108.5, 10.0),
        '70plus': (106.0,  9.5),
    },
    'F': {
        '20s':    (107.0, 13.5),
        '30s':    (110.5, 13.5),
        '40s':    (112.5, 13.0),
        '50s':    (113.0, 13.0),
        '60s':    (111.5, 12.5),
        '70plus': (107.0, 12.0),
    },
}

# MID-UPPER ARM CIRCUMFERENCE (cm) - NHANES 2015-2018, Tables 22/16
ARM_CIRC_BY_AGE = {
    'M': {
        '20s':    (32.5, 4.0),
        '30s':    (34.0, 4.2),
        '40s':    (34.8, 4.3),
        '50s':    (34.5, 4.2),
        '60s':    (33.5, 4.0),
        '70plus': (31.5, 3.8),
    },
    'F': {
        '20s':    (31.0, 5.5),
        '30s':    (33.0, 5.8),
        '40s':    (34.5, 6.0),
        '50s':    (35.5, 6.0),
        '60s':    (35.0, 5.8),
        '70plus': (33.0, 5.5),
    },
}

# POOLED DISTRIBUTIONS (not age-stratified in NHANES)
# BMI correlation applied at generation time.
OTHER_DISTRIBUTIONS = {
    'Neck_cm':     {'M': (39.0, 2.8),   'F': (33.5, 2.3)},
    'Chest_cm':    {'M': (104.5, 11.5), 'F': (98.0, 12.0)},
    'Wrist_cm':    {'M': (18.0, 1.2),   'F': (15.8, 1.0)},
    'Forearm_cm':  {'M': (29.5, 2.5),   'F': (25.5, 2.2)},
    'Bicep_cm':    {'M': (36.5, 4.0),   'F': (31.5, 4.5)},
    'Thigh_cm':    {'M': (58.0, 6.5),   'F': (59.5, 7.5)},
    'Calf_cm':     {'M': (39.0, 3.5),   'F': (37.5, 3.5)},
    'Ankle_cm':    {'M': (23.5, 1.8),   'F': (21.5, 1.6)},
    'Shoulder_cm': {'M': (44.0, 3.5),   'F': (38.5, 3.0)},
    # Body fat: Gallagher et al. 2000 + NHANES DXA subsample
    # Real US population means are much higher than textbook values.
    'BodyFatPct':  {'M': (28.0, 7.5),   'F': (38.5, 7.0)},
}

# ---------------------------------------------------------------------------
# DIRTY DATA CONFIG
# ---------------------------------------------------------------------------

MISSING_PROB       = 0.04
DUPLICATE_PROB     = 0.02
UNIT_ERROR_PROB    = 0.015
TRANSCRIPTION_PROB = 0.02
LAZY_ROUND_PROB    = 0.15
OUTLIER_PROB       = 0.035

SEX_LABELS = {
    'M': ['M', 'Male', 'male', 'm', 'MALE'],
    'F': ['F', 'Female', 'female', 'f', 'FEMALE'],
}


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def age_to_decade(age: int) -> str:
    if age < 30:   return '20s'
    if age < 40:   return '30s'
    if age < 50:   return '40s'
    if age < 60:   return '50s'
    if age < 70:   return '60s'
    return '70plus'


def maybe_missing(value, prob: float = MISSING_PROB):
    return None if random.random() < prob else value


def maybe_transcription_error(value: Optional[float],
                               prob: float = TRANSCRIPTION_PROB) -> Optional[float]:
    if value is None or random.random() >= prob:
        return value
    s = str(int(abs(value)))
    err = random.choice(['transpose', 'repeat_digit', 'off_by_ten'])
    if err == 'transpose' and len(s) >= 2:
        i = random.randint(0, len(s) - 2)
        lst = list(s); lst[i], lst[i+1] = lst[i+1], lst[i]
        return float(''.join(lst))
    elif err == 'repeat_digit' and len(s) >= 2:
        i = random.randint(0, len(s) - 1)
        lst = list(s); lst.insert(i, lst[i])
        return float(''.join(lst[:len(s)+1]))
    elif err == 'off_by_ten':
        return value + random.choice([-10, 10])
    return value


def maybe_unit_error(value: Optional[float], field: str) -> Optional[float]:
    if value is None or random.random() >= UNIT_ERROR_PROB:
        return value
    if field.endswith('_cm'):
        return round(value / 2.54, 1)   # inch value entered where cm expected
    if field.endswith('_kg'):
        return round(value * 2.205, 1)  # lbs entered where kg expected
    return value


def maybe_lazy_round(value: Optional[float]) -> Optional[float]:
    if value is None or random.random() >= LAZY_ROUND_PROB:
        return value
    return float(round(value / 5) * 5)


def add_decimal_noise(value: Optional[float]) -> Optional[float]:
    if value is None:
        return value
    return round(value, 1) if random.random() < 0.35 else round(value)


def inject_outlier(value: float, field: str, sex: str) -> float:
    archetype = random.choice(['elite_athlete', 'severe_obesity', 'anomaly'])
    if archetype == 'elite_athlete':
        if field == 'BodyFatPct':
            return random.uniform(4, 10) if sex == 'M' else random.uniform(10, 16)
        if field in ('Bicep_cm', 'Thigh_cm', 'Chest_cm', 'UpperArm_cm'):
            return value * random.uniform(1.15, 1.4)
        if field == 'Weight_kg':
            return value * random.uniform(1.05, 1.2)
    elif archetype == 'severe_obesity':
        if field == 'BodyFatPct':
            return random.uniform(45, 58)
        if field in ('Waist_cm', 'Hip_cm', 'Chest_cm'):
            return value * random.uniform(1.25, 1.55)
        if field == 'Weight_kg':
            return value * random.uniform(1.5, 2.2)
    else:
        return value * random.uniform(0.78, 1.22)
    return value


def sample_with_outlier(mean: float, std: float, field: str, sex: str,
                        lo: float, hi: float) -> float:
    val = np.random.normal(mean, std)
    if random.random() < OUTLIER_PROB:
        val = inject_outlier(val, field, sex)
    return clamp(val, lo, hi)


def apply_dirty_pipeline(value: Optional[float], field: str,
                         missing_prob: float = MISSING_PROB) -> Optional[float]:
    value = add_decimal_noise(value)
    value = maybe_lazy_round(value)
    value = maybe_unit_error(value, field)
    value = maybe_transcription_error(value)
    value = maybe_missing(value, prob=missing_prob)
    return value


# ---------------------------------------------------------------------------
# CORE GENERATOR
# ---------------------------------------------------------------------------

_last_record: Optional[Dict] = None


def generate_measurement() -> Dict:
    """
    Generate a single body measurement record calibrated to NHANES 2021-2023.

    Uses age-stratified means for height, weight, waist, hip, arm circumference.
    BMI z-score drives correlated adjustments to waist, chest, body fat, etc.
    Right-skewed weight distribution via lognormal noise component.
    Full dirty-data pipeline applied to every field.

    Returns:
        Dict of all body measurements; None for missing fields.
    """
    global _last_record

    # Near-duplicate injection (~2% of records)
    if _last_record is not None and random.random() < DUPLICATE_PROB:
        dup = dict(_last_record)
        for field in random.sample([k for k, v in dup.items()
                                    if isinstance(v, (int, float))],
                                   k=min(3, len(dup))):
            dup[field] = round(dup[field] + random.uniform(-2, 2), 1)
        return dup

    # --- Demographics -------------------------------------------------------
    age = random.randint(18, 74)
    canonical_sex = random.choice(['M', 'F'])
    sex_label = random.choice(SEX_LABELS[canonical_sex])
    decade = age_to_decade(age)

    # --- Height (NHANES Table 7) --------------------------------------------
    h_mean, h_std = HEIGHT_BY_AGE[canonical_sex][decade]
    height_raw = sample_with_outlier(h_mean, h_std, 'Height_cm', canonical_sex,
                                     lo=145, hi=215)
    height = apply_dirty_pipeline(height_raw, 'Height_cm', missing_prob=0.01)

    # --- Weight (NHANES Table 3, right-skewed) ------------------------------
    w_mean, w_std = WEIGHT_BY_AGE[canonical_sex][decade]
    h_z = (height_raw - h_mean) / h_std
    w_mean_adj = w_mean + h_z * 7  # Taller = heavier correlation

    # Lognormal right-skew: real weight distributions have long right tails
    skew = np.random.lognormal(mean=0, sigma=0.18) - 1
    weight_raw = np.random.normal(w_mean_adj, w_std) + skew * 12
    if random.random() < OUTLIER_PROB:
        weight_raw = inject_outlier(weight_raw, 'Weight_kg', canonical_sex)
    weight_raw = clamp(weight_raw, 35, 250)
    weight = apply_dirty_pipeline(weight_raw, 'Weight_kg', missing_prob=0.02)

    # BMI for downstream correlations (use raw values)
    bmi = weight_raw / ((height_raw / 100) ** 2)
    bmi_z = (bmi - 27.5) / 6.5  # z-score relative to US population mean BMI

    # --- Waist (NHANES Table 12) --------------------------------------------
    wst_mean, wst_std = WAIST_BY_AGE[canonical_sex][decade]
    waist_raw = sample_with_outlier(wst_mean + bmi_z * 9, wst_std,
                                    'Waist_cm', canonical_sex, lo=55, hi=175)
    waist = apply_dirty_pipeline(waist_raw, 'Waist_cm')

    # --- Hip (NHANES Table 14) ----------------------------------------------
    hip_mean, hip_std = HIP_BY_AGE[canonical_sex][decade]
    hip_raw = sample_with_outlier(hip_mean + bmi_z * 7, hip_std,
                                  'Hip_cm', canonical_sex, lo=75, hi=175)
    hip = apply_dirty_pipeline(hip_raw, 'Hip_cm')

    # --- Mid-upper arm (NHANES 2015-2018) -----------------------------------
    arm_mean, arm_std = ARM_CIRC_BY_AGE[canonical_sex][decade]
    upper_arm_raw = sample_with_outlier(arm_mean + bmi_z * 3.5, arm_std,
                                        'UpperArm_cm', canonical_sex, lo=20, hi=58)
    upper_arm = apply_dirty_pipeline(upper_arm_raw, 'UpperArm_cm')

    # --- Remaining fields (pooled, BMI-correlated) --------------------------
    def gen(field: str, lo: float, hi: float, bmi_sens: float = 0.0) -> Optional[float]:
        m, s = OTHER_DISTRIBUTIONS[field][canonical_sex]
        val = sample_with_outlier(m + bmi_z * bmi_sens, s, field, canonical_sex, lo, hi)
        return apply_dirty_pipeline(val, field)

    neck     = gen('Neck_cm',     lo=27,  hi=58,  bmi_sens=1.8)
    chest    = gen('Chest_cm',    lo=68,  hi=175, bmi_sens=5.0)
    wrist    = gen('Wrist_cm',    lo=12,  hi=25,  bmi_sens=0.3)
    forearm  = gen('Forearm_cm',  lo=18,  hi=42,  bmi_sens=0.8)
    bicep    = gen('Bicep_cm',    lo=22,  hi=58,  bmi_sens=2.0)
    thigh    = gen('Thigh_cm',    lo=35,  hi=90,  bmi_sens=3.5)
    calf     = gen('Calf_cm',     lo=25,  hi=55,  bmi_sens=1.5)
    ankle    = gen('Ankle_cm',    lo=17,  hi=33,  bmi_sens=0.5)
    shoulder = gen('Shoulder_cm', lo=30,  hi=58,  bmi_sens=0.5)

    # --- Body fat % (Gallagher et al. 2000 + NHANES DXA) -------------------
    bf_mean, bf_std = OTHER_DISTRIBUTIONS['BodyFatPct'][canonical_sex]
    bf_raw = np.random.normal(bf_mean + bmi_z * 5.5, bf_std)
    if random.random() < OUTLIER_PROB:
        bf_raw = inject_outlier(bf_raw, 'BodyFatPct', canonical_sex)
    bf_raw = clamp(bf_raw, 4, 60)
    body_fat = apply_dirty_pipeline(bf_raw, 'BodyFatPct')

    # --- Muscle mass (derived; ~13% chance missing) -------------------------
    if random.random() < 0.13:
        muscle_mass = None
    else:
        muscle_pct = np.random.normal(0.42, 0.06)
        muscle_mass = round(weight_raw * clamp(muscle_pct, 0.26, 0.60), 1)
        muscle_mass = maybe_missing(muscle_mass, prob=0.04)

    record = {
        'Age':           age,
        'Sex':           sex_label,
        'Height_cm':     height,
        'Weight_kg':     weight,
        'Wrist_cm':      wrist,
        'Waist_cm':      waist,
        'Hip_cm':        hip,
        'Neck_cm':       neck,
        'UpperArm_cm':   upper_arm,
        'Thigh_cm':      thigh,
        'Calf_cm':       calf,
        'Forearm_cm':    forearm,
        'Chest_cm':      chest,
        'Shoulder_cm':   shoulder,
        'Ankle_cm':      ankle,
        'Bicep_cm':      bicep,
        'BodyFatPct':    body_fat,
        'MuscleMass_kg': muscle_mass,
    }

    _last_record = record
    return record


# ---------------------------------------------------------------------------
# DATA GENERATION ENTRY POINT
# ---------------------------------------------------------------------------

def generate_data(num_records: int, output_file: str) -> int:
    """
    Generate and save body measurement data.

    Args:
        num_records: Number of records to generate
        output_file: Path to the output CSV file

    Returns:
        Number of rows added to the file
    """
    from utils.csv_utils import append_to_csv, get_row_count
    from utils.file_utils import file_exists

    print(f"Generating {num_records} records (NHANES 2021-2023 calibrated)...")
    data = [generate_measurement() for _ in range(num_records)]

    rows_added = append_to_csv(output_file, data)
    total_rows = get_row_count(output_file)
    file_status = "Updated existing file" if file_exists(output_file) else "Created new file"

    print(f"\n[OK] {file_status}: {output_file}")
    print(f"[OK] Added {rows_added} new records")
    print(f"[OK] Total records in file: {total_rows}")

    return rows_added