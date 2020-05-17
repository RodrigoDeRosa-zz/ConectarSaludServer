import uuid
from datetime import datetime
from typing import Tuple

from src.database.daos.affiliate_dao import AffiliateDAO
from src.database.daos.consultation_dao import ConsultationDAO
from src.database.daos.doctor_dao import DoctorDAO
from src.model.consultations.consultation import Consultation, ConsultationScore, ConsultationStatus
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
        consultation = Consultation(id=consultation_id, affiliate_dni=affiliate_dni, creation_date=datetime.now())
        await ConsultationDAO.store(consultation)
        # Return id for response
        return consultation_id

    @classmethod
    async def start_call(cls, doctor_id: str) -> str:
        """ Returns a call ID if there is any for the given doctor. """
        if not await DoctorDAO.find_by_id(doctor_id):
            raise BusinessError(f'There is no doctor with ID {doctor_id}.', 404)
        consultation = await ConsultationDAO.consultation_waiting_call(doctor_id)
        # There may be no affiliate to talk with at the moment
        if not consultation:
            raise BusinessError(f'There is no consultation waiting for the given doctor.', 404)
        # Create a call id for the consultation
        call_id = str(uuid.uuid4())
        # TODO -> Notify Android application with the call id
        # TODO
        # Update consultation with new call id and IN_PROGRESS status
        consultation.status = ConsultationStatus.IN_PROGRESS
        consultation.call_id = call_id
        await ConsultationDAO.store(consultation)
        # Return the id of the call
        return call_id

    @classmethod
    async def put_scoring_data(cls, affiliate_dni: str, consultation_id: str, score: ConsultationScore):
        """ Update a consultation with the affiliate's score. """
        # Get consultation to update
        consultation = await cls.__get_consultation_if_exists(affiliate_dni, consultation_id)
        # Update and store
        consultation.score = score.points
        consultation.score_opinion = score.opinion
        await ConsultationDAO.store(consultation)

    @classmethod
    async def get_consultation(cls, affiliate_dni: str, consultation_id: str) -> Tuple[Consultation, Doctor]:
        """ Get consultation and check if affiliate and consultation are related. """
        consultation = await cls.__get_consultation_if_exists(affiliate_dni, consultation_id)
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
    async def __get_consultation_if_exists(affiliate_dni: str, consultation_id: str) -> Consultation:
        if not await AffiliateDAO.find(affiliate_dni):
            raise BusinessError(f'There is no affiliate with DNI {affiliate_dni}.', 404)
        # Get consultation to update
        consultation = await ConsultationDAO.find(consultation_id)
        if not consultation:
            raise BusinessError(f'There is no consultation with ID {consultation_id}.', 404)
        return consultation
