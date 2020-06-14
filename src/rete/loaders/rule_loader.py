import json
from typing import List

from src.rete.model.condition import Condition
from src.rete.model.joint import Joint
from src.rete.model.node import Node
from src.rete.model.result import Result


class RuleLoader:

    @classmethod
    def load_rules_from_file(cls, path: str) -> dict:
        with open(path, 'r') as fd:
            raw_rules = json.load(fd)
        return raw_rules

    @classmethod
    def parse_rules(cls, rules_dict: dict) -> dict:
        return {
            'nodes': cls.__parse_nodes(rules_dict.get('nodes', [])),
            'joints': cls.__parse_joints(rules_dict.get('joints', [])),
            'outputs': cls.__parse_results(rules_dict.get('outputs', []))
        }

    @classmethod
    def __parse_nodes(cls, raw_nodes: list) -> List[Node]:
        nodes = []
        for node in raw_nodes:
            conditions = [
                Condition().with_field(cond['field']).with_value(cond['value']).with_operation(cond['operation'])
                for cond in node.get('conditions', [])
            ]
            nodes.append(Node().with_id(node['id']).with_conditions(conditions).with_output(node.get('output')))
        return nodes

    @classmethod
    def __parse_joints(cls, raw_joints: dict) -> List[Joint]:
        return [
            Joint().with_id(joint['id']).with_nodes(joint['nodes']).with_output(joint['output'])
            for joint in raw_joints
        ]

    @classmethod
    def __parse_results(cls, raw_results: dict) -> List[Result]:
        return [
            Result().with_id(result['id']).with_object(result['object'])
            for result in raw_results
        ]
