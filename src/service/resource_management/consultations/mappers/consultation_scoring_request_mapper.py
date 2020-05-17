from src.model.consultations.consultation import ConsultationScore
from src.model.errors.business_error import BusinessError


class ConsultationScoringRequestMapper:

    @staticmethod
    def map(request_body: dict) -> ConsultationScore:
        if 'score' not in request_body:
            raise BusinessError(f'Invalid request. Missing field "score".', 400)
        return ConsultationScore(
            points=request_body['score'],
            opinion=request_body.get('score_opinion')
        )
