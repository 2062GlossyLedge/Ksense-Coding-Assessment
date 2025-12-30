from typing import Any, Dict, Optional


class Patient:
    """Standardized patient data object"""

    def __init__(
        self,
        patient_id: str,
        age: Optional[int],
        blood_pressure: Optional[str],
        temperature: Optional[float],
    ):
        self.patient_id = patient_id
        self.age = age
        self.blood_pressure = blood_pressure
        self.temperature = temperature

    def to_dict(self) -> Dict[str, Any]:
        """Convert patient object to dictionary"""
        return {
            "patient_id": self.patient_id,
            "age": self.age,
            "blood_pressure": self.blood_pressure,
            "temperature": self.temperature,
        }
