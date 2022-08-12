from pint import UnitRegistry
ureg = UnitRegistry()
from antenna_calculator import args

def quarter_wave_monopole(f):
    return(3e8 / (4 * f))

def unit_print(name, value, unit=None):
    if unit != None:
        print("[*]", name, "= {:.2f}".format((value*ureg.meter).to(args.unit)))
    else:
        print("[*]", name, "= {:.2f}".format((value*ureg.meter).to_compact()))

def quarter_wave_monopole_calculator():
    f = args.frequency
    l = quarter_wave_monopole(f)
    unit_print("Quarter Wave Monopole Length", l, args.unit)





