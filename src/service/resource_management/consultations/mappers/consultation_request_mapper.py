from src.model.consultations.consultation import ConsultationDTO
from src.model.errors.business_error import BusinessError


class ConsultationRequestMapper:

    @staticmethod
    def map(request_body: dict) -> ConsultationDTO:
        if 'symptoms' not in request_body:
            raise BusinessError(f'Invalid request. Missing field "symptoms".', 400)
        return ConsultationDTO(
            symptoms=request_body['symptoms'],
            reason=request_body.get('reason'),
            patient_dni=request_body.get('patient_dni')
        )
