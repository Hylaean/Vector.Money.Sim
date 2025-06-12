from mesa import Agent


class Household(Agent):
    """Household agent with income, wealth and technology choice."""

    def __init__(
        self,
        unique_id,
        model,
        income=0.0,
        wealth=0.0,
        technology=None,
        carbon_rate=1.0,
        water_rate=0.5,
        biomass_rate=0.1,
        mineral_rate=0.05,
        needs_vector=None,
    ):
        super().__init__(unique_id, model)
        self.income = income
        self.wealth = wealth
        self.technology = technology
        self.carbon_rate = carbon_rate
        self.water_rate = water_rate
        self.biomass_rate = biomass_rate
        self.mineral_rate = mineral_rate
        self.needs_vector = list(needs_vector or [0.0, 0.0, 0.0, 0.0])

    def step(self):
        """Update the household's wealth and potentially its technology choice."""
        # Accumulate income into wealth
        self.wealth += self.income

        # Example placeholder for technology choice update
        technologies = getattr(self.model, "technologies", None)
        if technologies:
            # Simple random choice among available technologies
            self.technology = self.random.choice(technologies)

        # Update bio-physical stocks if present on the model
        stocks = getattr(self.model, "stocks", None)
        if stocks:
            stocks.carbon_budget.apply(-self.carbon_rate)
            stocks.water.apply(-self.water_rate)
            stocks.biomass.apply(-self.biomass_rate)
            stocks.minerals.apply(-self.mineral_rate)
