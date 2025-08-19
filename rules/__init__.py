# rules/__init__.py
import pkgutil
import inspect
from typing import Dict, Callable

# available_rules 字典將會被 RuleEngine 使用
available_rules: Dict[str, Callable] = {}

# 遍歷 'rules' 這個 package 下的所有模組
for _, name, _ in pkgutil.iter_modules(__path__):
    # 匯入找到的模組 (e.g., rules.split_basic)
    module = __import__(f"{__name__}.{name}", fromlist=[""])
    
    # 在模組中尋找所有以 "split_" 開頭的函式
    for item_name, item in inspect.getmembers(module, inspect.isfunction):
        if item_name.startswith("split_"):
            # 將 "split_vertical" 轉換為 "vertical" 作為規則名稱
            rule_name = item_name.split("_", 1)[1]
            available_rules[rule_name] = item

print(f"自動註冊規則: {list(available_rules.keys())}")