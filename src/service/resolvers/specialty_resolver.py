from typing import List

from src.service.resolvers.resolver import Resolver


class SpecialtyResolver(Resolver):

    __PATH = 'resources/rules/specialties.json'
    __RULES = None
    DEFAULT_VALUE = 'Medicina general'
    PEDIATRICS = 'Pediatría'

    @classmethod
    def resolve(cls, symptoms: List[str], sex: str, age: int) -> List[str]:
        """ Returns the name of the specialty based on the received symptoms. """
        specialties = set()
        for symptom in symptoms:
            alpha, beta = cls.create_memories()
            alpha.update_knowledge({'symptom': symptom, 'sex': sex, 'age': age})
            # Check for results
            if (result := alpha.evaluate()) or (result := beta.evaluate()):
                specialties.add(result.result_object['specialty'])
        # If pediatrics is present, then that should be the returned specialty
        if cls.PEDIATRICS in specialties: return [cls.PEDIATRICS]
        # If there are no specific specialties or more than one, then the default value will be returned
        if not specialties: return [cls.DEFAULT_VALUE]
        # Return the specific specialty that was found
        return list(specialties)

    @classmethod
    def file_path(cls):
        return cls.__PATH
