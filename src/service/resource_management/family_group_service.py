from typing import List

from src.database.daos.affiliate_dao import AffiliateDAO
from src.database.daos.family_group_dao import FamilyGroupDAO


class FamilyGroupService:

    @classmethod
    def get_family_group(cls, affiliate_dni: str) -> List[dict]:
        """ Retrieve the given affiliate's family group. """
        family_group = []
        for member_dni in await FamilyGroupDAO.find(affiliate_dni):
            affiliate = await AffiliateDAO.find(member_dni)
            family_group.append(
                {
                    'dni': affiliate.dni,
                    'affiliate_first_name': affiliate.first_name,
                    'affiliate_last_name': affiliate.last_name
                }
            )
        return family_group
