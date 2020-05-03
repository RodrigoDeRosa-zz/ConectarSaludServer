from typing import List

from src.model.doctors.doctor import Doctor


class DoctorManagementResponseMapper:

    @classmethod
    def map_all_doctors(cls, doctors: List[Doctor]) -> list:
        return [cls.map_doctor(doctor) for doctor in doctors]

    @staticmethod
    def map_doctor(doctor: Doctor) -> dict:
        return {k: getattr(doctor, k) for k in doctor.fields()}
