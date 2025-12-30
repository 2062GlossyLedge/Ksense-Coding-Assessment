from typing import List, Dict, Any
from patient import Patient


def get_data_quality_issues(patients: List[Patient]) -> List[str]:
    """
    Returns a list of patient IDs with invalid/missing data.

    A patient has data quality issues if any of the following are missing or invalid:
    - Blood Pressure (BP)
    - Age
    - Temperature (Temp)

    Args:
        patients: List of Patient objects to validate

    Returns:
        List of patient IDs with data quality issues
    """
    patient_ids_with_issues = []

    for patient in patients:
        has_issue = False

        # Check for missing or invalid blood pressure
        if not _is_valid_bp(patient.blood_pressure):
            has_issue = True

        # Check for missing or invalid age
        if not _is_valid_age(patient.age):
            has_issue = True

        # Check for missing or invalid temperature
        if not _is_valid_temperature(patient.temperature):
            has_issue = True

        if has_issue:
            patient_ids_with_issues.append(patient.patient_id)

    return patient_ids_with_issues


def _is_valid_bp(bp) -> bool:
    """Check if blood pressure is valid."""
    if bp is None or not isinstance(bp, str):
        return False

    parts = bp.split("/")
    if len(parts) != 2:
        return False

    try:
        systolic = int(parts[0].strip())
        diastolic = int(parts[1].strip())
        # Validate reasonable BP ranges
        if systolic <= 0 or systolic > 300 or diastolic <= 0 or diastolic > 200:
            return False
        return True
    except (ValueError, AttributeError):
        return False


def _is_valid_age(age) -> bool:
    """Check if age is valid."""
    if age is None or not isinstance(age, (int, float)):
        return False

    # Validate reasonable age range
    if age < 0 or age > 150:
        return False

    return True


def _is_valid_temperature(temperature) -> bool:
    """Check if temperature is valid."""
    if temperature is None or not isinstance(temperature, (int, float)):
        return False

    # Validate reasonable temperature range
    if temperature <= 0 or temperature > 115:
        return False

    return True


def debug_data_quality_issues(patients: List[Patient]) -> List[Dict[str, Any]]:
    """
    Returns detailed information about invalid or malformed data with corresponding patient IDs.

    This debugging function shows exactly what data is missing or malformed for each patient.

    Args:
        patients: List of Patient objects to validate

    Returns:
        List of dictionaries containing patient ID and their specific data quality issues
    """
    issues_details = []

    for patient in patients:
        patient_issues = {
            "patient_id": patient.patient_id,
            "issues": [],
        }

        # Check blood pressure
        if not _is_valid_bp(patient.blood_pressure):
            patient_issues["issues"].append(
                {
                    "field": "blood_pressure",
                    "status": "missing/invalid",
                    "value": patient.blood_pressure,
                }
            )

        # Check age
        if not _is_valid_age(patient.age):
            patient_issues["issues"].append(
                {"field": "age", "status": "missing/invalid", "value": patient.age}
            )

        # Check temperature
        if not _is_valid_temperature(patient.temperature):
            patient_issues["issues"].append(
                {
                    "field": "temperature",
                    "status": "missing/invalid",
                    "value": patient.temperature,
                }
            )

        # Only add to results if there are issues
        if patient_issues["issues"]:
            issues_details.append(patient_issues)

    return issues_details


def print_data_quality_report(patients: List[Patient]) -> None:
    """
    Prints a formatted report of data quality issues.

    Args:
        patients: List of Patient objects to validate
    """
    print("=" * 80)
    print("DATA QUALITY REPORT")
    print("=" * 80)

    # Get summary
    patient_ids_with_issues = get_data_quality_issues(patients)
    print(f"\nTotal patients checked: {len(patients)}")
    print(f"Patients with data quality issues: {len(patient_ids_with_issues)}")

    if patient_ids_with_issues:
        print(f"\nPatient IDs with issues: {', '.join(patient_ids_with_issues)}")

    # Get detailed issues
    detailed_issues = debug_data_quality_issues(patients)

    if detailed_issues:
        print("\n" + "=" * 80)
        print("DETAILED ISSUES")
        print("=" * 80)

        for patient_issue in detailed_issues:
            print(f"\nPatient ID: {patient_issue['patient_id']}")
            print(f"Name: {patient_issue['name']}")
            print("Issues:")
            for issue in patient_issue["issues"]:
                print(
                    f"  - {issue['field']}: {issue['status']} (value: {issue['value']})"
                )
    else:
        print("\n✓ No data quality issues found!")

    print("\n" + "=" * 80)


# Example usage
if __name__ == "__main__":
    from routes import getPatients
    from patient import Patient

    print("Fetching patient data from API...\n")

    # Use the getPatients function from routes.py
    result = getPatients()

    # Convert dictionaries back to Patient objects
    all_patients = []
    for patient_dict in result.get("data", []):
        patient = Patient(
            patient_id=patient_dict["patient_id"],
            age=patient_dict["age"],
            blood_pressure=patient_dict["blood_pressure"],
            temperature=patient_dict["temperature"],
        )
        all_patients.append(patient)

    print(f"\nTotal patients fetched: {len(all_patients)}\n")

    # Run the data quality report
    print_data_quality_report(all_patients)
