from datetime import datetime


from src.database.daos.consultation_dao import ConsultationDAO


class SpecialtyStatisticsService:

    @classmethod
    async def get_statistics(cls, from_date: datetime, to_date: datetime):
        consultations = await ConsultationDAO.finished_consultations(from_date=from_date, to_date=to_date)
        # Count consultations by specialty
        by_specialty = dict()
        for consultation in consultations:
            if len(consultation.specialties) > 1 and 'Medicina general' in consultation.specialties:
                consultation.specialties.remove('Medicina general')
            specialty = consultation.specialties[0]
            by_specialty[specialty] = by_specialty.get(specialty, 0) + 1
        # Map to API model
        return {
            'total': len(consultations),
            'by_specialty': [
                {'specialty': key, 'count': value}
                for key, value in by_specialty.items()
            ]
        }
