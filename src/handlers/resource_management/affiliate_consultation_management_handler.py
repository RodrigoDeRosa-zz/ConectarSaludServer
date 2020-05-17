from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.errors.business_error import BusinessError
from src.service.resource_management.consultations.consultation_service import ConsultationService
from src.service.resource_management.consultations.mappers.consultation_response_mapper import \
    ConsultationResponseMapper
from src.service.resource_management.consultations.mappers.consultation_scoring_request_mapper import \
    ConsultationScoringRequestMapper


class AffiliateConsultationManagementHandler(CustomRequestHandler):

    async def post(self, affiliate_dni, consultation_id):
        """ Creates a new consultation for the given affiliate. """
        try:
            consultation_id = await ConsultationService.create_for_affiliate(affiliate_dni)
            self.make_response({'consultation_id': consultation_id}, status_code=200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def patch(self, affiliate_dni, consultation_id):
        """ Creates a new consultation for the given affiliate. """
        try:
            consultation_score = ConsultationScoringRequestMapper.map(self._parse_body())
            await ConsultationService.put_scoring_data(affiliate_dni, consultation_id, consultation_score)
            # This service only returns an HTTP 200
            self.make_response(status_code=200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def get(self, affiliate_dni, consultation_id):
        """ Returns relevant information for the affiliate about the consultation. """
        try:
            consultation, doctor = await ConsultationService.get_consultation(affiliate_dni, consultation_id)
            self.make_response(ConsultationResponseMapper.map_for_affiliate(consultation, doctor), status_code=200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)
