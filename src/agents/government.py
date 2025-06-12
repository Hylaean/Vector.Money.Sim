from mesa import Agent

class Government(Agent):
    """Government agent collecting taxes and providing spending."""

    def __init__(self, unique_id, model, tax_rate=0.0):
        super().__init__(unique_id, model)
        self.tax_rate = tax_rate
        self.revenue = 0.0

    def step(self):
        """Collect taxes from households and firms in the model."""
        total_tax = 0.0
        if hasattr(self.model, 'schedule'):
            for agent in self.model.schedule.agents:
                income = getattr(agent, 'income', 0.0)
                profit = getattr(agent, 'output', 0.0)
                total_tax += (income + profit) * self.tax_rate
        self.revenue += total_tax
