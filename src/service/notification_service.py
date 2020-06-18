import os

from pyfcm import FCMNotification


class NotificationService:

    notifier = FCMNotification(api_key=os.environ['FIREBASE_API_KEY'])
    __MESSAGE_TITLE = 'Tu médico está listo!'

    @classmethod
    def notify_call_start(cls, device_id: str, doctor_last_name: str, patient_first_name: str):
        message_body = f'El doctor {doctor_last_name} está esperando a {patient_first_name}.'
        cls.notifier.notify_single_device(
            registration_id=device_id,
            message_title=cls.__MESSAGE_TITLE,
            message_body=message_body
        )
