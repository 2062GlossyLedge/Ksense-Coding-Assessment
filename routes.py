import requests
import os
import time
from dotenv import load_dotenv
from datetime import datetime
from sanitizer import sanitize_patient

load_dotenv()


# def getPatient():
#     KSense_api_key = os.getenv("KSENSE_API_KEY")
#     url = "https://assessment.ksensetech.com/api/patients?page=1&limit=1"

#     headers = {"x-api-key": KSense_api_key, "Content-Type": "application/json"}
#     max_retries = 3
#     backoff_factor = 1
#     response = None

#     for attempt in range(max_retries):
#         try:
#             response = requests.get(url, headers=headers, timeout=5)
#             if response.status_code == 200:
#                 break
#             elif response.status_code >= 500 and attempt < max_retries - 1:
#                 wait_time = backoff_factor * (2**attempt)
#                 time.sleep(wait_time)
#             else:
#                 break
#         except requests.RequestException as e:
#             if attempt < max_retries - 1:
#                 wait_time = backoff_factor * (2**attempt)
#                 time.sleep(wait_time)
#             else:
#                 raise

#     if response and response.status_code == 200:
#         data = response.json()

#         # Sanitize the patient data
#         sanitized_patients = []
#         if "data" in data and len(data["data"]) > 0:
#             for raw_patient in data["data"]:
#                 sanitized_patient = sanitize_patient(raw_patient)
#                 sanitized_patients.append(sanitized_patient.to_dict())

#         # Return in the ideal response format
#         return {
#             "data": sanitized_patients,
#             "pagination": data.get("pagination", {}),
#             "metadata": {
#                 "timestamp": datetime.now().isoformat() + "Z",
#                 "version": "v1.0",
#                 "requestId": f"req_{int(time.time())}",
#             },
#         }
#     else:
#         return {
#             "error": f"Failed with status code {response.status_code} and message: {response.text}"
#         }


def getPatients():
    KSense_api_key = os.getenv("KSENSE_API_KEY")
    base_url = "https://assessment.ksensetech.com/api/patients"

    headers = {"x-api-key": KSense_api_key, "Content-Type": "application/json"}
    max_retries = 10
    backoff_factor = 1
    all_patients = []
    last_pagination = {}  # Store the last pagination response

    page = 1
    has_next = True

    # Loop through pages dynamically using pagination metadata
    while has_next:
        url = f"{base_url}?page={page}"

        # Retry logic with exponential backoff
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    print("***rawdata:", data)

                    # Extract and sanitize patients from 'data' field
                    if "data" in data:
                        raw_patients = data["data"]
                        # Sanitize each patient to match the standardized format
                        for raw_patient in raw_patients:
                            sanitized_patient = sanitize_patient(raw_patient)
                            all_patients.append(sanitized_patient.to_dict())

                    # Check pagination metadata to see if there are more pages
                    if "pagination" in data:
                        last_pagination = data["pagination"]  # Store it
                        has_next = data["pagination"].get("hasNext", False)
                        print(
                            f"Fetched page {page}/{data['pagination'].get('totalPages', '?')}"
                        )
                    else:
                        has_next = False

                    break
                elif response.status_code == 429:
                    # Rate limit error - wait longer before retrying
                    wait_time = 2 * (2**attempt)
                    print(f"Rate limit hit on page {page}, waiting {wait_time}s...")
                    time.sleep(wait_time)
                elif response.status_code >= 500 and attempt < max_retries - 1:
                    # Server error - retry with exponential backoff
                    wait_time = backoff_factor * (2**attempt)
                    print(f"Server error on page {page}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    # Client error or final retry - don't retry
                    print(f"Failed to fetch page {page}: Status {response.status_code}")
                    has_next = False
                    break

            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = backoff_factor * (2**attempt)
                    print(f"Request error on page {page}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(
                        f"Error fetching page {page} after {max_retries} attempts: {str(e)}"
                    )
                    has_next = False
                    break

        # Add delay between page requests to avoid rate limiting
        if has_next:
            time.sleep(1)  # Wait 1 second between each page request

        page += 1

    print("$$$sanitized total patients:", all_patients)
    # Return in the ideal response format
    return {
        "data": all_patients,
        "pagination": {
            "page": 1,  # Since we're returning all pages combined
            "limit": len(all_patients),  # All patients
            "total": len(all_patients),
            "totalPages": 1,  # All data in one response
            "hasNext": False,
            "hasPrevious": False,
        },
        "metadata": {
            "timestamp": datetime.now().isoformat() + "Z",
            "version": "v1.0",
            "requestId": f"req_{int(time.time())}",
            "sourcePages": last_pagination.get("totalPages", page - 1),  # Track source
        },
    }


if __name__ == "__main__":
    # patient_data = getPatient()
    # print(patient_data)

    patients_data = getPatients()
    print("!!!Sanitized data with ideal format:", patients_data)
