from mesa import Agent

class Firm(Agent):
    """Firm agent representing a production unit."""

    def __init__(self, unique_id, model, capital=1.0, productivity=1.0):
        super().__init__(unique_id, model)
        self.capital = capital
        self.productivity = productivity
        self.output = 0.0

    def step(self):
        """Produce output based on current capital and productivity."""
        self.output = self.capital * self.productivity
