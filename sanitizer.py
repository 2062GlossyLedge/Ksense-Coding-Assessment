from typing import Any, Dict, Optional
from datetime import datetime
from patient import Patient
import re


def validate_blood_pressure(bp_value: Any) -> Optional[str]:
    """
    Validate blood pressure format.
    Valid format: "xxx/yyy" where xxx and yyy are numeric.
    Returns None for invalid values.
    """
    if bp_value is None or bp_value == "":
        return None

    bp_str = str(bp_value).strip()

    # Check for non-numeric placeholders
    # what about other invalid strings?
    if bp_str.upper() in ["N/A", "NA", "INVALID", "UNKNOWN", "INVALID_BP_FORMAT"]:
        return None

    # Validate format: must be "xxx/yyy" with numbers
    bp_pattern = r"^(\d+)/(\d+)$"
    match = re.match(bp_pattern, bp_str)

    if not match:
        # Check for incomplete formats like "150/" or "/90"
        if "/" in bp_str:
            parts = bp_str.split("/")
            if len(parts) == 2:
                if not parts[0] or not parts[1]:  # Missing systolic or diastolic
                    return None
        return None

    return bp_str


def validate_age(age_value: Any) -> Optional[int]:
    """
    Validate age value.
    Returns None for null, undefined, empty, or non-numeric values.
    """
    if age_value is None or age_value == "":
        return None

    try:
        # handles numeric strings
        age = int(age_value)

        return age
    except (ValueError, TypeError):
        # Non-numeric string like "fifty-three" or "unknown"
        return None


def validate_temperature(temp_value: Any) -> Optional[float]:
    """
    Validate temperature value.
    Returns None for null, undefined, empty, or non-numeric values.
    """
    if temp_value is None or temp_value == "":
        return None

    # Check for non-numeric placeholders
    temp_str = str(temp_value).strip().upper()
    if temp_str in ["TEMP_ERROR", "INVALID", "UNKNOWN", "N/A", "NA"]:
        return None

    try:
        temp = float(temp_value)
        return temp
    except (ValueError, TypeError):
        return None


def sanitize_patient(patient_data: Dict[str, Any]) -> Patient:
    """
    Sanitize incoming patient data to match the standardized Patient format.
    Handles various field names and data types.
    Sets invalid data to None instead of default values.
    """
    # Handle patient_id variations
    patient_id = patient_data.get("patient_id")

    # Handle age with validation
    age_raw = patient_data.get("age")
    age = validate_age(age_raw)

    # Handle blood pressure with validation
    bp_raw = patient_data.get("blood_pressure")
    blood_pressure = validate_blood_pressure(bp_raw)

    # Handle temperature with validation
    temp_raw = patient_data.get("temperature")
    temperature = validate_temperature(temp_raw)

    return Patient(
        patient_id=str(patient_id),
        age=age,  # Now can be None
        blood_pressure=blood_pressure,  # Now can be None
        temperature=temperature,  # Now can be None
    )
