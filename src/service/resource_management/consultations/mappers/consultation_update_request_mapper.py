from src.model.consultations.consultation import ConsultationOpinion


class ConsultationUpdateRequestMapper:

    @staticmethod
    def map(request_body: dict) -> ConsultationOpinion:
        return ConsultationOpinion(
            prescription=request_body.get('prescription'),
            indications=request_body.get('indications')
        )
