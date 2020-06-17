from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from typing import List

from src.model.affiliates.affiliate import Affiliate
from src.service.resolvers.priority_resolver import PriorityResolver
from src.service.resolvers.specialty_resolver import SpecialtyResolver


@dataclass
class ConsultationOpinion:
    prescription: str = None
    indications: str = None


class ConsultationStatus(Enum):
    WAITING_DOCTOR = 'WAITING_DOCTOR'
    WAITING_CALL = 'WAITING_CALL'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'


@dataclass
class Consultation:
    id: str
    creation_date: datetime = field(default_factory=datetime.now)
    affiliate_dni: str = None
    patient_dni: str = None
    symptoms: List[str] = field(default_factory=list)
    reason: str = None
    priority: int = 0
    specialties: List[str] = None
    status: ConsultationStatus = ConsultationStatus.WAITING_DOCTOR
    doctor_id: str = None
    call_id: str = None
    score: float = None
    score_opinion: str = None
    prescription: str = None
    indications: str = None
    socket_id: str = None
    # Used for priority calculation
    affiliate: Affiliate = None
    # Used for post construct control
    retrieval: bool = False

    def __post_init__(self):
        """ Resolve priority and specialty based on the received information. """
        if self.retrieval: return
        self.affiliate_dni = self.affiliate.dni
        # TODO -> Replace this for the patient's id
        self.patient_dni = self.affiliate_dni
        # TODO -> Sex and age. This should depend on the consultation's "patient" instead of affiliate
        self.specialties = SpecialtyResolver.resolve(self.symptoms, self.affiliate.sex, self.affiliate.age)
        # Resolve priority based on symptoms and affiliate plan
        self.priority = PriorityResolver.resolve(self.symptoms, self.affiliate.plan)


@dataclass
class ConsultationScore:
    points: float
    opinion: str = None


@dataclass
class ConsultationDTO:
    symptoms: List[str]
    reason: str
    patient_dni: str = None


@dataclass
class QueueableData:
    id: str
    socket_id: str
    creation_time: datetime
    priority: int
    specialties: List[str] = field(default_factory=list)

    SECONDS_IN_MINUTE = 60
    PRIORITY_MINUTES = 30

    def __lt__(self, other):
        """ Used for priority queue ordering. Higher priority value means lower position in queue. """
        return self.priority_value() > other.priority_value()

    def priority_value(self) -> float:
        # Get the minutes this consultation has been waiting
        elapsed_minutes = (datetime.now() - self.creation_time).total_seconds() / self.SECONDS_IN_MINUTE
        # Each level of priority is equivalent to half an hour
        priority_equivalent_minutes = self.priority * self.PRIORITY_MINUTES
        # Total priority is the sum of both
        return elapsed_minutes + priority_equivalent_minutes
