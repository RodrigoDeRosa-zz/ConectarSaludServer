from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class ConsultationStatus(Enum):
    WAITING_DOCTOR = 'WAITING_DOCTOR'
    WAITING_CALL = 'WAITING_CALL'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'


@dataclass
class Consultation:
    id: str
    affiliate_dni: str
    creation_date: datetime
    status: ConsultationStatus = ConsultationStatus.WAITING_DOCTOR
    doctor_id: str = None
    call_id: str = None
    score: float = None
    score_opinion: str = None
    prescription: str = None
    indications: str = None


@dataclass
class ConsultationScore:
    points: float
    opinion: str = None
