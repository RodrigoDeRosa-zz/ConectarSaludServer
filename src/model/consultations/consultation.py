from dataclasses import dataclass


@dataclass
class Consultation:
    id: str
    affiliate_dni: str
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
