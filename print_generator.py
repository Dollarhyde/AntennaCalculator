#! /usr/bin/python3

from PIL import Image, ImageDraw

class PrintGenerator:
    def __init__(self, args):
        self.args = args

    def print_patch(self, filename, W, L, x0, y0, Ws=None):
        w_cm, h_cm = (22, 28)             # Size of letter paper in cm
        res_x, res_y = (300, 300)           # Desired resolution

        # Inch-to-cm factor
        f = 2.54

        # Determine image size w.r.t. resolution
        width = int(w_cm / f * res_x)
        height = int(h_cm / f * res_y)

        # Create new image with proper size
        img = Image.new('RGB', (width, height), color=(255, 255, 255))

        # Draw elements
        draw = ImageDraw.Draw(img)

        # Supporing variables
        if self.args.type == "microstrip":
            g = Ws / 3
            W_cut = (W - Ws - g * 2) / 2

        # Substrate origin
        substrate_origin = 5.0
        if W * 2 > 15:
            substrate_origin = 1.0
        if W * 2 > 22:
            print("[*] The substrate is too large for letter paper. Please adjust paper size.")

        # Origin of patch
        originW = substrate_origin + 0.5 * W
        originL = substrate_origin + 0.5 * L

        # Draw patch
        if self.args.type == "microstrip":
            microstrip_patch_coords_cm = [(originW, originL), (originW+W, originL), (originW+W, originL+L),
            ((originW+W_cut + Ws + g * 2), originL+L), (originW+W_cut + Ws + g*2, originL+L-x0), (originW+W_cut + Ws + g, originL+L - x0),
            (originW+W_cut + Ws + g, originL+L * 1.5), (originW+W_cut + g, originL+L * 1.5 ), (originW+W_cut + g, originL+L - x0),
            (originW+W_cut, originL+L - x0), (originW + W_cut, originL+L), (originW, originL+L), (originW, originL)]
            microstrip_patch_coords = [(int(c[0] / f * res_x), int(c[1] / f * res_y)) for c in microstrip_patch_coords_cm]
            draw.polygon(tuple(microstrip_patch_coords), fill=(0, 0, 0))
        elif self.args.type == "probe":
            probe_patch_coords_cm = [(originW, originL), (originW+W, originL),  (originW+W, originL+L),(originW, originL+L), (originW, originL)]
            probe_patch_coords = [(int(c[0] / f * res_x), int(c[1] / f * res_y)) for c in probe_patch_coords_cm]
            draw.polygon(tuple(probe_patch_coords), fill=(0, 0, 0))

            probe_feed_coords_cm = [(originW+W-y0-0.0707/2, originL+L-x0-0.0707/2),(originW+W-y0+0.0707/2, originL+L-x0+0.0707/2)]
            probe_feed_coords = [(int(c[0] / f * res_x), int(c[1] / f * res_y)) for c in probe_feed_coords_cm]
            draw.ellipse(tuple(probe_feed_coords), fill=(255, 255, 255))

        # Draw substrate
        substrate_coords_cm = [(substrate_origin, substrate_origin), (substrate_origin+ 2* W, substrate_origin+ 2*L)]
        substrate_coords = [(int(c[0] / f * res_x), int(c[1] / f * res_y)) for c in substrate_coords_cm]
        draw.rectangle(tuple(substrate_coords), outline=(0, 0, 0))

        # Show image for debugging
        if self.args.verbose:
            img.show() # enable for debugging

        # Save image
        img.save(filename, dpi=(res_x, res_y))
        print("[*] Image saved: " + filename)

