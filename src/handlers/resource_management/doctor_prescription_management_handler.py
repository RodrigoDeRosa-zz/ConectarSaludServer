from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.resource_management.consultations.consultation_service import ConsultationService
from src.service.resource_management.consultations.mappers.consultation_response_mapper import \
    ConsultationResponseMapper


class DoctorPrescriptionManagementHandler(CustomRequestHandler):

    async def get(self, doctor_id, consultation_id):
        await self.wrap_coroutine(
            self.__get_prescription_data,
            **{'doctor_id': doctor_id, 'consultation_id': consultation_id}
        )

    """ Handling methods """

    async def __get_prescription_data(self, doctor_id, consultation_id):
        consultation, doctor, affiliate = await ConsultationService.doctor_consultation(doctor_id, consultation_id)
        self.make_response(ConsultationResponseMapper.map_prescription(consultation, doctor, affiliate))
