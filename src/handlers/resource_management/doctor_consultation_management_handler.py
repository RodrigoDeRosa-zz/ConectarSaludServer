from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.resource_management.consultations.consultation_service import ConsultationService
from src.service.resource_management.consultations.mappers.consultation_update_request_mapper import \
    ConsultationUpdateRequestMapper


class DoctorConsultationManagementHandler(CustomRequestHandler):

    async def get(self, doctor_id, consultation_id):
        await self.wrap_coroutine(self.__start_call, **{'doctor_id': doctor_id})

    async def patch(self, doctor_id, consultation_id):
        params = {'doctor_id': doctor_id, 'consultation_id': consultation_id}
        await self.wrap_coroutine(self.__update_consultation, **params)

    """ Handling methods """

    async def __start_call(self, doctor_id):
        """ Returns the id of the call to attend to, if such call exists. """
        call_id = await ConsultationService.start_call(doctor_id)
        self.make_response({'call_id': call_id})

    async def __update_consultation(self, doctor_id, consultation_id):
        """ Adds the doctor's prescription and indications to a given consultation. """
        consultation_opinion = ConsultationUpdateRequestMapper.map(self._parse_body())
        await ConsultationService.put_doctors_opinion(doctor_id, consultation_id, consultation_opinion)
        self.make_response()
