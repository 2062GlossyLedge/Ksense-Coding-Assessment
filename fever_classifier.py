"""
Fever Patient Classifier

Identifies patients with elevated temperature (≥ 99.6°F).
"""

from typing import List
from patient import Patient


def get_fever_patients(patients: List[Patient]) -> List[str]:
    """
    Identify patients with fever (temperature ≥ 99.6°F).

    Args:
        patients: List of Patient objects to evaluate

    Returns:
        List of patient IDs with temperature ≥ 99.6°F
    """
    fever_ids = []

    for patient in patients:
        # Check if temperature is valid and >= 99.6
        if patient.temperature is not None and isinstance(
            patient.temperature, (int, float)
        ):
            if patient.temperature >= 99.6:
                fever_ids.append(patient.patient_id)

    return fever_ids
