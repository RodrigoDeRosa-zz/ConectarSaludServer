from src.database.mongo import Mongo
from src.handlers.custom_request_handler import CustomRequestHandler


class CollectionCleaningHandler(CustomRequestHandler):

    async def post(self, collection_name):
        await self.wrap_handling(self.__clean_collection, **{'collection_name': collection_name})

    """ Handling methods """

    @staticmethod
    async def __clean_collection(collection_name: str):
        await Mongo.get()[collection_name].delete_many({})
