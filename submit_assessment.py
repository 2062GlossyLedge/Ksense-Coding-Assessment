"""
Assessment Submission Module

Handles submission of patient classification results to the KSense API.
"""

import os
import json
import requests
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()


def submit_to_ksense(
    high_risk_patients: List[str],
    fever_patients: List[str],
    data_quality_issues: List[str],
) -> Dict[str, Any]:
    """
    Submit patient classification results to the KSense API.

    Args:
        high_risk_patients: List of patient IDs with total risk score ≥ 4
        fever_patients: List of patient IDs with temperature ≥ 99.6°F
        data_quality_issues: List of patient IDs with invalid/missing data

    Returns:
        Dictionary containing the API response with score, status, breakdown, etc.

    Raises:
        requests.RequestException: If the request fails
    """
    api_key = os.getenv("KSENSE_API_KEY")
    url = "https://assessment.ksensetech.com/api/submit-assessment"

    headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    # Build request body
    payload = {
        "high_risk_patients": high_risk_patients,
        "fever_patients": fever_patients,
        "data_quality_issues": data_quality_issues,
    }

    print("\n" + "=" * 80)
    print("SUBMITTING ASSESSMENT RESULTS")
    print("=" * 80)
    print(f"High-risk patients: {len(high_risk_patients)}")
    print(f"Fever patients: {len(fever_patients)}")
    print(f"Data quality issues: {len(data_quality_issues)}")
    print("=" * 80 + "\n")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"HTTP {response.status_code}",
                "status_code": response.status_code,
                "message": response.text,
            }

    except requests.Timeout:
        return {
            "error": "Request timeout",
            "message": "Request timed out",
        }

    except requests.RequestException as e:
        return {"error": "Request failed", "message": str(e)}


def print_submission_results(result: Dict[str, Any]) -> None:
    """
    Print prettified JSON submission results from the KSense API.

    Args:
        result: API response dictionary
    """
    print("\n" + "=" * 80)
    print("ASSESSMENT SUBMISSION RESULTS")
    print("=" * 80)
    print(json.dumps(result, indent=2))
    print("=" * 80)
