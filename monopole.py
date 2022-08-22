from pint import UnitRegistry
ureg = UnitRegistry()

class Monopole:
    def __init__(self, args):
        self.args = args

    def quarter_wave_monopole(self, f):
        return(3e8 / (4 * f))

    def unit_print(self, name, value, unit=None):
        if unit != None:
            print("[*]", name, "= {:.2f}".format((value*ureg.meter).to(self.args.unit)))
        else:
            print("[*]", name, "= {:.2f}".format((value*ureg.meter).to_compact()))

    def quarter_wave_monopole_calculator(self):
        f = self.args.frequency
        l = self.quarter_wave_monopole(f)
        self.unit_print("Quarter Wave Monopole Length", l, self.args.unit)





