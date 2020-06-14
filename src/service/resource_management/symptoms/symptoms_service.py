class SymptomsService:

    __SYMPTOMS_DICT = None

    @classmethod
    def symptoms_by_body_part(cls):
        """ Returns a map of `body_part: ["symptom"]`. """
        return cls.__SYMPTOMS_DICT

    @classmethod
    def set_symptoms(cls, symptoms: dict):
        cls.__SYMPTOMS_DICT = symptoms
