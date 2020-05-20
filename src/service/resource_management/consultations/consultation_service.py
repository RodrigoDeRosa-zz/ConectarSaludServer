import uuid
from datetime import datetime
from typing import Tuple

from src.database.daos.affiliate_dao import AffiliateDAO
from src.database.daos.consultation_dao import ConsultationDAO
from src.database.daos.doctor_dao import DoctorDAO
from src.handlers.socket.socket_manager import SocketManager
from src.model.consultations.consultation import Consultation, ConsultationScore, ConsultationStatus, \
    ConsultationOpinion
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
    async def link_socket_to_consultation(cls, consultation_id: str, socket_id: str):
        """ Stores a relationship between a socket and a consultation. """
        consultation = await ConsultationDAO.find(consultation_id)
        # Set socket ID and update
        consultation.socket_id = socket_id
        await ConsultationDAO.store(consultation)
        # TODO -> Add to queue at this point in the future

    @classmethod
    async def next_consultation(cls, doctor_id):
        """ Returns a consultation that is waiting for a doctor. """
        # TODO -> This should be automatic and triggered by the queue in the future
        if not await DoctorDAO.find_by_id(doctor_id):
            raise BusinessError(f'There are no doctors with ID {doctor_id}.', 404)
        consultation = await ConsultationDAO.next_consultation_waiting_doctor()
        if not consultation:
            raise BusinessError('There are no consultations waiting for a doctor.', 404)
        # Update information
        consultation.doctor_id = doctor_id
        consultation.status = ConsultationStatus.WAITING_CALL
        await ConsultationDAO.store(consultation)
        # Return id
        return consultation.id

    @classmethod
    async def start_call(cls, doctor_id: str) -> str:
        """ Returns a call ID if there is any for the given doctor. """
        if not await DoctorDAO.find_by_id(doctor_id):
            raise BusinessError(f'There is no doctor with ID {doctor_id}.', 404)
        consultation = await ConsultationDAO.next_consultation_waiting_call(doctor_id)
        # There may be no affiliate to talk with at the moment
        if not consultation:
            raise BusinessError(f'There is no consultation waiting for the given doctor.', 404)
        # Create a call id for the consultation
        call_id = str(uuid.uuid4())
        # Notify start of call to affiliate via socket
        socket_id = consultation.socket_id
        await SocketManager.notify_call_start(call_id, socket_id)
        # Update consultation with new call id and IN_PROGRESS status
        consultation.status = ConsultationStatus.IN_PROGRESS
        consultation.call_id = call_id
        await ConsultationDAO.store(consultation)
        # Return the id of the call
        return call_id

    @classmethod
    async def affiliate_consultation(cls, affiliate_dni: str, consultation_id: str) -> Tuple[Consultation, Doctor]:
        """ Get consultation and check if affiliate and consultation are related. """
        consultation = await cls.__get_affiliate_consultation(affiliate_dni, consultation_id)
        # Check that the consultation belongs to the affiliate
        if not consultation.affiliate_dni == affiliate_dni:
            raise BusinessError(f'Failed to match affiliate DNI to consultation ID.', 400)
        # TODO -> remove this if when full flow is implemented
        # Get consultation doctor
        if consultation.doctor_id:
            doctor = await DoctorDAO.find_by_id(consultation.doctor_id)
        else:
            doctor = Doctor(first_name='Fernando', last_name='Acero')
        # Return both objects for mapping
        return consultation, doctor

    @classmethod
    async def put_scoring_data(cls, affiliate_dni: str, consultation_id: str, score: ConsultationScore):
        """ Update a consultation with the affiliate's score. """
        # Get consultation to update
        consultation = await cls.__get_affiliate_consultation(affiliate_dni, consultation_id)
        # Update and store
        consultation.score = score.points
        consultation.score_opinion = score.opinion
        await ConsultationDAO.store(consultation)

    @classmethod
    async def put_doctors_opinion(cls, doctor_id: str, consultation_id: str, opinion: ConsultationOpinion):
        """ Update a consultation with prescription and indications. """
        consultation = await cls.__get_doctor_consultation(doctor_id, consultation_id)
        # Check that the consultation belongs to the doctor
        if not consultation.doctor_id == doctor_id:
            raise BusinessError(f'Failed to match doctor ID to consultation ID.', 400)
        # Update and store
        consultation.prescription = opinion.prescription
        consultation.indications = opinion.indications
        await ConsultationDAO.store(consultation)

    @classmethod
    async def __get_affiliate_consultation(cls, affiliate_dni: str, consultation_id: str) -> Consultation:
        if not await AffiliateDAO.find(affiliate_dni):
            raise BusinessError(f'There is no affiliate with DNI {affiliate_dni}.', 404)
        return await cls.__get_consultation(consultation_id)

    @classmethod
    async def __get_doctor_consultation(cls, doctor_id: str, consultation_id: str) -> Consultation:
        if not await DoctorDAO.find_by_id(doctor_id):
            raise BusinessError(f'There is no doctor with ID {doctor_id}.', 404)
        return await cls.__get_consultation(consultation_id)

    @classmethod
    async def __get_consultation(cls, consultation_id: str) -> Consultation:
        consultation = await ConsultationDAO.find(consultation_id)
        if not consultation:
            raise BusinessError(f'There is no consultation with ID {consultation_id}.', 404)
        return consultation
