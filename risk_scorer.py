"""
Risk Scoring Module for Patient Assessment

Calculates risk scores based on:
- Blood Pressure (1-4 points)
- Temperature (0-2 points)
- Age (1-2 points)

Total Risk Score = BP Score + Temp Score + Age Score
"""

from typing import Optional
from patient import Patient


def calculate_bp_risk(bp: Optional[str]) -> int:
    """
    Calculate blood pressure risk score.

    Risk Levels:
    - Normal (Systolic <120 AND Diastolic <80): 0 points
    - Elevated (Systolic 120-129 AND Diastolic <80): 1 point
    - Stage 1 (Systolic 130-139 OR Diastolic 80-89): 2 points
    - Stage 2 (Systolic ≥140 OR Diastolic ≥90): 3 points
    - Invalid/Missing Data: 0 points

    Note: If systolic and diastolic fall into different risk categories,
    use the higher risk stage for scoring.

    Args:
        bp: Blood pressure string in format "systolic/diastolic" (e.g., "120/80")

    Returns:
        Risk score from 0-3
    """
    if not bp or not isinstance(bp, str):
        return 0

    # Parse BP value
    parts = bp.split("/")
    if len(parts) != 2:
        return 0

    try:
        systolic = int(parts[0].strip())
        diastolic = int(parts[1].strip())
    except (ValueError, AttributeError):
        return 0

    # Calculate risk for systolic
    systolic_risk = 0
    if systolic < 120:
        systolic_risk = 0
    elif 120 <= systolic <= 129:
        systolic_risk = 1
    elif 130 <= systolic <= 139:
        systolic_risk = 2
    else:  # systolic >= 140
        systolic_risk = 3

    # Calculate risk for diastolic
    diastolic_risk = 0
    if diastolic < 80:
        diastolic_risk = 0
    elif 80 <= diastolic <= 89:
        diastolic_risk = 2
    else:  # diastolic >= 90
        diastolic_risk = 3

    # Return the higher risk (as per requirements)
    return max(systolic_risk, diastolic_risk)


def calculate_temp_risk(temperature: Optional[float]) -> int:
    """
    Calculate temperature risk score.

    Risk Levels:
    - Normal (≤99.5°F): 0 points
    - Low Fever (99.6-100.9°F): 1 point
    - High Fever (≥101.0°F): 2 points
    - Invalid/Missing Data: 0 points

    Args:
        temperature: Temperature in Fahrenheit

    Returns:
        Risk score from 0-2
    """
    if temperature is None or not isinstance(temperature, (int, float)):
        return 0

    if temperature <= 99.5:
        return 0
    elif 99.6 <= temperature <= 100.9:
        return 1
    else:  # temperature >= 101.0
        return 2


def calculate_age_risk(age: Optional[int]) -> int:
    """
    Calculate age risk score.

    Risk Levels:
    - Under 40 (<40 years): 0 points
    - 40-65 (40-65 years, inclusive): 1 point
    - Over 65 (>65 years): 2 points
    - Invalid/Missing Data: 0 points

    Args:
        age: Age in years

    Returns:
        Risk score from 0-2
    """
    if age is None or not isinstance(age, (int, float)):
        return 0

    if age < 40:
        return 0
    elif 40 <= age <= 65:
        return 1
    else:  # age > 65
        return 2


def calculate_total_risk(patient: Patient) -> int:
    """
    Calculate total risk score for a patient.

    Total Risk = BP Risk + Temperature Risk + Age Risk

    Args:
        patient: Patient object with blood_pressure, temperature, and age attributes

    Returns:
        Total risk score (sum of all component scores)
    """
    bp_score = calculate_bp_risk(patient.blood_pressure)
    temp_score = calculate_temp_risk(patient.temperature)
    age_score = calculate_age_risk(patient.age)

    return bp_score + temp_score + age_score


def get_risk_breakdown(patient: Patient) -> dict:
    """
    Get detailed risk breakdown for a patient.

    Args:
        patient: Patient object

    Returns:
        Dictionary with individual and total scores
    """
    bp_score = calculate_bp_risk(patient.blood_pressure)
    temp_score = calculate_temp_risk(patient.temperature)
    age_score = calculate_age_risk(patient.age)
    total_score = bp_score + temp_score + age_score

    return {
        "patient_id": patient.patient_id,
        "bp_score": bp_score,
        "temp_score": temp_score,
        "age_score": age_score,
        "total_score": total_score,
    }
