from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.errors.business_error import BusinessError
from src.service.resource_management.doctors.doctor_management_service import DoctorManagementService
from src.service.resource_management.doctors.mappers.doctor_management_request_mapper import \
    DoctorManagementRequestMapper


class DoctorManagementHandler(CustomRequestHandler):

    SUPPORTED_METHODS = ['POST', 'PATCH', 'GET', 'DELETE']

    async def post(self, doctor_id):
        """ Doctor resource creation endpoint. """
        try:
            doctor = DoctorManagementRequestMapper.map_creation(self._parse_body())
            await DoctorManagementService.create(doctor)
            # This service only returns an HTTP 200
            self.set_status(200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)
