from datetime import datetime

from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.statistics.specialty_statistics_service import SpecialtyStatisticsService


class SpecialtyStatisticsHandler(CustomRequestHandler):

    async def get(self):
        await self.wrap_coroutine(self.__specialty_statistics, **{})

    """ Handling methods. """

    async def __specialty_statistics(self):
        """ Creates a new consultation for the given affiliate. """
        # Parse query params
        from_date = self.get_argument('from_date', None)
        # If there is no from_date, we get all consultations
        from_date = datetime.min if not from_date else datetime.strptime(from_date, '%d-%m-%Y')
        to_date = self.get_argument('to_date', None)
        to_date = None if not to_date else datetime.strptime(to_date, '%d-%m-%Y')
        # Retrieve statistics
        statistics = await SpecialtyStatisticsService.get_statistics(from_date, to_date)
        self.make_response(statistics)
