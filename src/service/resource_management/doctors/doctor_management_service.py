from typing import List
from uuid import uuid4

from src.database.daos.doctor_dao import DoctorDAO
from src.model.doctors.doctor import Doctor
from src.model.errors.business_error import BusinessError


class DoctorManagementService:

    @classmethod
    async def add(cls, doctor: Doctor):
        # Check if doctor with given dni exists
        if await DoctorDAO.find_by_dni(doctor.dni):
            raise BusinessError(f'Doctor with DNI {doctor.dni} already exists.', 409)
        # Check if doctor with given licence exists
        if await DoctorDAO.find_by_licence(doctor):
            raise BusinessError(f'Doctor with licence {doctor.licence} already exists.', 409)
        # Assign id and store new doctor
        doctor.id = str(uuid4())
        await DoctorDAO.store(doctor)

    @classmethod
    async def remove(cls, doctor_id: str):
        # Check if doctor with given id exists
        if not await DoctorDAO.find_by_id(doctor_id):
            raise BusinessError(f'There is no doctor with id {doctor_id}.', 404)
        await DoctorDAO.delete(doctor_id)

    @classmethod
    async def update_information(cls, doctor: Doctor):
        # Check if doctor to be modified exists
        db_doctor = await DoctorDAO.find_by_id(doctor.id)
        if not db_doctor:
            raise BusinessError(f'There is no doctor with id {doctor.id}.', 404)
        # Check if doctor with given dni exists
        if doctor.dni and db_doctor.dni != doctor.dni and await DoctorDAO.find_by_dni(doctor.dni):
            raise BusinessError(f'Doctor with DNI {doctor.dni} already exists.', 409)
        # Check if doctor with given licence exists
        if doctor.licence and db_doctor.licence != doctor.licence and await DoctorDAO.find_by_licence(doctor):
            raise BusinessError(f'Doctor with licence {doctor.licence} already exists.', 409)
        # Assign id and store new doctor
        await DoctorDAO.store(doctor)

    @classmethod
    async def retrieve(cls, doctor_id: str) -> Doctor:
        """ Returns the doctor object associated to the given ID, if existent. """
        doctor = await DoctorDAO.find_by_id(doctor_id)
        if not doctor:
            raise BusinessError(f'There is no doctor with id {doctor_id}.', 404)
        return doctor

    @classmethod
    async def retrieve_all(cls) -> List[Doctor]:
        """ Returns all doctors stored in the database. """
        return await DoctorDAO.all()
