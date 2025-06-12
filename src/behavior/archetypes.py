"""Common behavioural archetypes for agents."""

from __future__ import annotations

import random
from collections import defaultdict
from typing import Callable, Dict, Hashable, List, MutableMapping


class RLArchetype:
    """Simple Q-learning based reinforcement learning archetype."""

    def __init__(
        self,
        actions: List[Hashable],
        learning_rate: float = 0.1,
        discount: float = 0.95,
        epsilon: float = 0.1,
    ) -> None:
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount = discount
        self.epsilon = epsilon
        self.q_table: MutableMapping[Hashable, MutableMapping[Hashable, float]] = (
            defaultdict(lambda: defaultdict(float))
        )

    def choose_action(self, state: Hashable) -> Hashable:
        """Return an action using an \epsilon-greedy policy."""
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        q_values = self.q_table[state]
        if not q_values:
            return random.choice(self.actions)
        return max(self.actions, key=lambda a: q_values[a])

    def update(
        self, state: Hashable, action: Hashable, reward: float, next_state: Hashable
    ) -> None:
        """Update the Q-table from an experience."""
        current = self.q_table[state][action]
        next_values = self.q_table[next_state]
        next_max = max(next_values.values()) if next_values else 0.0
        target = reward + self.discount * next_max
        self.q_table[state][action] = current + self.learning_rate * (target - current)


class LLMArchetype:
    """Lightweight archetype wrapper around a language model function."""

    def __init__(
        self, prompt: str, call_func: Callable[[str], str] | None = None
    ) -> None:
        self.prompt = prompt
        self.call_func = call_func or (lambda x: "")

    def generate(self, user_input: str) -> str:
        """Generate text using ``call_func``."""
        full_prompt = f"{self.prompt}\n{user_input}"
        return self.call_func(full_prompt)
