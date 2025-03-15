#! /usr/bin/python3

from os import sep
import ezdxf   # pip install ezdxf

class DXFGenerator:
    def __init__(self, args):
        self.args = args

    def generate_patch_dxf(self, filename, W, L, x0, y0, Ws=None, separate_layers=None):

        # Initialize drawing
        doc = ezdxf.new('R2000')

        if separate_layers:
            doc1 = ezdxf.new('R2000')
            doc2 = ezdxf.new('R2000')

        # Add new entities to the modelspace:
        msp = doc.modelspace()

        if separate_layers:
            msp1 = doc1.modelspace()
            msp2 = doc2.modelspace()

        # Set up origin and supporting variables
        substrate_origin = 0.0
        originW = substrate_origin + 0.5 * W
        originL = substrate_origin + 0.5 * L

        if self.args.type == "microstrip":
            g = Ws / 3
            W_cut = (W - Ws - g * 2) / 2

        # Draw patch
        if self.args.type == "microstrip":
            points = [(originW, originL), (originW+W, originL), (originW+W, originL+L),
                ((originW+W_cut + Ws + g * 2), originL+L), (originW+W_cut + Ws + g*2, originL+L-x0), (originW+W_cut + Ws + g, originL+L - x0),
                (originW+W_cut + Ws + g, originL+L * 1.5), (originW+W_cut + g, originL+L * 1.5 ), (originW+W_cut + g, originL+L - x0),
                (originW+W_cut, originL+L - x0), (originW + W_cut, originL+L), (originW, originL+L), (originW, originL)]
            msp.add_lwpolyline(points)
            if separate_layers:
                msp1.add_lwpolyline(points)
        elif self.args.type == "probe":
            points = [(originW, originL), (originW+W, originL), (originW+W, originL+L), (originW, originL+L), (originW, originL)]
            msp.add_lwpolyline(points)
            msp.add_circle((originW+W-y0, originL+L-x0), radius=0.0005)
            if separate_layers:
                msp1.add_lwpolyline(points)
                msp1.add_circle((originW+W-y0, originL+L-x0), radius=0.0005)

        # Draw substrate
        substrate_points = [(substrate_origin, substrate_origin), (substrate_origin+2*W, substrate_origin),
        (substrate_origin+2*W, substrate_origin+2*L), (substrate_origin, substrate_origin+2*L), (substrate_origin, substrate_origin)]
        msp.add_lwpolyline(substrate_points)
        if separate_layers:
            msp2.add_lwpolyline(substrate_points)

        # Save DXF file
        doc.saveas(filename)
        if separate_layers:
            doc1.saveas(filename.split(".")[0] + "_top.dxf")
            doc2.saveas(filename.split(".")[0] + "_substrate.dxf")

        # Print message
        print("[*] DXF file generated: " + filename)
        if separate_layers:
            print("[*] Top Layer DXF file generated: " + filename.split(".")[0] + "_top.dxf")
            print("[*] Substrate DXF file generated: " + filename.split(".")[0] + "_substrate.dxf")

