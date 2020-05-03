from uuid import uuid4

from src.database.daos.doctor_dao import DoctorDAO
from src.model.doctors.doctor import Doctor
from src.model.errors.business_error import BusinessError


class DoctorManagementService:

    @classmethod
    async def create(cls, doctor: Doctor):
        # Check if doctor with given dni exists
        if await DoctorDAO.find_by_dni(doctor):
            raise BusinessError(f'Doctor with DNI {doctor.dni} already exists.', 409)
        # Assign id and store new doctor
        doctor.id = str(uuid4())
        await DoctorDAO.store(doctor)
