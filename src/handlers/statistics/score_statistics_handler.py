from datetime import datetime

from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.statistics.score_statistics_service import ScoreStatisticsService


class ScoreStatisticsHandler(CustomRequestHandler):

    async def get(self):
        await self.wrap_coroutine(self.__score_statistics, **{})

    """ Handling methods. """

    async def __score_statistics(self):
        """ Creates a new consultation for the given affiliate. """
        # Parse query params
        doctor_id = self.get_argument('doctor_id', None)
        from_date = self.get_argument('from_date', None)
        # If there is no from_date, we get all consultations
        from_date = datetime.min if not from_date else datetime.strptime(from_date, '%d-%m-%Y')
        to_date = self.get_argument('to_date', None)
        to_date = None if not to_date else datetime.strptime(to_date, '%d-%m-%Y')
        specialty = self.get_argument('specialty', None)
        # Retrieve statistics
        score_list, detail = await ScoreStatisticsService.get_statistics(doctor_id, from_date, to_date, specialty)
        self.make_response({'average_by_date': score_list, 'scoring_data': detail})
