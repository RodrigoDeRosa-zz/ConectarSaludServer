from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.resource_management.consultations.consultation_service import ConsultationService
from src.service.resource_management.consultations.mappers.consultation_response_mapper import \
    ConsultationResponseMapper


class AffiliatePrescriptionManagementHandler(CustomRequestHandler):

    async def get(self, affiliate_dni, consultation_id):
        await self.wrap_coroutine(
            self.__get_prescription_data,
            **{'affiliate_dni': affiliate_dni, 'consultation_id': consultation_id}
        )

    """ Handling methods """

    async def __get_prescription_data(self, affiliate_dni, consultation_id):
        consultation, doctor, affiliate = await ConsultationService.affiliate_consultation(
            affiliate_dni,
            consultation_id
        )
        self.make_response(ConsultationResponseMapper.map_prescription(consultation, doctor, affiliate))
