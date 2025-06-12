from mesa import Agent

class Household(Agent):
    """Household agent with income, wealth and technology choice."""

    def __init__(self, unique_id, model, income=0.0, wealth=0.0, technology=None):
        super().__init__(unique_id, model)
        self.income = income
        self.wealth = wealth
        self.technology = technology

    def step(self):
        """Update the household's wealth and potentially its technology choice."""
        # Accumulate income into wealth
        self.wealth += self.income

        # Example placeholder for technology choice update
        technologies = getattr(self.model, "technologies", None)
        if technologies:
            # Simple random choice among available technologies
            self.technology = self.random.choice(technologies)
