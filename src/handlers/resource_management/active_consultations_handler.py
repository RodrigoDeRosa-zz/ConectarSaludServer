from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.resource_management.consultations.consultation_service import ConsultationService
from src.service.resource_management.consultations.mappers.consultation_response_mapper import \
    ConsultationResponseMapper


class ActiveConsultationHandler(CustomRequestHandler):

    async def get(self, affiliate_dni):
        params = {'affiliate_dni': affiliate_dni}
        await self.wrap_coroutine(self.__check_consultation_in_progress, **params)

    """ Handling methods """

    async def __check_consultation_in_progress(self, affiliate_dni):
        """ Returns a call id if the affiliate has a consultation in progress. """
        consultation = await ConsultationService.required_consultation(affiliate_dni)
        self.make_response(ConsultationResponseMapper.map_consultation_in_progress(consultation))
