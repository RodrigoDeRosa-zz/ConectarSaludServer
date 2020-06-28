from typing import List
from src.service.resolvers.resolver import Resolver


class PriorityResolver(Resolver):

    __PATH = 'resources/rules/priorities.json'
    __RULES = None
    PRIORITY_BY_PLAN = {
        'Basico': 0,
        'Premium': 1
    }
    DEFAULT_PRIORITY = 0

    @classmethod
    def resolve(cls, symptoms: List[str], plan: str, age: int) -> int:
        """ Resolves a particular consultation's priority. """
        return cls.resolve_symptoms(symptoms, age) + cls.resolve_plan(plan)

    @classmethod
    def resolve_symptoms(cls, symptoms: List[str], age: int) -> int:
        """ Returns a priority level based on the received symptoms. """
        priorities = list()
        for symptom in symptoms:
            alpha, beta = cls.create_memories()
            alpha.update_knowledge({'symptom': symptom, 'age': age})
            # Check for results
            if (results := alpha.evaluate()) or (results := beta.evaluate()):
                for result in results:
                    priorities.append(result.result_object['priority_level'])
        if not priorities: return cls.DEFAULT_PRIORITY
        # Return the sum of priority results
        return sum(priorities)

    @classmethod
    def resolve_plan(cls, plan: str) -> int:
        return cls.PRIORITY_BY_PLAN.get(plan, 0)

    @classmethod
    def file_path(cls):
        return cls.__PATH
