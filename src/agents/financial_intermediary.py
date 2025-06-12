from mesa import Agent


class FinancialIntermediary(Agent):
    """Agent modeling a simple financial intermediary."""

    def __init__(
        self,
        unique_id,
        model,
        deposits=0.0,
        loans=0.0,
        interest_rate=0.0,
        carbon_rate=0.1,
        water_rate=0.05,
        biomass_rate=0.0,
        mineral_rate=0.0,
    ):
        super().__init__(unique_id, model)
        self.deposits = deposits
        self.loans = loans
        self.interest_rate = interest_rate
        self.carbon_rate = carbon_rate
        self.water_rate = water_rate
        self.biomass_rate = biomass_rate
        self.mineral_rate = mineral_rate

    def step(self):
        """Accrue interest on loans and deposits."""
        self.loans *= 1 + self.interest_rate
        self.deposits *= 1 + self.interest_rate * 0.5

        stocks = getattr(self.model, "stocks", None)
        if stocks:
            stocks.carbon_budget.apply(-self.carbon_rate)
            stocks.water.apply(-self.water_rate)
            stocks.biomass.apply(-self.biomass_rate)
            stocks.minerals.apply(-self.mineral_rate)
