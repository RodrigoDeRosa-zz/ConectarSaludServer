from src.model.doctors.doctor import Doctor
from src.model.errors.business_error import BusinessError


class DoctorManagementRequestMapper:

    @staticmethod
    def map_creation(request_body: dict) -> Doctor:
        # Check if the request contains all needed fields
        for field in Doctor.fields():
            if field not in request_body and field != 'id':
                raise BusinessError(f'Invalid resource creation request. Missing field {field}.', 400)
        # Create model object
        return Doctor(
            dni=request_body['dni'],
            licence=request_body['licence'],
            first_name=request_body['first_name'],
            last_name=request_body['last_name'],
            email=request_body['email'],
            centers=request_body['centers'],
            specialties=request_body['specialties'],
            availability_times=request_body['availability_times']
        )

    @staticmethod
    def map_modification(request_body: dict, doctor_id: str) -> Doctor:
        # Check if the request contains all needed fields
        if not doctor_id: raise BusinessError('Doctor ID is compulsory for this service.', 400)
        if not request_body: raise BusinessError('Tried to update doctor with an empty patch body.', 400)
        # Create model object only with the elements that were received
        doctor = Doctor(id=doctor_id)
        if 'dni' in request_body: doctor.dni = request_body['dni']
        if 'licence' in request_body: doctor.licence = request_body['licence']
        if 'first_name' in request_body: doctor.first_name = request_body['first_name']
        if 'last_name' in request_body: doctor.last_name = request_body['last_name']
        if 'email' in request_body: doctor.email = request_body['email']
        if 'centers' in request_body: doctor.centers = request_body['centers']
        if 'specialties' in request_body: doctor.specialties = request_body['specialties']
        if 'availability_times' in request_body: doctor.availability_times = request_body['availability_times']
        return doctor
