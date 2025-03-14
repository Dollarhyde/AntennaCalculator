#! /usr/bin/python3

import gerberex # pip install pcb-tools-extension

class GerberGenerator:
    def __init__(self, args):
        self.args = args    

    def read(self, filename):
        # temporary replacement for pcb-tools-extension python 3 compatibility issue for gerberex.read()
        with open(filename, 'r') as f:
            data = f.read()
        load_gerber = gerberex.loads(data, filename)
        return load_gerber

    def generate_gerber(self, filename):

        # Generate the top layer gerber file
        tl_dxf = self.read(filename.split(".")[0] + '_top.dxf')
        tl_ctx = gerberex.GerberComposition()
        tl_dxf.draw_mode = tl_dxf.DM_FILL
        tl_ctx.merge(tl_dxf)
        tl_ctx.dump(filename.split(".")[0] + '_top.gtl')
        print("[*] Top layer gerber file generated: " + filename.split(".")[0] + "_top.gtl")

        # Generate the substrate gerber file
        s_dxf = self.read(filename.split(".")[0] + '_substrate.dxf')
        s_ctx = gerberex.GerberComposition()
        s_ctx.merge(s_dxf)
        s_ctx.dump(filename.split(".")[0] + '_substrate.gml')
        print("[*] Substrate gerber file generated: " + filename.split(".")[0] + "_substrate.gml")
