#! /usr/bin/python3

from pint import UnitRegistry  # pip install pint

ureg = UnitRegistry()


class Dipole:
    def __init__(self, args):
        self.args = args

    def half_wave_dipole(self, f):
        return 3e8 / (2 * f)

    def unit_print(self, name, value, unit=None):
        if unit is not None:
            print("[*]", name, f"= {(value * ureg.meter).to(unit):.2f}")
        else:
            print("[*]", name, f"= {(value * ureg.meter).to_compact():.2f}")

    def half_wave_dipole_calculator(self):
        f = self.args.frequency
        length = self.half_wave_dipole(f)
        if self.args.verbose:
            self.unit_print("Total Dipole Length", length, self.args.unit)
            self.unit_print("Each Dipole Element Length", length / 2, self.args.unit)
        else:
            self.unit_print("L_total", length, self.args.unit)
            self.unit_print("L_element", length / 2, self.args.unit)
        if self.args.variable_return:
            return length
