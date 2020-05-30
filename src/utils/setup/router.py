from src.handlers.authentication_handler import AuthenticationHandler
from src.handlers.health_check_handler import HealthCheckHandler
from src.handlers.resource_management.affiliate_consultation_management_handler import \
    AffiliateConsultationManagementHandler
from src.handlers.resource_management.consultation_management_handler import ConsultationManagementHandler
from src.handlers.resource_management.doctor_consultation_management_handler import DoctorConsultationManagementHandler
from src.handlers.resource_management.doctor_management_handler import DoctorManagementHandler
from src.handlers.socket.socket_manager import SocketManager
from src.handlers.utils.collection_cleaning_handler import CollectionCleaningHandler


class Router:

    # Dictionary to map route to Tornado RequestHandler subclasses
    ROUTES = {
        '/health/health-check': HealthCheckHandler,
        '/authenticate': AuthenticationHandler,
        '/doctors/?(?P<doctor_id>[^/]+)?': DoctorManagementHandler,
        '/consultations/?(?P<consultation_id>[^/]+)?': ConsultationManagementHandler,
        '/doctors/(?P<doctor_id>[^/]+)/consultations/?(?P<consultation_id>[^/]+)?': DoctorConsultationManagementHandler,
        '/affiliates/(?P<affiliate_dni>[^/]+)/consultations/?(?P<consultation_id>[^/]+)?':
            AffiliateConsultationManagementHandler,
        '/utils/collections/clear/(?P<collection_name>[^/]+)': CollectionCleaningHandler,
        r'/socket.io/': SocketManager.handler()
    }

    @classmethod
    def get_routes(cls):
        """ Get routes with their respective handlers"""
        return [(k, v) for k, v in cls.ROUTES.items()]
