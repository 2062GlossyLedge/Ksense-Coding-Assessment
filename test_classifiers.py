"""
Test Cases for Patient Classification System

Tests high-risk, fever, and data quality classifiers to ensure
they capture the correct number of patients (not too few, not too many).
"""

from patient import Patient
from high_risk_classifier import get_high_risk_patients
from fever_classifier import get_fever_patients
from data_quality_classifier import get_data_quality_issues
from risk_scorer import calculate_total_risk, get_risk_breakdown


def run_test(
    test_name, patients, expected_high_risk, expected_fever, expected_data_quality
):
    """
    Run a single test case and compare results with expected values.

    Args:
        test_name: Name of the test
        patients: List of Patient objects
        expected_high_risk: Expected number of high-risk patients
        expected_fever: Expected number of fever patients
        expected_data_quality: Expected number of patients with data quality issues
    """
    print(f"\n{'=' * 80}")
    print(f"TEST: {test_name}")
    print(f"{'=' * 80}")

    # Run classifiers
    high_risk_ids = get_high_risk_patients(patients)
    fever_ids = get_fever_patients(patients)
    data_quality_ids = get_data_quality_issues(patients)

    # Display results
    print(f"\nResults:")
    print(
        f"  High-Risk Patients: {len(high_risk_ids)} (expected: {expected_high_risk})"
    )
    print(f"  Fever Patients: {len(fever_ids)} (expected: {expected_fever})")
    print(
        f"  Data Quality Issues: {len(data_quality_ids)} (expected: {expected_data_quality})"
    )

    # Show detailed breakdown for high-risk patients
    if patients:
        print(f"\nDetailed Risk Scores:")
        for patient in patients:
            breakdown = get_risk_breakdown(patient)
            status = "HIGH-RISK ⚠️" if breakdown["total_score"] >= 4 else "Normal"
            fever_status = (
                "FEVER 🌡️" if patient.temperature and patient.temperature >= 99.6 else ""
            )
            data_status = (
                "DATA ISSUE ❌" if patient.patient_id in data_quality_ids else ""
            )
            print(
                f"  {patient.patient_id}: Total={breakdown['total_score']} "
                f"(BP={breakdown['bp_score']}, Temp={breakdown['temp_score']}, Age={breakdown['age_score']}) "
                f"{status} {fever_status} {data_status}"
            )

    # Validate results
    passed = True
    if len(high_risk_ids) != expected_high_risk:
        print(f"\n❌ FAILED: High-risk count mismatch!")
        passed = False
    if len(fever_ids) != expected_fever:
        print(f"\n❌ FAILED: Fever count mismatch!")
        passed = False
    if len(data_quality_ids) != expected_data_quality:
        print(f"\n❌ FAILED: Data quality count mismatch!")
        passed = False

    if passed:
        print(f"\n✅ PASSED: All counts match expected values!")

    return passed


def test_case_1_boundary_high_risk_score():
    """Test Case 1: Boundary test for high-risk score = 4"""
    patients = [
        # BP=0, Temp=0, Age=0: Score = 0
        Patient("TEST001", 35, "119/79", 98.6),
        # BP=0, Temp=0, Age=2: Score = 2
        Patient("TEST002", 70, "119/79", 98.6),
        # BP=1, Temp=0, Age=0: Score = 1
        Patient("TEST003", 35, "128/79", 98.6),
        # BP=2, Temp=1, Age=1: Score = 4
        Patient("TEST004", 50, "135/79", 99.6),
    ]
    return run_test(
        "Boundary Test: High-Risk Score = 4",
        patients,
        expected_high_risk=1,  # TEST004 only
        expected_fever=1,  # TEST004
        expected_data_quality=0,
    )


def test_case_2_fever_boundary():
    """Test Case 2: Boundary test for fever temperature = 99.6°F"""
    patients = [
        # BP=2, Temp=0, Age=1: Score = 3
        Patient("TEST005", 45, "120/80", 99.5),
        # BP=2, Temp=1, Age=1: Score = 4
        Patient("TEST006", 45, "120/80", 99.6),
        # BP=2, Temp=1, Age=1: Score = 4
        Patient("TEST007", 45, "120/80", 100.0),
        # BP=2, Temp=2, Age=1: Score = 5
        Patient("TEST008", 45, "120/80", 101.5),
    ]
    return run_test(
        "Boundary Test: Fever Temperature = 99.6°F",
        patients,
        expected_high_risk=3,  # TEST008
        expected_fever=3,  # TEST006, TEST007, TEST008
        expected_data_quality=0,
    )


def test_case_3_bp_risk_stages():
    """Test Case 3: Blood pressure risk stage transitions"""
    patients = [
        # BP=0 Temp=0 Age=1: Score = 1
        Patient("TEST009", 40, "115/75", 98.6),
        # BP=1 Temp=0 Age=1: Score = 2
        Patient("TEST010", 40, "125/75", 98.6),
        # BP=2 Temp=0 Age=1: Score = 3
        Patient("TEST011", 40, "135/75", 98.6),
        # BP=2 Temp=0 Age=1: Score = 3
        Patient("TEST012", 40, "115/85", 98.6),
        # BP=3 Temp=0 Age=1: Score = 4
        Patient("TEST013", 40, "145/75", 98.6),
        # BP=3 Temp=0 Age=1: Score = 4
        Patient("TEST014", 40, "115/95", 98.6),
    ]
    return run_test(
        "Blood Pressure Risk Stage Transitions",
        patients,
        expected_high_risk=2,  # TEST013, TEST014
        expected_fever=0,
        expected_data_quality=0,
    )


def test_case_4_missing_data():
    """Test Case 4: Missing/invalid data handling"""
    patients = [
        # Missing BP
        # BP=0, Temp=0, Age=1: Score = 1
        Patient("TEST015", 45, None, 98.6),
        # Missing temperature
        # BP=2, Temp=0, Age=1: Score = 3
        Patient("TEST016", 45, "120/80", None),
        # Missing age
        # BP=2, Temp=0, Age=0: Score = 2
        Patient("TEST017", None, "120/80", 98.6),
        # All valid
        # BP=2, Temp=0, Age=1: Score = 3
        Patient("TEST018", 45, "120/80", 98.6),
        # Missing age
        # BP=2, Temp=2, Age=0: Score = 4
        Patient("TEST019", None, "120/80", 101.0),
    ]
    return run_test(
        "Missing/Invalid Data Handling",
        patients,
        expected_high_risk=1,  # TEST019
        expected_fever=1,  # TEST019
        expected_data_quality=4,  # TEST015, TEST016, TEST017, TEST019
    )


def test_case_7_invalid_bp_formats():
    """Test Case 7: Invalid blood pressure formats"""
    patients = [
        # Invalid format - incomplete
        # BP=0, Temp=0, Age=1: Score = 1
        Patient("TEST028", 45, "120/", 98.6),
        # Invalid format - missing systolic
        # BP=0, Temp=0, Age=1: Score = 1
        Patient("TEST029", 45, "/80", 98.6),
        # Invalid format - non-numeric
        # BP=0, Temp=0, Age=1: Score = 1
        Patient("TEST030", 45, "INVALID", 98.6),
        # Valid format
        # BP=2, Temp=0, Age=1: Score = 3
        Patient("TEST031", 45, "120/80", 98.6),
    ]
    return run_test(
        "Invalid Blood Pressure Formats",
        patients,
        expected_high_risk=0,
        expected_fever=0,
        expected_data_quality=3,  # TEST028, TEST029, TEST030
    )


def test_case_9_mixed_data_quality():
    """Test Case 9: Mix of valid and invalid data across all fields"""
    patients = [
        # All valid, high-risk
        # BP=3, Temp=2, Age=2: Score = 7
        Patient("TEST035", 70, "145/95", 101.0),
        # Valid but low risk
        # BP=0, Temp=0, Age=0: Score = 0
        Patient("TEST036", 35, "115/75", 98.0),
        # Missing all critical fields
        # BP=0, Temp=0, Age=0: Score = 0
        Patient("TEST037", None, None, None),
        # Partial data - missing BP only High Risk
        # BP=0, Temp=2, Age=2: Score = 4
        Patient("TEST038", 70, None, 101.0),
    ]
    return run_test(
        "Mixed Data Quality",
        patients,
        expected_high_risk=2,
        expected_fever=2,
        expected_data_quality=2,
    )


def test_case_10_edge_case_extreme_values():
    """Test Case 10: Edge cases with extreme but valid values"""
    patients = [
        # Very high BP (within valid range)
        # BP=3, Temp=0, Age=1: Score = 4
        Patient("TEST039", 40, "200/120", 98.6),
        # Very old patient
        # BP=2, Temp=0, Age=2: Score = 4
        Patient("TEST040", 100, "120/80", 98.6),
        # Very young patient with high fever
        # BP=0, Temp=2, Age=0: Score = 2
        Patient("TEST041", 18, "115/75", 103.5),
        # All maximum risk factors
        # BP=3, Temp=2, Age=2: Score = 7
        Patient("TEST042", 80, "180/100", 102.0),
    ]
    return run_test(
        "Edge Cases: Extreme Values",
        patients,
        expected_high_risk=3,
        expected_fever=2,
        expected_data_quality=0,
    )


def main():
    """Run all test cases"""
    print("\n" + "=" * 80)
    print("PATIENT CLASSIFICATION SYSTEM - TEST SUITE")
    print("=" * 80)
    print("\nRunning 10 test cases to validate classifier accuracy...")

    test_results = []

    # Run all test cases
    test_results.append(test_case_1_boundary_high_risk_score())
    test_results.append(test_case_2_fever_boundary())
    test_results.append(test_case_3_bp_risk_stages())
    test_results.append(test_case_4_missing_data())

    test_results.append(test_case_7_invalid_bp_formats())

    test_results.append(test_case_9_mixed_data_quality())
    test_results.append(test_case_10_edge_case_extreme_values())

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUITE SUMMARY")
    print("=" * 80)
    passed = sum(test_results)
    total = len(test_results)
    print(f"\nTests Passed: {passed}/{total}")
    print(f"Tests Failed: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Classifiers are working correctly.")
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED! Review the output above.")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
