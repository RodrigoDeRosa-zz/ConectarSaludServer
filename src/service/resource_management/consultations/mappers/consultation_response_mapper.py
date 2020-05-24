from src.model.affiliates.affiliate import Affiliate
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

    @staticmethod
    def map_for_doctor(consultation_id: str, affiliate: Affiliate) -> dict:
        return {
            'consultation_id': consultation_id,
            'affiliate_first_name': affiliate.first_name,
            'affiliate_last_name': affiliate.last_name,
            'affiliate_plan': affiliate.plan,
            'affiliate_id': affiliate.id
        }
