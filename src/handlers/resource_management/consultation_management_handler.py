from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.errors.business_error import BusinessError
from src.service.resource_management.consultations.consultation_service import ConsultationService


class ConsultationManagementHandler(CustomRequestHandler):

    async def get(self, consultation_id):
        doctor_id = self.get_argument('doctor', None, True)
        if not doctor_id: raise BusinessError('Missing query parameter "doctor".', 400)
        await self.wrap_handling(self.__next_consultation, **{'doctor_id': doctor_id})

    """ Handling methods. """

    async def __next_consultation(self, doctor_id):
        """ Return a consultation in need of a doctor. """
        consultation_id = await ConsultationService.next_consultation(doctor_id)
        self.make_response({'consultation_id': consultation_id})
