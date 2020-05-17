import ast


class MappingUtils:

    @staticmethod
    def decode_request_body(body: bytes) -> dict:
        """ Remove unwanted characters from the given body. """
        return ast.literal_eval(body.decode('utf-8').replace('\t', '').replace('\n', ''))

    @staticmethod
    def map_socket_message(message: str) -> dict:
        """ Parse string message to JSON. """
        return ast.literal_eval(message)
