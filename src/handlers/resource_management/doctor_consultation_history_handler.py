from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.resource_management.consultations.consultation_service import ConsultationService
from src.service.resource_management.consultations.mappers.consultation_response_mapper import \
    ConsultationResponseMapper


class DoctorConsultationHistoryHandler(CustomRequestHandler):

    async def get(self, doctor_id):
        await self.wrap_coroutine(self.__doctor_history, **{'doctor_id': doctor_id})

    """ Handling methods """

    async def __doctor_history(self, doctor_id):
        """ Returns the id of the call to attend to, if such call exists. """
        consultations, affiliates = await ConsultationService.get_doctor_consultations(doctor_id)
        response = ConsultationResponseMapper.map_doctor_consultation_list(consultations, affiliates)
        self.make_response(response)
