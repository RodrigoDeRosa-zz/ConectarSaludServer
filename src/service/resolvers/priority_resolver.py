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
    def resolve(cls, symptoms: List[str], plan: str) -> int:
        """ Resolves a particular consultation's priority. """
        return cls.resolve_symptoms(symptoms) + cls.resolve_plan(plan)

    @classmethod
    def resolve_symptoms(cls, symptoms: List[str]) -> int:
        """ Returns a priority level based on the received symptoms. """
        priorities = list()
        for symptom in symptoms:
            alpha, beta = cls.create_memories()
            alpha.update_knowledge({'symptom': symptom})
            # Check for results
            if (result := alpha.evaluate()) or (result := beta.evaluate()):
                priorities.append(result[0].result_object['priority_level'])
        if not priorities: return cls.DEFAULT_PRIORITY
        # Return the maximum priority value
        return max(priorities)

    @classmethod
    def resolve_plan(cls, plan: str) -> int:
        return cls.PRIORITY_BY_PLAN.get(plan, 0)

    @classmethod
    def file_path(cls):
        return cls.__PATH
