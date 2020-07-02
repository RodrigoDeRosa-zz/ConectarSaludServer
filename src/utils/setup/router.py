from src.handlers.authentication_handler import AuthenticationHandler
from src.handlers.health_check_handler import HealthCheckHandler
from src.handlers.resource_management.active_consultations_handler import ActiveConsultationHandler
from src.handlers.resource_management.affiliate_consultation_management_handler import \
    AffiliateConsultationManagementHandler
from src.handlers.resource_management.affiliate_prescription_management_handler import \
    AffiliatePrescriptionManagementHandler
from src.handlers.resource_management.consultation_management_handler import ConsultationManagementHandler
from src.handlers.resource_management.doctor_consultation_history_handler import DoctorConsultationHistoryHandler
from src.handlers.resource_management.doctor_consultation_management_handler import DoctorConsultationManagementHandler
from src.handlers.resource_management.doctor_management_handler import DoctorManagementHandler
from src.handlers.resource_management.doctor_prescription_management_handler import DoctorPrescriptionManagementHandler
from src.handlers.resource_management.family_group_handler import FamilyGroupHandler
from src.handlers.socket.socket_manager import SocketManager
from src.handlers.symptoms_handler import SymptomsHandler
from src.handlers.utils.collection_cleaning_handler import CollectionCleaningHandler


class Router:

    # Dictionary to map route to Tornado RequestHandler subclasses
    ROUTES = {
        '/health/health-check': HealthCheckHandler,
        '/authenticate': AuthenticationHandler,
        '/doctors/?(?P<doctor_id>[^/]+)?': DoctorManagementHandler,
        '/consultations/?(?P<consultation_id>[^/]+)?': ConsultationManagementHandler,
        '/doctors/(?P<doctor_id>[^/]+)/consultations/history': DoctorConsultationHistoryHandler,
        '/doctors/(?P<doctor_id>[^/]+)/consultations/?(?P<consultation_id>[^/]+)?': DoctorConsultationManagementHandler,
        '/doctors/(?P<doctor_id>[^/]+)/prescriptions/?(?P<consultation_id>[^/]+)?': DoctorPrescriptionManagementHandler,
        '/affiliates/(?P<affiliate_dni>[^/]+)/consultations/?(?P<consultation_id>[^/]+)?':
            AffiliateConsultationManagementHandler,
        '/affiliates/(?P<affiliate_dni>[^/]+)/prescriptions/?(?P<consultation_id>[^/]+)?':
            AffiliatePrescriptionManagementHandler,
        '/affiliates/(?P<affiliate_dni>[^/]+)/active-consultations': ActiveConsultationHandler,
        '/affiliates/(?P<affiliate_dni>[^/]+)/family': FamilyGroupHandler,
        '/utils/collections/clear/(?P<collection_name>[^/]+)': CollectionCleaningHandler,
        '/symptoms': SymptomsHandler,
        r'/socket.io/': SocketManager.handler()
    }

    @classmethod
    def get_routes(cls):
        """ Get routes with their respective handlers"""
        return [(k, v) for k, v in cls.ROUTES.items()]
