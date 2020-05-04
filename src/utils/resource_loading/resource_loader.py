from json import load
from os.path import abspath, join, dirname

from tornado.ioloop import IOLoop

from src.database.daos.doctor_dao import DoctorDAO
from src.service.resource_management.doctors.doctor_management_service import DoctorManagementService
from src.service.resource_management.doctors.mappers.doctor_management_request_mapper import \
    DoctorManagementRequestMapper
from src.utils.logging.logger import Logger


class ResourceLoader:

    DOCTORS = 'doctors.json'

    @classmethod
    def load_resources(cls):
        """ Load resources to database for every non-existent collection. """
        IOLoop.current().add_timeout(0, cls.__load_doctors)

    @classmethod
    async def __load_doctors(cls):
        """ Read doctors file and load on database if it was not previously done. """
        if await DoctorDAO.all(): return
        # Only load file if there are no doctors in the database
        Logger(cls.__name__).info('Creating basic doctor database entries...')
        file_name = f'{abspath(join(dirname(__file__), "../../.."))}/resources/initial_resources/{cls.DOCTORS}'
        with open(file_name) as fd:
            doctors = load(fd)
        # Add every doctor to the database
        for doctor in doctors:
            await DoctorManagementService.add(DoctorManagementRequestMapper.map_creation(doctor))
