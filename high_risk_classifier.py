"""
High-Risk Patient Classifier

Identifies patients with total risk score ≥ 4 based on blood pressure,
temperature, and age risk factors.
"""

from typing import List
from patient import Patient
from risk_scorer import calculate_total_risk


def get_high_risk_patients(patients: List[Patient]) -> List[str]:
    """
    Identify high-risk patients based on total risk score.

    A patient is considered high-risk if their total risk score is ≥ 4.
    Total risk score is the sum of:
    - Blood Pressure Risk (1-3 points)
    - Temperature Risk (0-2 points)
    - Age Risk (0-2 points)

    Args:
        patients: List of Patient objects to evaluate

    Returns:
        List of patient IDs with risk score ≥ 4
    """
    high_risk_ids = []

    for patient in patients:
        total_risk = calculate_total_risk(patient)
        if total_risk >= 4:
            high_risk_ids.append(patient.patient_id)

    return high_risk_ids
