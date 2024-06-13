#! /usr/bin/python3

from pint import UnitRegistry
ureg = UnitRegistry()

class Dipole:
    def __init__(self, args):
        self.args = args

    def half_wave_dipole(self, f):
        return(3e8 / (2 * f))

    def unit_print(self, name, value, unit=None):
        if unit != None:
            print("[*]", name, "= {:.2f}".format((value*ureg.meter).to(self.args.unit)))
        else:
            print("[*]", name, "= {:.2f}".format((value*ureg.meter).to_compact()))

    def half_wave_dipole_calculator(self):
        f = self.args.frequency
        l = self.half_wave_dipole(f)
        if self.args.verbose:
            self.unit_print("Total Dipole Length", l, self.args.unit)
            self.unit_print("Each Dipole Element Length", l/2, self.args.unit)
        else:
            self.unit_print("L_total", l, self.args.unit)
            self.unit_print("L_element", l/2, self.args.unit)
        if self.args.variable_return:
            return l

