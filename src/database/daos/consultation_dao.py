import pymongo

from src.database.daos.generic_dao import GenericDAO
from src.database.mongo import Mongo
from src.model.consultations.consultation import Consultation, ConsultationStatus


class ConsultationDAO(GenericDAO):

    @classmethod
    async def find(cls, consultation_id: str) -> Consultation:
        """ Return consultation with given id if existent. """
        document = await cls.get_first({'_id': consultation_id})
        # Get instance directly from its name
        return None if not document else cls.__to_object(document)

    @classmethod
    async def next_consultation_waiting_call(cls, doctor_id: str) -> Consultation:
        """ Returns consultation in progress for given doctor if it exists. """
        document = await cls.get_first({'doctor_id': doctor_id, 'status': ConsultationStatus.WAITING_CALL.value})
        return None if not document else cls.__to_object(document)

    @classmethod
    async def next_consultation_waiting_doctor(cls) -> Consultation:
        """ Returns consultation waiting to have a doctor assigned. """
        documents = await cls.get_sorted(
            query={'status': ConsultationStatus.WAITING_DOCTOR.value},
            sort_list=[('creation_date', pymongo.ASCENDING)]
        )
        document = None if not documents else documents[0]
        return None if not document else cls.__to_object(document)

    @classmethod
    async def store(cls, consultation: Consultation):
        """ Upsert consultation in database. Creates if non existent, updates otherwise. """
        await cls.upsert(
            {'_id': consultation.id},
            {'$set': cls.__to_document(consultation)}
        )

    @classmethod
    def __to_object(cls, document: dict) -> Consultation:
        return Consultation(
            id=document['_id'],
            affiliate_dni=document['affiliate_dni'],
            status=ConsultationStatus[document['status']],
            creation_date=document['creation_date'],
            doctor_id=document.get('doctor_id'),
            call_id=document.get('call_id'),
            score=document.get('score'),
            score_opinion=document.get('score_opinion'),
            prescription=document.get('prescription'),
            indications=document.get('indications'),
        )

    @classmethod
    def __to_document(cls, consultation: Consultation) -> dict:
        document = dict()
        # Add only existent fields to the document. This way we can create and update with the same code
        if consultation.affiliate_dni: document['affiliate_dni'] = consultation.affiliate_dni
        if consultation.status: document['status'] = consultation.status.value
        if consultation.creation_date: document['creation_date'] = consultation.creation_date
        if consultation.doctor_id: document['doctor_id'] = consultation.doctor_id
        if consultation.call_id: document['call_id'] = consultation.call_id
        if consultation.score: document['score'] = consultation.score
        if consultation.score_opinion: document['score_opinion'] = consultation.score_opinion
        if consultation.prescription: document['prescription'] = consultation.prescription
        if consultation.indications: document['indications'] = consultation.indications
        # Return create/update document
        return document

    @classmethod
    def create_indexes(cls, db):
        db.doctors.create_index('doctor_id')
        db.doctors.create_index('affiliate_dni')
        db.doctors.create_index('creation_date')

    @classmethod
    def collection(cls):
        return Mongo.get().consultations
