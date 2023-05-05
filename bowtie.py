# Traditional bowtie calculator
# input: frequency
# antenna params: height, width, gap

import math
from cmath import e
from pint import UnitRegistry
ureg = UnitRegistry()

from print_generator import PrintGenerator
from dxf_generator import DXFGenerator
from gerber_generator import GerberGenerator

class Bowtie():
    def __init__(self, args):
        self.printGen = PrintGenerator(args)
        self.dxfGen = DXFGenerator(args)
        self.gerberGen = GerberGenerator(args)
        self.args = args

    def unit_print(self, name, value, unit=None):
        if unit != None:
            print("[*]", name, "= {:.2f}".format((value*ureg.meter).to(self.args.unit)))
        else:
            print("[*]", name, "= {:.2f}".format((value*ureg.meter).to_compact()))

    def export_png(self, filename, W, L, g):
        if self.args.pngoutput:
             filename = self.args.pngoutput

        self.printGen.print_bowtie(filename, round((W * ureg.meter).to(ureg.centimeter), 3).magnitude, round((L * ureg.meter).to(ureg.centimeter), 3).magnitude,
        round((g * ureg.meter).to(ureg.centimeter), 3).magnitude)

    def export_dxf(self, filename, W, L, g, separate_layers=None):
        if self.args.gerberoutput:
            filename = self.args.gerberoutput
        elif self.args.dxfoutput:
            filename = self.args.dxfoutput

        if self.args.dxfunit:
            self.dxfGen.generate_bowtie_dxf(filename, round((W * ureg.meter).to(self.args.dxfunit), 5).magnitude, round((L * ureg.meter).to(self.args.dxfunit), 5).magnitude,
            round((g * ureg.meter).to(self.args.dxfunit), 5).magnitude, separate_layers)
        else:
            self.dxfGen.generate_bowtie_dxf(filename, round((W * ureg.meter), 5).magnitude, round((L * ureg.meter), 5).magnitude,
            round((g * ureg.meter), 5).magnitude, separate_layers)
       
    def export_bowtie_to_png(self):
        self.export_png(self.args.pngoutput, self.args.width, self.args.length, self.args.g)

    def export_bowtie_to_dxf(self):
        self.export_dxf(self.args.dxfoutput, self.args.width, self.args.length, self.args.g)

    def export_bowtie_to_gerber(self):
        self.export_dxf(self.args.gerberoutput, self.args.width, self.args.length, self.args.g, True)
        self.gerberGen.generate_gerber(self.args.gerberoutput)

    def bowtie_calculator(self):
        c = 3e8 #speed of light m/s
        f = self.args.frequency 
        lam =  c/f #wavelength

        W = 0.375 * lam  
        if not (self.args.variable_return):
            self.unit_print("W", W, self.args.unit)
            #print("[*] W = {:.5f}".format(W))

        L = 0.25 * lam 
        if not (self.args.variable_return):
            self.unit_print("L", L, self.args.unit)
            #print("[*] L = {:.5f}".format(L))

        g = 0.02066 * lam #gap between wings
        if not (self.args.variable_return):
            self.unit_print("gap", g, self.args.unit)
            # print("[*] gap = {:.5f}".format(g))
        
        # BW = 0.33 * f #estimated bandwidth
        # if self.args.verbose:
        #     print("[*] bandwidth = {:.2f}".format(BW))


        if self.args.pngoutput:
            self.export_png(self.args.pngoutput, W, L, g)

        if self.args.dxfoutput:
            self.export_dxf(self.args.dxfoutput, W, L, g)

        if self.args.gerberoutput:
            self.export_dxf(self.args.gerberoutput, W, L, g)
            self.gerberGen.generate_gerber(self.args.gerberoutput)

        if self.args.variable_return:
            return W, L, g
