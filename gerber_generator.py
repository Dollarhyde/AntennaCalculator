#! /usr/bin/python3

import gerberex # pip install pcb-tools-extension

class GerberGenerator:
    def __init__(self, args):
        self.args = args    

    def generate_gerber(self, filename):

        # Generate the top layer gerber file
        tl_dxf = gerberex.read(filename.split(".")[0] + '_top.dxf')
        tl_ctx = gerberex.GerberComposition()
        tl_dxf.draw_mode = tl_dxf.DM_FILL
        tl_ctx.merge(tl_dxf)
        tl_ctx.dump(filename.split(".")[0] + '_top.gtl')
        print("[*] Top layer gerber file generated: " + filename.split(".")[0] + "_top.gtl")

        # Generate the substrate gerber file
        s_dxf = gerberex.read(filename.split(".")[0] + '_substrate.dxf')
        s_ctx = gerberex.GerberComposition()
        s_ctx.merge(s_dxf)
        s_ctx.dump(filename.split(".")[0] + '_substrate.gml')
        print("[*] Substrate gerber file generated: " + filename.split(".")[0] + "_substrate.gml")