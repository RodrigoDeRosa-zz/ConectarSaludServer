from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.resource_management.consultations.consultation_service import ConsultationService


class DoctorConsultationManagementHandler(CustomRequestHandler):

    async def get(self, doctor_id):
        await self.wrap_handling(self.__start_call, **{'doctor_id': doctor_id})

    """ Handling methods """

    async def __start_call(self, doctor_id):
        """ Returns the id of the call to attend to, if such call exists. """
        call_id = await ConsultationService.start_call(doctor_id)
        self.make_response({'call_id': call_id})
