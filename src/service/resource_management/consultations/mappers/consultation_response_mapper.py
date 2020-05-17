from src.model.consultations.consultation import Consultation
from src.model.doctors.doctor import Doctor


class ConsultationResponseMapper:

    @staticmethod
    def map_for_affiliate(consultation: Consultation, doctor: Doctor) -> dict:
        return {
            'doctor_first_name': doctor.first_name,
            'doctor_last_name': doctor.last_name,
            'prescription': consultation.prescription,
            'indications': consultation.indications
        }
