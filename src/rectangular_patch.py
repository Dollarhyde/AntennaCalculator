#! /usr/bin/python3

import math
from cmath import e
from pint import UnitRegistry  #pip install pint
ureg = UnitRegistry()

from print_generator import PrintGenerator
from dxf_generator import DXFGenerator
from gerber_generator import GerberGenerator

class RectangularPatch():
    def __init__(self, args):
        self.printGen = PrintGenerator(args)
        self.dxfGen = DXFGenerator(args)
        self.gerberGen = GerberGenerator(args)
        self.args = args

    def patch_width(self, f, er):
        return (3e8 / (2 * f)) * math.sqrt(2/(er+1))

    def effective_relative_permittivity(self, f, er, h, W):
        return ((er+1)/2) + (((er-1)/2)*(1+(12*(h/W)))**-0.5)

    def delta_length(self, h, ereff, W):
        return h * 0.412 * ((ereff+0.3)*((W/h)+0.264))/((ereff-0.258)*((W/h)+0.8))

    def effective_length(self, f, ereff):
        return 3e8 / (2 * f * math.sqrt(ereff))

    def A_calculation(self, Z0, er):
        return Z0/60 * math.sqrt((er+1)/2) + ((er-1)/(er+1)) * (0.23+0.11/er)

    def A_check(self, Z0, er):
        A = self.A_calculation(Z0, er)
        if self.args.verbose:
            print("[*] A =", A)
        wsd = (8 * e**(A))/(e**(2*A) - 2)
        if self.args.verbose:
            print("[*] A Ws/d =", wsd)
        if wsd < 2:
            if self.args.verbose:
                print("[*] A is valid")
            return wsd
        else:
            if self.args.verbose:
                print("[*] A is not valid")
            return -1

    def B_calculation(self, Z0, er):
        return (377*math.pi)/(2*Z0*math.sqrt(er))

    def B_check(self, Z0, er):
        B = self.B_calculation(Z0, er)
        if self.args.verbose:
            print("[*] B =", B)
        wsd = (2/math.pi)*(B - 1 - math.ln(2*B-1) + (er-1)/(2*er) * (math.ln(B-1) + 0.39 - 0.61/(er)))
        if self.args.verbose:
            print("[*] B Ws/d =", wsd)
        if wsd > 2:
            if self.args.verbose:
                print("[*] B is valid")
            return wsd
        else:
            if self.args.verbose:
                print("[*] B is not valid")
            return -1

    def ws_calculation(self, h, Z0, er):
        if self.A_check != -1:
            return self.A_check(Z0, er) * h
        elif self.B_check != -1:
            return self.B_check(Z0, er) * h
        else:
            if self.args.verbose:
                print("No valid Stripline width found")

    def y0_calculation(self, W):
        if self.args.verbose:
            print("[*] y0 =", W/2)
        return W/2

    def x0_calculation(self, L, W, er, Z0):
        Zin_0 = (90 * (er**2))/(er-1) * (L/W)
        if self.args.verbose:
            print("[*] Zin_0 =", Zin_0)
        Zin_x0 = Z0
        if self.args.verbose:
            print("[*] Zin_x0 =", Zin_x0)
        x0 = math.acos(math.sqrt(Zin_x0/Zin_0)) * (L/math.pi)
        if self.args.verbose:
            print("[*] x0 =", x0)
        return x0

    def unit_print(self, name, value, unit=None):
        if unit != None:
            print("[*]", name, "= {:.2f}".format((value*ureg.meter).to(self.args.unit)))
        else:
            print("[*]", name, "= {:.2f}".format((value*ureg.meter).to_compact()))

    def export_png(self, filename, W, L, x0, y0, ws):
        if self.args.pngoutput:
             filename = self.args.pngoutput
        if self.args.type == "microstrip":
            self.printGen.print_patch(filename, round((W * ureg.meter).to(ureg.centimeter), 3).magnitude, round((L * ureg.meter).to(ureg.centimeter), 3).magnitude,
            round((x0 * ureg.meter).to(ureg.centimeter), 3).magnitude, round((y0 * ureg.meter).to(ureg.centimeter), 3).magnitude,
            round((ws * ureg.meter).to(ureg.centimeter), 3).magnitude)
        elif self.args.type == "probe":
            self.printGen.print_patch(filename, round((W * ureg.meter).to(ureg.centimeter), 3).magnitude, round((L * ureg.meter).to(ureg.centimeter), 3).magnitude,
            round((x0 * ureg.meter).to(ureg.centimeter), 3).magnitude, round((y0 * ureg.meter).to(ureg.centimeter), 3).magnitude)

    def export_dxf(self, filename, W, L, x0, y0, ws, separate_layers=None):
        if self.args.gerberoutput:
            filename = self.args.gerberoutput
        elif self.args.dxfoutput:
            filename = self.args.dxfoutput
        if self.args.type == "microstrip":
            if self.args.dxfunit:
                self.dxfGen.generate_patch_dxf(filename, round((W * ureg.meter).to(self.args.dxfunit), 5).magnitude, round((L * ureg.meter).to(self.args.dxfunit), 5).magnitude,
                round((x0 * ureg.meter).to(self.args.dxfunit), 5).magnitude, round((y0 * ureg.meter).to(self.args.dxfunit), 5).magnitude,
                round((ws * ureg.meter).to(self.args.dxfunit), 5).magnitude, separate_layers)
            else:
                self.dxfGen.generate_patch_dxf(filename, round((W * ureg.meter), 5).magnitude, round((L * ureg.meter), 5).magnitude,
                round((x0 * ureg.meter), 5).magnitude, round((y0 * ureg.meter), 5).magnitude,
                round((ws * ureg.meter), 5).magnitude, separate_layers)
        elif self.args.type == "probe":
            if self.args.dxfunit:
                self.dxfGen.generate_patch_dxf(filename, round((W * ureg.meter).to(self.args.dxfunit), 5).magnitude, round((L * ureg.meter).to(self.args.dxfunit), 5).magnitude,
                round((x0 * ureg.meter).to(self.args.dxfunit), 5).magnitude, round((y0 * ureg.meter).to(self.args.dxfunit), 5).magnitude, None, separate_layers)
            else:
                self.dxfGen.generate_patch_dxf(filename, round((W * ureg.meter), 5).magnitude, round((L * ureg.meter), 5).magnitude,
                round((x0 * ureg.meter), 5).magnitude, round((y0 * ureg.meter), 5).magnitude, None, separate_layers)

    def export_patch_to_png(self):
        if self.args.type == 'microstrip':
            self.export_png(self.args.pngoutput, self.args.width, self.args.length, self.args.x0, self.args.y0, self.args.strip_width if self.args.type == "microstrip" else None)
        elif self.args.type == 'probe':
            self.export_png(self.args.pngoutput, self.args.width, self.args.length, self.args.x0, self.args.y0, self.args.strip_width if self.args.type == "microstrip" else None)

    def export_patch_to_dxf(self):
        if self.args.type == 'microstrip':
            self.export_dxf(self.args.dxfoutput, self.args.width, self.args.length, self.args.x0, self.args.y0, self.args.strip_width if self.args.type == "microstrip" else None)
        elif self.args.type == 'probe':
            self.export_dxf(self.args.dxfoutput, self.args.width, self.args.length, self.args.x0, self.args.y0, self.args.strip_width if self.args.type == "microstrip" else None)

    def export_patch_to_gerber(self):
        if self.args.type == 'microstrip':
            self.export_dxf(self.args.gerberoutput, self.args.width, self.args.length, self.args.x0, self.args.y0, self.args.strip_width if self.args.type == "microstrip" else None, True)
            self.gerberGen.generate_gerber(self.args.gerberoutput)
        elif self.args.type == 'probe':
            self.export_dxf(self.args.gerberoutput, self.args.width, self.args.length, self.args.x0, self.args.y0, self.args.strip_width if self.args.type == "microstrip" else None, True)
            self.gerberGen.generate_gerber(self.args.gerberoutput)


    def microstrip_patch_calculator(self, Z0=50):

        Z0 = Z0 #50 ohms by default

        W = self.patch_width(self.args.frequency, self.args.relative_permittivity)
        if not (self.args.variable_return):
            self.unit_print("W", W, self.args.unit)

        ereff = self.effective_relative_permittivity(self.args.frequency, self.args.relative_permittivity, self.args.height, W)
        if self.args.verbose:
            print("[*] Ereff = {:.2f}".format(ereff))

        dL = self.delta_length(self.args.height, ereff, W)
        if self.args.verbose:
            self.unit_print("dL", dL, self.args.unit)

        Leff = self.effective_length(self.args.frequency, ereff)
        if self.args.verbose:
            self.unit_print("Leff", Leff, self.args.unit)

        L = Leff - 2*dL
        if not (self.args.variable_return):
            self.unit_print("L", L, self.args.unit)

        x0 = self.x0_calculation(L, W, self.args.relative_permittivity, Z0)
        if not (self.args.variable_return):
            self.unit_print("x0", x0, self.args.unit)

        y0 = self.y0_calculation(W)
        if not (self.args.variable_return):
            self.unit_print("y0", y0, self.args.unit)

        if self.args.type == "microstrip":
            ws = self.ws_calculation(self.args.height, Z0, self.args.relative_permittivity)
            if not (self.args.variable_return):    
                self.unit_print("Ws", ws, self.args.unit)

        if self.args.pngoutput:
            self.export_png(self.args.pngoutput, W, L, x0, y0, ws if self.args.type == "microstrip" else None)

        if self.args.dxfoutput:
            self.export_dxf(self.args.dxfoutput, W, L, x0, y0, ws if self.args.type == "microstrip" else None)

        if self.args.gerberoutput:
            self.export_dxf(self.args.gerberoutput, W, L, x0, y0, ws if self.args.type == "microstrip" else None, True)
            self.gerberGen.generate_gerber(self.args.gerberoutput)

        if self.args.variable_return:
            if self.args.type == "microstrip":
                return W, L, x0, y0, ws
            elif self.args.type == "probe":
                return W, L, x0, y0

