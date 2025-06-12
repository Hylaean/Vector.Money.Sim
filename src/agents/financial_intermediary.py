from mesa import Agent

class FinancialIntermediary(Agent):
    """Agent modeling a simple financial intermediary."""

    def __init__(self, unique_id, model, deposits=0.0, loans=0.0, interest_rate=0.0):
        super().__init__(unique_id, model)
        self.deposits = deposits
        self.loans = loans
        self.interest_rate = interest_rate

    def step(self):
        """Accrue interest on loans and deposits."""
        self.loans *= (1 + self.interest_rate)
        self.deposits *= (1 + self.interest_rate * 0.5)
