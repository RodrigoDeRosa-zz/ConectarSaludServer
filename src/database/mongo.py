from motor.motor_tornado import MotorClient

from src.utils.logging.logger import Logger


class Mongo:
    """ MongoDB access point. """

    __CLIENT = None
    DB = None

    @classmethod
    def init(cls, host='localhost', port=27017, db_name='connecting_health', user=None, password=None):
        """ Create database with asynchronous connector."""
        cls.get_logger().info('Establishing database connection...')
        uri = cls.__create_uri(host, port, user, password, db_name)
        # Create db client
        cls.__CLIENT = MotorClient(uri)
        cls.DB = cls.__CLIENT.get_default_database()

    @classmethod
    def create_indexes(cls):
        """ Create indexes for all collections. """
        # Imports need to be here to avoid circular import issues.
        from src.database.daos.doctor_dao import DoctorDAO
        from src.database.daos.affiliate_dao import AffiliateDAO
        from src.database.daos.authentication_dao import AuthenticationDAO
        from src.database.daos.consultation_dao import ConsultationDAO
        from src.database.daos.queue_dao import QueueDAO
        cls.get_logger().info('Configuring database indexes...')
        DoctorDAO.create_indexes(cls.DB)
        AffiliateDAO.create_indexes(cls.DB)
        ConsultationDAO.create_indexes(cls.DB)
        AuthenticationDAO.create_indexes(cls.DB)
        QueueDAO.create_indexes(cls.DB)

    @classmethod
    def set(cls, db):
        # The received db will always be the same object so concurrence won't be a problem.
        # This is just for a more comfortable usage
        cls.DB = db

    @classmethod
    def get(cls):
        return cls.DB

    @classmethod
    def _drop_database(cls, db_name):
        """ Visible for testing """
        cls.__CLIENT.drop_database(db_name)

    @classmethod
    def __create_uri(cls, host, port, user, password, db_name):
        """ Generates database URI"""
        # Create auth string from parameters
        auth = f'{user}:{password}@' if user and password else ''
        # Create database URI
        return f'mongodb://{auth}{host}:{port}/{db_name}?retryWrites=false'

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)
