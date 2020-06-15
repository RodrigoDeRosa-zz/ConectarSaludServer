from os.path import abspath, join, dirname
from typing import Tuple

from src.rete.loaders.rule_loader import RuleLoader
from src.rete.memories.alpha_memory import AlphaMemory
from src.rete.memories.beta_memory import BetaMemory
from src.rete.memories.output_memory import OutputMemory
from src.utils.logging.logger import Logger


class Resolver:

    __PATH = None  # On subclass
    __RULES = None  # On subclass

    @classmethod
    def create_memories(cls) -> Tuple[AlphaMemory, BetaMemory]:
        rules = RuleLoader.parse_rules(cls.__RULES)
        output = OutputMemory(rules['outputs'])
        alpha = AlphaMemory(rules['nodes'], output)
        return alpha, BetaMemory(rules['joints'], alpha, output)

    @classmethod
    def set_up(cls, env):
        Logger(cls.__name__).info(f'Creating {cls.__name__} rules engine...')
        rules_path = f'{abspath(join(dirname(__file__), "../../.."))}{"/" if env != "docker" else ""}{cls.file_path()}'
        cls.__RULES = RuleLoader.load_rules_from_file(rules_path)

    @classmethod
    def file_path(cls):
        # On subclass
        return None
