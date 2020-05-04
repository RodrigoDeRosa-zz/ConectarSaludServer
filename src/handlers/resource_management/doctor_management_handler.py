from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.errors.business_error import BusinessError
from src.service.resource_management.doctors.doctor_management_service import DoctorManagementService
from src.service.resource_management.doctors.mappers.doctor_management_request_mapper import \
    DoctorManagementRequestMapper
from src.service.resource_management.doctors.mappers.doctor_management_response_mapper import \
    DoctorManagementResponseMapper


class DoctorManagementHandler(CustomRequestHandler):

    async def post(self, doctor_id):
        """ Doctor resource creation endpoint. """
        try:
            doctor = DoctorManagementRequestMapper.map_creation(self._parse_body())
            await DoctorManagementService.add(doctor)
            # This service only returns an HTTP 200
            self.make_response(status_code=200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def patch(self, doctor_id):
        """ Modify an specific doctor's information. """
        try:
            doctor = DoctorManagementRequestMapper.map_modification(self._parse_body(), doctor_id)
            await DoctorManagementService.update_information(doctor)
            # This service only returns an HTTP 200
            self.make_response(status_code=200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def get(self, doctor_id):
        """ Retrieve doctor information. If parameter is null, all doctors are returned. """
        try:
            if not doctor_id:
                response = await DoctorManagementService.retrieve_all()
                self.make_response(DoctorManagementResponseMapper.map_all_doctors(response))
            else:
                response = await DoctorManagementService.retrieve(doctor_id)
                self.make_response(DoctorManagementResponseMapper.map_doctor(response))
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def delete(self, doctor_id):
        """ Delete the specified doctor from the database. """
        try:
            if not doctor_id: raise BusinessError('No doctor ID specified for deletion.')
            await DoctorManagementService.remove(doctor_id)
            # This service only returns an HTTP 200
            self.make_response(status_code=200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)