from datetime import datetime


from src.database.daos.consultation_dao import ConsultationDAO


class ScoreStatisticsService:

    @classmethod
    async def get_statistics(cls, doctor_id: str, from_date: datetime, to_date: datetime, specialty: str):
        """ Retrieve scoring statistics and adapt for response. """
        if doctor_id:
            score_by_date, detail = await cls.__get_scoring_data(doctor_id, from_date, to_date, specialty)
        else:
            score_by_date, detail = await cls.__get_scoring_data(None, from_date, to_date, specialty)
        # Map to API model
        date_score_list = []
        for date, pair in score_by_date.items():
            date_score_list.append(
                {
                    'date': date.strftime('%d-%m-%Y'),
                    'average_score': pair[0]
                }
            )
        # Return all information
        return date_score_list, detail

    @classmethod
    async def __get_scoring_data(cls, doctor_id, from_date, to_date, specialty):
        # Retrieve consultations
        consultations = await ConsultationDAO.finished_consultations_score(doctor_id, from_date, to_date, specialty)
        # Group consultations by date
        score_by_date = dict()
        for consultation in consultations:
            consultation_date = datetime.combine(consultation.creation_date.date(), datetime.min.time())
            # Calculate new average
            if consultation_date not in score_by_date:
                score_by_date[consultation_date] = 1, consultation.score
            else:
                count, average = score_by_date[consultation_date]
                score_by_date[consultation_date] = count + 1, float((average + consultation.score) / (count + 1))
        # Get the detail of the score of every consultation
        detail = [
            {
                'score': consultation.score,
                'opinion': consultation.score_opinion,
                'date': datetime.combine(consultation.creation_date.date(), datetime.min.time())
            }
            for consultation in consultations
        ]
        # Return statistic data
        return score_by_date, detail
