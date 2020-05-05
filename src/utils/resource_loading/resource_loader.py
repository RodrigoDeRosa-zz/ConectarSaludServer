from json import load
from os.path import abspath, join, dirname

from tornado.ioloop import IOLoop

from src.database.daos.authentication_dao import AuthenticationDAO
from src.database.daos.doctor_dao import DoctorDAO
from src.model.authentication.auth_data import AuthData
from src.service.resource_management.doctors.doctor_management_service import DoctorManagementService
from src.service.resource_management.doctors.mappers.doctor_management_request_mapper import \
    DoctorManagementRequestMapper
from src.utils.logging.logger import Logger


class ResourceLoader:

    DOCTORS = 'doctors.json'
    USERS = 'users.json'
    FOLDER = 'resources/initial_resources/'
    PATH = None

    @classmethod
    def load_resources(cls, env):
        """ Load resources to database for every non-existent collection. """
        cls.PATH = f'{abspath(join(dirname(__file__), "../../.."))}{"/" if env != "docker" else ""}{cls.FOLDER}'
        IOLoop.current().add_timeout(0, cls.__load_doctors)
        IOLoop.current().add_timeout(0, cls.__load_users)

    @classmethod
    async def __load_users(cls):
        """ Read users file and load on database if it was not previously done. """
        if await AuthenticationDAO.get_all({}): return
        # Only load file if there are no users in the database
        Logger(cls.__name__).info('Creating basic authentication database entries...')
        file_name = f'{cls.PATH}{cls.USERS}'
        with open(file_name) as fd:
            users = load(fd)
        # Add every doctor to the database
        for user in users:
            await AuthenticationDAO.add(AuthData(user_id=user['user_id'], password=user['password'], role=user['role']))

    @classmethod
    async def __load_doctors(cls):
        """ Read doctors file and load on database if it was not previously done. """
        if await DoctorDAO.all(): return
        # Only load file if there are no doctors in the database
        Logger(cls.__name__).info('Creating basic doctor database entries...')
        file_name = f'{cls.PATH}{cls.DOCTORS}'
        with open(file_name) as fd:
            doctors = load(fd)
        # Add every doctor to the database
        for doctor in doctors:
            await DoctorManagementService.add(DoctorManagementRequestMapper.map_creation(doctor))
