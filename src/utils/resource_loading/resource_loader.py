from json import load
from os.path import abspath, join, dirname

from tornado.ioloop import IOLoop

from src.database.daos.affiliate_dao import AffiliateDAO
from src.database.daos.authentication_dao import AuthenticationDAO
from src.database.daos.doctor_dao import DoctorDAO
from src.database.daos.family_group_dao import FamilyGroupDAO
from src.model.affiliates.affiliate import Affiliate
from src.model.authentication.auth_data import AuthData
from src.service.resource_management.doctors.doctor_management_service import DoctorManagementService
from src.service.resource_management.doctors.mappers.doctor_management_request_mapper import \
    DoctorManagementRequestMapper
from src.service.resource_management.symptoms.symptoms_service import SymptomsService
from src.utils.logging.logger import Logger


class ResourceLoader:

    BASE_PATH = 'resources/'
    INITIAL_RESOURCES_FOLDER = f'{BASE_PATH}/initial_resources/'
    DOCTORS = 'doctors.json'
    USERS = 'users.json'
    AFFILIATES = 'affiliates.json'
    FAMILY_GROUPS = 'family_groups.json'
    SYMPTOMS = f'{BASE_PATH}/symptoms.json'
    PATH = None

    @classmethod
    def load_resources(cls, env):
        """ Load resources to database for every non-existent collection. """
        cls.PATH = f'{abspath(join(dirname(__file__), "../../.."))}{"/" if env != "docker" else ""}'
        SymptomsService.set_symptoms(cls.__load_symptoms())
        IOLoop.current().add_timeout(0, cls.__load_doctors)
        IOLoop.current().add_timeout(0, cls.__load_users)
        IOLoop.current().add_timeout(0, cls.__load_affiliates)
        IOLoop.current().add_timeout(0, cls.__load_family_groups)

    @classmethod
    def __load_symptoms(cls):
        """ Load accepted symptoms from file. """
        Logger(cls.__name__).info('Loading accepted symptoms...')
        file_name = f'{cls.PATH}{cls.SYMPTOMS}'
        with open(file_name) as fd:
            symptoms = load(fd)
        return symptoms

    @classmethod
    async def __load_users(cls):
        """ Read users file and load on database if it was not previously done. """
        if await AuthenticationDAO.get_all({}): return
        # Only load file if there are no users in the database
        Logger(cls.__name__).info('Creating basic authentication database entries...')
        file_name = f'{cls.PATH}{cls.INITIAL_RESOURCES_FOLDER}{cls.USERS}'
        with open(file_name) as fd:
            users = load(fd)
        # Add every user to the database
        for user in users:
            await AuthenticationDAO.add(
                AuthData(
                    user_id=user['user_id'],
                    password=user['password'],
                    role=user['role'],
                    device_id=''
                )
            )

    @classmethod
    async def __load_doctors(cls):
        """ Read doctors file and load on database if it was not previously done. """
        if await DoctorDAO.all(): return
        # Only load file if there are no doctors in the database
        Logger(cls.__name__).info('Creating basic doctor database entries...')
        file_name = f'{cls.PATH}{cls.INITIAL_RESOURCES_FOLDER}{cls.DOCTORS}'
        with open(file_name) as fd:
            doctors = load(fd)
        # Add every doctor to the database
        for doctor in doctors:
            await DoctorManagementService.add(DoctorManagementRequestMapper.map_creation(doctor))

    @classmethod
    async def __load_family_groups(cls):
        """ Read family groups file and load on database if it was not previously done. """
        if await FamilyGroupDAO.all(): return
        # Only load file if there are no doctors in the database
        Logger(cls.__name__).info('Creating basic family group database entries...')
        file_name = f'{cls.PATH}{cls.INITIAL_RESOURCES_FOLDER}{cls.FAMILY_GROUPS}'
        with open(file_name) as fd:
            families = load(fd)
        # Add every doctor to the database
        for family in families:
            await FamilyGroupDAO.store(family.get('members', list()))

    @classmethod
    async def __load_affiliates(cls):
        """ Read affiliates file and load on database if it was not previously done. """
        if await AffiliateDAO.all(): return
        # Only load file if there are no doctors in the database
        Logger(cls.__name__).info('Creating basic affiliate database entries...')
        file_name = f'{cls.PATH}{cls.INITIAL_RESOURCES_FOLDER}{cls.AFFILIATES}'
        with open(file_name) as fd:
            affiliates = load(fd)
        # Add every affiliate to the database
        for affiliate in affiliates:
            await AffiliateDAO.store(
                Affiliate(
                    id=affiliate['id'],
                    dni=affiliate['dni'],
                    first_name=affiliate['first_name'],
                    last_name=affiliate['last_name'],
                    plan=affiliate['plan'],
                    sex=affiliate['sex'],
                    age=affiliate['age'],
                    device_id=''
                )
            )
