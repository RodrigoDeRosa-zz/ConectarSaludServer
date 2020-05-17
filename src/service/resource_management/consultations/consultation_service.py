import uuid
from typing import Tuple

from src.database.daos.affiliate_dao import AffiliateDAO
from src.database.daos.consultation_dao import ConsultationDAO
from src.database.daos.doctor_dao import DoctorDAO
from src.model.consultations.consultation import Consultation, ConsultationScore
from src.model.doctors.doctor import Doctor
from src.model.errors.business_error import BusinessError


class ConsultationService:

    @classmethod
    async def create_for_affiliate(cls, affiliate_dni: str) -> str:
        """ Creates a new consultation for the given affiliate and returns it's id. """
        if not await AffiliateDAO.find(affiliate_dni):
            raise BusinessError(f'There is no affiliate with DNI {affiliate_dni}.', 404)
        # Create new consultation and store
        consultation_id = str(uuid.uuid4())
        await ConsultationDAO.store(Consultation(id=consultation_id, affiliate_dni=affiliate_dni))
        # Return id for response
        return consultation_id

    @classmethod
    async def put_scoring_data(cls, affiliate_dni: str, consultation_id: str, score: ConsultationScore):
        """ Update a consultation with the affiliate's score. """
        # Get consultation to update
        consultation = await cls.check_existence(affiliate_dni, consultation_id)
        # Update and store
        consultation.score = score.points
        consultation.score_opinion = score.opinion
        await ConsultationDAO.store(consultation)

    @classmethod
    async def get_consultation(cls, affiliate_dni: str, consultation_id: str) -> Tuple[Consultation, Doctor]:
        """ Get consultation and check if affiliate and consultation are related. """
        consultation = await cls.check_existence(affiliate_dni, consultation_id)
        # Check that the consultation belongs to the affiliate
        if not consultation.affiliate_dni == affiliate_dni:
            raise BusinessError(f'Failed to match affiliate DNI to consultation ID.', 400)
        # Get consultation doctor
        # TODO -> Change this when the full flow is implemented
        doctor = await DoctorDAO.find_by_id('TODO')
        # TODO -> remove this when full flow is implemented
        doctor = Doctor(first_name='Fernando', last_name='Acero')
        # Return both objects for mapping
        return consultation, doctor

    @staticmethod
    async def check_existence(affiliate_dni: str, consultation_id: str) -> Consultation:
        if not await AffiliateDAO.find(affiliate_dni):
            raise BusinessError(f'There is no affiliate with DNI {affiliate_dni}.', 404)
        # Get consultation to update
        consultation = await ConsultationDAO.find(consultation_id)
        if not consultation:
            raise BusinessError(f'There is no consultation with ID {consultation_id}.', 404)
        return consultation
