import socketio

from src.utils.logging.logger import Logger
from src.utils.mapping.mapping_utils import MappingUtils


class SocketManager:
    SIO = socketio.AsyncServer(async_mode='tornado')

    @classmethod
    def handler(cls):
        return socketio.get_tornado_handler(cls.SIO)


@SocketManager.SIO.on('connect')
async def connect(sid, environ):
    Logger(sid).info('Connected')
    await SocketManager.SIO.emit('message', {'data': 'Connected', 'count': 0}, room=sid)


@SocketManager.SIO.on('message')
async def print_message(sid, message):
    decoded = MappingUtils.map_socket_message(message)
    Logger(sid).info(decoded)
    await SocketManager.SIO.emit('message', 'Received!', room=sid)
