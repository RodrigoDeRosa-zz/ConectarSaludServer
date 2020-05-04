from typing import List

from src.database.daos.generic_dao import GenericDAO
from src.database.mongo import Mongo
from src.model.doctors.doctor import Doctor


class DoctorDAO(GenericDAO):

    @classmethod
    async def find_by_id(cls, doctor_id: str) -> Doctor:
        """ Return doctor with given id if existent. """
        document = await cls.get_first({'_id': doctor_id})
        # Get instance directly from its name
        return None if not document else cls.__to_object(document)

    @classmethod
    async def find_by_dni(cls, doctor: Doctor) -> Doctor:
        """ Return doctor with given dni if existent. """
        document = await cls.get_first({'dni': doctor.dni})
        # Get instance directly from its name
        return None if not document else cls.__to_object(document)

    @classmethod
    async def find_by_licence(cls, doctor: Doctor) -> Doctor:
        """ Return doctor with given licence if existent. """
        document = await cls.get_first({'licence': doctor.licence})
        # Get instance directly from its name
        return None if not document else cls.__to_object(document)

    @classmethod
    async def all(cls) -> List[Doctor]:
        """ Returns all doctors stored in the database. """
        documents = await cls.get_all()
        return [cls.__to_object(document) for document in documents]

    @classmethod
    async def store(cls, doctor: Doctor):
        """ Upsert doctor in database. Creates if non existent, updates otherwise. """
        await cls.upsert(
            {'_id': doctor.id},
            {'$set': cls.__to_document(doctor)}
        )

    @classmethod
    async def delete(cls, doctor_id: str):
        """ Remove doctor from database. """
        await cls.delete_first({'_id': doctor_id})

    @classmethod
    def __to_object(cls, document: dict) -> Doctor:
        return Doctor(
            id=document['_id'],
            dni=document['dni'],
            licence=document['licence'],
            first_name=document['first_name'],
            last_name=document['last_name'],
            email=document['email'],
            specialties=document['specialties'],
            availability_times=document['availability_times']
        )

    @classmethod
    def __to_document(cls, doctor: Doctor) -> dict:
        document = dict()
        # Add only existent fields to the document. This way we can create and update with the same code
        if doctor.dni: document['dni'] = doctor.dni
        if doctor.licence: document['licence'] = doctor.licence
        if doctor.first_name: document['first_name'] = doctor.first_name
        if doctor.last_name: document['last_name'] = doctor.last_name
        if doctor.email: document['email'] = doctor.email
        if doctor.specialties: document['specialties'] = doctor.specialties
        if doctor.availability_times: document['availability_times'] = doctor.availability_times
        # Return create/update document
        return document

    @classmethod
    def create_indexes(cls, db):
        db.doctors.create_index('dni', unique=True)
        db.doctors.create_index('licence', unique=True)

    @classmethod
    def collection(cls):
        return Mongo.get().doctors
