import uuid
from typing import Tuple, List

from src.database.daos.affiliate_dao import AffiliateDAO
from src.database.daos.consultation_dao import ConsultationDAO
from src.database.daos.doctor_dao import DoctorDAO
from src.handlers.socket.socket_manager import SocketManager
from src.model.affiliates.affiliate import Affiliate
from src.model.consultations.consultation import Consultation, ConsultationScore, ConsultationStatus, \
    ConsultationOpinion, ConsultationDTO
from src.model.doctors.doctor import Doctor
from src.model.errors.business_error import BusinessError
from src.service.notification_service import NotificationService
from src.service.queue.queue_manager import QueueManager


class ConsultationService:

    @classmethod
    async def create_for_affiliate(cls, affiliate_dni: str, consultation_data: ConsultationDTO) -> Consultation:
        """ Creates a new consultation for the given affiliate and returns it's id. """
        # TODO -> We'll also need the "patient"
        affiliate = await AffiliateDAO.find(affiliate_dni)
        if not affiliate:
            raise BusinessError(f'There is no affiliate with DNI {affiliate_dni}.', 404)
        # If there is an ongoing call, return it's id
        consultation = await ConsultationDAO.affiliate_consultation_in_progress(affiliate_dni)
        if consultation: return consultation
        # Create new consultation and store
        consultation_id = str(uuid.uuid4())
        consultation = Consultation(
            id=consultation_id,
            affiliate=affiliate,
            symptoms=consultation_data.symptoms,
            reason=consultation_data.reason,
            patient_dni=consultation_data.patient_dni
        )
        await ConsultationDAO.store(consultation)
        # Return id for response
        return consultation

    @classmethod
    async def cancel_consultation(cls, affiliate_dni: str, consultation_id: str):
        """ Cancels a consultation that is waiting for a doctor. """
        consultation = await cls.__get_affiliate_consultation(affiliate_dni, consultation_id)
        consultation.status = ConsultationStatus.CANCELED
        await ConsultationDAO.store(consultation)

    @classmethod
    async def link_socket_to_consultation(cls, consultation_id: str, socket_id: str):
        """ Stores a relationship between a socket and a consultation. """
        consultation = await ConsultationDAO.find(consultation_id)
        # This is to avoid socket re-enqueueing on finished reservations
        if consultation.status == ConsultationStatus.FINISHED: return
        # Set socket ID and update
        consultation.socket_id = socket_id
        await ConsultationDAO.store(consultation)
        await QueueManager.enqueue(consultation)

    @classmethod
    async def next_consultation(cls, doctor_id) -> Tuple[Consultation, Affiliate]:
        """ Returns a consultation that is waiting for a doctor. """
        doctor = await DoctorDAO.find_by_id(doctor_id)
        if not doctor:
            raise BusinessError(f'There are no doctors with ID {doctor_id}.', 404)
        consultation = await QueueManager.pop(doctor.specialties)
        if not consultation:
            raise BusinessError('There are no consultations waiting for the given doctor.', 404)
        # Update information
        consultation.doctor_id = doctor_id
        consultation.status = ConsultationStatus.WAITING_CALL
        await ConsultationDAO.store(consultation)
        # Get associated affiliate
        affiliate = await AffiliateDAO.find(consultation.affiliate_dni)
        # Return id
        return consultation, affiliate

    @classmethod
    async def start_call(cls, doctor_id: str) -> str:
        """ Returns a call ID if there is any for the given doctor. """
        doctor = await DoctorDAO.find_by_id(doctor_id)
        if not doctor:
            raise BusinessError(f'There is no doctor with ID {doctor_id}.', 404)
        # There could be a consultation in progress (in which case we would return that same call_id)
        consultation = await ConsultationDAO.doctor_consultation_in_progress(doctor_id)
        if consultation: return consultation.call_id
        # If it is a new consultation, then we need to create the call
        consultation = await ConsultationDAO.next_consultation_waiting_call(doctor_id)
        # There may be no affiliate to talk with at the moment
        if not consultation:
            raise BusinessError(f'There is no consultation waiting for the given doctor.', 404)
        # Create a call id for the consultation
        call_id = str(uuid.uuid4())
        # Notify start of call to affiliate via socket
        socket_id = consultation.socket_id
        await SocketManager.notify_call_start(call_id, socket_id)
        # Notify start of call to affiliate via push notification
        affiliate = await AffiliateDAO.find(consultation.affiliate_dni)
        # TODO -> This if shouldn't be necessary, but it'll be here temporarily to avoid bugs
        if affiliate.device_id:
            NotificationService.notify_call_start(affiliate.device_id, doctor.last_name, affiliate.first_name)
        # Update consultation with new call id and IN_PROGRESS status
        consultation.status = ConsultationStatus.IN_PROGRESS
        consultation.call_id = call_id
        await ConsultationDAO.store(consultation)
        # Return the id of the call
        return call_id

    @classmethod
    async def affiliate_consultation(
            cls,
            affiliate_dni: str,
            consultation_id: str
    ) -> Tuple[Consultation, Doctor, Affiliate]:
        """ Get consultation and check if affiliate and consultation are related. """
        consultation = await cls.__get_affiliate_consultation(affiliate_dni, consultation_id)
        # Check that the consultation belongs to the affiliate
        if not consultation.affiliate_dni == affiliate_dni:
            raise BusinessError(f'Failed to match affiliate DNI to consultation ID.', 400)
        # Get consultation doctor
        doctor = await DoctorDAO.find_by_id(consultation.doctor_id)
        # Get consultation patient
        patient = await AffiliateDAO.find(consultation.patient_dni)
        # Return both objects for mapping
        return consultation, doctor, patient

    @classmethod
    async def put_scoring_data(cls, affiliate_dni: str, consultation_id: str, score: ConsultationScore):
        """ Update a consultation with the affiliate's score. """
        # Get consultation to update
        consultation = await cls.__get_affiliate_consultation(affiliate_dni, consultation_id)
        # Update and store
        consultation.score = score.points
        consultation.score_opinion = score.opinion
        consultation.status = ConsultationStatus.FINISHED
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
        consultation.status = ConsultationStatus.FINISHED
        await ConsultationDAO.store(consultation)

    @classmethod
    async def all_consultations(cls, affiliate_dni: str) -> Tuple[List[Consultation], List[Doctor]]:
        """ Returns all the past consultations of the given affiliate. """
        if not await AffiliateDAO.find(affiliate_dni):
            raise BusinessError(f'There is no affiliate with DNI {affiliate_dni}.', 404)
        consultations = await ConsultationDAO.all_affiliate_consultations(affiliate_dni)
        doctors = [await DoctorDAO.find_by_id(consultation.doctor_id) for consultation in consultations]
        return consultations, doctors

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
