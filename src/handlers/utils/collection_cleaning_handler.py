from src.database.mongo import Mongo
from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.queue.queue_manager import QueueManager


class CollectionCleaningHandler(CustomRequestHandler):

    async def post(self, collection_name):
        await self.wrap_coroutine(self.__clean_collection, **{'collection_name': collection_name})

    """ Handling methods """

    @staticmethod
    async def __clean_collection(collection_name: str):
        await Mongo.get()[collection_name].delete_many({})
        if collection_name == 'queue': QueueManager.clear()
