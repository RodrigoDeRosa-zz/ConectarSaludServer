from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.resource_management.consultations.consultation_service import ConsultationService
from src.service.resource_management.consultations.mappers.consultation_response_mapper import \
    ConsultationResponseMapper
from src.service.resource_management.consultations.mappers.consultation_scoring_request_mapper import \
    ConsultationScoringRequestMapper


class AffiliateConsultationManagementHandler(CustomRequestHandler):

    async def post(self, affiliate_dni, consultation_id):
        await self.wrap_handling(self.__create_affiliate_consultation, **{'affiliate_dni': affiliate_dni})

    async def delete(self, affiliate_dni, consultation_id):
        params = {'affiliate_dni': affiliate_dni, 'consultation_id': consultation_id}
        await self.wrap_handling(self.__cancel_affiliate_consultation, **params)

    async def patch(self, affiliate_dni, consultation_id):
        params = {'affiliate_dni': affiliate_dni, 'consultation_id': consultation_id}
        await self.wrap_handling(self.__set_consultation_score, **params)

    async def get(self, affiliate_dni, consultation_id):
        params = {'affiliate_dni': affiliate_dni, 'consultation_id': consultation_id}
        await self.wrap_handling(self.__retrieve, **params)

    """ Handling methods. """

    async def __create_affiliate_consultation(self, affiliate_dni):
        """ Creates a new consultation for the given affiliate. """
        consultation = await ConsultationService.create_for_affiliate(affiliate_dni)
        self.make_response(ConsultationResponseMapper.map_consultation(consultation))

    async def __cancel_affiliate_consultation(self, affiliate_dni, consultation_id):
        """ Cancel a consultation for the given affiliate. """
        await ConsultationService.cancel_consultation(affiliate_dni, consultation_id)

    async def __set_consultation_score(self, affiliate_dni, consultation_id):
        """ Creates a new consultation for the given affiliate. """
        consultation_score = ConsultationScoringRequestMapper.map(self._parse_body())
        await ConsultationService.put_scoring_data(affiliate_dni, consultation_id, consultation_score)
        # This service only returns an HTTP 200
        self.make_response()

    async def __retrieve(self, affiliate_dni, consultation_id):
        """ Returns relevant information for the affiliate about the consultation. """
        consultation, doctor = await ConsultationService.affiliate_consultation(affiliate_dni, consultation_id)
        self.make_response(ConsultationResponseMapper.map_for_affiliate(consultation, doctor))
