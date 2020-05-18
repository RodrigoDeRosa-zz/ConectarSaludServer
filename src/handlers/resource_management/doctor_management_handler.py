from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.errors.business_error import BusinessError
from src.service.resource_management.doctors.doctor_management_service import DoctorManagementService
from src.service.resource_management.doctors.mappers.doctor_management_request_mapper import \
    DoctorManagementRequestMapper
from src.service.resource_management.doctors.mappers.doctor_management_response_mapper import \
    DoctorManagementResponseMapper


class DoctorManagementHandler(CustomRequestHandler):

    SUPPORTED_METHODS = ['OPTIONS', 'GET', 'POST', 'PATCH', 'DELETE']

    async def post(self, doctor_id):
        await self.wrap_handling(self.__add_doctor, **{})

    async def patch(self, doctor_id):
        await self.wrap_handling(self.__update_doctor, **{'doctor_id': doctor_id})

    async def get(self, doctor_id):
        await self.wrap_handling(self.__retrieve, **{'doctor_id': doctor_id})

    async def delete(self, doctor_id):
        await self.wrap_handling(self.__remove_doctor, **{'doctor_id': doctor_id})

    """ Handling methods """

    async def __add_doctor(self):
        """ Doctor resource creation endpoint. """
        doctor = DoctorManagementRequestMapper.map_creation(self._parse_body())
        await DoctorManagementService.add(doctor)
        # This service only returns an HTTP 200
        self.make_response(status_code=200)

    async def __update_doctor(self, doctor_id):
        """ Modify an specific doctor's information. """
        doctor = DoctorManagementRequestMapper.map_modification(self._parse_body(), doctor_id)
        await DoctorManagementService.update_information(doctor)
        # This service only returns an HTTP 200
        self.make_response(status_code=200)

    async def __retrieve(self, doctor_id):
        """ Retrieve doctor information. If parameter is null, all doctors are returned. """
        if not doctor_id:
            response = await DoctorManagementService.retrieve_all()
            self.make_response(DoctorManagementResponseMapper.map_all_doctors(response))
        else:
            response = await DoctorManagementService.retrieve(doctor_id)
            self.make_response(DoctorManagementResponseMapper.map_doctor(response))

    async def __remove_doctor(self, doctor_id):
        """ Delete the specified doctor from the database. """
        if not doctor_id: raise BusinessError('No doctor ID specified for deletion.')
        await DoctorManagementService.remove(doctor_id)
        # This service only returns an HTTP 200
        self.make_response(status_code=200)
