import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

sys.modules.setdefault("mesa", types.ModuleType("mesa")).Agent = object

from src.behavior.archetypes import RLArchetype


def test_rl_archetype_updates_q_values():
    arch = RLArchetype(actions=["a", "b"], learning_rate=1.0, discount=0.0, epsilon=0.0)
    arch.update("s1", "a", reward=1.0, next_state="s2")
    assert arch.q_table["s1"]["a"] == 1.0
    assert arch.choose_action("s1") == "a"
