"""
Patient Risk Assessment - Main Orchestrator

Fetches all patient data, classifies patients into risk categories,
and submits results to the KSense API for assessment.
"""

from routes import getPatients
from patient import Patient
from high_risk_classifier import get_high_risk_patients
from fever_classifier import get_fever_patients
from data_quality_classifier import get_data_quality_issues
from submit_assessment import submit_to_ksense, print_submission_results


def main():
    """
    Main orchestrator function that:
    1. Fetches all patient data from the API
    2. Converts to Patient objects
    3. Runs all classifiers to identify:
       - High-risk patients (total risk score ≥ 4)
       - Fever patients (temperature ≥ 99.6°F)
       - Data quality issues (missing/invalid BP, age, or temperature)
    4. Submits results to KSense API
    5. Displays formatted results
    """

    print("\n" + "=" * 80)
    print("PATIENT RISK ASSESSMENT SYSTEM")
    print("=" * 80)
    print("\n📥 Fetching patient data from API...\n")

    # Step 1: Fetch all patient data
    result = getPatients()
    print(result)

    if "error" in result:
        print(f"\n❌ Error fetching patient data: {result['error']}")
        return

    # Step 2: Convert dictionaries to Patient objects
    all_patients = []
    for patient_dict in result.get("data", []):
        patient = Patient(
            patient_id=patient_dict["patient_id"],
            age=patient_dict["age"],
            blood_pressure=patient_dict["blood_pressure"],
            temperature=patient_dict["temperature"],
        )
        all_patients.append(patient)

    print(f"✅ Successfully fetched {len(all_patients)} patients\n")

    # Step 3: Run classifiers
    print("=" * 80)
    print("RUNNING PATIENT CLASSIFICATION")
    print("=" * 80)

    print("\n🔍 Identifying high-risk patients (total risk score ≥ 4)...")
    high_risk_ids = get_high_risk_patients(all_patients)
    print(f"   Found {len(high_risk_ids)} high-risk patients")

    print("\n🌡️  Identifying fever patients (temperature ≥ 99.6°F)...")
    fever_ids = get_fever_patients(all_patients)
    print(f"   Found {len(fever_ids)} fever patients")

    print("\n⚠️  Identifying data quality issues (missing/invalid BP, age, or temp)...")
    data_quality_ids = get_data_quality_issues(all_patients)
    print(f"   Found {len(data_quality_ids)} patients with data quality issues")

    print("\n" + "=" * 80)
    print("CLASSIFICATION SUMMARY")
    print("=" * 80)
    print(f"Total Patients: {len(all_patients)}")
    print(f"High-Risk Patients: {len(high_risk_ids)}")
    print(f"Fever Patients: {len(fever_ids)}")
    print(f"Data Quality Issues: {len(data_quality_ids)}")

    if high_risk_ids:
        print(
            f"\nHigh-Risk IDs: {', '.join(high_risk_ids[:10])}"
            + (
                f" ... ({len(high_risk_ids) - 10} more)"
                if len(high_risk_ids) > 10
                else ""
            )
        )
    if fever_ids:
        print(
            f"Fever IDs: {', '.join(fever_ids[:10])}"
            + (f" ... ({len(fever_ids) - 10} more)" if len(fever_ids) > 10 else "")
        )
    if data_quality_ids:
        print(
            f"Data Quality IDs: {', '.join(data_quality_ids[:10])}"
            + (
                f" ... ({len(data_quality_ids) - 10} more)"
                if len(data_quality_ids) > 10
                else ""
            )
        )

    # Step 4: Submit to KSense API
    result = submit_to_ksense(
        high_risk_patients=high_risk_ids,
        fever_patients=fever_ids,
        data_quality_issues=data_quality_ids,
    )

    # Step 5: Display results
    print_submission_results(result)


if __name__ == "__main__":
    main()
