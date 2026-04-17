import random
class TriangularDistribution:
    def __init__(self, min_val, max_val, mode):
        self.min = min_val
        self.max = max_val
        self.mode = mode

    def sample(self):
        return random.triangular(self.min, self.max, self.mode)
    
class Inputs:
    def __init__(self):
        self.flighthours = TriangularDistribution(20.00, 80.00, 45.00)  
        self.priceperminute = 35.00
        
    def additional_revenue(self):
        r = random.random()

        if r < 0.80: #80% no additional revenue
            return 0.00
        else: #20% additional revenue 
            return TriangularDistribution(2_000.00, 12_000.00, 5_000.00).sample()
    
    def revenue(self, flighthours):
        base_revenue = flighthours * 60 * self.priceperminute
        extra_revenue = self.additional_revenue()
        return base_revenue + extra_revenue 
        
class VariableCosts:
    def __init__(self):
        self.doc = TriangularDistribution(800.00, 1_150.00, 950.00)
        self.overhaul_reserve = TriangularDistribution(300.00, 500.00, 400.00)

    def total_variable_costs(self, flighthours):
        doc_cost = self.doc.sample() * flighthours
        overhaul_cost = self.overhaul_reserve.sample() * flighthours
        return doc_cost, overhaul_cost

class FixedCosts:
    def __init__(self):
        self.aoc = TriangularDistribution(60_000.00, 100_000.00, 80_000.00)
        self.insurance = TriangularDistribution(60_000.00, 120_000.00, 80_000.00)
        self.salary = 5_000.00
        self.admin = TriangularDistribution(25_000.00, 60_000.00, 40_000.00)

    def other(self):
        r = random.random()

        if r < 0.80: #80% normal cost
            other_costs = random.uniform(10_000.00, 20_000.00)
        elif r < 0.95: #15% medium cost
            other_costs = random.uniform(20_000.00, 30_000.00)
        else: #5% high cost
            other_costs = random.uniform(30_000.00, 40_000.00)

        return other_costs
    
    def total_fixed_costs(self):
        return(
            self.aoc.sample()
            + self.insurance.sample()
            + (self.salary * 12)
            + self.admin.sample()
            + self.other()
        )

class Financing:
    def __init__(self):
        self.purchase_price = None
        self.equity = None
        self.loan = self.purchase_price - self.equity

        self.duration = None
        self.remaining_loan = self.loan
        self.remaining_months = self.duration * 12

        self.current_rate = 0.055

    def update_rate(self):
        r = random.random()

        if r < 0.70:  # 70% small movement (±0.3%)
            change = random.triangular(-0.003, 0.003, 0.0)
        elif r < 0.90:  # 20% medium movement (±1.0%)
            change = random.triangular(-0.01, 0.01, 0.0)
        else:  # 10% large movement (±2.0%)
            change = random.triangular(-0.02, 0.02, 0.0)

        self.current_rate += change

        # realistic limits: 2% to 9%
        self.current_rate = max(0.02, min(0.09, self.current_rate))

        return self.current_rate

    def monthly_payment(self):
        r = self.current_rate / 12
        n = self.remaining_months
        L = self.remaining_loan

        if n <= 0:
            return 0.0

        if r == 0:
            return L / n

        return L * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    def apply_month(self, payment):
        if self.remaining_months <= 0 or self.remaining_loan <= 0:
            return 0.0, 0.0

        r = self.current_rate / 12
        interest = self.remaining_loan * r
        principal = payment - interest

        self.remaining_loan -= principal
        self.remaining_loan = max(0.0, self.remaining_loan)

        self.remaining_months -= 1

        return interest, principal

class Depreciation:
    def __init__(self):
        self.holding_period = None
        self.purchase_price = None
        self.residual_value = None

    def monthly_depreciation(self):
        return (self.purchase_price - self.residual_value) / (self.holding_period * 12)

class Events:
    def technical_failure(self):
        r = random.random()

        if r < 0.85: #85% no additional maintenance
            return 0.0
        elif r < 0.97: #12% medium maintenance
            return TriangularDistribution(5000.00, 50000.00, 15000.00).sample() 
        elif r < 0.997: #2.7 high maintenance 
            return TriangularDistribution(30000.00, 200000.00, 80000.00).sample()
        else: #0.3% medium + high maintenance
            medium = TriangularDistribution(5000.00, 50000.00, 15000.00).sample()
            high = TriangularDistribution(30000.00, 200000.00, 80000.00).sample()
            return medium + high

    def weather_demand(self):
        r = random.random()

        if r < 0.60: #60% normal weather/demand
            return 1.00
        elif r < 0.85: #25% bad weather/demand
            return 0.5
        else: #15% good weather/demand
            return 1.4
        

class OverhaulSystem:
    def __init__(self):
        self.total_overhaul = 0.00

    def addition(self, overhaul):
        self.total_overhaul += overhaul

    def yearly_deduction(self):
        r = random.random()

        if r < 0.55: #55% calm year
            factor = random.uniform(0.10, 0.50)
        elif r < 0.90: #35% normal year
            factor = random.uniform(0.60, 1.00)
        else: #10% expensive year
            factor = random.uniform(1.20, 2.20)
        
        deduction = self.total_overhaul * factor
        self.total_overhaul -= deduction
        return deduction

