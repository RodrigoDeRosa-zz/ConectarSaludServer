from src.model.doctors.doctor import Doctor
from src.model.errors.business_error import BusinessError


class DoctorManagementRequestMapper:

    @staticmethod
    def map_creation(request_body: dict) -> Doctor:
        # Check if the request contains all needed fields
        for field in Doctor.fields():
            if field not in request_body and field != 'id':
                raise BusinessError(f'Invalid resource creation request. Missing field {field}.')
        # Create model object
        return Doctor(
            dni=request_body['dni'],
            first_name=request_body['first_name'],
            last_name=request_body['last_name'],
            phone=request_body['phone'],
            email=request_body['email'],
            specialties=request_body['specialties'],
            availability_times=request_body['availability_times']
        )
