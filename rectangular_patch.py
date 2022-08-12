import math
from cmath import e
from print_generator import print_patch
from dxf_generator import generate_dxf
from pint import UnitRegistry
ureg = UnitRegistry()
from antenna_calculator import args


def patch_width(f, er):
    return (3e8 / (2 * f)) * math.sqrt(2/(er+1))

def effective_relative_permittivity(f, er, h, W):

    return ((er+1)/2) + (((er-1)/2)*(1+(12*(h/W)))**-0.5)

def delta_length(h, ereff, W):
    return h * 0.412 * ((ereff+0.3)*((W/h)+0.264))/((ereff-0.258)*((W/h)+0.8))

def effective_length(f, ereff):
    return 3e8 / (2 * f * math.sqrt(ereff))

def A_calculation(Z0, er):
    return Z0/60 * math.sqrt((er+1)/2) + ((er-1)/(er+1)) * (0.23+0.11/er)

def A_check(Z0, er):
    A = A_calculation(Z0, er)
    if args.verbose: 
        print("[*] A =", A)
    wsd = (8 * e**(A))/(e**(2*A) - 2)
    if args.verbose:
        print("[*] A Ws/d =", wsd)
    if wsd < 2:
        if args.verbose:
            print("[*] A is valid")
        return wsd
    else:
        if args.verbose:
            print("[*] A is not valid")
        return -1

def B_calculation(Z0, er):
    return (377*math.pi)/(2*Z0*math.sqrt(er))

def B_check(Z0, er):
    B = B_calculation(Z0, er)
    if args.verbose:
        print("[*] B =", B)
    wsd = (2/math.pi)*(B - 1 - math.ln(2*B-1) + (er-1)/(2*er) * (math.ln(B-1) + 0.39 - 0.61/(er)))
    if args.verbose:
        print("[*] B Ws/d =", wsd)
    if wsd > 2:
        if args.verbose:
            print("[*] B is valid")
        return wsd
    else:
        if args.verbose:
            print("[*] B is not valid")
        return -1

def ws_calculation(h, Z0, er):
    if A_check != -1:
        return A_check(Z0, er) * h
    elif B_check != -1:
        return B_check(Z0, er) * h
    else:
        if args.verbose:
            print("No valid Stripline width found")

def y0_calculation(W):
    if args.verbose:
        print("[*] y0 =", W/2)
    return W/2

def x0_calculation(L, W, er, Z0):
    Zin_0 = (90 * (er**2))/(er-1) * (L/W) 
    if args.verbose:
        print("[*] Zin_0 =", Zin_0)
    Zin_x0 = Z0
    if args.verbose:
        print("[*] Zin_x0 =", Zin_x0)
    x0 = math.acos(math.sqrt(Zin_x0/Zin_0)) * (L/math.pi)
    if args.verbose:
        print("[*] x0 =", x0)
    return x0

def unit_print(name, value, unit=None):
    if unit != None:
        print("[*]", name, "= {:.2f}".format((value*ureg.meter).to(args.unit)))
    else:
        print("[*]", name, "= {:.2f}".format((value*ureg.meter).to_compact()))


def microstrip_patch_calculator():

    Z0 = 50 # change if Z0 if necessary

    W = patch_width(args.frequency, args.relative_permittivity)
    unit_print("W", W, args.unit)

    ereff = effective_relative_permittivity(args.frequency, args.relative_permittivity, args.height, W)
    if args.verbose:
        print("[*] Ereff = {:.2f}".format(ereff))

    dL = delta_length(args.height, ereff, W)
    if args.verbose:
        unit_print("dL", dL, args.unit)

    Leff = effective_length(args.frequency, ereff)
    if args.verbose:
        unit_print("Leff", Leff, args.unit)

    L = Leff - 2*dL
    unit_print("L", L, args.unit)

    if args.type == "microstrip":
        ws = ws_calculation(args.height, Z0, args.relative_permittivity)
        unit_print("Ws", ws, args.unit)

    y0 = y0_calculation(W)
    unit_print("y0", y0, args.unit)

    x0 = x0_calculation(L, W, args.relative_permittivity, Z0)
    unit_print("x0", x0, args.unit)
    
    if args.pngoutput:
        if args.type == "microstrip":
            print_patch(round((W * ureg.meter).to(ureg.centimeter), 3).magnitude, round((L * ureg.meter).to(ureg.centimeter), 3).magnitude,
            round((x0 * ureg.meter).to(ureg.centimeter), 3).magnitude, round((y0 * ureg.meter).to(ureg.centimeter), 3).magnitude,
            round((ws * ureg.meter).to(ureg.centimeter), 3).magnitude)
        elif args.type == "probe":
            print_patch(round((W * ureg.meter).to(ureg.centimeter), 3).magnitude, round((L * ureg.meter).to(ureg.centimeter), 3).magnitude,
            round((x0 * ureg.meter).to(ureg.centimeter), 3).magnitude, round((y0 * ureg.meter).to(ureg.centimeter), 3).magnitude)

    if args.dxfoutput:
        if args.type == "microstrip":
            if args.dxfunit:
                generate_dxf(round((W * ureg.meter).to(args.dxfunit), 5).magnitude, round((L * ureg.meter).to(args.dxfunit), 5).magnitude,
                round((x0 * ureg.meter).to(args.dxfunit), 5).magnitude, round((y0 * ureg.meter).to(args.dxfunit), 5).magnitude,
                round((ws * ureg.meter).to(args.dxfunit), 5).magnitude)
            else:
                generate_dxf(round((W * ureg.meter), 5).magnitude, round((L * ureg.meter), 5).magnitude,
                round((x0 * ureg.meter), 5).magnitude, round((y0 * ureg.meter), 5).magnitude,
                round((ws * ureg.meter), 5).magnitude)
        elif args.type == "probe":
            if args.dxfunit:
                generate_dxf(round((W * ureg.meter).to(args.dxfunit), 5).magnitude, round((L * ureg.meter).to(args.dxfunit), 5).magnitude,
                round((x0 * ureg.meter).to(args.dxfunit), 5).magnitude, round((y0 * ureg.meter).to(args.dxfunit), 5).magnitude)
            else:
                generate_dxf(round((W * ureg.meter), 5).magnitude, round((L * ureg.meter), 5).magnitude,
                round((x0 * ureg.meter), 5).magnitude, round((y0 * ureg.meter), 5).magnitude)

