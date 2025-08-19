# rule_engine.py
from typing import List, Dict, Callable
from component import Component
from rules import available_rules # 從 rules package 匯入自動註冊的規則字典

class RuleSelector:
    def __init__(self):
        self.rules: Dict[str, Callable] = available_rules
        self.modes: List[str] = ["keep_all", "keep_first", "keep_second", "keep_random"]

    def apply(self, component: Component, rule_name: str, mode: str, **kwargs) -> List[Component]:
        if rule_name not in self.rules:
            raise ValueError(f"規則 '{rule_name}' 不存在. 可用規則: {list(self.rules.keys())}")
        if mode not in self.modes:
            raise ValueError(f"模式 '{mode}' 不存在.")
            
        rule_func = self.rules[rule_name]
        new_components = rule_func(component, **kwargs)

        if len(new_components) <= 1:
            return new_components
            
        if mode == "keep_all":
            return new_components
        elif mode == "keep_first":
            return [new_components[0]]
        elif mode == "keep_second":
            return [new_components[1]]
        elif mode == "keep_random":
            return [random.choice(new_components)]
        
        return []