from pint import UnitRegistry
ureg = UnitRegistry()
from antenna_calculator import args

def half_wave_dipole(f):
    return(3e8 / (2 * f))

def unit_print(name, value, unit=None):
    if unit != None:
        print("[*]", name, "= {:.2f}".format((value*ureg.meter).to(args.unit)))
    else:
        print("[*]", name, "= {:.2f}".format((value*ureg.meter).to_compact()))

def half_wave_dipole_calculator():
    f = args.frequency
    l = half_wave_dipole(f)
    unit_print("Total Dipole Length", l, args.unit)
    unit_print("Each Dipole Element Length", l/2, args.unit)
    




