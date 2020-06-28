from typing import List

from src.database.daos.affiliate_dao import AffiliateDAO
from src.model.affiliates.affiliate import Affiliate
from src.model.consultations.consultation import Consultation
from src.model.doctors.doctor import Doctor


class ConsultationResponseMapper:

    @staticmethod
    async def map_consultation_list(consultations: List[Consultation], doctors: List[Doctor]) -> List[dict]:
        response = list()
        for consultation, doctor in zip(consultations, doctors):
            patient = await AffiliateDAO.find(consultation.patient_dni)
            response.append(
                {
                    'consultation_id': consultation.id,
                    'doctor_first_name': doctor.first_name,
                    'doctor_last_name': doctor.last_name,
                    'doctor_specialties': doctor.specialties,
                    'patient_first_name': patient.first_name,
                    'patient_last_name': patient.last_name,
                    'patient_dni': patient.dni,
                    'date': consultation.creation_date.strftime('%d-%m-%Y %H:%M:%S')
                }
            )
        return response

    @classmethod
    def map_consultation(cls, consultation: Consultation) -> dict:
        response = {'consultation_id': consultation.id}
        if consultation.call_id:
            response['call_id'] = consultation.call_id
        return response

    @classmethod
    def map_consultation_in_progress(cls, consultation: Consultation) -> dict:
        response = {
            'consultation_id': None,
            'call_id': None,
            'symptoms': list(),
            'reason': None
        }
        if not consultation: return response
        response['consultation_id'] = consultation.id
        response['call_id'] = consultation.call_id
        response['symptoms'] = consultation.symptoms
        response['reason'] = consultation.reason
        return response

    @staticmethod
    def map_for_affiliate(consultation: Consultation, doctor: Doctor, patient: Affiliate) -> dict:
        return {
            'date': consultation.creation_date.strftime('%d-%m-%Y %H:%M:%S'),
            'patient_first_name': patient.first_name,
            'patient_last_name': patient.last_name,
            'patient_dni': patient.dni,
            'doctor_first_name': doctor.first_name,
            'doctor_last_name': doctor.last_name,
            'doctor_specialties': doctor.specialties,
            'symptoms': consultation.symptoms,
            'has_prescription': consultation.prescription is not None,
            'indications': consultation.indications
        }

    @staticmethod
    def map_prescription(consultation: Consultation, doctor: Doctor, patient: Affiliate) -> dict:
        return {
            'date': consultation.creation_date.strftime('%d-%m-%Y %H:%M:%S'),
            'patient_first_name': patient.first_name,
            'patient_last_name': patient.last_name,
            'patient_plan': patient.plan,
            'patient_id': patient.id,
            'doctor_first_name': doctor.first_name,
            'doctor_last_name': doctor.last_name,
            'doctor_licence': doctor.licence,
            'doctor_specialties': doctor.specialties,
            'prescription_text': consultation.prescription
        }

    @staticmethod
    def map_for_doctor(consultation: Consultation, affiliate: Affiliate) -> dict:
        return {
            'consultation_id': consultation.id,
            'symptoms': consultation.symptoms,
            'reason': consultation.reason,
            'affiliate_first_name': affiliate.first_name,
            'affiliate_last_name': affiliate.last_name,
            'affiliate_plan': affiliate.plan,
            'affiliate_id': affiliate.id
        }
