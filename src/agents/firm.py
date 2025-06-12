from mesa import Agent

class Firm(Agent):
    """Firm agent representing a production unit."""

    def __init__(self, unique_id, model, capital=1.0, productivity=1.0,
                 carbon_rate=2.0, water_rate=1.0, biomass_rate=0.5, mineral_rate=0.3):
        super().__init__(unique_id, model)
        self.capital = capital
        self.productivity = productivity
        self.output = 0.0
        self.carbon_rate = carbon_rate
        self.water_rate = water_rate
        self.biomass_rate = biomass_rate
        self.mineral_rate = mineral_rate

    def step(self):
        """Produce output based on current capital and productivity."""
        self.output = self.capital * self.productivity

        stocks = getattr(self.model, "stocks", None)
        if stocks:
            stocks.carbon_budget.apply(-self.carbon_rate)
            stocks.water.apply(-self.water_rate)
            stocks.biomass.apply(-self.biomass_rate)
            stocks.minerals.apply(-self.mineral_rate)
