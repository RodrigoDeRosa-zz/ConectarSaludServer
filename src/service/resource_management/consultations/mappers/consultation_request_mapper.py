from src.model.consultations.consultation import ConsultationDTO
from src.model.errors.business_error import BusinessError


class ConsultationRequestMapper:

    @staticmethod
    def map(request_body: dict) -> ConsultationDTO:
        for field in ['patient_dni', 'symptoms']:
            if field not in request_body:
                raise BusinessError(f'Invalid request. Missing field "{field}".', 400)
        return ConsultationDTO(
            symptoms=request_body['symptoms'],
            patient_dni=request_body['patient_dni'],
            reason=request_body.get('reason')
        )
