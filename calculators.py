import math

def calculate_bmi(age_years: int, gender: bool, weight_kg: float, height_cm: float) -> dict:
    bmi_value = weight_kg / ((height_cm/100) ** 2)

    if bmi_value < 18.5:
        bmi_category = "Underweight"
    elif bmi_value > 18.5 and bmi_value < 24.9:
        bmi_category = "Normal"
    elif bmi_value > 25.0 and bmi_value < 29.9:
        bmi_category = "Overweight"
    elif bmi_value >= 30:
        bmi_category = "Obese"

    return {
        "bmi_value": round(bmi_value, 2),
        "bmi_category": bmi_category
    }

def calculate_body_fat(age_years: int, gender: bool, weight_kg: float, height_cm: float, neck_cm: float, waist_cm: float, hip_cm: float) -> dict:
    if gender is True:
        # Male: log10(waist - neck)
        body_fat_percentage = 495 / (1.0324 - 0.19077 * math.log10(waist_cm - neck_cm) + 0.15456 * math.log10(height_cm)) - 450
    else:
        # Female: log10(waist + hip - neck)
        body_fat_percentage = 495 / (1.29579 - 0.35004 * math.log10(waist_cm + hip_cm - neck_cm) + 0.22100 * math.log10(height_cm)) - 450

    return {
        "body_fat_percentage": round(body_fat_percentage, 2)
    }

def calculate_calories(age_years: int, gender: bool, weight_kg: float, height_cm: float, activity_factor: str) -> dict:
    # Compute BMR first (Mifflin-St Jeor)
    if gender is True:  # Male
        bmr_value = 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
    else:  # Female
        bmr_value = 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161

    # Map activity_factor string to multiplier
    activity_map = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9,
    }

    factor = activity_map.get(activity_factor)
    if factor is None:
        # Fallback or raise error for unknown activity_factor
        # Default to sedentary to avoid UnboundLocalError
        factor = 1.2

    daily_calories = int(round(bmr_value * factor))

    return {"daily_calories": daily_calories}

def calculate_bmr(age_years: int, gender: bool, weight_kg: float, height_cm: float) -> dict:
    if gender is True:
        bmr_value = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) + 5
    else:
        bmr_value = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) - 161
    
    return {
        "bmr_value": int(bmr_value)
    }

def calculate_ideal_weight(age_years: int, gender: bool, height_cm: float) -> dict:
    extra_height_in = (height_cm - 152.4) / 2.54
    if gender:
        base_weight = 48 + 2.7 * extra_height_in
    else:
        base_weight = 45.5 + 2.2 * extra_height_in
    min_weight_kg = base_weight * 0.90  # -10%
    max_weight_kg = base_weight * 1.10  # +10%    

    return {
        "min_weight_kg": round(min_weight_kg, 2),
        "max_weight_kg": round(max_weight_kg, 2)
    }
