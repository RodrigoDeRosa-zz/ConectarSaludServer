from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.resource_management.symptoms.symptoms_service import SymptomsService


class SymptomsHandler(CustomRequestHandler):

    def get(self):
        self.wrap_method(self.__retrieve_symptoms, **{})

    """ Handling methods. """

    def __retrieve_symptoms(self):
        self.make_response(SymptomsService.symptoms_by_body_part())
