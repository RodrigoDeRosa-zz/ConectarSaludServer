from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.resource_management.family_group_service import FamilyGroupService


class FamilyGroupHandler(CustomRequestHandler):

    async def get(self, affiliate_dni):
        await self.wrap_coroutine(
            self.__get_family_group,
            **{'affiliate_dni': affiliate_dni}
        )

    """ Handling methods """

    async def __get_family_group(self, affiliate_dni):
        self.make_response(await FamilyGroupService.get_family_group(affiliate_dni))
