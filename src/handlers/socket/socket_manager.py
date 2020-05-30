from json import dumps

import socketio

from src.utils.logging.logger import Logger
from src.utils.mapping.mapping_utils import MappingUtils


class SocketManager:
    SIO = socketio.AsyncServer(async_mode='tornado')

    USER_EVENT_TYPE = 'waiting_call'
    CALL_STARTED_EVENT_TYPE = 'call_started'
    REMAINING_TIME_EVENT_TYPE = 'remaining_time'

    @classmethod
    def handler(cls):
        return socketio.get_tornado_handler(cls.SIO)

    @staticmethod
    @SIO.on('connect')
    async def connect(sid, environ):
        Logger('SocketManager').info(f'User opened socket with id {sid}.')

    @staticmethod
    @SIO.on(USER_EVENT_TYPE)
    async def user_waiting_call(sid, message):
        # This is here to avoid circular import errors
        from src.service.resource_management.consultations.consultation_service import ConsultationService
        Logger('Socket Manager').info(f'Received message through socket {sid}')
        decoded = MappingUtils.map_socket_message(message)
        await ConsultationService.link_socket_to_consultation(decoded['consultation_id'], sid)

    @classmethod
    async def notify_call_start(cls, call_id, sid):
        """ Notify user with call id to join Agora video conference. """
        Logger('Socket Manager').info(f'Emitting call ID through socket {sid}.')
        await cls.SIO.emit(cls.CALL_STARTED_EVENT_TYPE, dumps({'call_id': call_id}), room=sid)

    @classmethod
    async def notify_remaining_time(cls, remaining_time, sid):
        """ Notifies the user the approximate remaining time. """
        Logger('Socket Manager').info(f'Emitting remaining time through socket {sid}.')
        await cls.SIO.emit(cls.REMAINING_TIME_EVENT_TYPE, dumps({'remaining_time': remaining_time}), room=sid)
