from antenna_calculator import args

def generate_dxf(filename, W, L, x0, y0, Ws=None):
    import ezdxf

    # Initialize drawing
    doc = ezdxf.new('R2000')

    # Add new entities to the modelspace:
    msp = doc.modelspace()

    # Set up origin and supporting variables
    substrate_origin = 0.0
    originW = substrate_origin + 0.5 * W
    originL = substrate_origin + 0.5 * L

    if args.type == "microstrip":
        g = Ws / 3
        W_cut = (W - Ws - g * 2) / 2

    # Draw patch
    if args.type == "microstrip":
        points = [(originW, originL), (originW+W, originL), (originW+W, originL+L),
            ((originW+W_cut + Ws + g * 2), originL+L), (originW+W_cut + Ws + g*2, originL+L-x0), (originW+W_cut + Ws + g, originL+L - x0),
            (originW+W_cut + Ws + g, originL+L * 1.5), (originW+W_cut + g, originL+L * 1.5 ), (originW+W_cut + g, originL+L - x0),
            (originW+W_cut, originL+L - x0), (originW + W_cut, originL+L), (originW, originL+L), (originW, originL)]
        msp.add_lwpolyline(points)
    elif args.type == "probe":
        points = [(originW, originL), (originW+W, originL), (originW+W, originL+L), (originW, originL+L), (originW, originL)]
        msp.add_lwpolyline(points)
        msp.add_circle((originW+W-y0, originL+L-x0), radius=0.0005)    
    

    # Draw substrate
    substrate_points = [(substrate_origin, substrate_origin), (substrate_origin+2*W, substrate_origin), 
    (substrate_origin+2*W, substrate_origin+2*L), (substrate_origin, substrate_origin+2*L), (substrate_origin, substrate_origin)]
    msp.add_lwpolyline(substrate_points)

    # Save DXF file
    doc.saveas(filename)