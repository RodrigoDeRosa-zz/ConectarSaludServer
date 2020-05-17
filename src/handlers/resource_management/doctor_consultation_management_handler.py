from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.errors.business_error import BusinessError
from src.service.resource_management.consultations.consultation_service import ConsultationService


class DoctorConsultationManagementHandler(CustomRequestHandler):

    async def get(self, doctor_id):
        """ Returns the id of the call to attend to, if such call exists. """
        try:
            call_id = await ConsultationService.start_call(doctor_id)
            self.make_response({'call_id': call_id})
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)
