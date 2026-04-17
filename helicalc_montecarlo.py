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

        def weather():
            r = random.random()

            if r < 0.60: #60% normal weather
                return 1.00
            
            elif r < 0.85: #25% bad weather
                return 0.5
            
            else: #15% good weather
                return 1.4
        
        self.priceperminute = 32.00
        
        def additional_revenue():
            r = random.random()

            if r < 0.80: #80% no additional revenue
                self.additional_revenue = 0.00
            
            else: #20% additional revenue 
                self.additional_revenue = TriangularDistribution(2000.00, 12000.00, 5000.00)
            
            return self.additional_revenue
        
class VariableCosts:
    def __init__(self):
        self.doc = TriangularDistribution()
        self.overhaul_reserve = TriangularDistribution()

class FixedCosts:
    def __init__(self):
        self.aoc = TriangularDistribution()
        self.insurance = TriangularDistribution()
        self.salary = 5000.00
        self.admin = TriangularDistribution()

        def other():
            pass

class Financing: 
    def __init__(self):
        self.purchase_price = None
        self.equity = None
        self.loan = None
        
        def interest_rate():
            pass

        self.duration = None
        self.monthly_payment = None


class Depreciation:
    def __init__(self):
        self.holding_period = None
        self.monthly_depreciation = None
        self.residual_value = None


            
                
                





