from os.path import abspath, join, dirname
from typing import List, Tuple

from src.rete.loaders.rule_loader import RuleLoader
from src.rete.memories.alpha_memory import AlphaMemory
from src.rete.memories.beta_memory import BetaMemory
from src.rete.memories.output_memory import OutputMemory
from src.utils.logging.logger import Logger


class SpecialtyResolver:

    __PATH = 'resources/rules/specialties.json'
    __RULES = None
    DEFAULT_VALUE = 'Medicina general'
    PEDIATRICS = 'Pediatría'

    @classmethod
    def resolve(cls, symptoms: List[str], sex: str, age: int) -> str:
        """ Returns the name of the specialty based on the received symptoms. """
        specialties = set()
        for symptom in symptoms:
            alpha, beta = cls.create_memories()
            alpha.update_knowledge({'symptom': symptom, 'sex': sex, 'age': age})
            # Check for results
            if (result := alpha.evaluate()) or (result := beta.evaluate()):
                specialties.add(result.result_object['specialty'])
        # If pediatrics is present, then that should be the returned specialty
        if cls.PEDIATRICS in specialties: return cls.PEDIATRICS
        # If there are no specific specialties or more than one, then the default value will be returned
        if not specialties or len(specialties) > 1: return cls.DEFAULT_VALUE
        # Return the specific specialty that was found
        return specialties.pop()

    @classmethod
    def create_memories(cls) -> Tuple[AlphaMemory, BetaMemory]:
        rules = RuleLoader.parse_rules(cls.__RULES)
        output = OutputMemory(rules['outputs'])
        alpha = AlphaMemory(rules['nodes'], output)
        return alpha, BetaMemory(rules['joints'], alpha, output)

    @classmethod
    def set_up(cls, env):
        Logger(cls.__name__).info('Creating specialties rules engine...')
        rules_path = f'{abspath(join(dirname(__file__), "../../.."))}{"/" if env != "docker" else ""}{cls.__PATH}'
        cls.__RULES = RuleLoader.load_rules_from_file(rules_path)
