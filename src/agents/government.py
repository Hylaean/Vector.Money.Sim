from mesa import Agent


class Government(Agent):
    """Government agent collecting taxes and providing spending."""

    def __init__(
        self,
        unique_id,
        model,
        tax_rate=0.0,
        carbon_capture=0.5,
        water_supply=0.2,
        biomass_program=0.1,
        mineral_program=0.05,
    ):
        super().__init__(unique_id, model)
        self.tax_rate = tax_rate
        self.revenue = 0.0
        self.carbon_capture = carbon_capture
        self.water_supply = water_supply
        self.biomass_program = biomass_program
        self.mineral_program = mineral_program

    def step(self):
        """Collect taxes from households and firms in the model."""
        total_tax = 0.0
        if hasattr(self.model, "schedule"):
            for agent in self.model.schedule.agents:
                income = getattr(agent, "income", 0.0)
                profit = getattr(agent, "output", 0.0)
                total_tax += (income + profit) * self.tax_rate
        self.revenue += total_tax

        stocks = getattr(self.model, "stocks", None)
        if stocks:
            stocks.carbon_budget.apply(self.carbon_capture)
            stocks.water.apply(self.water_supply)
            stocks.biomass.apply(self.biomass_program)
            stocks.minerals.apply(self.mineral_program)
