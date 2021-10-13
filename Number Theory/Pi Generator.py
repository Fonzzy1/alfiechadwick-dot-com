import decimal as d


class Pi:
    def __init__(self, length = 10, steps = 1000):
        self.null = 0
        self.length = length
        self.steps = steps
        self.leibniz = 0

        self.leibniz()

    def leibniz(self):

     d.getcontext().prec = self.length
     self.leibniz = d.Decimal(0)
     i = 0
     while i <= self.steps:
        self.leibniz += d.Decimal(4 * (-1) ** i * 1 / (2 * i + 1))
        i += 1


pi = Pi()


